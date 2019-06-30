from movement import *
from utilities import *
import constants as c
from wallaby import *
import camera as p
import gyro as g
import movement as m
import electricLineMotor as em


burning_MC = False
colorOrder = []
burningSky = 0

# def wambulanceGrab():
#     motor(c.ambulance_motor, -10)
#     msleep(1000)
#     motor(c.ambulance_motor, 0)
#     enable_servo(c.ambulance_claw)
#     set_servo_position(c.ambulance_claw, 1485)
#     msleep(1000)
#     disable_servo(c.ambulance_claw)
#     motor(c.ambulance_motor, -10)
#     msleep(4000)
#     motor(c.ambulance_motor, 0)
#     enable_servo(c.ambulance_claw)
#     set_servo_position(c.ambulance_claw, 1100)
#     msleep(2000)
#     motor(c.ambulance_motor, 10)
#     msleep(5000)
#     motor(c.ambulance_motor, 0)
#     msleep(2000)
#     disable_servo(0)


def turn_calibration():
    g.rotate(180, 100)
    msleep(500)
    DEBUG()

def init(): #Test to make sure all the moving parts and sensors work the way they should
    global first
    global burning_MC

    if c.IS_PRIME:
        print("I are prime")
    if c.IS_CLONE:
        print("I are clone")
    #SETUP
    #Arm pointing towards the medical centers
    #Edges of create line up with the black tape intersection
    #Align square up surface with left side of middle bump
    #This should ensure that the robot is pointing directly towards the middle bump (DRS forward)
    print("Starting init")
    print("Enabling my servos")
    enable_servos()
    print("Camera Init")
    p.camera_init()
    p.camera_update()
    msleep(500)
    print("Testing Servos")
    msleep(500)
    msleep(500)
    move_servo(c.sky_arm, c.arm_vertical)
    msleep(500)
    move_servo(c.sky_claw, c.claw_open)
    msleep(500)
    move_servo(c.sky_claw, c.claw_closed_water)
    msleep(500)
    u.move_servo(c.electric_arm_base, c.electric_base_right)
    em.clear_ticks_button()
    u.move_servo(c.electric_arm_base, c.electric_base_down)
    move_servo(c.ambulance_claw, c.wambulance_closed)
    move_servo(c.ambulance_claw, c.wambulance_open)
    u.wambulance_down()
    msleep(100)
    u.wambulance_up()
    move_servo(c.ambulance_claw, c.wambulance_closed + 200)
    print("Connecting to Create")
    create_connect()
    create_full()
    ###################################################
    print("Press right button to check camera.")
    u.wait_for_button_camera_check()
    if u.camera_works:
        print("The camera is working! Continue....")
    else:
        while not u.camera_works:
            print("The camera is NOT working! Press right button to check again. Press left button to continue anyways.")
            u.wait_for_button_camera_check()
        print("Test passed. Continue....")
    u.wait_for_button()
    ###################################################
    print("Drive and Sensor Testing")
    g.rotate(-56, 150)
    msleep(500)
    p.find_burning_sky()
    done = seconds() + 3
    first = False
    print("Waiting for you to press the switch and check which building is burning")
    while not u.get_pipe_switch():
        pass
    g.rotate(56, 150)
    msleep(500)
    m.drive_to_black_and_square_up(-200)
    g.drive_condition(on_black_left_tophat, -250, False)
    print("Setting servos for the run")
    move_servo(c.sky_arm, c.arm_start-30)
    msleep(500)
    move_servo(c.sky_claw, c.claw_open+200)
    msleep(500)
    u.wait_for_button_camera()
    u.wait_4_light()
    c.START_TIME = seconds()
    shut_down_in(119.5)
    print(k.camera_reads)
    burning_MC = u.compute_burning_MC()
    if burning_MC == False: #burning MC is on right
        print("Pushing switch")
        msleep(300)
        u.move_servo(c.sky_arm, c.arm_moving)
        u.move_servo(c.sky_arm, c.arm_button, 5)
        msleep(100)
        u.move_servo(c.sky_arm, c.arm_vertical, 15)
        u.thread_servo(c.electric_arm_base, c.electric_base_left, 20)#####
        u.move_servo(c.ambulance_claw, c.wambulance_open, 20)
        u.wambulance_down()
        msleep(200)
        move_servo(c.ambulance_claw, c.wambulance_closed, 20)
        msleep(200)
        u.wambulance_up()
    else: #burning MC is on left
        print("Not pushing switch")
        u.move_servo(c.sky_arm, c.arm_vertical, 15)
        u.thread_servo(c.electric_arm_base, c.electric_base_left, 20)#####
        u.move_servo(c.ambulance_claw, c.wambulance_open, 20)
        u.wambulance_down()
        msleep(200)
        move_servo(c.ambulance_claw, c.wambulance_closed, 20)
        msleep(200)
        u.wambulance_up()
        msleep(1000)
    msleep(100)
    g.calibrate_gyro()
    #u.move_servo(c.electric_arm_base, c.electric_base_left, 20)

def grab_bot_mayor():
    global burningSky
    if c.IS_CLONE:
        g.rotate(-50, 100)
    else:
        g.rotate(-56, 100)
    msleep(300)#600
    burningSky = p.find_burning_sky()
    if burningSky == 0:
        print("doing code for left")
    elif burningSky == 1:
        print("doing code for middle")
    else:
        print("doing code for right")
    print ("Going to 1/2 building")
    g.create_drive_timed(400, .35)
    m.pivot_till_black(300)
    m.drive_to_black_and_square_up(300)
    msleep(10)
    g.create_drive_timed(200, 0.5)
    m.drive_to_black_and_square_up(300)
    if burningSky!=0:
        grab_first()
        if burningSky!=1:
            grab_second()
        else:
            grab_third()
    else:
        grab_second()
        grab_third()

def grab_second():
    arm_up(c.arm_high_sky_deliver, 20)#
    g.create_drive_timed(200, 0.925)#
    move_servo(c.sky_claw, c.claw_closed_mayor, 20)#
    move_servo(c.sky_arm, c.arm_high_sky)
    g.create_drive_timed(-200, 0.1)  #
    #######################################################
    g.create_drive_timed(-200, 1)
    g.rotate(180, 200)
    m.drive_to_black_and_square_up(250)
    if burningSky == 0:
        g.rotate(10, 200)
    else:
        g.rotate(-10, 200)
    arm_down(c.arm_down, 10)
    move_servo(c.sky_claw, c.claw_open +500, 10)
    move_servo(c.sky_arm, c.arm_low_sky, 10)
    move_servo(c.sky_claw, c.claw_open)
    arm_up(c.arm_high_sky, 15)
    if burningSky == 0:
        g.rotate(-6, 150)
    else:
        g.rotate(6, 150)
    g.rotate(180, 200)
    m.drive_to_black_and_square_up(250)


def grab_first():
    g.create_drive_timed(400, 0.3)
    g.rotate(40, 200)
    move_servo(c.sky_claw, c.claw_open+300, 20)
    g.create_drive_timed(200, .6)
    move_servo(c.sky_arm, c.arm_low_grab + 30, 10)  #
    move_servo(c.sky_claw, c.claw_closed_mayor, 15)  #
    move_servo(c.sky_arm, c.arm_high_sky, 20)
    g.create_drive_timed(-200, .325)
    g.rotate(-40, 200)
    g.create_drive_timed(-200, .5)
    ######################################################
    g.rotate(180, 250)
    m.drive_to_black_and_square_up(250)
    g.rotate(6, 250)
    arm_down(c.arm_down, 10)
    move_servo(c.sky_claw, c.claw_open + 500, 15)
    move_servo(c.sky_arm, c.arm_low_sky, 20)
    move_servo(c.sky_claw, c.claw_open, 20)
    arm_up(c.arm_high_sky, 20)
    g.rotate(174, 250)
    m.drive_to_black_and_square_up(250)


def grab_third():
    em.electric_line_motor(150, 0)
    g.create_drive_timed(200, 0.6)
    if c.IS_PRIME:
        g.rotate(-35, 200)
    else:
        g.rotate(-35, 200)
    move_servo(c.sky_claw, c.claw_open + 300, 20)
    g.create_drive_timed(200, .35)
    move_servo(c.sky_arm, c.arm_low_grab +20, 10)  #
    g.create_drive_timed(200, 0.3)
    move_servo(c.sky_claw, c.claw_closed_mayor, 15)  #
    move_servo(c.sky_arm, c.arm_high_sky, 15)
    g.create_drive_timed(-200, 0.55)
    if c.IS_PRIME:
        g.rotate(35, 200)
    else:
        g.rotate(35, 200)
    g.create_drive_timed(-400, .25)
    #####################################################
    g.rotate(180, 200)
    m.drive_to_black_and_square_up(250)
    g.rotate(-6, 200)
    arm_down(c.arm_down, 10)
    move_servo(c.sky_claw, c.claw_open + 500)
    move_servo(c.sky_arm, c.arm_low_sky, 20)
    move_servo(c.sky_claw, c.claw_open, 20)
    move_servo(c.sky_arm, c.arm_high_sky, 20)
    g.rotate(6, 200)
    g.rotate(180, 200)
    m.drive_to_black_and_square_up(250)


def head_to_elec_lines(): # Goes to electric lines and attatches them
    print("Heading to electric lines")
    thread_servo(c.sky_arm, c.arm_vertical +100, 20)
    thread_servo(c.electric_arm_base, c.electric_base_up, 20)
    if c.IS_PRIME:
        g.create_drive_timed(-400, .8)
        g.create_drive_timed(400, .6)
    else:
        g.create_drive_timed(-400, .8)
        g.create_drive_timed(400, .6)
    g.rotate(-90, 200)
    em.electric_line_motor(150, -600)
    #g.create_drive_timed(500, 3.5) #Square up on wall
    g.drive_timed_condition(u.get_pipe_switch, 500, 3.5, False)
    if not u.get_pipe_switch():
        clear_motor_position_counter(c.electric_line_motor)  # Clears motor counter
        g.create_drive_timed(-400, .40)#.65
        if c.IS_PRIME:
            em.electric_line_motor(150, -1070) #-1170 # Moves motor to a certain position
        else:
            em.electric_line_motor(150, -1070)
        g.rotate(-90, 250)
        g.drive_condition(u.l_or_r_bumped, -300, False)
        g.create_drive_timed(400, .3)
        m.drive_to_black_and_square_up(250)
        msleep(10)
        g.create_drive_timed(-120, .25)
        g.rotate(90, 250)
        #g.create_drive_timed(125, 2.5) #Square up on wall
        g.drive_timed_condition(u.get_pipe_switch, 125, 2.5, False)
        if not u.get_pipe_switch():
            g.create_drive_timed(-250, .5)
            g.create_drive_timed(500, 1)
            msleep(300)
    else:
        g.create_drive_timed(-200, .5)
        clear_motor_position_counter(c.electric_line_motor)  # Clears motor counter
        if c.IS_PRIME:
            em.electric_line_motor(150, -1070) #-1170 # Moves motor to a certain position
        else:
            em.electric_line_motor(150, -1070)
        g.create_drive_timed(400, .3)
        msleep(3000)

def connect_elec_lines():
    #Controls a servo and motor to connect both of the electric lines
    #clear_motor_position_counter(c.electric_line_motor) #Clears motor counter
    #em.electric_line_motor(50, -900) #Moves motor to a certain position
    #u.move_servo(c.electric_arm_base, c.electric_base_swing, 20)
    #em.clear_ticks(-25) #Runs motor until it hits PVC then zeros motor counter
    u.move_servo(c.electric_arm_base, c.electric_base_right, 4)
    em.clear_ticks(-25)
    em.electric_line_motor(25, 493)#525
    rotate(-7, 50)
    # msleep(200)
    # em.clear_ticks(-50)
    msleep(100)
    em.electric_line_motor(30, 170)
    rotate(7, 50)
    msleep(100)
    g.create_drive_timed(-100, 1) #Drive functions use Wallaby gyro
    u.move_servo(c.electric_arm_base, c.electric_base_start_left+100)  # Servo functions use a loop to control servo speed
    em.electric_line_motor(50, 50)  # 85
    u.move_servo(c.electric_arm_base, c.electric_base_start_left+30) #Servo functions use a loop to control servo speed
    em.electric_line_motor(30, -85)#85
    g.create_drive_timed(100, 1.2)
    msleep(100)
    em.clear_ticks(25)
    if c.IS_PRIME:
        em.electric_line_motor(30, -500)
    else:
        em.electric_line_motor(30, -530)
    g.rotate(3, 50)
    msleep(500)
    if c.IS_PRIME:
        em.electric_line_motor(30, -485)
    g.rotate(-3, 50)
    em.electric_line_motor(50, -75)


def drop_wambulance(): # Drives to cube of water
    global burning_MC
    if c.IS_PRIME:
        g.create_drive_timed(-350, 5.09)#-400, 4.45
    else:
        g.create_drive_timed(-400, 4.45)#-450, 3.6
    em.electric_line_motor(250, 0)
    u.move_servo(c.electric_arm_base, c.electric_base_down, 25)
    g.rotate(-90, 200)
    g.drive_condition(u.l_or_r_bumped, -350, False)
    g.create_drive_timed(200, .17)
    #g.create_drive_timed(-250, .7)#.6
    g.rotate(90, 200)
    drive_to_black_and_square_up(-150)
    if burning_MC:
        print ("deliver ambulance to right MC")
        g.rotate(-60, 200)
    else:
        print ("deliver ambulance to left MC")
        g.rotate(30, 200)
    u.wambulance_down()
    u.move_servo(c.ambulance_claw, c.wambulance_open)
    msleep(100)
    wambulance_up()
    if burning_MC:
        g.rotate(60, 200)
    else:
        g.rotate(-30, 200)

def get_water_cube():
    g.create_drive_timed(400, .8)
    g.rotate(-90, 250)
    drive_to_black_and_square_up(250)
    g.create_drive_timed(500, 1.5)
    g.rotate(-85, 250)
    g.drive_condition(u.on_black_left_tophat, -300, False)
    m.drive_to_black_and_square_up(300)
    msleep(10)
    if c.IS_PRIME:
        g.rotate(4, 120)
    else:
        g.rotate(5, 120) #6, 200
    msleep(10)
    if c.IS_PRIME:
        g.create_drive_timed(200, .95)
    else:
        g.create_drive_timed(200, .75)
        g.create_drive_timed(100, .3)
    move_servo(c.sky_arm, c.arm_down, 15)
    msleep(100) # do not remove
    move_servo(c.sky_claw, c.claw_closed_water, 15)
    msleep(100) # do not remoove
    move_servo(c.sky_arm, c.arm_vertical, 10)


def drop_water_cube():
    #Create deposits large water cube on burning building
    g.rotate(70, 300)
    g.create_drive_timed(400, .5)
    g.drive_condition(m.on_black_left_tophat, -250, False)
    g.create_drive_timed(200, .5)
    g.rotate(-90, 200)
    g.create_drive_timed(-400, 1.3)
    g.create_drive_timed(-200, .1)#.2
    g.rotate(-90, 200)
    g.create_drive_timed(400, .65)
    m.drive_to_black_and_square_up(-200)
    if burningSky == 0:
        print("Left")
        if c.IS_CLONE:
            g.rotate(35, 200)
        else:
            g.rotate(35, 200)
        g.create_drive_timed(200, .7)
        move_servo(c.sky_arm, c.arm_low_sky+30, 15)
    elif burningSky == 1:
        print("middle")
        g.create_drive_timed(200, .75)
        g.create_drive_timed(50, .3)
        #g.rotate(-4, 200)
        move_servo(c.sky_arm, c.arm_high_sky_deliver - 15, 15)
    else:
        print("Right")
        if c.IS_PRIME:
            g.rotate(-34, 200)
            g.create_drive_timed(200, .5) #(50,2.5)
            g.create_drive_timed(150, .4)
        elif c.IS_CLONE:
            g.rotate(-42, 200)
            g.create_drive_timed(200, .25)
            g.create_drive_timed(150, .4)
        msleep(100)
        move_servo(c.sky_arm, c.arm_low_sky+30, 15)


def push_cube_test():
    create_connect()
    u.wait_for_button()
    u.move_servo(c.sky_arm, c.arm_vertical)
    u.move_servo(c.sky_claw, c.claw_closed_water)
    g.rotate(-20, 200)
    msleep(100)
    g.rotate(20,200)
    msleep(100)
    u.move_servo(c.sky_arm, c.arm_high_sky_deliver)
    u.DEBUG()


    
