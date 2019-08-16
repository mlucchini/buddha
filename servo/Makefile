# Arduino Makefile. Refer to https://github.com/sudar/Arduino-Makefile

UNAME := $(shell uname)

# Default board
# --- nano ide 1.6
BOARD_TAG    = nano
BOARD_SUB    = atmega328old

# Common
ARDUINO_LIBS = ACE128 EEPROM Wire commands memory pid serial servo
ARDUINO_SKETCHBOOK = .
ARDUINO_LIB_PATH = $(HOME)/Documents/Arduino/libraries
MONITOR_BAUDRATE = 115200
CFLAGS_STD = -std=gnu11
CXXFLAGS_STD = -std=gnu++11

# Linux / Raspberry Pi
ifeq ($(UNAME), Linux)
    MONITOR_PORT = $(shell ls /dev/ttyUSB*)
    ARDUINO_DIR = /usr/share/arduino
    include /usr/share/arduino/Arduino.mk
endif

# MacOSX
ifeq ($(UNAME), Darwin)
    MONITOR_PORT = $(shell ls /dev/tty.wchusbserial*)
    ARDUINO_DIR = /Applications/Arduino.app/Contents/Java
    include /usr/local/opt/arduino-mk/Arduino.mk
endif
