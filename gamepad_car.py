from gpiozero import Motor, PWMLED
import pygame
import subprocess
from time import sleep

redpwm = PWMLED(9)
greenpwm = PWMLED(10)
bluepwm = PWMLED(11)

steering = Motor(forward=4, backward=14)
motor = Motor(forward=17, backward=18)

# initialize pygame
pygame.init()

controller = ''

try:
    while controller == '':
        try:
            # create a controller object
            controller = pygame.joystick.Joystick(0)
            # initialize the controller
            controller.init()
            print("car started")
            print("press ctrl + c to exit")
            greenpwm.value = 0.5
        except:
            print('Please connect a controller. Restart in 10 seconds.')
            print("press ctrl + c to exit")
            bluepwm.pulse()
            redpwm.pulse()
            sleep(10)
            subprocess.call(
                ["lxterminal", "--command=python3 gamepad_controlled_car/gamepad_car.py"])
            exit()
except KeyboardInterrupt:
    print("ending program")
    pygame.quit()
    exit()

speed = 1.0

try:
    while True:
        events = pygame.event.get()
        for event in events:
            if controller.get_axis(0) < 0:
                print(controller.get_axis(0))
                steering.forward()
            elif controller.get_axis(0) > 0:
                print(controller.get_axis(0))
                steering.backward()
            elif controller.get_axis(0) == 0:
                steering.stop()

            if event.type == pygame.JOYBUTTONDOWN:
                if controller.get_button(0):
                    if speed >= 0.70:
                        speed -= 0.10
                    print("Cross (X) Pressed")
                    print(speed)
                elif controller.get_button(1):
                    print("Circle Pressed")
                elif controller.get_button(2):
                    print("Triangle Pressed")
                    if controller.get_button(10):
                        print('shutdown')
                        subprocess.call(
                            ["lxterminal", "--command=sudo shutdown -h now"])
                elif controller.get_button(3):
                    if speed <= 0.90:
                        speed += 0.10
                    print("Square Pressed")
                    print(speed)
                elif controller.get_button(4):
                    print("L1 Pressed")
                elif controller.get_button(5):
                    print("R1 Pressed")
                    motor.backward()
                elif controller.get_button(6):
                    print("L2 Pressed")
                    motor.backward(speed)
                elif controller.get_button(7):
                    print("R2 Pressed")
                    motor.forward(speed)
                    if controller.get_button(5):
                        print("R1 Pressed")
                        motor.backward()
                elif controller.get_button(8):
                    print("SHARE Pressed")
                elif controller.get_button(9):
                    print("OPTIONS Pressed")
                elif controller.get_button(10):
                    print("Power (PS) Button Pressed")
                elif controller.get_button(11):
                    print("Left Analog (L3) Pressed")
                elif controller.get_button(12):
                    print("Right Analog (R3) Pressed")

                if speed == 1.0:
                    greenpwm.value = 0.10
                    redpwm.value = 0.0
                elif speed >= 0.9:
                    greenpwm.value = 0.07
                    redpwm.value = 0.03
                elif speed >= 0.8:
                    greenpwm.value = 0.04
                    redpwm.value = 0.06
                elif speed >= 0.7:
                    greenpwm.value = 0.02
                    redpwm.value = 0.08
                elif speed >= 0.6:
                    greenpwm.value = 0.0
                    redpwm.value = 0.10

            elif event.type == pygame.JOYBUTTONUP:
                print("Button Released")
                motor.stop()

except KeyboardInterrupt:
    print("ending program")
    greenpwm.value = 0
    redpwm.value = 0
    bluepwm.value = 0
    controller.quit()
    pygame.quit()
