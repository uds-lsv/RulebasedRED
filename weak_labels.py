import json
import utils
import argparse

def get_arg_parser():
    p = argparse.ArgumentParser("ATCO-pilot input to generate noisy label")
    p.add_argument(
        'atco',
        help='ATCO command')
    p.add_argument(
        'pilot',
        help='Pilot readback')
    return p

def assign_readback(atco, pilot, callsign, callsign_availability):
    turn_group = []
    command_dict_result = {}
    label_list = []
    label = 'NA'
    pilot_nocall = pilot

    if not atco == callsign:
        atco_nocall_split = atco.replace(callsign, '').strip().split()
        num_group = utils.get_command_value(atco_nocall_split)

        # Remove callsign from pilot - not to clash with other command values
        for group in num_group.copy():
            if len(group) > 1 or group[0] in ['LEFT', 'RIGHT']:
                num = " ".join(group).strip()
                if num in pilot:
                    command_dict_result[num] = 'Present'
                    pilot = pilot.replace(num, '')
                    num_group.remove(group)

        for group in num_group.copy():
            if len(group) > 1 or group[0] in ['LEFT', 'RIGHT']:

                # check for contact - dot and first letter
                if 'DOT' in group.copy():
                    pilot_nocall, command_dict_result, label_list = utils.run_for_contact(
                        group.copy(), 
                        pilot_nocall, 
                        command_dict_result, 
                        num_group)
                    

                # Check for Wrong readback turn command
                elif group[0] in ['LEFT', 'RIGHT'] and len(group) == 1:
                    if 'LEFT' in group and 'RIGHT' in pilot_nocall:
                        command_dict_result[" ".join(group).strip()] = "Wrong readback"
                    elif 'LEFT' in group and 'RIGHT' in pilot_nocall:
                        command_dict_result[" ".join(group).strip()] = "Wrong readback"
                    else:
                        label_list = utils.add_label_list(group, pilot_nocall, label_list)

                else:
                    label_list = utils.add_label_list(group, pilot_nocall, label_list)

                if label_list:
                    if 'NA' in label_list and 'Present' in label_list:
                        command_dict_result[" ".join(group).strip()] = "Wrong readback"
                    elif 'NA' in label_list:
                        command_dict_result[" ".join(group).strip()] = "NA"
                    elif 'Present' in label_list:
                        command_dict_result[" ".join(group).strip()] = "Present"
                else:
                    if not command_dict_result.get(" ".join(group).strip(), None):
                        return "Not available!"
        result = list(command_dict_result.values())

        # Assign labels
        if 'Wrong readback' in result:
            label = 'Wrong readback'
        elif 'NA' in result and 'Present' in result:
            label = 'Partial readback'
        elif 'NA' not in result:
            label = 'Correct'
        elif 'Present' not in result:
            label = 'Missing readback'
        else:
            label = 'NA'

        if ('HELLO' in pilot_nocall) or 'GOOD MORNING' in pilot_nocall or 'GOOD DAY' in pilot_nocall or 'GOOD EVENING' in pilot_nocall or 'MORGEN' in pilot_nocall:
            label = 'Wrong pair'
        elif (callsign_availability == 'Wrong/Missing') and (label == 'Missing readback'):
            label = 'Wrong pair'

    else:
        return "Not detected!"
    return label


if __name__ == "__main__":
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()


    atco = utils.replace_words(args.atco.upper())
    pilot = utils.replace_words(args.pilot.upper())

    atco_split = atco.split()

    callsign = utils.naive_callsign_extraction(atco_split)
    # callsign = callsign.strip()
    num_group, letter_group = utils.split_callsign(callsign)
    callsign_availability = utils.assign_callsign_type(num_group, letter_group, pilot)

    callsign = utils.form_callsign(num_group, letter_group)
    if callsign in pilot:
        pilot_nocall = pilot.replace(callsign, '').strip()
    else:
        pilot_nocall = pilot

    # Check command values
    turn_group = []
    command_dict_result = {}
    label_list = []

    # Get command values
    label = assign_readback(atco, pilot, callsign, callsign_availability)

    print(f'ATCO: {args.atco} \nPilot: {args.pilot} \nCall_availability: {callsign_availability}\nLabel: {label}')