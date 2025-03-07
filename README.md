# Simulação de Transferência de Calor

Este projeto simula a transferência de calor entre três quadrados adjacentes usando a equação de condução de calor de Fourier. O primeiro quadrado atua como uma fonte de calor constante, enquanto o calor se propaga para os outros dois quadrados ao longo do tempo.

## Modelo Físico

- **Primeiro Quadrado**: Fonte de calor constante a 100°C (configurável)
- **Segundo Quadrado**: Inicialmente a 25°C, em contato direto com a fonte de calor
- **Terceiro Quadrado**: Inicialmente a 25°C, em contato direto com o segundo quadrado

A simulação usa a lei de condução de calor de Fourier:

q = -k ∇T

Onde:
- q é o fluxo de calor (W/m²)
- k é a condutividade térmica (W/m·K)
- ∇T é o gradiente de temperatura (K/m)

## Funcionalidades

- Propriedades do material configuráveis (condutividade térmica, densidade, calor específico)
- Dimensões dos quadrados ajustáveis
- Tempo de simulação e passo de tempo variáveis
- Visualização da temperatura ao longo do tempo
- Visualização animada da propagação do calor
- Interface gráfica para fácil ajuste de parâmetros

## Como Usar

### Pré-requisitos

- Python 3.6 ou superior
- Bibliotecas necessárias: NumPy, Matplotlib, Tkinter

Instale os pacotes necessários:
```bash
pip install numpy matplotlib
```

## Executando a Simulação

Execute a interface gráfica:

```bash
python heat_transfer_gui.py
```

Ajuste os parâmetros conforme necessário:

- Propriedades físicas (condutividade térmica, densidade, calor específico)
- Dimensões dos quadrados
- Configurações de temperatura
- Tempo de simulação e passo de tempo

Clique em "Run Simulation" para executar

Use "Plot Results" para visualizar a temperatura ao longo do tempo

Clique em "Create Animation" para gerar uma visualização animada

### Usando a Versão de Linha de Comando

Alternativamente, você pode executar a simulação diretamente:

```bash
python heat_transfer_simulation.py
```

### Parâmetros

#### Propriedades do Material

- Condutividade Térmica: Taxa na qual o calor passa através de um material (W/m·K)
- Densidade: Massa por unidade de volume (kg/m³)
- Calor Específico: Energia necessária para aumentar 1kg em 1°C (J/kg·K)

#### Materiais Predefinidos

- Alumínio (padrão): k=237 W/m·K, ρ=2700 kg/m³, c=900 J/kg·K
- Cobre: k=400 W/m·K, ρ=8960 kg/m³, c=386 J/kg·K
- Ferro: k=80 W/m·K, ρ=7870 kg/m³, c=447 J/kg·K
- Aço: k=50 W/m·K, ρ=7850 kg/m³, c=490 J/kg·K
- Vidro: k=1.05 W/m·K, ρ=2500 kg/m³, c=840 J/kg·K
- Concreto: k=1.7 W/m·K, ρ=2300 kg/m³, c=880 J/kg·K

### Saídas

- Gráfico Temperatura vs Tempo: Mostra a evolução da temperatura para os três quadrados
- Animação: Representação visual da transferência de calor ao longo do tempo
- Log da Simulação: Detalhes sobre o progresso e resultados da simulação

### Entendendo os Resultados

A simulação demonstra vários princípios importantes de transferência de calor:

- Gradiente de Temperatura: O calor flui de regiões de alta para baixa temperatura
- Propriedades do Material: Diferentes materiais conduzem calor a taxas diferentes
- Equilíbrio Térmico: Dado tempo suficiente, corpos conectados atingem a mesma temperatura
- Taxa de Fluxo de Calor: A transferência de calor inicial é rápida, depois desacelera à medida que as temperaturas se aproximam do equilíbrio