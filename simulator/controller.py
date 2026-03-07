class ACController:
    def __init__(self):
        self.ac_on = False
        self.deadband = 0.4

    def update(self, current_temp, set_temp):

        if current_temp >= set_temp + self.deadband:
            self.ac_on = True

        elif current_temp <= set_temp:
            self.ac_on = False

        return self.ac_on
