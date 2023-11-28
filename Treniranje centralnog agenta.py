import random
import numpy as np
import x2ap_services
import math
import wifi_protocol_services #hipotetička biblioteka za Wi-Fi protokole 

# Parametri
alpha = 0.3 #stopa učenja
epsilon = 0.5
Ttarget = 160 # Ciljana brzina podataka u Mbps
M = 160 # Ciljana maksimalna brzina podataka u Mbps
A = [0.2,0.4,0.6,0.8] # Radni ciklusi
S = [0,1,2,3] # Stanja
wi_fi_cells_data_rate = [500000, 1000000, 2000000, 4000000] # Brzine podataka Wi - Fi ćelija
lteu_cells_data_rate = [500000, 1000000, 2000000, 4000000] # Brzine podataka LTE-U ćelija
Ttxwifi = sum(wi_fi_cells_data_rate) #Ukupna brzina podataka Wi-Fi ćelija
Ttxlteu = sum(lteu_cells_data_rate) #Ukupna brzina podataka LTE-U ćelija
UDPRate = [2, 4]
duty_cycles = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
data_rates = [2, 4]
ABS_pattern = 40

# Q-tabela sa nasumičnom procjenom početnih vrijednosti
Q = np.random.rand(4,8)

# Funkcija za provjeru trenutnog stanja sistema
def check_state(Ttxwifi, Ttxlteu, UDPRate):
    if Ttxwifi + Ttxlteu <= 40 and UDPRate <= 2:
        return 0
    elif Ttxwifi + Ttxlteu <= 80 and UDPRate <= 4:
        return 1
    elif Ttxwifi + Ttxlteu <= 120 and UDPRate <= 6:
        return 2
    else:
        return 3

def calculate_reward(Ttxwifi, Ttxlteu, Ttarget):
    # Izračun brzine prijenosa podataka
    data_rate = Ttxwifi + Ttxlteu

    # Izračun interferencirajućih signala
    interference = 0

    # Izračun nagrade
    reward = data_rate - interference

    return reward


class WifiCell:
    def __init__(self, id, duty_cycle, data_rate, position, frequency, modulation, coding, distance, CSI, handover_flag, fading_coefficient):
        self.id = id
        self.duty_cycle = duty_cycle
        self.data_rate = data_rate
        self.position = position
        self.frequency = frequency
        self.modulation = modulation
        self.coding = coding
        self.distance = distance
        self.CSI = CSI
        self.handover_flag = handover_flag
        self.fading_coefficient = fading_coefficient

    def update_fading(self, new_coefficient):
        self.fading_coefficient = new_coefficient
    def set_duty_cycle(self, new_dc):
        self.duty_cycle = new_dc

    def update_frequency(self, new_frequency):
        self.frequency = new_frequency

    def update_modulation(self, new_modulation):
        self.modulation = new_modulation

    def update_coding(self, new_coding):
        self.coding = new_coding

    def update_distance(self, new_distance):
        self.distance = new_distance

    def update_CSI(self, new_CSI):
        self.CSI = new_CSI

    def update_handover_flag(self, new_handover_flag):
        self.handover_flag = new_handover_flag

wifi_cells = []


for i in range(4):
    position = (i * 25, 0) 
    frequency = random.choice(range(2400, 2500))
    modulation = random.choice(["OFDM", "DSSS"])
    coding = random.choice([1, 2, 3])
    distance = random.uniform(0, 100)
    CSI = random.uniform(-30, -20)
    handover_flag = random.choice([True, False])
    wifi_cells.append(WifiCell(i, random.choice(duty_cycles), random.choice(data_rates), position, frequency, modulation, coding, distance, CSI, handover_flag))

class LTECell:
    def __init__(self, id, duty_cycle, data_rate, position, frequency, modulation, coding, distance, CSI, handover_flag):
        self.id = id
        self.duty_cycle = duty_cycle
        self.data_rate = data_rate
        self.position = position
        self.frequency = frequency
        self.modulation = modulation
        self.coding = coding
        self.distance = distance
        self.CSI = CSI
        self.handover_flag = handover_flag

    def set_duty_cycle(self, new_dc):
        self.duty_cycle = new_dc

    def update_frequency(self, new_frequency):
        self.frequency = new_frequency

    def update_modulation(self, new_modulation):
        self.modulation = new_modulation

    def update_coding(self, new_coding):
        self.coding = new_coding

    def update_distance(self, new_distance):
        self.distance = new_distance

    def update_CSI(self, new_CSI):
        self.CSI = new_CSI

    def update_handover_flag(self, new_handover_flag):
        self.handover_flag = new_handover_flag

lteu_cells = []

for i in range(4):
    position = (i * 25, 0) 
    frequency = random.choice(range(1900, 2100))
    modulation = random.choice(["QPSK", "16QAM", "64QAM"])
    coding = random.choice([1, 2, 3])
    distance = random.uniform(0, 100)
    CSI = random.uniform(-30, -20)
    handover_flag = random.choice([True, False])
    lteu_cells.append(LTECell(i, random.choice(duty_cycles), random.choice(data_rates), position, frequency, modulation, coding, distance, CSI, handover_flag))

def parse_parameter(new_dc, new_frequency, new_modulation, new_coding, new_distance, new_CSI, new_handover_flag):
# Upotreba x2ap_services modula za slanje informacija o novom stanju i parametrima LTE-u ćelijama
    x2ap_services.send_dc_update(new_dc)
    x2ap_services.send_frequency_update(new_frequency)
    x2ap_services.send_modulation_update(new_modulation)
    x2ap_services.send_coding_update(new_coding)
    x2ap_services.send_distance_update(new_distance)
    x2ap_services.send_CSI_update(new_CSI)
    x2ap_services.send_handover_flag_update(new_handover_flag)

def update_parameters(new_dc, new_frequency, new_modulation, new_coding, new_distance, new_CSI, new_handover_flag):
    for cell in lteu_cells:
        cell.set_duty_cycle(new_dc)
        cell.update_frequency(new_frequency)
        cell.update_modulation(new_modulation)
        cell.update_coding(new_coding)
        cell.update_distance(new_distance)
        cell.update_CSI(new_CSI)
        cell.update_handover_flag(new_handover_flag)

def update_parameters(new_channel, new_frequency, new_modulation, new_coding, new_distance, new_CSI, new_roaming_flag):
    for cell in wifi_cells:
        cell.set_channel(new_channel)
        cell.update_frequency(new_frequency)
        cell.update_modulation(new_modulation)
        cell.update_coding(new_coding)
        cell.update_distance(new_distance)
        cell.update_CSI(new_CSI)
        cell.update_roaming_flag(new_roaming_flag)

def update_duty_cycle(new_duty_cycle):
    # Ažuriranje ćelija na novi duty cycle
    print(f"Updating duty cycle to {new_duty_cycle}")

num_episodes = 1000 #broj treninga koje će agent proći
episode = 0

for episode in range(num_episodes):
    current_state = check_state(Ttxwifi, Ttxlteu, UDPRate)

#Izbor nasumične akcije baziranom na epsilon-greedy politici
if np.random.uniform(0,1) < epsilon:
    action = np.random.choice(A)
else:
    action = np.argmax(Q[current_state,:])

#Uzimanje akcije i računanje novog stanja i nagrade
parse_parameter(action)
update_duty_cycle(action)
Ttxwifi = sum([cell.data_rate * cell.fading_coefficient for cell in wifi_cells])
Ttxlteu = sum([cell.data_rate * cell.duty_cycle for cell in lteu_cells])
new_state = check_state(Ttxwifi, Ttxlteu, UDPRate)
reward = calculate_reward(Ttxwifi, Ttxlteu, Ttarget)

#Ažuriranje Q-table prema Bellmanovoj jednačini za q-algoritam
Q[current_state, action] = Q[current_state, action] + alpha * (reward + np.max(Q[new_state,:]) - Q[current_state, action])


#Provjera uvjeta za prekid treninga
if  episode == num_episodes-1:
    print("Training converged/completed in episode: ", episode)
        

#Finalna Q-tabela
print("Final Q-Table: ", Q)

# Kolekcija novih podataka
new_Ttxwifi = sum([cell.data_rate * cell.fading_coefficient for cell in wifi_cells])
new_Ttxlteu = sum([cell.data_rate * cell.duty_cycle for cell in lteu_cells])
new_UDPRate = sum([cell.data_rate for cell in lteu_cells])
new_state = check_state(new_Ttxwifi, new_Ttxlteu, new_UDPRate)

# Izračun nagrade
new_data_rate = sum([cell.data_rate * cell.fading_coefficient * cell.duty_cycle for cell in lteu_cells]) + sum([cell.data_rate * cell.fading_coefficient for cell in wifi_cells])
new_interference = sum([cell1.data_rate * math.exp(-distance / 10) for cell1 in lteu_cells for cell2 in lteu_cells if cell1 != cell2]) + sum([cell1.data_rate * math.exp(-distance / 10) for cell1 in wifi_cells for cell2 in wifi_cells if cell1 != cell2])
new_reward = new_data_rate - new_interference

# Ažuriranje Q-tabele
Q[current_state, action] = Q[current_state, action] + alpha * (new_reward + epsilon * max(Q[new_state, :]) - Q[current_state, action])

# Ažuriranje trenutnog stanja i akcija
current_state = new_state
action = np.argmax(Q[current_state, :])












