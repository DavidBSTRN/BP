from pyrplidar import PyRPlidar
import pygame
import time
import os
from math import sin,cos,pi

if __name__ == "__main__":
    
    lidar = PyRPlidar()
    lidar.connect(port="/dev/ttyUSB0", baudrate=256000, timeout=3) 
    
    # pygame init
    pygame.init()
    
    width = 800
    height = 480
    screen = pygame.display.set_mode((width,height))
    
    black = (0,0,0)
    white = (255,255,255)
    red = (255,0,0)
    
    lets_continue = True
    
    while lets_continue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lets_continue = False
            if event.type == pygame.KEYDOWN:
                coordinates = []
                                
                lidar.set_motor_pwm(660)
                time.sleep(2)
                                
                scan_generator = lidar.start_scan_express(0)
                                
                for scan in scan_generator():
                                    
                    angle = scan.angle
                    distance = scan.distance
                                
                    scale = 15
                                    
                    x = int((distance * cos(angle * pi/180)) / scale)
                    y = int((distance * sin(angle * pi/180)) / scale)
                                    
                    coordinates.append((x,y))
                                    
                    if len(coordinates) >= 720:
                
                        screen.fill(black) 
                                                
                        for x,y in coordinates:
                            pygame.draw.circle(screen,white,(int((width/2)+x),int((height/2)+y)),1)
                                        
                        pygame.display.update()
                                    
                        coordinates = []
                        break
                        
                lidar.stop()
                lidar.set_motor_pwm(0)
    
    lidar.disconnect()
                                
    pygame.quit()
