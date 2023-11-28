import random

class Station:
    def __init__(self, id, position, velocity, max_speed, max_acceleration, environment, battery_level):
        self.id = id
        self.position = position
        self.velocity = velocity
        self.max_speed = max_speed
        self.max_acceleration = max_acceleration
        self.environment = environment
        self.battery_level = battery_level
        self.connection_status = True

    def update_position(self, time_interval, obstacles, stations):
        self.velocity = self.calculate_velocity(obstacles, stations)
        self.position[0] += self.velocity[0] * time_interval
        self.position[1] += self.velocity[1] * time_interval

    def calculate_velocity(self, obstacles, stations):
        # Ograničenje brzine maksimalnom brzinom  maksimalnom akceleracijom
        new_velocity = [min(self.velocity[0] + self.max_acceleration, self.max_speed),
                        min(self.velocity[1] + self.max_acceleration, self.max_speed)]

    def environment_factor(self, environment):
        if environment == "windy":
            return 0.7
        elif environment == "hot":
            return 0.8
        elif environment == "cold":
            return 0.9
        else:
            return 1.0
        
        # Utjecaj okruženja na brzinu
        new_velocity[0] *= self.environment_factor(self.environment)
        new_velocity[1] *= self.environment_factor(self.environment)
        
        # Utjecaj prepreka na brzinu
        for obstacle in obstacles:
            distance = math.sqrt((self.position[0] - obstacle[0])**2 + (self.position[1] - obstacle))
            distance = math.sqrt((self.position[0] - obstacle[0])**2 + (self.position[1] - obstacle[1])**2)
            if distance < obstacle[2]:
                new_velocity[0] *= 0.5
                new_velocity[1] *= 0.5





   # Utjecaj interferencija od drugih stanica na brzinu
        for station in stations:
            if station.id != self.id:
                distance = math.sqrt((self.position[0] - station.position[0])**2 + (self.position[1] - station.position[1])**2)
                if distance < 50:
                    new_velocity[0] *= 0.8
                    new_velocity[1] *= 0.8

        # Utjecaj nivoa baterije na brzinu
        if self.battery_level < 20:
            new_velocity[0] *= 0.5
            new_velocity[1] *= 0.5

        # Utjecaj statusa konekcije na brzinu
        if not self.connection_status:
            new_velocity[0] *= 1.2
            new_velocity[1] *= 1.2

        return new_velocity