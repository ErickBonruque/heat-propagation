# c:\Users\bonru\OneDrive\Área de Trabalho\IC-EVANDRO\heat_transfer_gui.py

import tkinter as tk
from tkinter import ttk, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading
import sys
import io
from heat_transfer_simulation import HeatTransferSimulation

class HeatTransferGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulação de Transferência de Calor")
        self.root.geometry("1200x800")
        
        # Criar frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Criar frame esquerdo para parâmetros
        left_frame = ttk.LabelFrame(main_frame, text="Parâmetros da Simulação", padding="10")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Criar frame direito para plotagem
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Criar frame inferior para logs
        bottom_frame = ttk.LabelFrame(main_frame, text="Log da Simulação", padding="10")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5, before=right_frame)
        
        # Criar frame para plots
        plots_frame = ttk.LabelFrame(right_frame, text="Resultados da Simulação", padding="10")
        plots_frame.pack(fill=tk.BOTH, expand=True)
        
        # Criar a figura para plotagem
        self.figure, self.ax = plt.subplots(figsize=(7, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=plots_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Adicionar widgets de parâmetros
        self.create_parameters_widgets(left_frame)
        
        # Adicionar widget de log
        self.log_text = scrolledtext.ScrolledText(bottom_frame, height=8)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Redirecionar stdout para o widget de log
        self.redirect_stdout()
        
        # Inicializar simulação
        self.simulation = None
    
    def create_parameters_widgets(self, parent):
        # Parâmetros Físicos
        phys_frame = ttk.LabelFrame(parent, text="Propriedades Físicas")
        phys_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Propriedades do material (usando alumínio como padrão)
        ttk.Label(phys_frame, text="Condutividade Térmica (W/m·K):").grid(row=0, column=0, sticky=tk.W)
        self.thermal_conductivity = tk.DoubleVar(value=237.0)
        ttk.Entry(phys_frame, textvariable=self.thermal_conductivity, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(phys_frame, text="Densidade (kg/m³):").grid(row=1, column=0, sticky=tk.W)
        self.density = tk.DoubleVar(value=2700.0)
        ttk.Entry(phys_frame, textvariable=self.density, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        ttk.Label(phys_frame, text="Calor Específico (J/kg·K):").grid(row=2, column=0, sticky=tk.W)
        self.specific_heat = tk.DoubleVar(value=900.0)
        ttk.Entry(phys_frame, textvariable=self.specific_heat, width=10).grid(row=2, column=1, padx=5, pady=2)
        
        # Menu suspenso de materiais predefinidos
        ttk.Label(phys_frame, text="Material Predefinido:").grid(row=3, column=0, sticky=tk.W)
        self.material_var = tk.StringVar(value="Alumínio")
        materials = ["Alumínio", "Cobre", "Ferro", "Aço", "Vidro", "Concreto"]
        material_menu = ttk.Combobox(phys_frame, textvariable=self.material_var, values=materials, width=10)
        material_menu.grid(row=3, column=1, padx=5, pady=2)
        material_menu.bind("<<ComboboxSelected>>", self.on_material_selected)
        
        # Parâmetros de Geometria
        geom_frame = ttk.LabelFrame(parent, text="Geometria")
        geom_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(geom_frame, text="Largura do Quadrado (m):").grid(row=0, column=0, sticky=tk.W)
        self.square_width = tk.DoubleVar(value=0.05)
        ttk.Entry(geom_frame, textvariable=self.square_width, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(geom_frame, text="Altura do Quadrado (m):").grid(row=1, column=0, sticky=tk.W)
        self.square_height = tk.DoubleVar(value=0.05)
        ttk.Entry(geom_frame, textvariable=self.square_height, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        # Parâmetros de Temperatura
        temp_frame = ttk.LabelFrame(parent, text="Temperaturas")
        temp_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(temp_frame, text="Temperatura da Fonte (°C):").grid(row=0, column=0, sticky=tk.W)
        self.source_temp = tk.DoubleVar(value=100.0)
        ttk.Entry(temp_frame, textvariable=self.source_temp, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(temp_frame, text="Temperatura Inicial (°C):").grid(row=1, column=0, sticky=tk.W)
        self.initial_temp = tk.DoubleVar(value=25.0)
        ttk.Entry(temp_frame, textvariable=self.initial_temp, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        # Parâmetros da Simulação
        sim_frame = ttk.LabelFrame(parent, text="Configurações da Simulação")
        sim_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(sim_frame, text="Tempo de Simulação (s):").grid(row=0, column=0, sticky=tk.W)
        self.simulation_time = tk.DoubleVar(value=300.0)
        ttk.Entry(sim_frame, textvariable=self.simulation_time, width=10).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(sim_frame, text="Passo de Tempo (s):").grid(row=1, column=0, sticky=tk.W)
        self.time_step = tk.DoubleVar(value=0.5)
        ttk.Entry(sim_frame, textvariable=self.time_step, width=10).grid(row=1, column=1, padx=5, pady=2)
        
        # Botões
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill=tk.X, padx=5, pady=10)
        
        ttk.Button(btn_frame, text="Executar Simulação", command=self.run_simulation).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Plotar Resultados", command=self.plot_results).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Criar Animação", command=self.create_animation).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Redefinir", command=self.reset).pack(fill=tk.X, pady=2)
    
    def on_material_selected(self, event):
        # Dicionário de propriedades térmicas dos materiais
        materials = {
            "Alumínio": (237, 2700, 900),
            "Cobre": (400, 8960, 386),
            "Ferro": (80, 7870, 447),
            "Aço": (50, 7850, 490),
            "Vidro": (1.05, 2500, 840),
            "Concreto": (1.7, 2300, 880)
        }
        
        selected = self.material_var.get()
        if selected in materials:
            k, rho, c = materials[selected]
            self.thermal_conductivity.set(k)
            self.density.set(rho)
            self.specific_heat.set(c)
            print(f"Material alterado para {selected}: k={k} W/m·K, ρ={rho} kg/m³, c={c} J/kg·K")
    
    def redirect_stdout(self):
        class StdoutRedirector:
            def __init__(self, text_widget):
                self.text_widget = text_widget
                
            def write(self, string):
                self.text_widget.insert(tk.END, string)
                self.text_widget.see(tk.END)
                
            def flush(self):
                pass
                
        sys.stdout = StdoutRedirector(self.log_text)
    
    def run_simulation(self):
        # Limpar o log
        self.log_text.delete(1.0, tk.END)
        
        print("Iniciando simulação...")
        
        # Criar instância da simulação
        self.simulation = HeatTransferSimulation(
            square_width=self.square_width.get(),
            square_height=self.square_height.get(),
            thermal_conductivity=self.thermal_conductivity.get(),
            density=self.density.get(),
            specific_heat=self.specific_heat.get(),
            simulation_time=self.simulation_time.get(),
            time_step=self.time_step.get(),
            source_temp=self.source_temp.get(),
            initial_temp=self.initial_temp.get()
        )
        
        # Executar simulação em uma thread separada para manter a GUI responsiva
        threading.Thread(target=self._run_sim_thread, daemon=True).start()
    
    def _run_sim_thread(self):
        if self.simulation:
            self.simulation.run_simulation()
            print("Simulação concluída com sucesso.")
            # Plotar resultados na thread principal
            self.root.after(0, self.plot_results)
    
    def plot_results(self):
        if self.simulation:
            try:
                # Desabilitar botões durante o plot
                self.disable_buttons()
                
                # Limpar a figura atual
                self.ax.clear()
                
                # Plotar temperaturas
                self.ax.plot(self.simulation.time_points, self.simulation.temps[0], 'r-', label='Quadrado 1 (Fonte)')
                self.ax.plot(self.simulation.time_points, self.simulation.temps[1], 'g-', label='Quadrado 2')
                self.ax.plot(self.simulation.time_points, self.simulation.temps[2], 'b-', label='Quadrado 3')
                
                self.ax.set_xlabel('Tempo (s)')
                self.ax.set_ylabel('Temperatura (°C)')
                self.ax.set_title('Transferência de Calor Entre Três Quadrados')
                self.ax.grid(True)
                self.ax.legend()
                
                # Atualizar o canvas
                self.canvas.draw()
                print("Plot atualizado")
            except Exception as e:
                print(f"Erro ao plotar resultados: {str(e)}")
            finally:
                # Reabilitar botões após concluir
                self.enable_buttons()
        else:
            print("Execute a simulação primeiro")

    def create_animation(self):
        if self.simulation:
            print("Criando animação...")
            try:
                # Desabilitar botões durante a animação
                self.disable_buttons()
                # Executar animação na thread principal
                self.simulation.create_animation()
                print("Animação salva como 'animacao_transferencia_calor.gif'")
            except Exception as e:
                print(f"Erro ao criar animação: {str(e)}")
            finally:
                # Reabilitar botões após concluir
                self.enable_buttons()
        else:
            print("Execute a simulação primeiro")

    def disable_buttons(self):
        # Desabilitar todos os botões durante processamento
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Button):
                        widget.configure(state='disabled')
        self.root.update()

    def enable_buttons(self):
        # Reabilitar todos os botões após processamento
        for child in self.root.winfo_children():
            if isinstance(child, ttk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Button):
                        widget.configure(state='normal')
        self.root.update()
    
    def reset(self):
        # Redefinir a simulação
        self.simulation = None
        
        # Limpar o plot
        self.ax.clear()
        self.canvas.draw()
        
        # Limpar o log
        self.log_text.delete(1.0, tk.END)
        
        print("Redefinição concluída")

if __name__ == "__main__":
    root = tk.Tk()
    app = HeatTransferGUI(root)
    root.mainloop()