import os
import sys

from gopigo import *

import Tkinter as tk

import picamera

import thread
import threading
import time


#Remote controls
#==> move wheels
#==> move servo
#==> play sound
#==> get distance from objects
#==> take pictures
#==> led blinking

#p = picamera.PiCamera()
i = 1
#for sound
x = 0
#for led
b = 0

#center the servo (get the central position)
servo_central = 50
servo_pos = servo_central
servo(servo_pos)


def remote_control(event):
    key_press = event.keysym.lower()
    print(key_press)

    if key_press =='w':
        fwd()
    elif key_press == 's':
        bwd()
    elif key_press == 'd':
        right()
    elif key_press == 'q':
        left_rot()
    elif key_press == 'e':
        right_rot()
    elif key_press == 't':
        increase_speed()
    elif key_press=='y':
        decrease_speed()
    elif key_press == 'space':
        stop()
    elif key_press == 'u':
        print ('The object is ' + str(us_dist(15)) + 'cm far from our device')
    elif key_press == 'c': #take a picture
        global i
        i+= 1
        with picamera.PiCamera() as camera:
            camera.vflip = True
            picName = 'foto' + str(i) + '.jpg'
            camera.capture (picName)
            print ('Picture taken : ' + picName)
            
    #servo (4=left; 5=center; 6=right)
    elif key_press == '4':
        global servo_pos
        servo_pos -= 10
        if servo_pos>180:
            servo_pos=180
        if servo_pos<0:
            servo_pos=0
        servo(servo_pos)
        time.sleep(.1)
    elif key_press == '5':
        global servo_central
        servo(servo_central)
        time.sleep(.1)
    elif key_press=='6':
        global servo_pos
        servo_pos += 10
        if servo_pos>180:
            servo_pos=180
        if servo_pos<0:
            servo_pos=0
        servo(servo_pos)
        time.sleep(.1)


    #make a noise
    elif key_press=='o':
        buzz_pin = 10
        global x
        if x == 0:
            analogWrite(buzz_pin,255)
            x = 1
        else:
            analogWrite(buzz_pin,0)
            x = 0
            
    #blink leds
    elif key_press == 'b':
        global b
        if b == 0:
            print ('led ON')
            led_on(LED_L)
            led_on(LED_R)
            b = 1
        else:
            print('led OFF')
            led_off(LED_L)
            led_off(LED_R)
            b = 0
                  
        

def basic_function():
    command = tk.Tk()
    command.bind_all("<Key>", remote_control)
    command.mainloop()



#Recognize distance
#==> stop mooving if there is an obstacle
def security_stop():
    distance_to_stop=1    
    while True:
        dist = us_dist(5)
        if dist<distance_to_stop:
            print ('STOPPING!!')
            stop()
            time.sleep(1)


t1 = threading.Thread(name='td1', target=basic_function)
t2 = threading.Thread(name='td2', target=security_stop)

t1.start()
t2.start()