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

    samplerate = lidar.get_samplerate()
    print("samplerate :", samplerate)
    
    
    
    # pygame init
    pygame.init()
    
    width = 1200
    height = 900
    screen = pygame.display.set_mode((width,height))
    
    blue = (0,0,255)

    clock = pygame.time.Clock()
    
    #main loop
    buffer = []#buffer with x and y coordinates
    
    try:
        lidar.set_motor_pwm(660)
        time.sleep(2)
    
        scan_generator = lidar.start_scan_express(0)
        
        for count,scan in enumerate(scan_generator()):
            
            for event in pygame.event.get():            
                if event.type == pygame.QUIT:
                    print(buffer)
                    raise KeyboardInterrupt
                
            
            if scan.quality != 0:             #ignore low quality data
            
                angle = scan.angle     #degree
                distance = scan.distance    #mm
                
                scale = 10
                
                x = int((distance * cos(angle * pi/180)) / scale)      # x coordinate   
                y = int((distance * sin(angle * pi/180)) / scale)      # y coordinate 
                
                buffer.append((x,y)) #add angle,distance to buffer
                    
                if (count % 720) == 0:
                    
                    screen.fill((255,255,255))          #white background
                    
                    for x,y in buffer:
                        pygame.draw.circle(screen,blue,(int((width/2)+x),int((height/2)+y)),1)    
                    
                    pygame.display.update()
                    buffer = []
                
     
    except KeyboardInterrupt:               # ctrl-c
        
        pygame.quit()
        lidar.stop()
        lidar.set_motor_pwm(0)

        
        lidar.disconnect()
