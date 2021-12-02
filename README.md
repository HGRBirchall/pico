# pico

A set of programmes written (probably badly) for the Raspberry Pi Pico.

flux_mp.py - Reading heat flux sensors using HX711 ADC. The file relies on the HX711 library provided by robert-hh

soil.py is a soil monitoring and data logger that can be adapted to for a data logger for any analogue sensor.

newfile.py contains the class NewFile that takes the arguments file_name and j (for incrementing)
NewFile checks if a file exists and if it does increment the file number to prevent overwriting.
