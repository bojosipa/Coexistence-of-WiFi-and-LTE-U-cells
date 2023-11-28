import random
import numpy as np
import x2ap_services # hipotetički modul za X2AP protokol
import math

# Path loss model
def path_loss(distance, frequency):
    # Example of a log-distance path loss model with shadowing
    PLd = 127.41 + 37.6 * math.log10(distance) - 13.82 * math.log10(frequency)
    shadowing = random.normalvariate(0, 8) # shadowing with standard deviation of 8 dB
    PL = PLd + shadowing
    return PL

# Shadowing model
def shadowing(distance, frequency):
    # Primjer log-normal shadowing modela
    standard_deviation = 8 # dB
    shadowing = random.normalvariate(0, standard_deviation) # mean = 0, standard deviation = 8 dB
    return shadowing

# Upotreba primjera
distance = 50 # meters
frequency = 2.4 # GHz
shadow = shadowing(distance, frequency)
print("Shadowing: ", shadow, " dB")
loss = path_loss(distance, frequency)
print("Path loss: ", loss, " dB")