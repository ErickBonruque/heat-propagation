# c:\Users\bonru\OneDrive\Área de Trabalho\IC-EVANDRO\heat_transfer_simulation.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

class HeatTransferSimulation:
    def __init__(self, 
                 # Dimensões do quadrado (metros)
                 square_width=0.1, 
                 square_height=0.1, 
                 # Propriedades térmicas (Alumínio)
                 thermal_conductivity=237,  # W/(m·K)
                 density=2700,              # kg/m³
                 specific_heat=900,         # J/(kg·K)
                 # Parâmetros da simulação
                 simulation_time=600,       # segundos
                 time_step=0.1,             # segundos
                 # Temperaturas iniciais
                 source_temp=100,           # °C
                 initial_temp=25):          # °C
        
        # Armazenar parâmetros
        self.square_width = square_width
        self.square_height = square_height
        self.area = square_width * square_height
        self.thermal_conductivity = thermal_conductivity
        self.density = density
        self.specific_heat = specific_heat
        self.simulation_time = simulation_time
        self.time_step = time_step
        self.source_temp = source_temp
        self.initial_temp = initial_temp
        
        # Calcular difusividade térmica (alpha = k/(rho*c))
        self.thermal_diffusivity = thermal_conductivity / (density * specific_heat)
        
        # Inicializar temperaturas
        self.temps = [
            np.full((int(simulation_time/time_step) + 1,), source_temp),  # Fonte (sempre a 100°C)
            np.full((int(simulation_time/time_step) + 1,), initial_temp), # Quadrado 2
            np.full((int(simulation_time/time_step) + 1,), initial_temp)  # Quadrado 3
        ]
        
        # Pontos no tempo
        self.time_points = np.arange(0, simulation_time + time_step, time_step)
        
        # Área de contato entre os quadrados (assumindo que tocam ao longo de um lado)
        self.contact_area = square_height  # Largura do contato é a altura do quadrado
        
        # Distância entre centros (para cálculo do fluxo de calor)
        self.distance = square_width
    
    def run_simulation(self):
        """Executar a simulação de transferência de calor"""
        start_time = time.time()
        
        # Coeficiente de transferência de calor (k/distância)
        heat_transfer_coeff = self.thermal_conductivity / self.distance
        
        # Capacidade de armazenar calor (m*c)
        heat_capacity = self.density * self.area * self.square_width * self.specific_heat
        
        # Executar simulação para todos os passos de tempo
        for t in range(1, len(self.time_points)):
            # Quadrado 1 (fonte de calor) permanece a temperatura constante
            # Calcular fluxo de calor do quadrado 1 para o quadrado 2
            q1_to_2 = heat_transfer_coeff * self.contact_area * (
                self.temps[0][t-1] - self.temps[1][t-1]) * self.time_step
            
            # Calcular fluxo de calor do quadrado 2 para o quadrado 3
            q2_to_3 = heat_transfer_coeff * self.contact_area * (
                self.temps[1][t-1] - self.temps[2][t-1]) * self.time_step
            
            # Atualizar temperaturas (energia recebida / capacidade térmica = mudança de temperatura)
            self.temps[1][t] = self.temps[1][t-1] + (q1_to_2 - q2_to_3) / heat_capacity
            self.temps[2][t] = self.temps[2][t-1] + q2_to_3 / heat_capacity
        
        end_time = time.time()
        print(f"Simulação concluída em {end_time - start_time:.3f} segundos")
    
    def plot_temperatures(self):
        """Plotar a evolução da temperatura ao longo do tempo para todos os quadrados"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.time_points, self.temps[0], 'r-', label='Quadrado 1 (Fonte)')
        plt.plot(self.time_points, self.temps[1], 'g-', label='Quadrado 2')
        plt.plot(self.time_points, self.temps[2], 'b-', label='Quadrado 3')
        
        plt.xlabel('Tempo (s)')
        plt.ylabel('Temperatura (°C)')
        plt.title('Transferência de Calor Entre Três Quadrados')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        
        # Salvar e mostrar a figura
        plt.savefig('evolucao_temperatura.png', dpi=300)
        plt.show()
    
    def create_animation(self, interval=100):
        """Criar uma animação mostrando a distribuição de calor ao longo do tempo"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Criar um array para representar nossos três quadrados
        squares = np.zeros((3, 1))
        
        # Criar uma grade para visualização
        x = np.array([0, 1, 2])
        y = np.zeros(3)
        
        # Configurar o mapa de cores
        min_temp = self.initial_temp
        max_temp = self.source_temp
        
        # Definir cores iniciais
        cmap = plt.cm.plasma
        colors = [cmap((temp - min_temp) / (max_temp - min_temp)) for temp in [self.source_temp, self.initial_temp, self.initial_temp]]
        
        # Criar os quadrados
        rects = [plt.Rectangle((i-0.4, -0.4), 0.8, 0.8, color=colors[i]) for i in range(3)]
        for rect in rects:
            ax.add_patch(rect)
            
        # Adicionar rótulos de texto para as temperaturas
        texts = [ax.text(i, 0, f"{self.temps[i][0]:.1f}°C", 
                         ha='center', va='center', color='white', fontweight='bold') 
                 for i in range(3)]
        
        # Definir limites e rótulos do gráfico
        ax.set_xlim(-0.5, 2.5)
        ax.set_ylim(-0.5, 0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(['Fonte', 'Quadrado 2', 'Quadrado 3'])
        ax.set_yticks([])
        ax.set_title('Simulação de Transferência de Calor')
        
        time_text = ax.text(1.25, 0.4, '', transform=ax.transAxes)
        
        # Definir função de atualização para a animação
        def update(frame):
            # Pular quadros para acelerar a animação
            actual_frame = min(frame * 10, len(self.time_points) - 1)
            
            # Atualizar cores com base nas temperaturas atuais
            for i, rect in enumerate(rects):
                temp = self.temps[i][actual_frame]
                color_val = (temp - min_temp) / (max_temp - min_temp)
                rect.set_color(cmap(color_val))
                texts[i].set_text(f"{temp:.1f}°C")
                
            time_text.set_text(f"Tempo: {self.time_points[actual_frame]:.1f}s")
            return rects + texts + [time_text]
            
        # Criar animação
        frames = min(100, len(self.time_points))  # Limitar número de quadros para animação mais suave
        ani = FuncAnimation(fig, update, frames=frames, interval=interval, blit=True)
        
        # Salvar animação como GIF
        ani.save('animacao_transferencia_calor.gif', writer='pillow', fps=10)
        
        plt.tight_layout()
        plt.show()
        
        return ani

if __name__ == "__main__":
    # Criar e executar a simulação
    sim = HeatTransferSimulation(
        square_width=0.05,      # Quadrados de 5 cm
        square_height=0.05,
        simulation_time=300,    # 5 minutos
        time_step=0.5           # Passos de 0.5 segundos
    )
    
    # Executar simulação
    sim.run_simulation()
    
    # Plotar resultados
    sim.plot_temperatures()
    
    # Criar animação
    sim.create_animation()