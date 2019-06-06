import sys
import time
import pygame

import Adafruit_MPR121.MPR121 as MPR121


#DEFINICAO DE VARIAVEIS
cap = MPR121.MPR121()
mode = 1
#a variavel mode determina o modo de reproducao de sons do sensor capacitivo
#mode tem valor inicial 1
#1: Bateria Eletronica    2: Animais 
mode_max = 2
SOUND_MAPPING = {}
sounds = [0,0,0,0,0,0,0,0,0,0,0,0]
time_pressing_mode_button = 0
pressing_mode = False
pressing_pedal = False


#DEFINICAO DE FUNCOES:
def shutdown_pi():
    command = "/usr/bin/sudo /sbin/shutdown -P now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print output

def set_sound_mode(new_mode):
    global SOUND_MAPPING
    global sounds
    if new_mode == 1: #Nao mexer nesse modo padrao da bateria
        SOUND_MAPPING = {
        0: '/home/pi/Documents/drummies/Sons/hat.wav',
        1: '/home/pi/Documents/drummies/Sons/kick.wav',
        2: '/home/pi/Documents/drummies/Sons/snare.wav',
        3: '/home/pi/Documents/drummies/Sons/ride_bell_loud.wav',
        4: '/home/pi/Documents/drummies/Sons/sidestick.wav',
        5: '/home/pi/Documents/drummies/Sons/perc_2.wav',
        6: '/home/pi/Documents/drummies/Sons/tom.wav',
        7: '/home/pi/Documents/drummies/Sons/hat_open_3.wav',
        8: '/home/pi/Documents/drummies/Sons/perc_1.wav',
        9: '/home/pi/Documents/drummies/Sons/rimshot_2.wav',
        10: '/home/pi/Documents/drummies/Sons/snare_rimshot.wav',
        #11: '/home/pi/Documents/drummies/Sons/kick_light.wav',
        }
    if new_mode == 2:
        SOUND_MAPPING = {
        0: '/home/pi/Documents/drummies/Animal/Bird.wav',
        1: '/home/pi/Documents/drummies/Animal/Cricket.wav',
        2: '/home/pi/Documents/drummies/Animal/Dog1.wav',
        3: '/home/pi/Documents/drummies/Animal/Dog2.wav',
        4: '/home/pi/Documents/drummies/Animal/Duck.wav',
        5: '/home/pi/Documents/drummies/Animal/Goose.wav',
        6: '/home/pi/Documents/drummies/Animal/Horse.wav',
        7: '/home/pi/Documents/drummies/Animal/Kitten.wav',
        8: '/home/pi/Documents/drummies/Animal/Meow.wav',
        9: '/home/pi/Documents/drummies/Animal/Owl.wav',
        10: '/home/pi/Documents/drummies/Animal/Rooster.wav',
        #11: '/home/pi/Documents/drummies/Animal/WolfHowl.wav',
        }
    for key,soundfile in SOUND_MAPPING.iteritems():
            sounds[key] =  pygame.mixer.Sound(soundfile)
            sounds[key].set_volume(1);

def change_sound_mode():
    global mode
    global mode_max
    if (mode % mode_max) != 0:
        mode += 1
    else:
        mode = 1
    print('Mudando para o modo {0}'.format(mode))


print('Teste de emissão de som no sensor capacitivo Adafruit MPR121')

if not cap.begin():
    print('Erro ao iniciar o MPR121. Cheque suas conexões.')
    sys.exit(1)


pygame.mixer.pre_init(44100, -16, 12, 512)
pygame.init()

#como mode tem valor inicial 1, podemos ja de inicio definir os sons de bateria
#eletronica como, tambem, os sons iniciais
set_sound_mode(mode)

print('Aperte Ctrl-C para sair')
last_touched = cap.touched()
while (time_pressing_mode_button <= 0.03):
    initial_time = time.clock()
    current_touched = cap.touched()
    for i in range(12):
        pin_bit = 1 << i
        if current_touched & pin_bit and not last_touched & pin_bit:
            print('{0} apertado!'.format(i))
            if mode == 1:
                if  i == 10:
                    pressing_pedal = True
                else:
                    if i == 9 and pressing_pedal == True:
                        if sounds[10]:
                            sounds[10].play()
                    elif i == 9 and not pressing_pedal == True:
                        if sounds[9]:
                            sounds[9].play()
                    else:
                        if sounds[i]:
                            sounds[i].play()
            else:
                if sounds[i]:
                    sounds[i].play()
            if i == 11:
                change_sound_mode()
                set_sound_mode(mode)
                pressing_mode = True
        if not current_touched & pin_bit and last_touched & pin_bit:
            print('{0} solto!'.format(i))
            if (i == 10):
                pressing_pedal = False
            if (i == 11):
                pressing_mode = False
    if pressing_mode == True:
        time_pressing_mode_button += (time.clock() - initial_time)
    else :
        time_pressing_mode_button = 0
                


    last_touched = current_touched
    time.sleep(0.1)
    
shutdown_pi()