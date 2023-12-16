import json

commands = open('commands.txt').read().split('\n')[:-1]
num_words = open('numbers.txt').read().split('\n')[:-1]
letter_words = open('letters.txt').read().split('\n')[:-1]
turn = ["LEFT", "RIGHT"]

def naive_callsign_extraction(atco):
    callsign = ''
    for words in atco:
        if words not in commands:
            callsign = callsign + ' ' + words
        else:
            break
    return callsign.strip()

def replace_words(sent):
    if '.' in sent:
        sent = sent.replace('.', 'DOT ')
    return sent.strip()

def split_callsign(callsign):
    word_group =[]
    num_group = []
    letter_group = []

    # Get the numbers in the callsign
    for words in callsign.split():
        if words in num_words:
            word_group.append(words)
        else:
            if word_group:
                num_group.append(" ".join(word_group).strip())
                word_group = []
    if word_group:
        num_group.append(" ".join(word_group).strip())

    # Get the letters in the callsign
    word_group = []
    for words in callsign.split():
        if words in letter_words:
            word_group.append(words)
        else:
            if word_group:
                letter_group.append(" ".join(word_group).strip())
                word_group = []
    if word_group:
        letter_group.append(" ".join(word_group).strip())

    return num_group, letter_group

def assign_callsign_type(num_group, letter_group, pilot):
    callsign_availability = 'NA'

    # Check if callsign is present - Partial and full
    if num_group and letter_group:
        if num_group[0] in pilot or letter_group[0] in pilot:
            callsign_availability = 'Fully available'
        elif num_group and num_group[0] in pilot:
            callsign_availability = 'Partial'
        elif letter_group and letter_group[0] in pilot:
            callsign_availability = 'Partial'
        else:
            callsign_availability = 'Wrong/Missing'
    elif not letter_group:
        if num_group and num_group[0] in pilot:
            callsign_availability = 'Fully available'
        else:
            callsign_availability = 'Wrong/Missing'
    elif not num_group:
        if letter_group and letter_group[0] in pilot:
            callsign_availability = 'Fully available'
        else:
            callsign_availability = 'Wrong/Missing'
    else:
        callsign_availability = 'NA'
    return callsign_availability

def form_callsign(num_group, letter_group):
    callsign = ''
    if num_group and letter_group:
        callsign = num_group[0] + ' ' + letter_group[0]
    elif num_group and not letter_group:
        callsign = num_group[0]
    elif letter_group and not num_group:
        callsign = letter_group[0]
    return callsign

def get_command_value(atco, ):
    word_group =[]
    num_group = []
    turn_group = []
    for words in atco:
        if words in num_words:
            word_group.append(words)
        else:
            if word_group:
                num_group.append(word_group)
                word_group = []
        if words in turn:
            num_group.append([words])
    if word_group:
            num_group.append(word_group)
    return num_group

def add_label_list(group, pilot, label_list):
    for num in group:
        if num in pilot:
            label_list.append("Present")
        else:
            label_list.append("NA")
    return label_list

def run_for_contact(group, pilot, command_dict_result, num_group):
    group_copy = group.copy()
    label_list = []
    for case in ['scenario 1', 'scenario 2', 'scenario 3', 'scenario 4']:
        if case == 'scenario 1':
            group_copy.remove('DOT')
            num = " ".join(group_copy).strip()
        elif case == 'scenario 2':
            group_copy.remove('DOT')
            group_copy = group_copy[1:]
            num = " ".join(group_copy).strip()
        elif case == 'scenario 3':
            group_copy = group_copy[1:]
            num = " ".join(group_copy).strip()
            num_group.remove(group)
        else:
            label_list = add_label_list(group_copy, pilot, [])
            return pilot, command_dict_result, label_list
        if num in pilot:
            command_dict_result[" ".join(group).strip()] = "Present"
            pilot = pilot.replace(num, '')
            group_copy = group.copy()
            return pilot, command_dict_result, label_list
