from pyrplidar import PyRPlidar
import pygame
import time
import button
import os
from math import sin,cos,radians
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def one_scan(): #take an area scan and retrun polar coordinates,then disconnect lidar
    #connect lidar a start scan
    lidar = PyRPlidar()
    lidar.connect(port="/dev/ttyUSB0", baudrate=256000  , timeout=3) 
    
    coordinates = []
                                
    lidar.set_motor_pwm(660)
    time.sleep(2)
                                
    scan_generator = lidar.start_scan_express(0)
                                
    for counter,scan in enumerate(scan_generator()):
        
        quality = scan.quality
        angle = scan.angle
        distance = scan.distance
        # fixne na 3 metry - PREDELAT PAK                        
        if distance < 3000 and quality != 0:#dane na 3 metry kvuli testum v pokoji - PREDELAT
            
            new_distance = distance/12.5#240 pixlu je max co se vejde 3000/12.5 = 240 - PREDELAT       
                                    
            coordinates.append((angle,new_distance))

        if counter == 720: 
            #sort coord low to high
            sort_coordinates = sorted(coordinates, key = lambda tup: tup[0])
            break
                    
        
    #stop lidar and return sort coords
    lidar.stop()
    lidar.set_motor_pwm(0)
    lidar.disconnect()
    return sort_coordinates
    
def round_half(coord):
    fi,r = coord
    return (round(fi * 2) / 2, r)

if __name__ == "__main__":
    
    # ============pygame init==============
    pygame.init()
    
    #window
    width = 800
    height = 480
    #screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN)
    screen = pygame.display.set_mode((width,height))
    
    #colours
    black = (0,0,0)
    white = (255,255,255)
    green = (0,255,0)
    red = (255,0,0)
    
    #text default page
    menu_font = pygame.font.SysFont("dejavuserif", 20)    
    menu_text = menu_font.render("Stiskni pro sken okoli", True, white, black)
    menu_text_rect = menu_text.get_rect()
    menu_text_rect.center = (width//2, height//4)
    
    #modes text
    obj_font = pygame.font.SysFont("dejavuserif", 12)    
    obj_text = menu_font.render("Object det.", True, white, black)
    obj_text_rect = menu_text.get_rect()
    obj_text_rect.center = (310, 180)
    
    prsn_font = pygame.font.SysFont("dejavuserif", 12)    
    prsn_text = menu_font.render("Person det.", True, white, black)
    prsn_text_rect = menu_text.get_rect()
    prsn_text_rect.center = (550, 180)
    
    #buttons images
    start_img = pygame.image.load("button-finger.bmp").convert_alpha()
    scan_img = pygame.image.load("play-button.bmp").convert_alpha()
    back_img = pygame.image.load("entry-door.bmp").convert_alpha()
    block_img = pygame.image.load("cancel.bmp").convert_alpha()
    
    #buttons position (top left corner),scale
    start_button = button.Button(360,210,start_img,0.1)
    start_object_det_button = button.Button(230,210,start_img,0.1)
    start_person_det_button = button.Button(470,210,start_img,0.1)
    scan_button = button.Button(740,430,scan_img,0.1)
    back_button = button.Button(0,0,back_img,0.1)
    exit_button = button.Button(740,0,block_img,0.1)
    first_quadrant_button = button.Button(600,360,block_img,0.05)
    second_quadrant_button = button.Button(200,360,block_img,0.05)
    third_quadrant_button = button.Button(200,120,block_img,0.05)
    fourth_quadrant_button = button.Button(600,120,block_img,0.05)
    
    ##################################################################
    
    #state
    lets_continue = True
    state = "default"
    
    #settings - quadrants
    first_quadrant = False
    second_quadrant = False
    third_quadrant = False
    fourth_quadrant = False
    
    #main pygame loop
    while lets_continue:
        if state == "default":
            screen.fill(black)
            screen.blit(menu_text,menu_text_rect)#start txt
            
            if start_button.draw(screen):
                
                default_coordinates = one_scan()
                default_print = [(int(r * cos(radians(fi))),int(r * sin(radians(fi)))) for (fi,r) in default_coordinates]#kartezian cause of print
                
                state = "settings"
            
            if exit_button.draw(screen):
                lets_continue = False
            
            pygame.display.update()

        if state == "settings":
            screen.fill(black)
            
            if back_button.draw(screen):
                state = "default"
                
            if exit_button.draw(screen):
                lets_continue = False                
            
            if scan_button.draw(screen):
                #base coords of area 
                base_coordinates = []
                #start lidar and scan
                lidar = PyRPlidar()
                lidar.connect(port="/dev/ttyUSB0", baudrate=256000  , timeout=3)
                                
                lidar.set_motor_pwm(660)
                time.sleep(2)
                                
                scan_generator = lidar.start_scan_express(0)
                
                for count,scan in enumerate(scan_generator()):
                        
                    base_quality = scan.quality
                    base_angle = scan.angle
                    base_distance = scan.distance
                                    
                    if base_distance < 3000 and base_quality != 0:# 3 metry - PREDELAT
                        
                        new_base_distance = base_distance/12.5 #-PREDELAT
                        #add just points user wants
                        if first_quadrant == False:
                            if 0 <= base_angle <= 90:
                                base_coordinates.append((base_angle,new_base_distance))
                        if second_quadrant == False:
                            if 90 <= base_angle <= 180:
                                base_coordinates.append((base_angle,new_base_distance))
                        if third_quadrant == False:
                            if 180 <= base_angle <= 270:
                                base_coordinates.append((base_angle,new_base_distance))
                        if fourth_quadrant == False:
                            if 270 <= base_angle <= 360:
                                base_coordinates.append((base_angle,new_base_distance))
                    #after 720 iters    
                    if count == 720:
                        break
                base_list = [(x/2,240) for x in range(0,720)]#full angle list
                        #print(base_list)
                base_coordinates = sorted(base_coordinates, key = lambda tup: tup[0])#sorted coords low to high
                base_print = [(int(r * cos(radians(fi))),int(r * sin(radians(fi)))) for (fi,r) in base_coordinates]#kartezians cause of print
                        
                round_coords = [round_half(coord) for coord in base_coordinates]#round coord to the closest half
                        #take list of tuples, do average of R for values with same Fi and create new list with lookes like [(fi1,r1),(fi2,r)...] 
                base_sort_coordinates = []
                prev_fi = None
                sum_r = 0
                num_r = 0
                        
                for fi,r in round_coords:
                    if fi != prev_fi:
                        if prev_fi is not None:
                            average_r = sum_r / num_r
                            base_sort_coordinates.append((prev_fi,average_r))
                                
                        prev_fi = fi
                        sum_r = r
                        num_r = 1
                    else:
                        sum_r += r
                        num_r += 1
                        
                #print(base_sort_coordinates)
                #change dist in tuples with same angle
                diction = dict(base_sort_coordinates)
                for i, dist in enumerate(base_list):
                    if dist[0] in diction:
                        base_list[i] = (dist[0],diction[dist[0]])                        
                #print(base_list)
                        #base distances - MOZNA PREDELAT
                base_distance = [r for (fi,r) in base_list]
                #print(base_distance)
                scan_list = [(x/2,240) for x in range(0,720)]
                #stop scna and go next
                lidar.stop()
                lidar.set_motor_pwm(0)
                lidar.disconnect()
                    
                state = "scan_modes"
            #set quadrants to ignore
            if first_quadrant_button.draw(screen):
                first_quadrant = not first_quadrant
            if second_quadrant_button.draw(screen):
                second_quadrant = not second_quadrant
            if third_quadrant_button.draw(screen):
                third_quadrant = not third_quadrant                
            if fourth_quadrant_button.draw(screen):
                fourth_quadrant = not fourth_quadrant
                                
            for x,y in default_print: 
                pygame.draw.circle(screen,white,(int((width/2)+x),int((height/2)+y)),1)
            #drawing quadrants line white/red - open/block
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

        if state == "scan_modes":#add comms 
        
            screen.fill(black)
            screen.blit(obj_text,obj_text_rect)
            screen.blit(prsn_text,prsn_text_rect)
            
            if start_object_det_button.draw(screen):
                lidar = PyRPlidar()
                lidar.connect(port="/dev/ttyUSB0", baudrate=256000  , timeout=3)
                                
                lidar.set_motor_pwm(660)
                time.sleep(2)
                                
                scan_generator = lidar.start_scan_express(0)
                
                state = "object_scan"
                
            if start_person_det_button.draw(screen):
                state = "person_scan"
                
            if back_button.draw(screen):
                state = "settings"
            
            if exit_button.draw(screen):
                lets_continue = False
            
            pygame.display.update()
            
        if state == "object_scan":
            
            screen.fill(black)
            #scan and adding points to coordintase
            scan_coordinates = []
            
            for count,scan in enumerate(scan_generator()):
                    
                quality = scan.quality
                angle = scan.angle
                distance = scan.distance
                                
                if distance < 3000 and quality != 0:# - !!!!
                    
                    new_distance = distance/12.5  # - !!!
                    
                    if first_quadrant == False:
                        if 0 <= angle <= 90:
                            scan_coordinates.append((angle,new_distance))
                    if second_quadrant == False:
                        if 90 <= angle <= 180:
                            scan_coordinates.append((angle,new_distance))
                    if third_quadrant == False:
                        if 180 <= angle <= 270:
                            scan_coordinates.append((angle,new_distance))
                    if fourth_quadrant == False:
                        if 270 <= angle <= 360:
                            scan_coordinates.append((angle,new_distance))
                            
                if count == 720:
                    break
            #sort        
            sort_scan_coordinates = sorted(scan_coordinates, key = lambda tup: tup[0])
            scan_print = [(int(r * cos(radians(fi))),int(r * sin(radians(fi)))) for (fi,r) in sort_scan_coordinates]

            round_scan_coords = [round_half(coord) for coord in sort_scan_coordinates]
                
            new_scan_coordinates = []
            prev_scan_fi = None
            sum_scan_r = 0
            num_scan_r = 0
                
            for fi,r in round_scan_coords:
                if fi != prev_scan_fi:
                    if prev_scan_fi is not None:
                        average_scan_r = sum_scan_r / num_scan_r
                        new_scan_coordinates.append((prev_scan_fi,average_scan_r))
                    
                    prev_scan_fi = fi
                    sum_scan_r = r
                    num_scan_r = 1
                else:
                    sum_scan_r += r
                    num_scan_r += 1
            
            value_dict = dict(new_scan_coordinates)
            for i, new in enumerate(scan_list):
                if new[0] in value_dict:
                    scan_list[i] = (new[0],value_dict[new[0]])
                            
            new_dist = [r for (fi,r) in scan_list]
        ################################################################################################ 
            dif_count = 0   
            for i in range(len(base_distance)):
                if dif_count == 6:
                    break
                if base_distance[i] - new_dist[i] > 80:
                    dif_count += 1
                else:
                    dif_count = 0
    
            if dif_count == 6:
                for x,y in scan_print:
                    pygame.draw.circle(screen,red,(int((width/2)+x),int((height/2)+y)),1)               
            else:
                for x,y in scan_print:
                    pygame.draw.circle(screen,white,(int((width/2)+x),int((height/2)+y)),1)
        ######################################################################################  
            #EXIT
            if back_button.draw(screen):
                lidar.stop()
                lidar.set_motor_pwm(0)
                lidar.disconnect()
                state = "settings"
                
            if exit_button.draw(screen):
                lidar.stop()
                lidar.set_motor_pwm(0)
                lidar.disconnect()
                lets_continue = False

            pygame.display.update()
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lets_continue = False
                

                
    pygame.quit()
