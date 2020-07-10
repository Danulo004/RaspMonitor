# RaspMonitor
Remote controller for smart sauna, using Raspberry Pi and Telegram Bot Api
<hr>
<h2>Description</h2>
Fascinated by the Internet of Things and the idea of creating a smart home, I decided to combine a single-chamber computer Raspberry Pi, and the popular messenger Telegram, namely its HTTPS-requests service to the API Bot. By connecting DS18B20 digital thermometers and switching relays to control the heater to the Raspberry, I organized remote and autonomous sauna control. With many useful features: messaging, management and protection.

<h3>Functions</h3>
<ul>
          <li>Heater on/off</li>
          <li>Heating to the set temperature</li>
          <li>Hysteresis heating, with the ability to specify the width of the hysteresis</li>
          <li>User notification of status and threats</li>
          <li>Providing brief and complete information about the sensors</li>
          <li>Temperature and heater status data stream</li>
        </ul>


<h3>Front-end part</h3>
<p>
Keyboard to simplify working with the bot
Of course, traditional chat bots can be taught to understand human language. But sometimes you want to get some official input from the user - and this is where custom keyboards can be extremely useful.
Each time your bot sends a message, it can send a special keyboard with predefined response settings. Telegram applications that receive messages will display this keyboard to the user. Pressing any button will immediately send the appropriate command. This will dramatically simplify user interaction with your bot.
Here's how it's organized in my bot:
</p>
Example:
<ul>
          <li>"INFO" button - we get all the information about the sensors</li>
          <li>"ON" button - we send a request to turn on the heater</li>
          <li>"OFF" button - we send a request to turn off the heater</li>
          <li>"COMMANDS" button - we will get a list of all available commands</li>
        </ul>


<hr>
<h3>Hardware part</h3>
        <ul>
          <li>Raspberry Pi 3 Model B</li>
          <li>Digital thermometers DS18B20</li>
          <li>Heater</li>
          <li>Display</li>
          <li>Digital encoder</li>
          <li>Logic level converters</li>
        </ul>
        

 

