import logging
import time
import math
from cflib.positioning.motion_commander import MotionCommander

def turnRight(mc):
    time.sleep(1)
    mc.turn_right(90)
    time.sleep(1)
    
def linear(mc):
    time.sleep(1)
    mc.forward(1.25, velocity=0.7)
    time.sleep(1)

def arco(mc):
    time.sleep(1)
    mc.turn_right(90)
    mc.circle_left(0.63, velocity=0.5, angle_degrees=180)
    time.sleep(1)

def zigueZague(mc):
    time.sleep(1)
    mc.move_distance(0.35, 0.25, 0, velocity=0.4)
    time.sleep(1)
    mc.move_distance(0.55, -0.5, 0, velocity=0.4)
    time.sleep(1)
    mc.move_distance(0.35, 0.25, 0, velocity=0.4
    time.sleep(1)

def degrau(mc):
    time.sleep(1)
    mc.forward(0.3, velocity=0.5)
    mc.up(0.2)
    time.sleep(1)
    mc.forward(0.3, velocity=0.5)
    mc.down(0.2)
    time.sleep(1)
    mc.forward(0.3, velocity=0.5)
    mc.up(0.2)
    mc.forward(0.35, velocity=0.5)
    time.sleep(1)

def loop(mc):
    time.sleep(1)
    mc.forward(0.75, velocity=0.5)
    time.sleep(1)
    #loop
    velocity = 0.2
    radius_m = 0.2
    angular_velocity = velocity/radius_m
    theta = 0
    t = 0
    reflesh_rate = 0.05
    start_angle = -math.pi/2
    while (theta < (2*math.pi)):
        velocity_x = -angular_velocity*radius_m*math.sin(theta + start_angle)
        velocity_z = angular_velocity*radius_m*math.cos(theta + start_angle)
        mc.start_linear_motion(velocity_x, 0.0, velocity_z)
        t += reflesh_rate
        time.sleep(reflesh_rate)
        theta = angular_velocity*t
    mc.stop()
    #fim do loop
    time.sleep(1)
    mc.forward(0.5, velocity=0.5)

def espiral(mc):
    #parametros
    velocity = 0.2
    velocity_circle = 0.3
    radius_m = 0.15
    distance = 1.25
    angular_velocity = velocity_circle/radius_m
    flight_time = distance/velocity
    theta = 0
    t = 0
    reflesh_rate = 0.05
    start_angle = -math.pi/2

    #inicio da espiral
    while (t < flight_time):
        velocity_y = -angular_velocity*radius_m*math.sin(theta + start_angle)
        velocity_z = angular_velocity*radius_m*math.cos(theta + start_angle)
        mc.start_linear_motion(velocity, velocity_y, velocity_z)
        t += reflesh_rate
        time.sleep(reflesh_rate)
        theta = angular_velocity*t
    voltas_completas = (math.pi*2)*(theta//(math.pi*2))
    theta -= voltas_completas
    mc.stop()

    #termina a ultima rotaçao
    while (theta<math.pi*2):
        velocity_y = -angular_velocity*radius_m*math.sin(theta + start_angle)
        velocity_z = angular_velocity*radius_m*math.cos(theta + start_angle)
        mc.start_linear_motion(0.0, velocity_y, velocity_z)
        t += reflesh_rate
        time.sleep(reflesh_rate)
        theta = angular_velocity*t - voltas_completas
    mc.stop()
