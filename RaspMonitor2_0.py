import telepot
import telepot.api
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup
from picamera import PiCamera
from gpiozero import LED, Button, DigitalInputDevice
from w1thermsensor import W1ThermSensor
from threading import Thread
from datetime import datetime
from time import sleep
import json
import const
import lcddriver

led = LED(const.LED_PIN)
button = Button(const.BTN_PIN)

encA = DigitalInputDevice(pin=22)
encB = DigitalInputDevice(pin=27)

bot = telepot.Bot(const.TOKEN)


camera = PiCamera()
camera.rotation = 90
camera.resolution = (2592, 1944)

# Global variables
users = []
sensors = {}
avr_temp = 0

heat_flag = False

# Reply Keyboard
keyboard = ReplyKeyboardMarkup(keyboard=[
        ['INFO'],
        ['ON', 'OFF'],
        ['COMMANDS']
    ])


#Classes
class TempTracking (Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        global avr_temp, temperatures
        
        print("Temperature tracking is started")

        # TODO If temp > 110 degrees
        while True:
            sens = W1ThermSensor.get_available_sensors()
            if len(sens) > 0:
                summ = 0
                for i in range(len(sens)):
                    sens[i].get_temperature()
                    sensors[sens[i].id] = temp
                    summ += temp
                avr_temp = summ / len(sensors)
                #print(sensors)
                #print(avr_temp)
            else:
                sendToAllUsers("We couldn't recognize any sensor")
            
            sleep(3)
            
        
class HeatUp (Thread):
    def __init__(self, temp):
        Thread.__init__(self)
        self.temp = temp

    def run(self):
        global avr_temp, heat_flag
        
        sendToAllUsers('The heater is turned ON, heating is started')
        print("Starting heating")
        
        while heat_flag == True and avr_temp < self.temp:
            if led.value == 0:
                led.on()

        led.off()
        print("Finished heating")
        #if heat_flag == True:
        sendToAllUsers('The heater is turned OFF, because the avr_temp = %.2f°C'%avr_temp())
        heat_flag = False




heating_thread = HeatUp(10)


# Secondary functions
def btn_pressed():
    print('btn_pressed')
    
    if led.value == 0:
        led.on()
        sendToAllUsers('BTN was pressed and heater was turned ON!')
    else:
        global heat_flag, hyst_flag
        heat_flag = False
        hyst_flag = False
        led.off()
        sendToAllUsers('BTN was pressed and heater was turned OFF!')

def readJSON():
    with open('users.txt') as json_file:
        global users
        users = json.load(json_file)
        
def writeJSON():
    with open('users.txt', 'w') as outfile:
        json.dump(users, outfile)
        
def getTime():
    now = datetime.now()
    return str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

def getDate():
    now = datetime.now()
    return str(now.day) + "/" + str(now.month) + "/" + str(now.year)

def sendToAllUsers(msg):
    for user in users:
        bot.sendMessage(user, str(msg))





# Main message handeler
def handler(msg):
    global avr_temp, temperatures
    
    print(msg)
    
    chat_id = msg['chat']['id']
    command = msg['text']
    
    print('Received:' + str(command))
    print('Chat:' + str(chat_id))

    #inputs from custom keyboard
    if command.isupper() == True:
        command = '/' + command.lower()

    #account middleware, rejecting or adding access
    if chat_id not in users:
        if command.startswith('/add_access') == True:
            parms = command.split('_')
            if len(parms) > 2:
                password = parms[2]
                if password == 'pass1':
                    users.append(chat_id)
                    writeJSON()
                    bot.sendMessage(chat_id, 'Access alowed')
                else:
                    bot.sendMessage(chat_id, 'An incorrect password')
            else:
                bot.sendMessage(chat_id, 'You don\'t anter a password\nCommand example: /add_access_password')
        else: 
            bot.sendMessage(chat_id, "Access denied")
        return
    

    #PARSING
    if command.startswith('/on') == True:
        parms = command.split('_')
        temp = 90.0
        if len(parms) > 1:
            temp = float(parms[1])
            
        if avr_temp > temp:
            led.off()
            bot.sendMessage(
                chat_id, 'The heater is turned OFF, because the avr_temp is  %.2f°C' % avr_temp())
        else:
            #starting heating thread
            global heat_flag, heating_thread
            heat_flag = True
            heating_thread = HeatUp(temp)
            heating_thread.start()
    elif command == '/off':
        heat_flag = False
        if led.value == 0:
            bot.sendMessage(chat_id, 'The heater is already turned off')
        else:
            led.off()
            bot.sendMessage(chat_id, 'The heater is turned off')
    elif command == '/stream':              #TODO
        pass
    elif command == '/cancel_stream':       #TODO
        pass
    elif command == '/info':
        mes = ""
        if avr_temp != 0:
            mes += 'The average temp = %.2f°C\n' % avr_temp
        else:
            mes += 'Sorry we couldn\'t recognize any temp sensors\n'
        if led.value == 1:
            mes += 'The heater is turned ON'
        else:
            mes += 'The heater is turned OFF'
        bot.sendMessage(chat_id, mes)
    elif command == '/info_a':
        mes = ""
        if len(sensors) > 0:
            for key in sensors.keys():
                mes += "Sensor %s has temp %.2f°C;\n" %(key, sensors[key])
        else:
            mes += 'Sorry we couldn\'t recognize any temp sensors'
            
        mes += 'The average temp = %.2f°C\n' % avr_temp
        
        if led.value == 1:
            mes += '\nThe heater is turned ON'
        else:
            mes += '\nThe heater is turned OFF'

        bot.sendMessage(chat_id, mes)
    elif command == '/photo':
        camera.annotate_text = "Time: " + getTime() + " Date: " + getDate()
        camera.capture('/home/pi/Desktop/image.jpg')
        
        photo = open('/home/pi/Desktop/image.jpg', "rb")
        bot.sendPhoto(646243919, photo)
        print("photo is sent")
    elif command == '/getKeys':
        bot.sendMessage(chat_id, 'Keyboard updated', reply_markup=keyboard)
    else:
        mes = """/photo - make an image
/getKeys - to get a custom keyboard
"""
        bot.sendMessage(chat_id, mes)










# Start from here


#get temperatures
if len(W1ThermSensor.get_available_sensors()) > 0:
    sens = W1ThermSensor.get_available_sensors()
    summ = 0
    for i in range(len(sens)):
        temp = sens[i].get_temperature()
        sensors[sens[i].id] = temp
        summ += temp
        
    avr_temp = summ / len(sensors)
    
    print(sensors)
    print(avr_temp)


readJSON()

temp_tracking = TempTracking()
temp_tracking.start()

button.when_pressed = btn_pressed


#print(bot.getMe())
MessageLoop(bot, handler).run_as_thread()
print("Bot is started")




counter = 0
aState = encA.value
aLastState = encB.value
    
class Encooder (Thread):
    def __init__(self):
        Thread.__init__(self)
        
    def run(self):
        global counter, aState, aLastState
        
        while True:
            aState = encA.value
            if aState != aLastState:
                if encB.value != aState:
                    counter+=1
                else:
                    counter-=1
                print(counter)
            aLastState = aState


encooder = Encooder()
encooder.start()


lcd = lcddriver.lcd()
lcd.lcd_clear()

while True:
    lcd.lcd_display_string("Counter: %d"%counter, 2)
    sleep(.5)
    





