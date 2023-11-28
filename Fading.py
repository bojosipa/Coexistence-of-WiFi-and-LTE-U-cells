#OPĆI MODEL FADING -a


import numpy as np

class Channel:
    def __init__(self, path_loss_exponent, shadow_std_dev, doppler_frequency, frequency, antenna_height, polarization, environment):
        self.path_loss_exponent = path_loss_exponent
        self.shadow_std_dev = shadow_std_dev
        self.doppler_frequency = doppler_frequency
        self.frequency = frequency
        self.antenna_height = antenna_height
        self.polarization = polarization
        self.environment = environment

    def calculate_fading(self, distance, velocity):
        # Path loss
        path_loss = distance**(-self.path_loss_exponent)
        
        # Shadowing
        shadowing = np.random.normal(0, self.shadow_std_dev)
        
        # Dopplerov pomak
        doppler_shift = np.random.normal(0, self.doppler_frequency)
        doppler_fading = np.cos(2 * np.pi * doppler_shift * (velocity / self.frequency))
        
        # Visina i polarizacija antene
        antenna_fading = (self.antenna_height / distance)**2
        if self.polarization == "vertical":
            polarization_fading = (1/np.sqrt(2))
        elif self.polarization == "horizontal":
            polarization_fading = 1
        
        # Radio okruženje
        if self.environment == "urban":
            environment_fading = 1
        elif self.environment == "suburban":
            environment_fading = 0.8
        elif self.environment == "rural":

            environment_fading = 0.5
        
        # Ukupni fading
        fading = path_loss * shadowing * doppler_fading * antenna_fading * polarization_fading * environment_fading
        return fading


#Rayleighov fading


def calculate_rayleigh_fading(num_samples):
    fading_samples = np.random.normal(0,1,num_samples) + 1j*np.random.normal(0,1,num_samples)
    rayleigh_fading= np.abs(fading_samples)
    return rayleigh_fading


# RICIANOV FADING

def calculate_rician_fading(num_samples, k_factor):
    fading_samples= np.random.normal(0, 1, num_samples) + 1j*np.random.nromal(0, 1, num_samples)
    los_compnent = np.sqrt(k_factor / (k_factor+1))
    multipath_component = np.sqrt(1/(2*(k_factor + 1))) * fading_samples
    riician_fading = los_compnent + multipath_component
    return np.abs(rician_fading)

# NAKAGAMI FADING

def calculate_nakagami_fading(num_samples, m_factor):
    nakagami_fading= np.random.gamma(m_factor, 1, num_samples)
    return nakagami_fading