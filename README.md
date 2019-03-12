# 4-digit-motor-task
Motor task requiring to type 4-digit numbers with the left hand, EEG-compatible for between-blocks resting state recordings.

The program will store the results as .csv files in the folder 'Results' (created automatically if missing).

There is a 300 s resting state period at the beginning, which can be skipped by pressing RETURN, as for any other 120 s resting-state.

There is a total of 10 blocks, each followed by resting state recordings. Number of trials per block (max 40) and other settings can be changed under #task parameters (lines 68-74).

EEG triggers:
  -each resting block starts with a trigger going from 41 to 50 and always ends with the trigger 40.
  -the preliminary resting-state uses 1 as the trigger.
