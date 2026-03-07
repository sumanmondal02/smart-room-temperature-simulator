class TemperaturePhysics:
    def __init__(self, external_temp=36):
        self.external_temp = external_temp
        self.room_temp = 35
        self.thermal_mass = 0.05     # Slower response
        self.heating_rate = 0.02
        self.max_cooling_per_sec = 0.28  # Max °C drop per second
        self.compressor_power = 0

    def update(self, ac_on, set_temp, dt=1):

        if ac_on:
            # Desired cooling change
            delta = self.thermal_mass * (self.room_temp - set_temp)

            # Limit cooling rate (real AC constraint)
            delta = min(delta, self.max_cooling_per_sec)

            self.room_temp -= delta

        else:
            # Gradual heating toward external temperature
            delta = self.heating_rate * (self.external_temp - self.room_temp)
            self.room_temp += delta

        return self.room_temp
