import time
import dht11
from led_controller import LEDController
from temperature_listener import TemperatureListener
from temperature_publisher import TemperaturePublisher
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)



class TemperatureController:
    def __init__(self, led_controller, listener, publisher):
        self.led_controller = led_controller
        self.listener = listener
        self.publisher = publisher
         

    def control_temperature(self, current_temp, set_temp):
        temp_difference =current_temp -set_temp
        
        print("current_temp", current_temp)
        print("set temperature", set_temp)
        print("temp difference",temp_difference)

        if temp_difference <= -1.5:
            self.led_controller.turn_off_all()
            self.led_controller.red_on() 
            print("Heating...")

            while current_temp < set_temp:
                
                current_temp = self.publisher.publish_temperature()
                while current_temp == None or set_temp == None:
                    current_temp = self.publisher.publish_temperature()
                    set_temp = self.listener.target_temp
                print("set temperature", set_temp)
                
                time.sleep(2)  



        elif temp_difference >= 1.5:
            self.led_controller.turn_off_all()
            self.led_controller.blue_on()  
            print("Cooling...")
            while current_temp >  set_temp:
                current_temp = self.publisher.publish_temperature()
                while current_temp == None or set_temp == None:
                    current_temp = self.publisher.publish_temperature()
                    set_temp = self.listener.target_temp
                    
                print("current_temp in cooling", current_temp)    
                print("set temperature", set_temp)
                time.sleep(2)  



        else:
            
            if temp_difference < 1.5 and temp_difference > -1.5:
                self.led_controller.turn_off_all()
                self.led_controller.yellow_on()
                print("Temperature stable within range.")

   

if __name__ == "__main__":
    
    red_pin = 17
    blue_pin = 27
    yellow_pin = 22

    led_controller = LEDController(red_pin, blue_pin, yellow_pin)

    listener = TemperatureListener("broker.hivemq.com", 1883, "home/temperature/setpoint")
    sensor = dht11.DHT11(4)
    publisher = TemperaturePublisher("broker.hivemq.com", 1883, "home/temperature/current", sensor, 4)

    setpoint_temp = listener.get_target_temperature()  
    if setpoint_temp is None:
        setpoint_temp = 22.0  

    controller = TemperatureController(led_controller, listener, publisher)

    listener.start()
    publisher.start()

    try:
        while True:
            current_temp = publisher.current_temp
            set_temp = listener.target_temp

            controller.control_temperature(current_temp, set_temp)


    except KeyboardInterrupt:
        print("Stopping system.")

    finally:
        
        listener.stop()
        publisher.stop()



GPIO.cleanup()