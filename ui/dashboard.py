import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from simulator.physics import TemperaturePhysics
from simulator.controller import ACController
from simulator.predictor import predict_cooling_time
import numpy as np

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SmartRoomApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart Room Temperature Simulator")
        self.geometry("1200x800")

        self.physics = TemperaturePhysics()
        self.controller = ACController()

        self.set_temp = 30
        self.time_data = []
        self.temp_data = []
        self.time_counter = 0

        self.build_ui()
        self.update_system()

    def build_ui(self):

        self.temp_label = ctk.CTkLabel(self, text="Temperature: -- °C", font=("Arial", 26))
        self.temp_label.pack(pady=20)

        self.ac_label = ctk.CTkLabel(self, text="AC: OFF", font=("Arial", 20))
        self.ac_label.pack()

        self.prediction_label = ctk.CTkLabel(self, text="Estimated Cooling Time: -- min", font=("Arial", 16))
        self.prediction_label.pack(pady=5)

        self.slider_label = ctk.CTkLabel(self, text="Set Temperature: 30 °C", font=("Arial", 16))
        self.slider_label.pack()

        self.slider = ctk.CTkSlider(self, from_=16, to=40, command=self.slider_changed)
        self.slider.set(30)
        self.slider.pack(pady=10)

        # Graph
        self.fig, self.ax = plt.subplots(figsize=(6,4))
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_title("Temperature vs Time")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Temperature")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=20)

    def slider_changed(self, value):
        self.set_temp = round(value, 1)
        self.slider_label.configure(text=f"Set Temperature: {self.set_temp} °C")

    def update_system(self):
        current_temp = self.physics.update(self.controller.ac_on, self.set_temp)
        ac_state = self.controller.update(current_temp, self.set_temp)

        self.temp_label.configure(text=f"Temperature: {round(current_temp,2)} °C")

        if ac_state:
            self.ac_label.configure(text="AC: ON", text_color="cyan")
        else:
            self.ac_label.configure(text="AC: OFF", text_color="white")

        predicted = predict_cooling_time(current_temp, self.set_temp, self.physics.thermal_mass)
        self.prediction_label.configure(text=f"Estimated Cooling Time: {round(predicted,1)} sec")

        # Update graph
        self.time_counter += 1
        self.time_data.append(self.time_counter)
        self.temp_data.append(current_temp)

        self.line.set_data(self.time_data, self.temp_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()

        self.after(1000, self.update_system)
