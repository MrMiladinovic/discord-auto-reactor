# discord-auto-reactor
A simple and customizable bot for automatically reacting to messages in a Discord channel. This tool allows you to configure a Discord channel link, specify the reaction to use, set delays between checks, and even toggle headless browser mode for better performance.
# Discord Auto-Reactor Bot

## Features

- **Automatic Reactions**: React to the latest messages in a Discord channel.
- **Customizable Reaction**: Specify which emoji to react with.
- **Headless Mode**: Option to run the bot in headless mode (without opening a browser window).
- **Configurable Delays**: Set the delay between checks to control how frequently the bot reacts.
- **Persistent Settings**: The bot remembers your last entered values (channel link, reaction, etc.).
- **Log Output**: View logs and status updates in real-time.

## Requirements

- Python 3.x
- Chrome web browser
- ChromeDriver (compatible with your Chrome version)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/MrMiladinovic/discord-auto-reactor.git
    cd discord-auto-reactor
    ```

2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Download [ChromeDriver](https://sites.google.com/chromium.org/driver/) and make sure it is compatible with your Chrome version.
   [ChromeDriver Links](https://googlechromelabs.github.io/chrome-for-testing/#stable/)

5. Configure your bot:
    - Open the application and input the following:
        - **Discord Channel Link**: The link to the Discord channel you want to target.
        - **Path to ChromeDriver**: Select your ChromeDriver executable.
        - **Reaction Emoji**: The emoji you want the bot to react with (e.g., `❤️`).
        - **Delay Between Checks**: How often the bot checks for new messages in seconds.
        - **Headless Mode**: Option to toggle headless mode for a faster experience. Login with Chrome first to use the existing session / dont use headless on first run in order to log in

## Usage

1. Run the bot:
    - Simply run the Python script to launch the GUI:
    ```bash
    python bot_gui.py
    ```

2. Configure the settings in the user interface, then click **Start Bot** to begin the automation process.

3. If you need to stop the bot, click **Stop Bot**.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! If you'd like to improve the bot, feel free to fork the repository and submit a pull request.

### How to Contribute

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them.
4. Push your branch and create a pull request.

We appreciate your contributions to make this bot better!

## Disclaimer

This tool is intended for educational and personal use only. Use it responsibly and respect Discord's Terms of Service. The authors are not responsible for any misuse or violation of Discord's policies.

## Contact

For any questions or issues, please open an issue on the [GitHub repository](https://github.com/MrMiladinovic/discord-auto-reactor/issues).

---

**Developed by [MrMiladinovic]**
