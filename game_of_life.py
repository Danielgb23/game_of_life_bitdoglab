# Projeto 1 de EA801
# Jogo da vida do John Conway na placa bitdoglab
# Turma U
# 27/03/2025
#
# Daniel Goncalves Benvenutti 169448
# Leonardo Gurgel Carlos Pires Filho  239773

from machine import Pin, ADC, SoftI2C, PWM, Timer
import neopixel
import utime
from ssd1306 import SSD1306_I2C


# Configuração do OLED
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)


# Define a grid da tela OLED onde vai ser rodado o jogo da vida
# Definição do tamanho do tabuleiro
#
WIDTH = 128
HEIGHT = 64

CELL_SIZE = 4
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# desenha a grid do jogo no display OLED
def draw_oled():
    oled.fill(0)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y][x]:
                oled.fill_rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE, 1)
    oled.show()


# contabiliza os vizinhos para aplicar as regras do jogo na grid
def count_neighbors(x, y):
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for dx, dy in neighbors:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
            count += grid[ny][nx]
    return count


# atualiza a grid do jogo de acordo com as regras
def game_of_life_step():
    global grid
    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            neighbors = count_neighbors(x, y)
            if grid[y][x]:
                if neighbors in (2, 3):
                    new_grid[y][x] = 1
            else:
                if neighbors == 3:
                    new_grid[y][x] = 1
    grid = new_grid


######################################

# Configuração do joystick
VRx = ADC(Pin(27))  # Eixo X
VRy = ADC(Pin(26))  # Eixo Y

# Configuração dos botoes
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

# Variável que define o estado de preencher o canvas da matriz de LEDs
set_game = True


# Variáveis de debouncing
deb_a = 0
deb_b = 0

### matriz de leds##################

# Configuração da matriz de LEDs
NUM_LEDS = 25
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)

# Definição da matriz 5x5 (índices dos LEDs)
LED_MATRIX = [
    [24, 23, 22, 21, 20],
    [15, 16, 17, 18, 19],
    [14, 13, 12, 11, 10],
    [5, 6, 7, 8, 9],
    [4, 3, 2, 1, 0],
]


# Posição inicial do cursor
x, y = 2, 2  # Começa no centro da matriz

# Cores da matriz de LEDs
cursor_dead = (255, 0, 0)  # Cor inicial do cursor (vermelho)
cursor_alive = (0, 0, 255)  # Azul
alive = (0, 255, 0)  # Verde
dead = (0, 0, 0)  # Apagado


# Função para atualizar a matriz
def update_matrix():
    global set_game
    np.fill((0, 0, 0))  # Apaga todos os LEDs
    # Acende todas as células vivas
    for i in range(5):
        for j in range(5):
            np[LED_MATRIX[j][i]] = alive if cell_matrix[j][i] else dead
    # Acende o LED do cursor com a cor correta
    if set_game:  # mostra o cursor apenas durante o set_game
        np[LED_MATRIX[y][x]] = cursor_alive if cell_matrix[y][x] else cursor_dead

    np.write()


#### clapper#########################3

# Configuração do microfone (ADC no GPIO28)
microphone = ADC(Pin(28))  # O microfone está conectado ao GPIO28


# Função do clapper (detecção de som)
def detect_clap():
    global sound_level
    global cell_matrix

    # Defina um limiar para detectar um som de clap (ajuste conforme necessário)
    clap_threshold = 33800  # Exemplo de limiar (ajuste conforme o seu microfone)

    if sound_level > clap_threshold:

        # Limpa matriz
        cell_matrix = [[False for _ in range(5)] for _ in range(5)]


# musica do jogo #########

# Configuração do buzzer
buzzer = PWM(Pin(21))  # Buzzer conectado ao GPIO8
buzzer.freq(440)
buzzer.duty_u16(0)

# Notas musicais (frequências em Hz)
NOTES = {
    "C4": 261,
    "D4": 294,
    "E4": 330,
    "F4": 349,
    "G4": 392,
    "A4": 440,
    "B4": 494,
    "C5": 523,
    "D5": 587,
    "E5": 659,
    "F5": 698,
    "G5": 784,
    "A5": 880,
    "B5": 988
}

# Melodia do jogo zelda
melody = [
    ("F4", 300),("A4", 300),("B4", 600),
    ("F4", 300),("A4", 300),("B4", 600),
    ("F4", 300),("A4", 300),("B4", 300),("E5", 300),("D5", 600),
    ("B4", 300),("C5", 300),("B4", 300),("G4", 300),("E4", 1400),
    (None, 300),
    ("D4", 300),("E4", 300),("G4", 300),("E4", 1400),
    (None, 300),
    
    ("F4", 300),("A4", 300),("B4", 600),
    ("F4", 300),("A4", 300),("B4", 600),
    ("F4", 300),("A4", 300),("B4", 300),("E5", 300),("D5", 600),
    ("B4", 300),("C5", 300),("E5", 300),("B4", 300),("G4", 1400),
    (None, 300),
    ("B4", 300),("G4", 300),("D4", 300),("E4", 1400),
    (None, 300),
    
    ("D4", 300), ("E4", 300), ("F4", 600),
    ("G4", 300), ("A4", 300), ("B4", 600),
    ("C5", 300), ("B4", 300), ("E4", 1200),
    (None, 300),
    ("F4", 300), ("G4", 300), ("A4", 600),
    ("B4", 300), ("C5", 300), ("D5", 600),
    ("E5", 300), ("F5", 300), ("G5", 1200),
    (None, 300),
    ("D4", 300), ("E4", 300), ("F4", 600),
    ("G4", 300), ("A4", 300), ("B4", 600),
    ("C5", 300), ("B4", 300), ("E4", 1200),
    (None, 300),
    ("F4", 300), ("E4", 300),
    ("A4", 300), ("G4", 300),
    ("B4", 300), ("A4", 300),
    ("C5", 300), ("B4", 300),
    ("D5", 300), ("C5", 300),
    ("E5", 300), ("D5", 300),
    ("F5", 300), ("E5", 600),
    (None, 100),
    ("E5", 300), ("F5", 200), ("D5", 300), ("E5", 1400),
    (None, 300),
]

melody_index = 0


def play_next_note(timer):
    global set_game
    global melody_index
    if not set_game:
        note, duration = melody[melody_index]
        if note is None:
            buzzer.duty_u16(0)  # Silencio
        else:
            buzzer.freq(NOTES[note]) # Frequencia da nota
            buzzer.duty_u16(512)  # Define volume
            
        # incrementa a nota da melodia
        melody_index += 1
        melody_index %= len(melody)
        
        melody_timer.init(period=duration, mode=Timer.ONE_SHOT, callback=play_next_note)
    else:
        buzzer.duty_u16(0)  # Desliga


# Configuração do timer para tocar a melodia
melody_timer = Timer()


############################
debounce_timer = Timer()

# Funções de interrupção dos botões
def button_a_pressed(pin):
    global set_game
    global deb_a
    # Laço para debouncing
    if deb_a == 0:
        # Inverte o estado do jogo (de setar as células para rodar o jogo e vice-versa)
        set_game = not set_game
        deb_a = 1
    # Para debouncing
    utime.sleep(0.2)


def button_b_pressed(pin):
    global deb_b
    # Laço para debouncing
    if deb_b == 0:
        deb_b = 1
        if cell_matrix[y][x]:
            buzzer.freq(NOTES["A4"])
        else:
            buzzer.freq(NOTES["C4"])
        buzzer.duty_u16(512)
        # Inverte o estado da célula sob o cursor
        cell_matrix[y][x] = not cell_matrix[y][x]        
        # Para debouncing
        utime.sleep(0.2)
        buzzer.duty_u16(0)
        #timer que poem zero na variavel de debouncing depois de 200us
        debounce_timer.init(mode=Timer.ONE_SHOT, period=200, callback=debounce_callback_b)
        
# Função chamada após o tempo de debounce
def debounce_callback_b(timer):
    global deb_b
    if deb_b == 1:
        deb_b = 0
            
# Interrupção botões
button_a.irq(trigger=Pin.IRQ_FALLING, handler=button_a_pressed)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=button_b_pressed)


# Inicializa estado das células na matriz de LEDs (False = morta)
cell_matrix = [[False for _ in range(5)] for _ in range(5)]

# Inicializa matriz de LEDs
np.fill((0, 0, 0))  # Apaga todos os LEDs
np[LED_MATRIX[y][x]] = cursor_dead  # Acende o LED do cursor com a cor atual
np.write()

# inicializa variaveis debouncing
deb_a = 0
deb_b = 0
# Loop principal
while True:

    # Loop da matriz de LEDs
    while set_game:
        # Leitura do joystick
        vx = VRx.read_u16()
        vy = VRy.read_u16()

        # Lê o valor do microfone (0-65535)
        sound_level = microphone.read_u16()
        print(sound_level)

        # Movimento horizontal
        if vx > 45000 and x < 4:
            x += 1
        elif vx < 20000 and x > 0:
            x -= 1

        # Movimento vertical
        if vy > 45000 and y > 0:
            y -= 1
        elif vy < 20000 and y < 4:
            y += 1

        update_matrix()
        utime.sleep(0.2)
        detect_clap()

    # Preenche a grid com o jogo
    for i in range(5):
        for j in range(5):
            grid[GRID_HEIGHT // 2 - 2 + j][GRID_WIDTH // 2 - 2 + i] = cell_matrix[j][i]
    update_matrix()

    utime.sleep(0.4)

    # Debouncing
    deb_a = 0

    # to play the song
    melody_index = 0
    play_next_note(melody_timer)

    while not set_game:
        draw_oled()
        utime.sleep(0.5)
        game_of_life_step()

    utime.sleep(0.4)
    deb_a = 0
    # Reseta a tela do jogo da vida
    grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    draw_oled()

