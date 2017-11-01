#Team 28 POC1 code

import time
import brickpi3
import math as m

#define distance MCMS needs to travel
distance = input("How far do you need to travel? [cm]")
timeAlloted = input("In what time (in [s]) do you need to travel")
distance = float(distance)
timeAlloted = float(timeAlloted)
wheelDiameter = 8.3 #hardcode in wheel diameter for our bot
distanceTraversed = 0
gearRatio = 24/40
calibrationConstant = 1.04
timeCalibrationConstant = 2

BP = brickpi3.BrickPi3()

BP.set_sensor_type(BP.PORT_2, BP.SENSOR_TYPE.TOUCH)
BP.offset_motor_encoder(BP.PORT_A, BP.get_motor_encoder(BP.PORT_A)) 
BP.offset_motor_encoder(BP.PORT_B, BP.get_motor_encoder(BP.PORT_B))
#reset encoder readings so we can use them to determine distance traveled


print("Press button to begin")

#create a function to determine the required speed in cm/s
def speedCalc(traverseDistance, traverseTime):
    speed = traverseDistance/traverseTime
    return(speed)

#set a global variable equal to the speed we need to traverse distance in set time
rawSpeed = speedCalc(distance, timeAlloted)

def motorSpeedConversion(speed, diameter):
    #a function to convert speed to motor outputs based on wheel diameter,
    #rates, etc
    global gearRatio
    global timeCalibrationConstant
    rotationRate = (speed/(diameter/2)/gearRatio)/timeCalibrationConstant
    return(rotationRate)
    #output required rotation rates in degree/sec

#set a global variable equal to the speed average we need to maintain
speedRequired = motorSpeedConversion(speedCalc(distance,timeAlloted), wheelDiameter)

#function to intake encoder ticks and then convert them to a rate
def readEncoders():
    i = 0
    encoderBaseL = BP.get_motor_encoder(BP.PORT_A)
    encoderBaseR = BP.get_motor_encoder(BP.PORT_B)
    encoderTickL = [0,0,0]
    encoderTickR = [0,0,0]
    angularVelocityArrayR = [0,0,0]
    angularVelocityArrayL = [0,0,0]
    for i in range (0,2): #take in encoder ticks over 0.03 sec
        encoderTickL[i] = (BP.get_motor_encoder(BP.PORT_A)-encoderBaseL)
        encoderTickR[i] = (BP.get_motor_encoder(BP.PORT_B)-encoderBaseR)
        encoderBaseL = BP.get_motor_encoder(BP.PORT_A)
        time.sleep(0.01)
        dt = 0.01
        xL = encoderTickL[i]
        angularVelocityArrayL[i] = xL/dt
        xR = encoderTickR[i]
        angularVelocityArrayR[i] = xR/dt
    averageAngularVelocityR = (((sum(angularVelocityArrayR)/3)/360)*m.pi*2)
    averageAngularVelocityL = (((sum(angularVelocityArrayL)/3)/360)*m.pi*2)
    return(averageAngularVelocityL, averageAngularVelocityR)

def distanceTraversedCalc():
    global wheelDiameter
    global gearRatio
    global calibrationConstant
    distanceTraveled = calibrationConstant*(((((BP.get_motor_encoder(BP.PORT_B))/360)*2*m.pi)*wheelDiameter/2)*(gearRatio))
    return(distanceTraveled)
value = 0
while not value:
    try:
       value = BP.get_sensor(BP.PORT_2)
    except brickpi3.SensorError:
       value = 0
loopCounter = 0
timeInitial = time.time()
while value:
    if loopCounter == 0:
        leftMotorSpeed = 25
        rightMotorSpeed = 27.5
        leftSpeed = 100
        rightSpeed = 100
        print("Speed required",speedRequired)
        print("L/R motor speeds", leftMotorSpeed, rightMotorSpeed)
        time.sleep(0.5)
    elif loopCounter >= 1:
        speedArray = readEncoders()
        leftSpeed = speedArray[0]
        rightSpeed = speedArray[1]
        print("L/R angular velocities",readEncoders())
        #print("Speed required:", speedRequired)
        print("L/R motor speeds", leftMotorSpeed, rightMotorSpeed)
    
    if leftMotorSpeed < 100 and rightMotorSpeed < 100:
        if leftSpeed < speedRequired:
            leftMotorSpeed = leftMotorSpeed + 2.5 #increment value (needs calibration)
        elif leftSpeed > speedRequired:
            leftMotorSpeed = leftMotorSpeed - 2.5 #increment value
    
        if rightSpeed < speedRequired:
            rightMotorSpeed = rightMotorSpeed + 2.5 #increment value
        elif rightSpeed > speedRequired:
            rightMotorSpeed = rightMotorSpeed - 2.5 #increment value
    elif rightMotorSpeed >= 100 or leftMotorSpeed >= 100:
        rightMotorSpeed = 100
        leftMotorSpeed = 100

    BP.set_motor_power(BP.PORT_A, leftMotorSpeed) #update motor speeds
    BP.set_motor_power(BP.PORT_B, rightMotorSpeed) 
    distanceTraveled = distanceTraversedCalc()
    print("Distance:", distanceTraveled)
    if distanceTraveled >= distance + 4: 
        #stop bot and break loop once it has traversed the desired distance
        rightSpeed = 0
        leftSpeed = 0
        BP.set_motor_power(BP.PORT_A, 0) #update motor speeds
        BP.set_motor_power(BP.PORT_B, 0)
        value = 0
        print("distanceBreak")
        print("distance:", distanceTraveled)
        print("loops:", loopCounter)
        print("time:", time.time()-timeInitial)
        break
    elif time.time()-timeInitial >= timeAlloted:
        rightSpeed = 0
        leftSpeed = 0
        BP.set_motor_power(BP.PORT_A, 0) #update motor speeds
        BP.set_motor_power(BP.PORT_B, 0)
        value = 0
        print("timeBreak")
        break
                #consider finding a brake function    
    time.sleep(0.01)
    loopCounter = loopCounter + 1
