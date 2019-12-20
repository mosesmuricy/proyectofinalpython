# -*- coding: utf-8 -*-
class GrowthCalculator(object):
    def __init__(self):
        """
        Establece valores predeterminados para las siguientes variables:
        """
        # Coeficientes de la ecuación de Lotka-Volterra
        self.a = 1.0              #Tasa de crecimiento de las presas cuando no hay depredadores
        self.b = 0.1              #Tasa de mortalidad de las presas debido a la depredación
        self.c = 1.0              #Tasa de mortalidad de los depredadores cuando no hay presas
        self.d = 0.075            #Tasa de reproducción de los depredadores por cada presa que come

        # Otros parámetros
        self.dt = 0.02            #Delta Tiempo
        self.iterations = 1000    #Número de iteraciones a ejecutar
        self.predators = 5        #Población inicial de depredadores
        self.prey = 10            #Población inicial de presas

    def dx(self, x, y):
        """
        Cálculo del cambio en el tamaño de la población de presas usando la ecuación 
        Lotka-Volterra para la presa y el delta de tiempo definido en "self.dt"
        """
        # Cálculo de  la tasa de cambio poblacional
        dx_dt = x * (self.a - self.b * y)

        # Cálculo del cambio poblacional de presas
        return dx_dt * self.dt

    def dy(self, x, y):
        """
        Cálculo del cambio en el tamaño de la población de depredadores usando la ecuación 
        Lotka-Volterra para los depredadores y el delta de tiempo definido en "self.dt"
        """
        # Cálculo de  la tasa de cambio poblacional
        dy_dt = y * (self.d * x - self.c)

        # Cálculo del cambio poblacional de depredadores
        return dy_dt * self.dt

    def calculate(self):
        """
        Cálculo del crecimiento de la población depredador / presa para los parámetros dados
        
       {'predador': [historial de la población de depredadores como una lista],
        'presa': [historial de la población de presas como una lista]}
        """
        predator_history = []
        prey_history = []

        for i in range(self.iterations):
            xk_1 = self.dx(self.prey, self.predators)
            yk_1 = self.dy(self.prey, self.predators)
            xk_2 = self.dx(self.prey + xk_1, self.predators + yk_1)
            yk_2 = self.dy(self.prey + xk_1, self.predators + yk_1)

            self.prey = self.prey + (xk_1 + xk_2) / 2
            self.predators = self.predators + (yk_1 + yk_2) / 2

            predator_history.append(self.predators)
            prey_history.append(self.prey)

        return {'predator': predator_history, 'prey': prey_history}
