
import picamera
import pygame as pg
import RPi.GPIO as IoPort
import time

#camera
cam = picamera.PiCamera()
cam.resolution = (1920, 1080)
cam.framerate = 29.97
cam.vflip = True

def Button(channel):
    global ButtonVal
    if channel == ButtonNum:
        ButtonVal = 1
    else:
        ButtonVal =0

def play_music(music):

    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(music)
    except pygame.error:
        return

    pg.mixer.music.play()
    
    while pg.mixer.music.get_busy():
        clock.tick(30)
        break

def Capture():
    str1 = '/home/pi/han/ ' +'Kids_Bridge_'+ Srl +'.JPG'
    cam.capture(str1)

def Count_r():
    log_r = open("log.txt", 'r')
    count = log_r.read()
    print(count)
    log_r.close()

def Count_w():
    log_w = open("log.txt", 'w')
    count = str(int(Srl) + 1)
    log_w.write(count)
    log_w.close()
    
#music
Mf1 = "wacci_start.mp3"
Mf2 = "wacci_sound.mp3"

#Button
ButtonNum = 14
ButtonVal = 0

#interrupt
IoPort.setmode(IoPort.BCM)
IoPort.setup(ButtonNum,IoPort.IN)
IoPort.add_event_detect(ButtonNum,IoPort.FALLING,callback=Button)

#speaker
freq = 44100
bitsize = -16
channels = 2
buffer = 2048
pg.mixer.init(freq, bitsize, channels, buffer)
pg.mixer.music.set_volume(1.0)

try:
    play_music(Mf1)
    while True:
        if ButtonVal == 1:
            
            #count
            log_r = open("log.txt",'r')
            Srl = log_r.read()
            print(Srl)
            log_r.close()
            
            time.sleep(0.1)
            play_music(Mf2)
            
            time.sleep(1.5)
            Capture()
            time.sleep(2.5)
            
            pg.mixer.music.fadeout(1000)
            pg.mixer.music.stop()
            
            ButtonVal = 0
            Count_w()

except:
    cam.close()
