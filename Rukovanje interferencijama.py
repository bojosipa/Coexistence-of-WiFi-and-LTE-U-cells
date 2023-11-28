import numpy as np #biblioteka za rad sa nizovima i matricama numeričkih podataka u Pythonu
import scipy.signal #SciPy biblioteka - zbirka naučnih računarskih i tehničkih računarskih modula
import subprocess

#RUKOVANJE INTERFERENCIJOM ZASNOVANOM NA MJERENJU

# Parametri mjerenja
sample_rate = 20e6 # u Hz
frequency = 5e9 # u Hz
measurement_time = 1 # u sekundama

# Mjerenje nivoa interferencije
samples = np.random.normal(size=int(sample_rate * measurement_time))
interference_levels = 20 * np.log10(np.abs(scipy.signal.fft(samples)))

# Pronalazak  bin frekvencije sa najvećom interferencijom
highest_interference_bin = np.argmax(interference_levels)
highest_interference_frequency = highest_interference_bin * sample_rate / len(samples)

def update_duty_cycle(new_duty_cycle):
    # Ažuriranje ćelija na novi duty cycle
    print(f"Updating duty cycle to {new_duty_cycle}")

# Odluka za novi ciklus rada na osnovu izmjerenih nivoa smetnji
if highest_interference_frequency < frequency - 2e6:
    new_duty_cycle = 0.8
elif highest_interference_frequency > frequency + 2e6:
    new_duty_cycle = 0.2
else:
    new_duty_cycle = 0.5

# Ažuriranje novog ciklusa rada za sve ćelije
update_duty_cycle(new_duty_cycle)


#IZBJEGAVANJE INTERFERENCIJA

# Definisanje parametara za FFT
sample_rate = 20e6 # 20 MHz
fft_size = 2048

def generate_lte_u_samples():
    output = subprocess.run(['lte_scanner', '-i', 'wlan0'], capture_output=True)
    return output.stdout

def generate_wifi_samples():
    output = subprocess.run(['iwlist', 'wlan0', 'scan'], capture_output=True)
    return output.stdout

# Generiranje uzoraka LTE-U i Wi-Fi signala
lte_u_samples = generate_lte_u_samples()
wifi_samples = generate_wifi_samples()

# Izvršavanje FFT na uzorcima da se dobije spektralna gustina snage
lte_u_psd = scipy.signal.periodogram(lte_u_samples, fs=sample_rate, nfft=fft_size)
wifi_psd = scipy.signal.periodogram(wifi_samples, fs=sample_rate, nfft=fft_size)

# Identificiranje frekvencije bin s najvišim najvišim nivoom interferencije
lte_u_interference_bin = np.argmax(lte_u_psd[1])
wifi_interference_bin = np.argmax(wifi_psd[1])

class WiFiDevice:
    def __init__(self, mac_address, channel, transmission_power):
        self.mac_address = mac_address
        self.channel = channel
        self.transmission_power = transmission_power
        
    def set_transmission_power(self, power):
        self.transmission_power = power
        
    def set_channel(self, channel):
        self.channel = channel

    def enable_coexistence_protocol(self):
        # Omogućavanje  802.11v Wireless Network Management (WNM) protokola
        self.wnm_enabled = True
        # Omogućavanje 802.11k Radio Resource Measurement (RRM) protokol
        self.rrm_enabled = True
        # Omogućavanje 802.11v/k coexistence protokola
        self.coexistence_protocol_enabled = True

class LTEUDevice:
    def __init__(self, mac_address, channel, transmission_power):
        self.mac_address = mac_address
        self.channel = channel
        self.transmission_power = transmission_power

    def set_transmission_power(self, power):
        self.transmission_power = power

    def set_channel(self, channel):
        self.channel = channel

    def enable_coexistence_protocol(self):
        # Omogućavanje LTE-U Listen-Before-Talk (LBT) protokola
        self.lbt_enabled = True
        # Omogućavanje LTE-U Random Access Channel (RACH) protokola
        self.rach_enabled = True
        # Omogućavaje LTE-U coexistence protokola
        self.coexistence_protocol_enabled = True

# Kreiranje instance za WiFiDevice klasu za svaki uređaj
device1 = WiFiDevice("00:11:22:33:44:55", 1, 20)
device2 = WiFiDevice("11:22:33:44:55:66", 6, 15)
device3 = WiFiDevice("22:33:44:55:66:77", 11, 10)
# Dodavanje instanci u wifi_devices listu
wifi_devices = [device1, device2, device3]

# Kreiranje instance za LTEUDevice klasu za svaki uređaj
deviceA = LTEUDevice("A1:B2:C3:D4:E5:F6", 36, 20)
deviceB = LTEUDevice("B1:C2:D3:E4:F5:A6", 40, 15)
deviceC = LTEUDevice("C1:D2:E3:F4:A5:B6", 44, 10)
# Dodavanje instanci u lte_u_devices listu
lte_u_devices = [deviceA, deviceB, deviceC]


reduced_power_lte = -10 # dBm
increased_frequency_lte = 5 # sekunde


def mitigate_lte_u_interference():
    # Korak 1: Smanjenje snage transmisije LTE-U uređaja
    for device in lte_u_devices:
        device.set_transmission_power(reduced_power_lte)
    # Korak 2: Povećanje frekvenciju prebacivanja kanala za LTE-U uređaje
    for device in lte_u_devices:
        device.set_channel_switch_frequency(increased_frequency_lte)
    # Korak 3: Implementacija protokola za pravednu koegzistenciju sa Wi-Fi uređajima
    for device in lte_u_devices:
        device.enable_coexistence_protocol()

reduced_power_wifi = -12 # dBm
increased_frequency_wifi = 2 # sekunde

def mitigate_wifi_interference():
    # Korak 1: Smanjenje snage transmisije za Wi-Fi uređaje
    for device in wifi_devices:
        device.set_transmission_power(reduced_power_wifi)
    # Korak 2: Povećanje frekvenciju prebacivanja kanala za LTE-U uređaje
    for device in wifi_devices:
        device.set_channel_switch_frequency(increased_frequency_wifi)
    # Korak 3: Implementacija protokola za pravednu koegzistenciju sa Wi-Fi uređajima
    for device in wifi_devices:
        device.enable_coexistence_protocol()

def calculate_duty_cycle():
    wifi_duty_cycle = 0
    lte_u_duty_cycle = 0
    total_time = 0
    
    for device in wifi_devices:
        wifi_duty_cycle += device.transmission_time
        total_time += device.transmission_time
        
    for device in lte_u_devices:
        lte_u_duty_cycle += device.transmission_time
        total_time += device.transmission_time
    
    wifi_duty_cycle = wifi_duty_cycle / total_time
    lte_u_duty_cycle = lte_u_duty_cycle / total_time
    
    return wifi_duty_cycle, lte_u_duty_cycle




# Računanje DC-a signala interferencije
lte_u_duty_cycle = calculate_duty_cycle(lte_u_samples, lte_u_interference_bin, sample_rate, fft_size)
wifi_duty_cycle = calculate_duty_cycle(wifi_samples, wifi_interference_bin, sample_rate, fft_size)

# Uspoređivanje DC-ijeva i određivanje koji signal ima viši nivo interferencije
if lte_u_duty_cycle > wifi_duty_cycle:
    print("LTE-U has higher interference")
    # Implementacija mjera izbjegavanja interferencija za LTE-U
    mitigate_lte_u_interference()
else:
    print("Wi-Fi has higher interference")
    #  Implementacija mjera izbjegavanja interferencija za Wi-Fi
    mitigate_wifi_interference()



#UBLAŽAVANJE INTERFERENCIJA

import random
import threading # modul koji  koji će pokrenuti funkciju nakon što prođe određeno vrijeme

# Frequency hopping parameteri
frequency_bands = [5.2e9, 5.4e9, 5.6e9] # in Hz
hop_interval = 5 # in seconds

# Parametri za dinamički odabir frekvencije
min_frequency_separation = 2e6 # in Hz

user_position = (0, 0)


# Beamforming parametri
beamforming_vectors = {
    (0, 0): np.array([1, 1, 1, 1]),
    (0, 1): np.array([1, -1, 1, -1]),
    (1, 0): np.array([1, 1, -1, -1]),
    (1, 1): np.array([1, -1, -1, 1])
}

#Kreiranje ćelija sa vlastitom frekvencijom i beamforming faktorima
class Cell:
    def __init__(self, frequency, beamforming_weight):
        self.frequency = frequency
        self.beamforming_weight = beamforming_weight

cells = [Cell(5.2e9, 1), Cell(5.4e9, -1), Cell(5.6e9, 1)]


# Funkcija za ažuriranje frekvencije ćelije
def update_frequency(cell, frequency):
    cell.frequency = frequency

# Funkcija za frequency hopping
def frequency_hopping(cells):
    for cell in cells:
        new_frequency = random.choice(frequency_bands)
        update_frequency(cell, new_frequency)
    schedule_next_hop()

# Funkcija za postavljanje sljedećeg frequency hopa
def schedule_next_hop():
    threading.Timer(hop_interval, frequency_hopping).start()

# Funkcija za dinamički odabir frekvencije
def dynamic_frequency_selection(cells):
    for cell1 in cells:
        for cell2 in cells:
            if cell1 != cell2:
                frequency_separation = abs(cell1.frequency - cell2.frequency)
                if frequency_separation < min_frequency_separation:
                    if cell1.frequency < cell2.frequency:
                        update_frequency(cell1, cell1.frequency + min_frequency_separation)
                    else:
                        update_frequency(cell2, cell2.frequency + min_frequency_separation)

# Funkcija za beamforming
def beamforming(cells, user_position):
    x, y = user_position
    beamforming_vector = beamforming_vectors[(x % 2, y % 2)]
    for i, cell in enumerate(cells):
        cell.beamforming_weight = beamforming_vector[i]

# Zakazivanje sljedećeg frequency hopa
schedule_next_hop()

# Obavljanje dinamičkog odabira frekvencije i beamforminga na regularnoj bazi
threading.Timer(5, dynamic_frequency_selection, args=(cells,)).start()
threading.Timer(5, beamforming, args=(cells, user_position)).start()


#PONIŠTAVANJE INTERFERENCIJA

adjustment_step = 0.1

# Parametri za poništavanje interferenciranja
filter_length = 8 # broj 'tapova' u filteru
training_time = 1 # vrijeme potrebno filteru da nauči interferenciranje

# Funkcija za poništavanje interferencija
def interference_cancellation(received_signal, interferer_signal):
    # Učenje interferencija
    interferer_filter = np.zeros(filter_length)
    for i in range(int(sample_rate * training_time)):
        interferer_filter += np.correlate(interferer_signal[i:i+filter_length], received_signal[i])

    # Poništavanje interferencija
    filtered_signal = received_signal - np.convolve(interferer_signal, interferer_filter, mode='same')

    return filtered_signal

# Primjer upotrebe
received_signal = np.random.normal(size=int(sample_rate * measurement_time))
interferer_signal = np.random.normal(size=int(sample_rate * measurement_time))
filtered_signal = interference_cancellation(received_signal, interferer_signal)

#RUKOVANJE INTERFERENCIJAMA ZASNOVANO NA MAŠINSKOM UČENJU

from sklearn.ensemble import RandomForestRegressor #biblioteka za mašinsko učenje

# Parametri za mašinsko učenje
training_data = np.random.normal(size=(10000, 2)) # input: interference levels from other sources, output: received signal strength
test_data = np.random.normal(size=(1000, 2))

# Treniranje modela
model = RandomForestRegressor(n_estimators=100)
model.fit(training_data[:, :-1], training_data[:, -1])

# Korištenje modela za predviđanje snage signala
predicted_signal_strength = model.predict(test_data[:, :-1])

def adjust_transmission_power(predicted_signal_strength):
    new_transmission_power = []
    threshold = 0.5
    for i in range(len(predicted_signal_strength)):
        if predicted_signal_strength[i] < threshold:
            new_transmission_power.append(predicted_signal_strength[i] + adjustment_step)
        else:
            new_transmission_power.append(predicted_signal_strength[i] - adjustment_step)
    return new_transmission_power



#Korištenje predviđene snage signala za prilagodbu snage transmisije
adjust_transmission_power(predicted_signal_strength)
