from pyrplidar import PyRPlidar
import time

if __name__ == "__main__":
    
    lidar = PyRPlidar()
    lidar.connect(port="/dev/ttyUSB0", baudrate=256000, timeout=3) 

                  
    info = lidar.get_info()
    print("info :", info)

    health = lidar.get_health()
    print("health :", health)

    lidar.set_motor_pwm(500)
    time.sleep(2)
    
    scan_generator = lidar.start_scan_express(4) #4 stability mode - ultracapsuled data
    
    try:
        
        for count, scan in enumerate(scan_generator()):
            print(count, scan)
        
    except KeyboardInterrupt: # ctrl-C
    
        lidar.stop()
        lidar.set_motor_pwm(0)

    
    lidar.disconnect()
    
