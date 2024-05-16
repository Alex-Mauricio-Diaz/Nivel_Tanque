import numpy as np
import matplotlib.pyplot as plt

class Tank:
    def __init__(self, A, k1, k2, valve_type, valve_opening_in, valve_opening_out, alpha=None):
        self.A = A
        self.k1 = k1
        self.k2 = k2
        self.valve_type = valve_type
        self.valve_opening_in = valve_opening_in
        self.valve_opening_out = valve_opening_out
        self.alpha = alpha
        self.historical_heights = []

    def a1(self):
        if self.valve_type == "lineal":
            return self.valve_opening_in
        elif self.valve_type == "isopercentual":
            return self.alpha / ((self.valve_opening_in + self.alpha)*3)
        elif self.valve_type == "apertura_rapida":
            return np.sqrt(self.valve_opening_in)


    def a2(self):
        return self.valve_opening_out

    def dh_dt(self, h):
        return (self.k1 * self.a1() - self.k2 * self.a2() * h) / self.A

    def euler_step(self, h, dt):
        return h + dt * self.dh_dt(h)

    def solve(self, initial_height, total_time, dt):
        num_steps = int(total_time / dt)
        height = initial_height
        for _ in range(num_steps):
            self.historical_heights.append(height)
            height = self.euler_step(height, dt)
        self.historical_heights.append(height)

    def plot(self):
        plt.plot(np.arange(0, len(self.historical_heights)), self.historical_heights, label=self.valve_type)

def get_user_input():
    A = float(input("Ingrese el área transversal del tanque (A): "))
    k1 = float(input("Ingrese la constante de la válvula de entrada (k1): "))
    k2 = float(input("Ingrese la constante de la válvula de salida (k2): "))
    valve_opening_in = float(input("Ingrese la apertura de la válvula de entrada (0-1): "))
    valve_opening_out = float(input("Ingrese la apertura de la válvula de salida (0-1): "))
    initial_height = float(input("Ingrese la altura inicial del tanque: "))
    total_time = float(input("Ingrese el tiempo total de simulación: "))
    dt = float(input("Ingrese el intervalo de tiempo (dt): "))
    alpha = float(input("Ingrese el valor de alpha para la válvula isopercentual: "))
    # A = 2  # Area transversal del tanque
    # k1 = 0.1  # Constante de la válvula de entrada
    # k2 = 0.05  # Constante de la válvula de salida
    # valve_opening_in = 0.5  # Apertura de la válvula de entrada (0-1)
    # valve_opening_out = 0.4  # Apertura de la válvula de salida (0-1)
    # initial_height = 0  # Altura inicial del tanque
    # total_time = 800  # Tiempo total de simulación
    # dt = 1  # Intervalo de tiempo (dt)
    # alpha = 10  # Valor de alpha para la válvula isopercentual
    return A, k1, k2, valve_opening_in, valve_opening_out, initial_height, total_time, dt, alpha

def main():
    A, k1, k2, valve_opening_in, valve_opening_out, initial_height, total_time, dt, alpha = get_user_input()
    valve_types = ["lineal", "isopercentual", "apertura_rapida"]

    for valve_type in valve_types:
        tank = Tank(A, k1, k2, valve_type, valve_opening_in, valve_opening_out)
        if valve_type == "isopercentual":
            tank.alpha = alpha
        tank.solve(initial_height, total_time, dt)
        tank.plot()

    plt.xlabel("Tiempo")
    plt.ylabel("Altura del tanque")
    plt.legend()
    plt.title("Comparacion de respuestas del sistema de tanque con diferetnes tipos de valvulas")
    plt.grid(True)  # Agregar cuadrícula
    plt.show()

if __name__ == "__main__":
    main()