# Soil moisture sensor data logger. Analogue sensor powering three pumps with LED status indicators and individual sensor adjustment.
# Sensors set to record as N/A below 35% reading due to no sensor attached reading ~20% on analogue pins.

import machine, utime, random
from newfile import NewFile

sensor_soil0 = machine.ADC(26)
sensor_soil1 = machine.ADC(27)
sensor_soil2 = machine.ADC(28)
pump0 = machine.Pin(1, machine.Pin.OUT)
led_pump0 = machine.Pin(0, machine.Pin.OUT)
pump1 = machine.Pin(2, machine.Pin.OUT)
led_pump1 = machine.Pin(3, machine.Pin.OUT)
pump2 = machine.Pin(4, machine.Pin.OUT)
led_pump2 = machine.Pin(5, machine.Pin.OUT)
led_satisfied = machine.Pin(7, machine.Pin.OUT)

button = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Make sure that LEDs and relays are not running. This prevents accidental watering.
pump0.value(1)
led_pump0.value(0)
pump1.value(1)
led_pump1.value(0)
pump2.value(1)
led_pump2.value(0)
led_satisfied.value(0)

# Set sleep period post test
wait = 1 # wait between readings
repeat = 600 # set to repeat code execution every 10 minutes

#create the button handlers for the 
def button_handler0(trigger):
    button.irq(handler=None)
    trigger = round(sensor_soil0.read_u16()*conversion_factor,1)
    print (trigger)
    led_pump0.value(0)
    led_satisfied.value(1)        
    for i in range (4):
        led_pump0.toggle()
        utime.sleep_ms(500)
    led_satisfied.value(0)
    global trigger0
    trigger0 = trigger + 1

def button_handler1(trigger):
    button.irq(handler=None)
    trigger = round(sensor_soil1.read_u16()*conversion_factor,1)
    print (trigger)
    led_pump1.value(0)
    led_satisfied.value(1)        
    for i in range (4):
        led_pump1.toggle()
        utime.sleep_ms(500)
    led_satisfied.value(0)
    global trigger1
    trigger1 = trigger + 1
    
def button_handler2(trigger):
    button.irq(handler=None)
    trigger = round(sensor_soil2.read_u16()*conversion_factor,1)
    print (trigger)
    led_pump2.value(0)
    led_satisfied.value(1)        
    for i in range (4):
        led_pump2.toggle()
        utime.sleep_ms(500)
    led_satisfied.value(0)
    global trigger2
    trigger2 = trigger + 1
    
def start(trigger):
    button.irq(handler=None)
    button_handler0(trigger)
    button_handler1(trigger)
    button_handler2(trigger)
    print ("Soil 0 ", trigger0, "Soil 1 ", trigger1, "Soil 2 ", trigger2)
    led_pump0.value(0)
    led_pump1.value(0)
    led_pump2.value(0)
    led_satisfied.value(1)        
    for i in range (4):
        led_pump0.toggle()
        led_pump1.toggle()
        led_pump2.toggle()
        utime.sleep_ms(500)
    led_satisfied.value(0)
 

# Flash green LED to show that programme has started then wait one second
for i in range (20):
    led_satisfied.toggle()
    utime.sleep_ms(100)

conversion_factor = 100/(65535)
trigger0 = 100
reading0 = round(sensor_soil0.read_u16()*conversion_factor,1)
trigger1 = 100
reading1 = round(sensor_soil1.read_u16()*conversion_factor,1)
trigger2 = 100
reading2 = round(sensor_soil2.read_u16()*conversion_factor,1)

if button.irq(trigger=machine.Pin.IRQ_RISING, handler=start) is True:
    trigger0 = trigger
    trigger1 = trigger
    trigger2 = trigger

# set up data logging to /data/data_logger(x).txt
j = 1
file_name = "/data/soil_logger"+str(j)+".txt"

NewFile(file_name, j)

file = open(file_name, "w")
log = "Soil 0 (V)", "Trigger0 (V)", "Soil 1 (V)", "Trigger0 (V)", "Soil 2 (V)", "Trigger0 (V)"
file.write(str(log)+"\n")
log = reading0, trigger0, reading1, trigger1, reading2, trigger2
file.write(str(log)+"\n")
file.flush

utime.sleep(10*wait)


while True:

# Check soil0 and run if soil is dryer than initial reading
# Analogue pins read ~20% when no sensor is plugged in.
# To prevent accidental watering when unplugged a low of 35% and high of 99% has been set.

    reading0 = round(sensor_soil0.read_u16()*conversion_factor,1)
    soil0 = trigger0 - reading0
    if reading0 >=99 or reading0<=35:
        reading0 = "N/A"
    else:
        if soil0 >= 0:
            led_pump0.value(0)
            led_satisfied.value(0)
            for i in range (8):
                led_satisfied.toggle()
                led_pump0.toggle()
                utime.sleep_ms(250)
            pump0.value(1)
            utime.sleep(wait)
        if soil0 < 0:
            led_pump0.value(1)
            led_satisfied.value(0)
            pump0.value(0)
            for i in range (20):
                led_pump0.toggle()
                utime.sleep_ms(250)
            pump0.value(1)
            utime.sleep(wait)
        
# Check soil1 and run if soil is dryer than initial reading 
    reading1 = round(sensor_soil1.read_u16()*conversion_factor,1)
    soil1 = trigger1 - reading1
    if reading1 >=99 or reading1<=35:
        reading1 = "N/A"
    else:
        if soil1 >= 0:
            led_pump1.value(0)
            led_satisfied.value(0)
            for i in range (8):
                led_satisfied.toggle()
                led_pump1.toggle()
                utime.sleep_ms(250)
            pump1.value(1)
            utime.sleep(wait)
        if soil1 < 0:
            led_pump1.value(1)
            led_satisfied.value(0)
            pump1.value(0)
            for i in range (20):
                led_pump1.toggle()
                utime.sleep_ms(250)
            pump1.value(1)
            utime.sleep(wait)
    
# Check soil1 and run if soil is dryer than initial reading 
    reading2 = round(sensor_soil2.read_u16()*conversion_factor,1)
    soil2 = trigger2 - reading2
    if reading2 >=99 or reading2<=35:
        reading2 = "N/A"
    else:
        if soil2 >= 0:
            led_pump2.value(0)
            led_satisfied.value(0)
            for i in range (8):
                led_satisfied.toggle()
                led_pump2.toggle()
                utime.sleep_ms(250)
            pump2.value(1)
            utime.sleep(wait)
        if soil2 < 0:
            led_pump2.value(1)
            led_satisfied.value(0)
            pump2.value(0)
            for i in range (20):
                led_pump2.toggle()
                utime.sleep_ms(250)
            pump2.value(1)
            utime.sleep(wait)
    log = reading0, trigger0, reading1, trigger1, reading2, trigger2
    file.write(str(log)+"\n")
    file.flush
    utime.sleep(repeat)
