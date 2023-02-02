from pyrplidar import PyRPlidar
import pygame
import time
from math import sin,cos,pi

if __name__ == "__main__":
    
    lidar = PyRPlidar()
    lidar.connect(port="/dev/ttyUSB0", baudrate=256000, timeout=3) 

                  
    info = lidar.get_info()
    print("info :", info)

    health = lidar.get_health()
    print("health :", health)

    lidar.set_motor_pwm(800)
    time.sleep(2)
    
    scan_generator = lidar.start_scan_express(4) #4 stability mode - ultracapsuled data
    
    #GUI
    #############################################################################
    pygame.init()
    
    width = 900
    height = 600
    screen = pygame.display.set_mode((width,height))

    
    
    #main loop
    buffer = [] #data for plotting
    num_plot_points = 1500 #number of plot points
    
    try:
        
        for scan in scan_generator():
            
            angle = scan.angle * pi/180     #radian
            distance = scan.distance    #mm
            
            x = int(distance * cos(angle))      # x coordinate
            y = int(distance * sin(angle))      # y coordinate 
            
            if distance > 0:            #low quality data
                
                buffer.append((x,y)) #add angle,distance to buffer
                
                if len(buffer) > num_plot_points:          #pop out the oldest angle,distance
                    buffer.pop(0) 
                    
            screen.fill((255,255,255))
            
            for x,y in buffer:
                pygame.draw.circle(screen,(0,0,255),(int((width/2)+x),int((height/2)+y)),2)
                
            pygame.display.update()
             
     
    except KeyboardInterrupt:               # ctrl-c
        
        pygame.quit()
        lidar.stop()
        lidar.set_motor_pwm(0)

        
        lidar.disconnect()
