# Exchange Rate Board
This project is a work in progress, and it is a collection of ideas for a Python application that will display the exchange rate of the dollar, blue dollar, Chilean pesos, and euros in relation to the Argentine peso. The board will include an image (which in the future will be a looping video) with the exchange rate changes that are modified on-demand using a Telegram API (probably in the future extended to WhatsApp) in which the user enters the values they want to display on the board and the application, through the Telegram bot, upon receiving the quotes in the established format, changes what is displayed on the TV.

## Project roadmap
1. **A simple Python application to cast a 16:9 image**.
This application will take an image and resize it to 16:9. It will then cast the image to the TV.
Status: Done
ToDo:
- better way to combine marquee with background
- frames should wait for time
- rectangle mate for the marquee
- future: scrapy to play random news?

2. **A service that listens for changes in a JSON file** that contains the value of the dollar, blue dollar, Chilean pesos, and euros, and then somehow casts the values over the background image.
This service will listen for changes in a JSON file that contains the value of the dollar, blue dollar, Chilean pesos, and euros. When the values change, the service will update the background image with the new values.
Status: Done

3. A **Pythonic Telegram bot** that changes the values.
This bot will allow users to change the values in the JSON file using Telegram.
Status: To-do

4. A simple **Python "client" application to change the JSON file** remotely with a tkinter interface.
This application will allow users to change the values in the JSON file remotely. It will have a simple tkinter interface.
Status: To-do

5. **Aesthetical improvements**.
This project will be improved aesthetically. This will include adding a logo, changing the background color, and making other changes to make the project look more professional.
Status: To-do

## Contributing
If you would like to contribute to this project, please feel free to fork the repository and submit a pull request.
