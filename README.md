
# Weather Forecast Telegram Bot

This Telegram bot provides weather forecast information
based on user-defined locations. It offers various
commands to interact with the bot and retrieve weather
data from tomorrow-io API.

## Commands:

- **/start**: Start the bot.
- **/set_location**: Set your location to enable weather forecast.
- **/current_weather**: Get hourly weather forecast at your location.
- **/weather_forecast**: Get weather forecast for the next 6 days at your location (including today).
- **/help**: List of commands and their descriptions.
- **/custom_forecast**: Custom weather forecast (timesteps, units, and other weather parameters).
- **/history**: History of requests.

## Installation Instructions:

To use this bot, follow these steps:

1. Ensure you have Python version 3.8 or higher installed. You can download Python from [here](https://www.python.org/downloads/).
2. Clone the repository by running the following command in your terminal:

    ```
    git clone https://gitlab.skillbox.ru/ivan_bolshakov/python_basic_diploma.git
    ```

3. Navigate to the project directory and create a virtual environment:

    ```
    cd python_basic_diploma
    python3 -m venv venv
    ```

4. Activate the virtual environment. (Note: Activation command may vary depending on your operating system.)

5. Install the required modules by running:

    ```
    pip install -r requirements.txt
    ```
   
6. Obtain the following tokens:
    - Telegram bot token - You can get it from BotFather in Telegram.
    - RapidAPI token for weather: [RapidAPI](https://rapidapi.com/tomorrow-tomorrow-default/api/tomorrow-io1/)
    - Geoapify token for location: [Geoapify](https://myprojects.geoapify.com/projects)

7. After gathering these tokens, open the `.env` file in the project directory and insert your tokens.
8. Run the `main.py` file:

    ```
    python main.py
    ```

9. Now, you can interact with the bot on Telegram. Start by sending the `/start` command to the bot to initiate the conversation.

Enjoy the weather forecasts provided by the bot! If you encounter any issues, feel free to raise them in the repository or contact the developer.

