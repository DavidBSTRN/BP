from pyrplidar import PyRPlidar
import pygame
import time
import button
import os
from math import sin,cos,pi

def first_scan(): #take an area scan and retrun coordinates,then disconnect lidar
        
    lidar = PyRPlidar()
    lidar.connect(port="/dev/ttyUSB0", baudrate=256000  , timeout=3) 
    
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
                                    
        if len(coordinates) == 720:
            break
                    
        

    lidar.stop()
    lidar.set_motor_pwm(0)
    lidar.disconnect()
    return coordinates

if __name__ == "__main__":
    
    # ============pygame init==============
    pygame.init()
    
    #window
    width = 800
    height = 480
    screen = pygame.display.set_mode((width,height))
    
    #colours
    black = (0,0,0)
    white = (255,255,255)
    
    #text
    menu_font = pygame.font.SysFont("dejavuserif", 20)    
    menu_text = menu_font.render("Stiskni pro sken okoli", True, white, black)
    menu_text_rect = menu_text.get_rect()
    menu_text_rect.center = (width//2, height//4)
    
    #buttons
    start_img = pygame.image.load("play-button.bmp").convert_alpha()
    home_img = pygame.image.load("house.bmp").convert_alpha()
    
    start_button = button.Button(360,210,start_img,0.1)
    scan_button = button.Button(740,430,start_img,0.1)
    home_button = button.Button(0,0,home_img,0.1)
    
    ##################################################################
    
    #state
    lets_continue = True
    state = "default"
    
    while lets_continue:
        
        if state == "default":
            screen.fill(black)
            screen.blit(menu_text,menu_text_rect)
            
            if start_button.draw(screen):
                
                default_coordinates = first_scan()
                state = "settings"
                
            pygame.display.update()

        if state == "settings":
            screen.fill(black)
            
            if home_button.draw(screen):
                state = "default"
            
            if scan_button.draw(screen):
                state = "scan"
            
            for x,y in default_coordinates:
                pygame.draw.circle(screen,white,(int((width/2)+x),int((height/2)+y)),1)
                
            pygame.display.update()
            
        if state == "scan":
            
            try:
                lidar = PyRPlidar()
                lidar.connect(port="/dev/ttyUSB0", baudrate=256000  , timeout=3) 
    
                scan_coordinates = []
                                
                lidar.set_motor_pwm(660)
                time.sleep(2)
                                
                scan_generator = lidar.start_scan_express(0)
                                
                for scan in scan_generator():
                    
                    angle = scan.angle
                    distance = scan.distance
                                
                    scale = 15
                                    
                    x = int((distance * cos(angle * pi/180)) / scale)
                    y = int((distance * sin(angle * pi/180)) / scale)
                                    
                    scan_coordinates.append((x,y))
                                    
                    if len(scan_coordinates) == 720:
                        
                        screen.fill(black)
                        home_button.draw(screen)
                        
                        for x,y in scan_coordinates:
                            pygame.draw.circle(screen,white,(int((width/2)+x),int((height/2)+y)),1) 
                            
                        pygame.display.update()
                        scan_coordinates = []
                    
        
            except KeyboardInterrupt:
                
                lidar.stop()
                lidar.set_motor_pwm(0)
                lidar.disconnect()
                state = "default"
            
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lets_continue = False
                

                
    pygame.quit()
