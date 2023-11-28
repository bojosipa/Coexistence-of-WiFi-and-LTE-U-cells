import random

class BaseStation:
    def __init__(self, id, position, frequency, tx_power, antenna_height, polarization):
        self.id = id
        self.position = position
        self.frequency = frequency
        self.tx_power = tx_power
        self.antenna_height = antenna_height
        self.polarization = polarization
        self.equipment_status = "OPERATIONAL"

    def check_equipment(self):
        """
        Metoda provjerava status opreme
       
        """
        if self.frequency > 100 and self.frequency < 1000:
            self.equipment_status = "OPERATIONAL"
        else:
            self.equipment_status = "FAILED"
        return self.equipment_status

    def repair_equipment(self):
        """
        Metoda popravlja pokvarenu opremu
        """
        if self.equipment_status == "FAILED":
            self.frequency = random.randint(100, 1000)
            self.equipment_status = "OPERATIONAL"
            print("Equipment has been repaired.")
        else:
            print("Equipment is already operational.")

# Kreiranje instanci bazne stanice
bs1 = BaseStation(1, (0, 0), 800, 20, 10, "VERTICAL")
bs2 = BaseStation(2, (25, 0), 900, 18, 8, "HORIZONTAL")
bs3 = BaseStation(3, (50, 0), 950, 15, 6, "VERTICAL")
bs4 = BaseStation(4, (75, 0), 700, 25, 12, "HORIZONTAL")

# Provjera statusa opreme
print(bs1.check_equipment()) # "OPERATIONAL"
print(bs2.check_equipment()) # "OPERATIONAL"
print(bs3.check_equipment()) # "OPERATIONAL"
print(bs4.check_equipment()) # "OPERATIONAL"

# Simulacija pada
bs4.frequency = 50
print(bs4.check_equipment()) # "FAILED"

# Popravka opreme
bs4.repair_equipment()
print(bs4.check_equipment()) # "OPERATIONAL"
