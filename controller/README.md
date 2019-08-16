### Main commands

```sh
# Install requirements
pip3 install -r requirements.txt
 
# Run tests
pytest
 
# Servo CLI: run this from a development machine to send commands to a single servo motor (typically MacOSX)
python3 cli-servo.py
 
# Platform CLI: run this from the machine connected to the 6 servo motors (typically Raspberry Pi)
python3 cli-platform.py

```

### Servo configuration

Make sure you configure each servo:

```sh
python3 cli-servo.py
 
# Each servo should be given a different identifier from 0 to 5 clockwise
# This is necessary for the platform to identify each servo and send the appropriate commands
set_identifier [0-5]
 
# Each servo should be given a raw position that corresponds to the arm being horizontal
# This is necessary to initialize the absolute encoder
# Use the sketch provided in "troubleshooting" in the servo project to figure this number out
set_zero_raw_position [0-255]
```
