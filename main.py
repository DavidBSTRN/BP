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
            
            new_distance = distance#/12.5#240 pixlu je max co se vejde 3000/12.5 = 240 - PREDELAT       
                                    
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
    obj_text = menu_font.render("Default", True, white, black)
    obj_text_rect = menu_text.get_rect()
    obj_text_rect.center = (310, 180)
    
    prsn_font = pygame.font.SysFont("dejavuserif", 12)    
    prsn_text = menu_font.render("Cluster", True, white, black)
    prsn_text_rect = menu_text.get_rect()
    prsn_text_rect.center = (550, 180)
    
    #info txt
    info_font = pygame.font.SysFont("dejavuserif", 12) 
       
    dist_text = info_font.render("Distance text info", True, white, black)
    dist_text_rect = dist_text.get_rect()
    dist_text_rect.center = (width//2, height//4)
    
    set_text = info_font.render("Sett text info", True, white, black)
    set_text_rect = set_text.get_rect()
    set_text_rect.center = (width//2, height//4)
        
    #buttons images
    start_img = pygame.image.load("button-finger.bmp").convert_alpha()
    scan_img = pygame.image.load("play-button.bmp").convert_alpha()
    back_img = pygame.image.load("entry-door.bmp").convert_alpha()
    block_img = pygame.image.load("cancel.bmp").convert_alpha()
    info_img = pygame.image.load("info.bmp").convert_alpha()
    
    #buttons position (top left corner),scale
    start_button = button.Button(360,210,start_img,0.1)
    start_object_det_button = button.Button(230,210,start_img,0.1)
    start_person_det_button = button.Button(470,210,start_img,0.1)
    scan_button = button.Button(740,430,scan_img,0.1)
    back_button = button.Button(0,0,back_img,0.1)
    exit_button = button.Button(740,0,block_img,0.1)
    info_button = button.Button(0,420,info_img,0.1)
    
    #settings
    first_quadrant_button = button.Button(560,300,block_img,0.05)
    second_quadrant_button = button.Button(460,400,block_img,0.05)
    third_quadrant_button = button.Button(290,400,block_img,0.05)
    fourth_quadrant_button = button.Button(210,300,block_img,0.05)
    fifth_quadrant_button = button.Button(210,155,block_img,0.05)
    sixth_quadrant_button = button.Button(290,55,block_img,0.05)
    seventh_quadrant_button = button.Button(460,55 ,block_img,0.05)
    eighth_quadrant_button = button.Button(560,155,block_img,0.05)
    #distance
    big_circle_button = button.Button(385,0,block_img,0.05)
    middle_circle_button = button.Button(385,70,block_img,0.05)
    small_circle_button = button.Button(385,150,block_img,0.05)
         
    ##################################################################
    
    #state
    lets_continue = True
    state = "default"
    
    #settings - quadrants
    first_quadrant = False
    second_quadrant = False
    third_quadrant = False
    fourth_quadrant = False
    fifth_quadrant = False
    sixth_quadrant = False
    seventh_quadrant = False
    eighth_quadrant = False
    
    #main pygame loop
    while lets_continue:
        if state == "default":
            screen.fill(black)
            screen.blit(menu_text,menu_text_rect)#start txt
            
            if start_button.draw(screen):
                
                default_coordinates = one_scan()
                
                state = "distance"
            
            if exit_button.draw(screen):
                lets_continue = False 
            
            pygame.display.update()

        if state == "distance":
            screen.fill(black)
            default_print = [(int(r/12.5 * cos(radians(fi))),int(r/12.5 * sin(radians(fi)))) for (fi,r) in default_coordinates]#kartezian cause of print
                
            if big_circle_button.draw(screen):
                print_scale = 3000/240
                dist_scale = 3000
                state = "settings"
            
            if middle_circle_button.draw(screen):
                print_scale = 2000/240
                dist_scale = 2000
                state = "settings"
            
            if small_circle_button.draw(screen):
                print_scale = 1000/240
                dist_scale = 1000
                state = "settings"    
            
            if info_button.draw(screen):
                state = "dist_info"
            
            if back_button.draw(screen):
                state = "default"     
                
            if exit_button.draw(screen):
                lets_continue = False
            
            for x,y in default_print:
                pygame.draw.circle(screen,green,(int((width/2)+x),int((height/2)+y)),1)
            
            pygame.draw.circle(screen,white,(int(width/2),int(height/2)),240,1)
            pygame.draw.circle(screen,white,(int(width/2),int(height/2)),160,1)
            pygame.draw.circle(screen,white,(int(width/2),int(height/2)),80,1)
            
            pygame.display.update()

        if state == "settings":
            screen.fill(black)
            
            default_print = [(int(r/print_scale * cos(radians(fi))),int(r/print_scale * sin(radians(fi)))) for (fi,r) in default_coordinates]
            
            if back_button.draw(screen):
                state = "distance"
            
            if info_button.draw(screen):
                state = "set_info"
                
            if exit_button.draw(screen):
                lets_continue = False                
            
            if scan_button.draw(screen):
                #base coords of area 
                base_coordinates_fix = []
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
                                    
                    if base_distance < dist_scale and base_quality != 0:# 3 metry - PREDELAT
                        
                        new_base_distance = base_distance#/12.5 #-PREDELAT
                        #add just points user wants
                        if first_quadrant == False:
                            if 0 <= base_angle <= 44:
                                base_coordinates_fix.append((base_angle,new_base_distance))
                        if second_quadrant == False:
                            if 45 <= base_angle <= 89:
                                base_coordinates_fix.append((base_angle,new_base_distance))
                        if third_quadrant == False:
                            if 90 <= base_angle <= 134:
                                base_coordinates_fix.append((base_angle,new_base_distance))
                        if fourth_quadrant == False:
                            if 135 <= base_angle <= 179:
                                base_coordinates_fix.append((base_angle,new_base_distance))
                        if fifth_quadrant == False:
                            if 180 <= base_angle <= 224:
                                base_coordinates_fix.append((base_angle,new_base_distance))
                        if sixth_quadrant == False:
                            if 225 <= base_angle <= 269:
                                base_coordinates_fix.append((base_angle,new_base_distance))
                        if seventh_quadrant == False:
                            if 270 <= base_angle <= 314:
                                base_coordinates_fix.append((base_angle,new_base_distance))
                        if eighth_quadrant == False:
                            if 315 <= base_angle <= 359:
                                base_coordinates_fix.append((base_angle,new_base_distance))
                        
                    #after 720 iters    
                    if count == 720:
                        break
                base_list = [(x/2,240) for x in range(0,720)]#full angle list
                        #print(base_list)
                base_coordinates = sorted(base_coordinates_fix, key = lambda tup: tup[0])#sorted coords low to high
                base_print = [(int(r/print_scale * cos(radians(fi))),int(r/print_scale * sin(radians(fi)))) for (fi,r) in base_coordinates]#kartezians cause of print
                        
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
            if fifth_quadrant_button.draw(screen):
                fifth_quadrant = not fifth_quadrant
            if sixth_quadrant_button.draw(screen):
                sixth_quadrant = not sixth_quadrant
            if seventh_quadrant_button.draw(screen):
                seventh_quadrant = not seventh_quadrant
            if eighth_quadrant_button.draw(screen):
                eighth_quadrant = not eighth_quadrant                
                
                                                
            for x,y in default_print: 
                pygame.draw.circle(screen,green,(int((width/2)+x),int((height/2)+y)),1) 
            #drawing quadrants line white/red - open/block
            if first_quadrant:
                pygame.draw.line(screen,red,(400,240),(639,240))
                pygame.draw.line(screen,red,(400,240),(639,478))
            else:
                pygame.draw.line(screen,white,(400,240),(639,240))
                pygame.draw.line(screen,white,(400,240),(639,478))                
                
            if second_quadrant:
                pygame.draw.line(screen,red,(399,241),(638,479))
                pygame.draw.line(screen,red,(399,241),(399,479))
            else:
                pygame.draw.line(screen,white,(399,241),(638,479))
                pygame.draw.line(screen,white,(399,241),(399,479))              
                                                                   
            if third_quadrant:
                pygame.draw.line(screen,red,(398,241),(398,479))
                pygame.draw.line(screen,red,(398,241),(161,479))
            else:
                pygame.draw.line(screen,white,(398,241),(398,479))
                pygame.draw.line(screen,white,(398,241),(161,479))

            if fourth_quadrant:
                pygame.draw.line(screen,red,(397,240),(160,478))
                pygame.draw.line(screen,red,(397,240),(160,240))
            else:     
                pygame.draw.line(screen,white,(397,240),(160,478))
                pygame.draw.line(screen,white,(397,240),(160,240)) 

            if fifth_quadrant:
                pygame.draw.line(screen,red,(397,239),(160,239))
                pygame.draw.line(screen,red,(397,239),(160,1))
            else:                     
                pygame.draw.line(screen,white,(397,239),(160,239))
                pygame.draw.line(screen,white,(397,239),(160,1)) 
                
            if sixth_quadrant:
                pygame.draw.line(screen,red,(398,238),(161,0))
                pygame.draw.line(screen,red,(398,238),(398,0))
            else:                                 
                pygame.draw.line(screen,white,(398,238),(161,0))
                pygame.draw.line(screen,white,(398,238),(398,0))  
                
            if seventh_quadrant:
                pygame.draw.line(screen,red,(399,238),(399,0))
                pygame.draw.line(screen,red,(399,238),(638,0))
            else:                                 
                pygame.draw.line(screen,white,(399,238),(399,0))
                pygame.draw.line(screen,white,(399,238),(638,0))                              
                
            if eighth_quadrant:
                pygame.draw.line(screen,red,(400,239),(639,1))
                pygame.draw.line(screen,red,(400,239),(639,239))
            else:                                 
                pygame.draw.line(screen,white,(400,239),(639,1))
                pygame.draw.line(screen,white,(400,239),(639,239))   
            
            pygame.draw.line(screen,white,(160,0),(160,479))
            pygame.draw.line(screen,white,(639,0),(639,479))
                
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
                
                scan_list = [(x/2,240) for x in range(0,720)]
                
                state = "object_scan"
                
            if start_person_det_button.draw(screen):
                K = np.array(base_coordinates)
                K = StandardScaler().fit_transform(K)
	
                dbscan_b = DBSCAN(eps = 0.35,min_samples = 6)
                labels_b = dbscan_b.fit_predict(K)
                                
                lidar = PyRPlidar()
                lidar.connect(port="/dev/ttyUSB0", baudrate=256000  , timeout=3)
                                
                lidar.set_motor_pwm(660)
                time.sleep(2)
                                
                scan_generator = lidar.start_scan_express(0)
                #print(labels_b) 
                state = "person_scan"
                
            if back_button.draw(screen):
                state = "settings"
            
            if exit_button.draw(screen):
                lets_continue = False
            
            pygame.display.update()
            
        if state == "object_scan":#add comms
            
            screen.fill(black)
            #scan and adding points to coordintase
            scan_coordinates = []
            
            for count,scan in enumerate(scan_generator()):
                    
                quality = scan.quality
                angle = scan.angle
                distance = scan.distance
                                
                if distance < dist_scale and quality != 0:# - !!!!
                    
                    new_distance = distance#/12.5  # - !!!
                                                
                    if first_quadrant == False:
                        if 0 <= angle <= 44:
                            scan_coordinates.append((angle,new_distance))
                    if second_quadrant == False:
                        if 45 <= angle <= 89:
                            scan_coordinates.append((angle,new_distance))
                    if third_quadrant == False:
                        if 90 <= angle <= 134:
                            scan_coordinates.append((angle,new_distance))
                    if fourth_quadrant == False:
                        if 135 <= angle <= 179:
                            scan_coordinates.append((angle,new_distance))
                    if fifth_quadrant == False:
                        if 180 <= angle <= 224:
                            scan_coordinates.append((angle,new_distance))
                    if sixth_quadrant == False:
                        if 225 <= angle <= 269:
                            scan_coordinates.append((angle,new_distance))
                    if seventh_quadrant == False:
                        if 270 <= angle <= 314:
                            scan_coordinates.append((angle,new_distance))
                    if eighth_quadrant == False:
                        if 315 <= angle <= 359:
                            scan_coordinates.append((angle,new_distance))
                            
                if count == 720:
                    break
            #sort        
            sort_scan_coordinates = sorted(scan_coordinates, key = lambda tup: tup[0])
            scan_print = [(int(r/print_scale * cos(radians(fi))),int(r/print_scale * sin(radians(fi)))) for (fi,r) in sort_scan_coordinates]

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
                if base_distance[i] - new_dist[i] > 30:
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
        if state == "person_scan":
            
            screen.fill(black)
            #scan and adding points to coordintase
            cluster_scan = []
            
            for count,scan in enumerate(scan_generator()):
                    
                quality = scan.quality
                angle = scan.angle
                distance = scan.distance
                                
                if distance < dist_scale and quality != 0:# - !!!!
                    
                    new_distance = distance#/12.5  # - !!!
                    
                    if first_quadrant == False:
                        if 0 <= angle <= 44:
                            cluster_scan.append((angle,new_distance))
                    if second_quadrant == False:
                        if 45 <= angle <= 89:
                            cluster_scan.append((angle,new_distance))
                    if third_quadrant == False:
                        if 90 <= angle <= 134:
                            cluster_scan.append((angle,new_distance))
                    if fourth_quadrant == False:
                        if 135 <= angle <= 179:
                            cluster_scan.append((angle,new_distance))
                    if fifth_quadrant == False:
                        if 180 <= angle <= 224:
                            cluster_scan.append((angle,new_distance))
                    if sixth_quadrant == False:
                        if 225 <= angle <= 269:
                            cluster_scan.append((angle,new_distance))
                    if seventh_quadrant == False:
                        if 270 <= angle <= 314:
                            cluster_scan.append((angle,new_distance))
                    if eighth_quadrant == False:
                        if 315 <= angle <= 359:
                            cluster_scan.append((angle,new_distance))
                                                        
                if count == 720:
                    break
            cluster_scan_sort = sorted(cluster_scan, key = lambda tup: tup[0])
            
            cluster_scan_kart = [(int(r * cos(radians(fi))),int(r * sin(radians(fi)))) for (fi,r) in cluster_scan_sort]
            #clustering
            X = np.array(cluster_scan_kart)
            X = StandardScaler().fit_transform(X)
	
            dbscan = DBSCAN(eps = 0.35,min_samples = 6)
            labels = dbscan.fit_predict(X)
            
            cluster_print = [(int(r/print_scale * cos(radians(fi))),int(r/print_scale * sin(radians(fi)))) for (fi,r) in cluster_scan]
            
            for i in range(max(labels)):
                cluster = X[labels == i]
                cluster_size = len(cluster)
                
                if 4 < cluster_size < 10:
                    for x,y in cluster_print: 
                        pygame.draw.circle(screen,red,(int((width/2)+x),int((height/2)+y)),1)                    
                else:
                    for x,y in cluster_print: 
                        pygame.draw.circle(screen,white,(int((width/2)+x),int((height/2)+y)),1)
            
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
        
        if state == "dist_info":
            screen.fill(black)
            screen.blit(dist_text,dist_text_rect)
            
            if info_button.draw(screen):
                state = "distance" 
            
            pygame.display.update()
        
        if state == "set_info":
            screen.fill(black)
            screen.blit(set_text,set_text_rect)
            
            if info_button.draw(screen):
                state = "settings"
            
            pygame.display.update()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lets_continue = False
                

                
    pygame.quit() 
