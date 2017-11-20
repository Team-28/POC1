#Team 28 Line Following Code

import time
import brickpi3
import grovepi
import math as m

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.TOUCH)
BP.offset_motor_encoder(BP.PORT_C, BP.get_motor_encoder(BP.PORT_C)) 
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.NXT_LIGHT_ON)
lightSensor = 2
sensorLed = 4
BP.set_motor_power(BP.PORT_C, 0)
BP.set_motor_power(BP.PORT_B, 0)
grovepi.pinMode(lightSensor, "INPUT")
grovepi.pinMode(sensorLed, "OUTPUT")
lightSensorBWThreshold = 300 #define value for black vs white
NXTLightSensorThreshold = 2000# define value for black vs white
speedCalibration =  8
lineFinder = 7


#########################################
timeNeeded = 1
timeOld = 0
motorSpeedDefault = 25 #dont make it abov 89
########################################


#initialize color sensor and line finder and NXT color sensor

print("Press button to begin")

value = 0
while not value:
    try:
       value = BP.get_sensor(BP.PORT_3)
    except brickpi3.SensorError:
       value = 0
loopCounter = 0
timeInitial = time.time()
while value:
    if loopCounter == 0:
        leftMotorSpeed = motorSpeedDefault
        rightMotorSpeed = motorSpeedDefault * 1.12
    elif loopCounter >= 1:
        i = grovepi.digitalRead(lineFinder)
        j = grovepi.analogRead(lightSensor)
        k = BP.get_sensor(BP.PORT_2)
        print("Line", i)
        print("Light", j)
        print("NXT", k)



        if (time.time() - timeOld > timeNeeded):
            timeOld = time.time()
            if i == 1:
                leftMotorSpeed = leftMotorSpeed - speedCalibration
                rightMotorSpeed = rightMotorSpeed + speedCalibration
                print(1)
                #time.sleep(1)
            elif j < lightSensorBWThreshold:
                leftMotorSpeed = leftMotorSpeed + speedCalibration
                rightMotorSpeed = rightMotorSpeed - speedCalibration
                print(2)
                #time.sleep(1)
            elif i == 0 and j > lightSensorBWThreshold:
                leftMotorSpeed = motorSpeedDefault
                rightMotorSpeed = motorSpeedDefault * 1.12
                print(3)
   


   
    BP.set_motor_power(BP.PORT_B, leftMotorSpeed) #update motor speeds
    BP.set_motor_power(BP.PORT_C, rightMotorSpeed)
    time.sleep(0.01)
    loopCounter = loopCounter + 1



























#        elif i != 1 and j >= lightSensorBWThreshold and k < NXTLightSensorThreshold:
#            timeInitial = time.time()
#            encoderBaseR = BP.get_motor_encoder(BP.PORT_C)
#            encoderBaseL = BP.get_motor_encoder(BP.PORT_B)
#            print(5)
#            x = True
#            z = 4
#            while x:
#                encoderR = BP.get_motor_encoder(BP.PORT_C)
#                encoderL= BP.get_motor_encoder(BP.PORT_B)
#                time.sleep(0.05)
#                BP.set_motor_power(BP.PORT_C, 28)
#                BP.set_motor_power(BP.PORT_B, 25)
#                if (encoderL-encoderBaseL)/360 >= 0.92 or (encoderR-encoderBaseR)/360 >= 0.92:
#                    x = False
#                    z = 0
#                    break
#                elif k > NXTLightSensorThreshold:
#                    x = False
#                    z = 1
#                    break
#                elif j <= lightSensorBWThreshold:
#                    x = False
#                    z = 2
#                    break
#                elif i == 1:
#                    x = False
#                    z = 3
#                    break
#            if z == 0:
#                #reverse in an s shape in order to reset starting point
#                BP.set_motor_power(BP.PORT_C, -56)
#                BP.set_motor_power(BP.PORT_B, -50)
#                time.sleep(1)
#                BP.set_motor_power(BP.PORT_C, -84)
#                BP.set_motor_power(BP.PORT_B, -50)
#                time.sleep(1)
#                BP.set_motor_power(BP.PORT_C, -56)
#                BP.set_motor_power(BP.PORT_B, -75)
#                time.sleep(1)
#                BP.set_motor_power(BP.PORT_C, -56)
#                BP.set_motor_power(BP.PORT_B, -50)
#                time.sleep(1)
#                BP.set_motor_power(BP.PORT_C, 56)
#                BP.set_motor_power(BP.PORT_B, 50)
#                x = True
#                z = 4
#        time.sleep(0.05) 