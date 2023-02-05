import RPi.GPIO as GPIO
import time

channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

iter = 0
dia_wheel = 0.3 # diameter in metres

#while True:
    #print(GPIO.input(pin))
    #if GPIO.input(pin):
    #    print("Pin 11 is HIGH")
    #else:
    #    print("Pin 11 is LOW")
    #time.sleep(1)

#def callback(channel):
'''
    if iter == 0:
        print("1 revolution")
        prev_time = time.time()
        iter += 1
    elif iter == 1:
        print("1 revolution")
        curr_time = time.time()
        print(calc_speed(prev_time, curr_time, dia_wheel))
        iter += 1
    else:
        print("1 revolution")
        prev_time = curr_time
        curr_time = time.time()
        print(calc_speed(prev_time, curr_time, dia_wheel))
'''
    #print("1 revolution")
        

#GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime = 300) # 300ms debounce
#GPIO.add_event_callback(channel, callback)


def calc_speed(prev_time, curr_time, dia_wheel):
    """return wheel speed in m/s"""
    return (dia_wheel * 3.14) / (curr_time - prev_time)

def loop():
    iter = 0
    while True:
        #print(GPIO.input(channel))
        #print(prev_time)
        #time.sleep(1)
        #print(time.time())
        if (GPIO.input(channel)):
            if iter == 0:
                print("iter 0, 1 revolution")
                prev_time = time.time()
                iter += 1
            elif iter == 1:
                print("iter 1, 1 revolution")
                curr_time = time.time()
                print(calc_speed(prev_time, curr_time, dia_wheel), "m/s")
                iter += 1
            else:
                print("iter x, 1 revolution")
                prev_time = curr_time
                curr_time = time.time()
                print(calc_speed(prev_time, curr_time, dia_wheel), "m/s")
        time.sleep(0.2)
        
if __name__ == "__main__":
    loop()