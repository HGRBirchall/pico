"""micropython Flux sensor"""
""" Raspberry Pi Pico adjusted code"""
""" FluxTeq Heat Flux Sensors on HX711 24 bit ADC """
from machine import ADC, Pin
import time, uos
from sys import exit
from hx711 import HX711

# Set up to read from HX711 using Pin 19 to read in and Pin 16 as the clock signal
gain = 128 # Channel A @ 128 or 64, Channel B @ 32
hx = HX711(16, 19, gain)

# Set program variables
j = 1
k = 1
file_name = "/data/flux_logger"
file = file_name + str(j) + ".txt"

#flux = ADC(Pin(28))
temp1 = ADC(Pin(27)) # Internal
temp2 = ADC(Pin(26)) # External

led_onboard = machine.Pin(25, machine.Pin.OUT)

# Define Heat Flux sensor calibration. Select sensor in use.
PH21611 = 0.00000125 # PHFS-01 SN: PH-21611 (10' lead)
PH21649 = 0.00000126 # PHFS-01 SN: PH-21649 (15' lead)
HFP0105 = 0.00006004 # HFP01-05 SN: 18482 (5m cable)

Scal = HFP0105

if Scal == HFP0105:
    SensA = 0.0008
     
elif Scal == PH21649:
    SensA = 0.000645

elif Scal == PH21611:
    SensA = 0.000645
    
else:
    exit()
    
# Define the thermistor values. Select thermistors in use
# Thermistor = [Ro, To, beta]
Pimoroni = [10000.0, 25.0, 3950.0]
Sandberg = [10000.0, 0.0, 3950.0]

Thermistor = Sandberg

# Programme delays
delay = 0.1
rest = 20 * delay
flash = 0.1

# check if file exists and create a new file if not, or increment the number if it does
def NewFile(file_name, j):
    file = file_name + str(j) + ".txt"
    try:
        while uos.stat(file):
            j = j + 1
            file = file_name + str(j) + ".txt"
        
    except OSError:
        file_create = open(file, "w")
        print ("File has been created as \"" , file ,"\"")
        file_name = file
        return file_name

# Steinhart-Hart equation for 10KO resistor at 25C with temperature coefficient of 3950
def steinhart_temperature_C(r, Ro=10000.0, To=25.0, beta=3950.0):
    import math
    steinhart = math.log(r / Ro) / beta      # log(R/Ro) / beta
    steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
    steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C
    return steinhart

def get_flux():
    val = hx.read()
    val = val / (16777216 * gain) # Reading in Volts
    return val

def Flux_sensor():
    # main programme loop
    
    led_onboard.value(0)
    Flux = []
    Temp1 = []
    Temp2 = []
    j = 1
    
    # create list to average
    for j in range(10):
        led_onboard.toggle()
        j = j + 1
        
        R1 = 10000 / (65535/temp1.read_u16() - 1)
        T1 = steinhart_temperature_C(R1, Thermistor[0], Thermistor[1], Thermistor[2])
        Temp1.append(T1)
        
        R2 = 10000 / (65535/temp2.read_u16() - 1)
        T2 = steinhart_temperature_C(R2, Thermistor[0], Thermistor[1], Thermistor[2])
        Temp2.append(T2)
        
        St = (0.00334 * T1 + 0.917) * Scal
        F = (get_flux()) / St
        Flux.append(F)
        
        time.sleep(delay)

    Flux_list = (Flux[0] + Flux[1] + Flux[2] + Flux[3] + Flux[4] + Flux[5] + Flux[6] + Flux[7] + Flux[8] + Flux[9])/10
    Flux_av = round(Flux_list, 2)
    
    Temp1_list = (Temp1[0] + Temp1[1] + Temp1[2] + Temp1[3] + Temp1[4] + Temp1[5] + Temp1[6] + Temp1[7] + Temp1[8] + Temp1[9])/10
    Temp1_av = round(Temp1_list, 2)
    
    Temp2_list = (Temp2[0] + Temp2[1] + Temp2[2] + Temp2[3] + Temp2[4] + Temp2[5] + Temp2[6] + Temp2[7] + Temp2[8] + Temp2[9])/10
    Temp2_av = round(Temp2_list, 2)
    
    # Creates list for appending results to file
#    B = round(get_voltage(bat) * 2.98 ,2)
    I = round((i - 1) * (10 * delay + rest))
    Watts = Flux_av * SensA
    Uav = Flux_av / (Temp1_av - Temp2_av)
    log = [I, Flux_av, Watts, Temp1_av, Temp2_av , Uav] #, B]
    
    led_onboard.value(0)
    time.sleep(rest)
    return log

led_onboard.value(1)

time.sleep(rest)

for i in range(9):
    led_onboard.toggle()
    time.sleep(flash)

# Stop the programme from running if no sensors are connected.
F=100 # comment out if using with sensor attached
# F=1000 # comment out is using without sensor for testing

# Check if file system is writable
try:
    
    File = NewFile(file_name, j)
    print (File)
    # Open new file to be written to
    file = open(File, "w")
    log = "Time (s), Flux (W/m2), Watts (W), Temp1 (C), Temp2 (C), U-vlaue"
    file.write(log+"\n")
    file.flush

    while F > 200:
        j = 1
        Flux = []
        for j in range(1,11):
            j = j + 1
            
            F1 = (get_flux()) * 60.04 * 100 / 8
            Flux.append(F1)
            
            time.sleep(delay)
            
        Flux = (Flux[0] + Flux[1] + Flux[2] + Flux[3] + Flux[4] + Flux[5] + Flux[6] + Flux[7] + Flux[8] + Flux[9])/10
        print(Flux)
        F = Flux
        
        time.sleep(rest)

    i = 1

    # main programme loop
    while True:
        
        for j in range(10):
            log = Flux_sensor()
            # Append results to file
            file.write(str(log)+"\n")
            print(log)
            file.flush
            
            i = i + 1
            led_onboard.value(0)
            time.sleep(rest)
            
        file.close()
        file = open(File, "a")

# If file system is locked run code instesd
except OSError:
    
    print("File system locked. No file being written")
    
    for i in range(1, 11):
        log = Flux_sensor()
        print (log)
        
    exit()
