# RulebasedRED
Code for  paper "Enabling noisy label usage for out-of-airspace data in air-traffic control" at ASRU 2023. The script for  generating noisy readback error labels using Rule-based method.

## Code
The script [weak_labels.py](weak_labels.py) generates noisy readback error labels for ATCO-pilot utterance. The [data](data/) folder contains the necessary ATC keyword list.

## Run
The script [weak_labels.py](weak_labels.py) takes an ATCO utterance containing one or more commands and the pilot readback as input. 
```
python weak_labels.py <ATCO_command> <pilot_readback>
```
The output returns the readback error labels assigned into one of five classes: Correct, Partial, Missing, Wrong readback and Wrong ATCO-pilot pairs. 