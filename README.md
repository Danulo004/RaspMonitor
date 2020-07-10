# RaspMonitor
Remote controller for smart sauna, using Raspberry Pi and Telegram Bot Api
<hr>
##Hardware part##
• Raspberry Pi 3 Model B
• Digital thermometers DS18B20
• Heater
• Display
• Digital encoder
• Logic level converters
<hr>
##Front-end part
Keyboard to simplify working with the bot
Of course, traditional chat bots can be taught to understand human language. But sometimes you want to get some official input from the user - and this is where custom keyboards can be extremely useful.
Each time your bot sends a message, it can send a special keyboard with predefined response settings. Telegram applications that receive messages will display this keyboard to the user. Pressing any button will immediately send the appropriate command. This will dramatically simplify user interaction with your bot.
Here's how it's organized in my bot:
 
Example:
• "INFO" button - we get all the information about the sensors
• "ON" button - we send a request to turn on the heater
• "OFF" button - we send a request to turn off the heater
• "COMMANDS" button - we will get a list of all available commands
