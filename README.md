# DD1354_Project

## What is this?

A simulation program done for the DD1354 course at KTH.

## Wanna run the simulation?

Make sure you have [Pygame](https://www.pygame.org/news) installed. The code is tested in Python 3.9.0

The code is tested and has a satisfactory results when running `py test_run.py 0.0001 0 0 0 8400`

Wanna mess around with parameters? To change ball, bat and visual setting, go into [stored.json](stored.json) and either change the values inside the existing ball bat or screen, or create a new one. Please note that the parameters must come in the same order as the already existing entries.

The arguments for `py test_run.py` are `(time step interval) (index of ball in stored.json) (index of bat in stored.json) <index of visual settings in stored.json> <interception index>` where `( )` is required and `< >` is optional (you will be requested to select an interception index in the program running if left out) (You must specify visual settings if you wanna specify interception on cmd-line)
