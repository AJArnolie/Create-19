from movement import *
from utilities import *
import constants as c
from wallaby import *
import camera as p
import gyro as g
import movement as m

colorOrder = []

burningMCLeft = True
burningSky = 0

def turnCalibration():
    g.rotate(180, 100)
    msleep(500)
    DEBUG()

def init():
    if c.IS_PRIME:
        print("I are prime")
    if c.IS_CLONE:
        print("I are clone")
    #SETUP
    #Arm pointing away from MCs
    #Edges of create line up with the black tape intersection
    #Align square up surface with left side of middle bump
    #   This should ensure that the robot is pointing directly towards the middle bump (DRS forward)
    print("Starting init")
    enable_servos()
    print("Enabling my servos")
    p.cameraInit()
    p.camera_update()
    print("Camera Init")
    msleep(500)
    msleep(500)
    moveServo(c.skyArm, c.armVertical)
    msleep(500)
    moveServo(c.skyClaw, c.clawOpen)
    msleep(500)
    moveServo(c.skyClaw, c.clawClosedWater)
    msleep(500)
    create_connect()
    create_full()
    #turnCalibration()
    print("Connecting create")
    g.rotate(-50, 150)
    msleep(500)
    g.rotate(50, 150)
    msleep(500)
    g.drive_condition(m.get_black_left, -250, False)
    moveServo(c.skyArm, c.armDown)
    msleep(500)
    moveServo(c.skyClaw, c.clawOpen)
    msleep(500)
    moveServo(c.electricalArm, c.electricArmUp)
    msleep(500)
    moveServo(c.electricalArm, c.electricArmDown, 10)
    disable_servo(c.electricalArm)
    wait_for_button()
    msleep(500)
    g.calibrate_gyro()
    c.START_TIME = seconds()


def findBurningBuildings():
    #Function determines which skyscraper and which MC are burning
    global burningMCLeft
    global burningSky
    moveServo(c.skyArm, c.armVertical)
    g.rotate(55, 100)
    msleep(500)
    burningMCLeft = p.findBurningMC()
    if burningMCLeft == True:
        print("doing code for left")
    else:
        print("doing code for right")
    msleep(500)
    g.rotate(-55, 100)
    msleep(900)
    burningSky = p.findBurningSky()
    if burningSky == 0:
        print("doing code for left")
    elif burningSky == 1:
        print("doing code for middle")
    else:
        print("doing code for right")
    #Do Bump to signal LEGO bot (not coded yet)


def grabBotMayor():
    print("Grabbing the botMayor")
    m.drive_to_black_and_square_up(-100)
    g.create_drive_timed(150, 1.6)
    g.rotate(-90, 150)
    g.create_drive_timed(200, 3.3)
    m.drive_to_black_and_square_up(-100)
    if burningSky == 0 or burningSky == 2: #center building
        #g.rotate(2.5, 50)
        if c.IS_CLONE:
            g.create_drive_timed(50, 3.2)
        else:
            g.create_drive_timed(50, 3.1)
        msleep(500)
        moveServo(c.skyArm, c.mayorArm, 5)
        msleep(100)
        moveServo(c.skyClaw, c.clawClosedMayor, 5)
        msleep(800)
        moveServo(c.skyArm, c.armVertical, 5)
        msleep(500)
        m.drive_to_black_and_square_up(-100)
        #g.create_drive_timed(-175, 1)
        g.rotate(180, 125)
        m.drive_to_black_and_square_up(100)
        moveServo(c.skyArm, c.armDown, 10)
        msleep(100)
        moveServo(c.skyClaw, c.clawOpen, 20)
        msleep(100)
        if burningSky == 0: #Right building
            moveServo(c.skyArm, c.armVertical, 10)
            msleep(100)
            m.drive_to_black_and_square_up(-75)
            g.rotate(145, 100)
            g.create_drive_timed(50, 4.9) #2.7
            msleep(100)
            moveServo(c.skyArm, c.armLowGrab, 10)
            msleep(100)
            moveServo(c.skyClaw, c.clawClosedMayor, 10)
            msleep(100)
            moveServo(c.skyArm, c.armVertical, 10)
            msleep(250)
            g.create_drive_timed(-50, 3.5)
            g.rotate(-155, 100)
            m.drive_to_black_and_square_up(100)
            g.rotate(5, 125)
            moveServo(c.skyArm, c.armDown + 75, 10)
            msleep(100)
            moveServo(c.skyClaw, c.clawOpen, 20)
            msleep(100)
            g.rotate(-5, 125)
        else: #Left building
            moveServo(c.skyArm, c.armVertical, 10)
            if c.IS_PRIME:
                g.rotate(-148, 125)
            else:
                g.rotate(-143, 125)
            g.create_drive_timed(50, 5.2)
            moveServo(c.skyArm, c.armLowGrab, 10)
            msleep(100)
            moveServo(c.skyClaw, c.clawClosedMayor, 10)
            msleep(100)
            moveServo(c.skyArm, c.armVertical, 10)
            msleep(250)
            g.create_drive_timed(-50, 2.7)
            g.rotate(143, 100)
            m.drive_to_black_and_square_up(100)
            moveServo(c.skyArm, c.armDown + 75, 10)
            msleep(100)
            moveServo(c.skyClaw, c.clawOpen, 20)
            msleep(100)
    else: #outside buildings
        moveServo(c.skyArm, c.armVertical, 10)
        msleep(100)
        m.drive_to_black_and_square_up(-75)
        g.rotate(-35, 100)
        g.create_drive_timed(50, 2.2)
        msleep(100)
        moveServo(c.skyArm, c.armLowGrab, 10)
        msleep(100)
        moveServo(c.skyClaw, c.clawClosedMayor, 10)
        msleep(100)
        moveServo(c.skyArm, c.armVertical, 10)
        msleep(250)
        g.create_drive_timed(-50, 2.2)
        g.rotate(-145, 100)
        m.drive_to_black_and_square_up(100)
        moveServo(c.skyArm, c.armDown, 10)
        msleep(100)
        moveServo(c.skyClaw, c.clawOpen, 20)
        msleep(100)
        moveServo(c.skyArm, c.armVertical, 10)
        msleep(500)
        g.rotate(-143, 125)
        g.create_drive_timed(100, 2.4)
        g.create_drive_timed(50, .5)
        msleep(100)
        moveServo(c.skyArm, c.armLowGrab, 10)
        msleep(100)
        moveServo(c.skyClaw, c.clawClosedMayor, 10)
        msleep(100)
        moveServo(c.skyArm, c.armVertical, 10)
        msleep(250)
        g.create_drive_timed(-50, 2.7)
        g.rotate(142, 100)
        m.drive_to_black_and_square_up(100)
        g.rotate(-10, 125)
        moveServo(c.skyArm, c.armDown + 75, 10)
        msleep(100)
        moveServo(c.skyClaw, c.clawOpen, 20)
        msleep(100)
        g.rotate(10, 125)


def headToElecLines():
    print("Heading to electric lines")
    moveServo(c.skyArm, c.armVertical, 10)
    wait_for_button()
    if c.IS_PRIME:
        g.create_drive_timed(-60, 1)
    else:
        g.create_drive_timed(-60,2)
    g.rotate_condition(m.get_right_front, -100, 100, False)
    msleep(100)
    m.timedLineFollowLeftFront(100, 12)
    g.rotate(180, 125)
    g.create_drive_timed(100, 3)
    msleep(100)
    g.create_drive_timed(-100, 1)
    g.rotate(87, 125)
    enable_servo(c.electricalArm)
    msleep(100)
    moveServo(c.electricalArm, c.electricArmStart, 10)
    msleep(100)
    g.create_drive_timed(125, 1)
    msleep(100)
    moveServo(c.electricalArm, c.electricArmUp, 3)
    msleep(100)
    g.create_drive_timed(125, 1)
    msleep(100)
    g.create_drive_timed(-50, 1)
    msleep(100)
    moveServo(c.electricalArm, c.electricArmDown, 10)
    m.drive_to_black_and_square_up(-100)
    g.create_drive_timed(-50, 1)
    g.rotate(-90, 125)
    g.create_drive_timed(125, 2)
    msleep(100)
    g.create_drive_timed(-100, 1)
    g.rotate(93, 125)
    g.create_drive_timed(-50, 2.5)
    moveServo(c.electricalArm, c.electricArmStart, 10)
    msleep(100)
    g.create_drive_timed(-125, 1)
    moveServo(c.electricalArm, c.electricArmUp, 3)
    msleep(100)
    g.create_drive_timed(-125, 1)
    msleep(100)
    g.create_drive_timed(125, 1)
    moveServo(c.electricalArm, c.electricArmDown, 10)
    disable_servo(c.electricalArm)


def headToWaterCube():
    g.create_drive_timed(250, .75)
    m.drive_to_black_and_square_up(125)
    msleep(100)
    g.create_drive_timed(125, .3)
    g.rotate(90, -125)
    m.timedLineFollowLeftFront(100, 17)


def grabWaterCube():
    #Create turns and grabs large water cube
    moveServo(c.skyArm, c.armVertical)
    msleep(300)
    if c.IS_PRIME:
        g.rotate(175, 150)
    msleep(500)
    if c.IS_PRIME:
        moveServo(c.skyArm, c.armDown)
    msleep(800)
    #driveTilBlackLCliffAndSquareUp(100)
    if c.IS_PRIME:
        m.drive_to_black_and_square_up(75)
    else:
        m.drive_to_black_and_square_up(150)
    msleep(500)
    if c.IS_PRIME:
        g.create_drive_timed(-100, 1)
    elif c.IS_CLONE:
        g.create_drive_timed(100, 1.5) #Will
    msleep(500)
    if c.IS_PRIME:
        g.rotate(13, 150)
        msleep(500)
        g.create_drive_timed(100, 2)
        msleep(100)
    if c.IS_CLONE:
        msleep(100)
        g.rotate(18, 150)
        moveServo(c.skyArm, c.armDown, 10)
    msleep(750)
    moveServo(c.skyClaw, c.clawClosedWater)
    msleep(1000)
    moveServo(c.skyArm, c.armVertical)
    msleep(300)
    if c.IS_PRIME:
        g.create_drive_timed(-100, 1.5)
    msleep(300)


def dropWaterCube():
    #Create deposits large water cube on burning building
    g.rotate(-10, 150)
    msleep(300)
    if c.IS_PRIME:
        g.create_drive_timed(-100, .7)
    else:
        m.drive_to_black_and_square_up(-150)
    msleep(500)
    if c.IS_PRIME:
        m.drive_to_black_and_square_up(-100)
    msleep(500)
    if c.IS_PRIME:
        g.create_drive_timed(100, 1.5)
    else:
        g.create_drive_timed(-200, 2.1)
    msleep(500)
    if c.IS_PRIME:
        g.rotate(90, 150)
        g.create_drive_timed(-200, 3)
        msleep(300)
        m.drive_to_black_and_square_up(75)
    else:
        g.rotate(-90, 150)
        g.create_drive_timed(200, 3.3)
        m.drive_to_black_and_square_up(-75)
    if burningSky == 0:
        print("Left")
        if c.IS_CLONE:
            g.rotate(40, 100)
        else:
            g.rotate(35, 100)
        msleep(500)
        g.create_drive_timed(100, 1.8) #Will
        moveServo(c.skyArm, c.armLowSkyscraper, 5)
        msleep(100)
        moveServo(c.skyClaw, c.clawOpen, 10)
    elif burningSky == 1:
        print("middle")
        if c.IS_CLONE:
            msleep(500)
            g.rotate(2.5, 50)
            msleep(500)
            g.create_drive_timed(50, 3.3)
            msleep(500)
        msleep(250)
        moveServo(c.skyArm, c.armHighSkyscraperDeliver, 5)
        msleep(100)
        moveServo(c.skyClaw, c.clawDeliver, 5)
    else:
        print("Right")
        if c.IS_PRIME:
            g.rotate(-23, 100)
            msleep(500)
            g.create_drive_timed(-50, .5)
        elif c.IS_CLONE:
            g.rotate(-35, 100)
            msleep(500)
            g.create_drive_timed(50, 1.3)
        msleep(100)
        moveServo(c.skyArm, c.armLowSkyscraper, 5)
        msleep(100)
        moveServo(c.skyClaw, c.clawDeliver, 10)

    #After this is successful, fill function below that picks up the Mayor and Botguy and places them in the startbox
    #You shouldn't have to move the robot at all because the arm is long enough to reach the start box

#Proposed strategy
def grabFirstSkyCube():
    pass
def grabSecondSkyCube():
    pass
def connectElectricalLines():
    pass