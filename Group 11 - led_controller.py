import RPi.GPIO as GPIO
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
class LEDController:
    def __init__(self, red_pin, blue_pin, yellow_pin):
        self.red_pin = red_pin
        self.blue_pin = blue_pin
        self.yellow_pin = yellow_pin

        # 设置GPIO模式为BCM或BOARD

        # 设置每个引脚为输出模式
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)
        GPIO.setup(self.yellow_pin, GPIO.OUT)

    def red_on(self):
        GPIO.output(self.red_pin, GPIO.HIGH)

    def red_off(self):
        GPIO.output(self.red_pin, GPIO.LOW)

    def blue_on(self):
        GPIO.output(self.blue_pin, GPIO.HIGH)

    def blue_off(self):
        GPIO.output(self.blue_pin, GPIO.LOW)

    def yellow_on(self):
        GPIO.output(self.yellow_pin, GPIO.HIGH)

    def yellow_off(self):
        GPIO.output(self.yellow_pin, GPIO.LOW)

    def cleanup(self):
        # 清理所有GPIO引脚，关闭所有LED
        GPIO.cleanup()
    def turn_off_all(self):
        # 关闭所有LED，系统进入空闲状态
        self.red_off()
        self.blue_off()
        self.yellow_off()
if __name__ == "__main__":
    
    red_pin = 17
    blue_pin = 27
    yellow_pin = 22
    

    # 创建LED控制器实例
    led_controller = LEDController(red_pin, blue_pin, yellow_pin)
    
    led_controller.turn_off_all()
    #quit()
    try:
        while True:
            led_controller.red_on()
            time.sleep(1)
            led_controller.red_off()
            led_controller.blue_on()
            time.sleep(1)
            led_controller.blue_off()
            led_controller.yellow_on()
            time.sleep(1)
            led_controller.yellow_off()
    except KeyboardInterrupt:
        print("Stopping system.")

    finally:
        # 关闭所有LED和清理GPIO
        led_controller.cleanup()
    
            
            
            

