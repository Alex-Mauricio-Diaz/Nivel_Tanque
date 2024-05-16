import numpy as np  # Importa la biblioteca numpy para cálculos numéricos
import matplotlib.pyplot as plt  # Importa matplotlib.pyplot para trazar gráficos

# Definición de la clase Tank para representar un tanque con diferentes tipos de válvulas
class Tank:
    def __init__(self, A, k1, k2, valve_type, valve_opening_in, valve_opening_out, alpha=None):
        # Inicialización de los atributos del tanque
        self.A = A  # Área transversal del tanque
        self.k1 = k1  # Constante de la válvula de entrada
        self.k2 = k2  # Constante de la válvula de salida
        self.valve_type = valve_type  # Tipo de válvula
        self.valve_opening_in = valve_opening_in  # Apertura de la válvula de entrada
        self.valve_opening_out = valve_opening_out  # Apertura de la válvula de salida
        self.alpha = alpha  # Parámetro adicional para la válvula isopercentual
        self.historical_heights = []  # Lista para almacenar las alturas históricas del tanque

    # Método para calcular el área de flujo de entrada dependiendo del tipo de válvula
    def a1(self):
        if self.valve_type == "lineal":
            return self.valve_opening_in
        elif self.valve_type == "isopercentual":
            return self.alpha / ((self.valve_opening_in + self.alpha)*3)
        elif self.valve_type == "apertura_rapida":
            return np.sqrt(self.valve_opening_in)

    # Método para calcular el área de flujo de salida
    def a2(self):
        return self.valve_opening_out

    # Método para calcular la tasa de cambio de la altura del tanque
    def dh_dt(self, h):
        return (self.k1 * self.a1() - self.k2 * self.a2() * h) / self.A

    # Método para realizar un paso en el método de Euler
    def euler_step(self, h, dt):
        return h + dt * self.dh_dt(h)

    # Método para resolver el sistema de ecuaciones diferenciales durante un tiempo total especificado
    def solve(self, initial_height, total_time, dt):
        num_steps = int(total_time / dt)  # Número de pasos de tiempo
        height = initial_height  # Altura inicial del tanque
        for _ in range(num_steps):
            self.historical_heights.append(height)  # Almacena la altura actual
            height = self.euler_step(height, dt)  # Calcula la nueva altura
        self.historical_heights.append(height)  # Almacena la última altura

    # Método para trazar la altura del tanque en función del tiempo
    def plot(self):
        plt.plot(np.arange(0, len(self.historical_heights)), self.historical_heights, label=self.valve_type)

# Función para obtener la entrada del usuario
def get_user_input():
    A = float(input("Ingrese el área transversal del tanque (A): "))  # Solicita el área transversal
    k1 = float(input("Ingrese la constante de la válvula de entrada (k1): "))  # Solicita la constante k1
    k2 = float(input("Ingrese la constante de la válvula de salida (k2): "))  # Solicita la constante k2
    valve_opening_in = float(input("Ingrese la apertura de la válvula de entrada (0-1): "))  # Solicita la apertura de la válvula de entrada
    valve_opening_out = float(input("Ingrese la apertura de la válvula de salida (0-1): "))  # Solicita la apertura de la válvula de salida
    initial_height = float(input("Ingrese la altura inicial del tanque: "))  # Solicita la altura inicial
    total_time = float(input("Ingrese el tiempo total de simulación: "))  # Solicita el tiempo total de simulación
    dt = float(input("Ingrese el intervalo de tiempo (dt): "))  # Solicita el intervalo de tiempo
    alpha = float(input("Ingrese el valor de alpha para la válvula isopercentual: "))  # Solicita el valor de alpha
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

# Función principal del programa
def main():
    # Obtener la entrada del usuario
    A, k1, k2, valve_opening_in, valve_opening_out, initial_height, total_time, dt, alpha = get_user_input()
    # Tipos de válvulas a probar
    valve_types = ["lineal", "isopercentual", "apertura_rapida"]

    # Iterar sobre los diferentes tipos de válvulas
    for valve_type in valve_types:
        # Crear un objeto Tank para cada tipo de válvula
        tank = Tank(A, k1, k2, valve_type, valve_opening_in, valve_opening_out)
        if valve_type == "isopercentual":
            tank.alpha = alpha  # Asigna alpha solo si es válvula isopercentual
        # Resolver el sistema y trazar la altura del tanque en función del tiempo
        tank.solve(initial_height, total_time, dt)
        tank.plot()

    # Personalizar la apariencia del gráfico
    plt.xlabel("Tiempo")  # Etiqueta del eje x
    plt.ylabel("Altura del tanque")  # Etiqueta del eje y
    plt.legend()  # Mostrar leyendas
    plt.title("Comparacion de respuestas del sistema de tanque con diferentes tipos de válvulas")  # Título del gráfico
    plt.grid(True)  # Agregar cuadrícula al gráfico
    plt.show()  # Mostrar el gráfico

# Ejecutar la función main si este archivo es ejecutado directamente
if __name__ == "__main__":
    main()
