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
    green = (0,255,0)
    red = (255,0,0)
    
    #text
    menu_font = pygame.font.SysFont("dejavuserif", 20)    
    menu_text = menu_font.render("Stiskni pro sken okoli", True, white, black)
    menu_text_rect = menu_text.get_rect()
    menu_text_rect.center = (width//2, height//4)
    
    set_font = pygame.font.SysFont("dejavuserif", 12)    
    set_text = set_font.render("0°", True, green, black)
    set_text_rect = set_text.get_rect()
    set_text_rect.center = (793,235)
    
    #buttons
    start_img = pygame.image.load("button-finger.bmp").convert_alpha()
    scan_img = pygame.image.load("play-button.bmp").convert_alpha()
    back_img = pygame.image.load("entry-door.bmp").convert_alpha()
    block_img = pygame.image.load("cancel.bmp").convert_alpha()
    
    start_button = button.Button(360,210,start_img,0.1)
    scan_button = button.Button(740,430,scan_img,0.1)
    back_button = button.Button(0,0,back_img,0.1)
    first_quadrant_button = button.Button(600,360,block_img,0.05)
    second_quadrant_button = button.Button(200,360,block_img,0.05)
    third_quadrant_button = button.Button(200,120,block_img,0.05)
    fourth_quadrant_button = button.Button(600,120,block_img,0.05)
    
    ##################################################################
    
    #state
    lets_continue = True
    state = "default"
    
    #quadrants
    first_quadrant = False
    second_quadrant = False
    third_quadrant = False
    fourth_quadrant = False
    
    
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
            
            if back_button.draw(screen):
                state = "default"
            
            if scan_button.draw(screen):
                lidar = PyRPlidar()
                lidar.connect(port="/dev/ttyUSB0", baudrate=256000  , timeout=3)
                                
                lidar.set_motor_pwm(660)
                time.sleep(2)
                                
                scan_generator = lidar.start_scan_express(0)
                state = "scan"
            
            if first_quadrant_button.draw(screen):
                first_quadrant = not first_quadrant
            if second_quadrant_button.draw(screen):
                second_quadrant = not second_quadrant
            if third_quadrant_button.draw(screen):
                third_quadrant = not third_quadrant                
            if fourth_quadrant_button.draw(screen):
                fourth_quadrant = not fourth_quadrant
                                
            for x,y in default_coordinates:
                pygame.draw.circle(screen,white,(int((width/2)+x),int((height/2)+y)),1)
            
            #screen.blit(set_text,set_text_rect)

            if first_quadrant:
                pygame.draw.line(screen,red,(400,240),(799,240))
                pygame.draw.line(screen,red,(400,240),(400,479))
            else:
                pygame.draw.line(screen,white,(400,240),(799,240))
                pygame.draw.line(screen,white,(400,240),(400,479))                
                
            if second_quadrant:
                pygame.draw.line(screen,red,(0,240),(399,240))
                pygame.draw.line(screen,red,(399,240),(399,479))
            else:
                pygame.draw.line(screen,white,(0,240),(399,240))
                pygame.draw.line(screen,white,(399,240),(399,479)) 
                
            if third_quadrant:
                pygame.draw.line(screen,red,(0,239),(399,239))
                pygame.draw.line(screen,red,(399,239),(399,0))
            else:
                pygame.draw.line(screen,white,(0,239),(399,239))
                pygame.draw.line(screen,white,(399,239),(399,0)) 
                
            if fourth_quadrant:
                pygame.draw.line(screen,red,(400,0),(400,239))
                pygame.draw.line(screen,red,(400,239),(799,239))
            else:
                pygame.draw.line(screen,white,(400,0),(400,239))
                pygame.draw.line(screen,white,(400,239),(799,239))  
                                                                             
            pygame.display.update()
            
            
        if state == "scan":
            
            screen.fill(black)
            
            scan_coordinates = []
                
            for count,scan in enumerate(scan_generator()):
                    
                angle = scan.angle
                distance = scan.distance
                                
                scale = 15
                                    
                x = int((distance * cos(angle * pi/180)) / scale)
                y = int((distance * sin(angle * pi/180)) / scale)
                
                if first_quadrant == False:
                    if 0 <= angle <= 90:
                        scan_coordinates.append((x,y))
                if second_quadrant == False:
                    if 90 <= angle <= 180:
                        scan_coordinates.append((x,y))
                if third_quadrant == False:
                    if 180 <= angle <= 270:
                        scan_coordinates.append((x,y))
                if fourth_quadrant == False:
                    if 270 <= angle <= 360:
                        scan_coordinates.append((x,y))
                    
                if count == 720:
                    break
                    
            for x,y in scan_coordinates:
                pygame.draw.circle(screen,white,(int((width/2)+x),int((height/2)+y)),1) 
            
            if back_button.draw(screen):
                lidar.stop()
                lidar.set_motor_pwm(0)
                lidar.disconnect()
                state = "settings"
                
            pygame.display.update()
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lets_continue = False
                

                
    pygame.quit()
