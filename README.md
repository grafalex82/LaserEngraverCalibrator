# Laser Engraver Calibrator

Laser Engraver Calibrator is a set of simple scripts supposed to help engraver calibration. 
These scripts generate gcode that run your engraver in different modes, speed, PWM power, etc.
The scripts were tested with grbl-based 2-axis laser engraver, but should also work fine with other machines as well (script produces standard GCODE)


Calibrator.py - this script help you to find optimal engraving speed and PWM power. 
The output gcode draws a 'matrix' of lines. One axis is engraving speed, the other is PWM power. 
Additionally script draws a ruler that is supposed to understand what the value is.

numpasses.py - this script helps to find minimal number of passes needed to cut a material. 
Script also draws a 'matrix'. One axis is number of passes, the other is cutting speed. Laser runs at maximum power.

Script parameters are located at the script header. Reasonable defaults are in.