# RaspMonitor
Remote controller for smart sauna, using Raspberry Pi and Telegram Bot Api
<hr>
<h2>Front-end part</h2>
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
<h2>Hardware part</h2>
        <ul>
          <li>Raspberry Pi 3 Model B</li>
          <li>Digital thermometers DS18B20</li>
          <li>Heater</li>
          <li>Display</li>
          <li>Digital encoder</li>
          <li>Logic level converters</li>
        </ul>
        

 

