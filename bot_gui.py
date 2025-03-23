import time
import pyautogui
import tkinter as tk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import threading
from PIL import ImageTk, Image
import configparser

# Initialize configparser to save and load values
config = configparser.ConfigParser()
config_file = 'config.ini'

# Global variables for the bot state
running = False
last_reacted_message_id = None

# Function to load saved values from config file
def load_config():
    if config.read(config_file):
        channel_link = config.get('Settings', 'channel_link', fallback="")
        driver_path = config.get('Settings', 'driver_path', fallback="")
        reaction = config.get('Settings', 'reaction', fallback="")
        delay = config.getint('Settings', 'delay', fallback=10)
        headless = config.getboolean('Settings', 'headless', fallback=True)
        return channel_link, driver_path, reaction, delay, headless
    return "", "", "", 10, True  # Return default values if no config file exists

# Function to save entered values to config file
def save_config(channel_link, driver_path, reaction, delay, headless):
    if not config.has_section('Settings'):
        config.add_section('Settings')
    config.set('Settings', 'channel_link', channel_link)
    config.set('Settings', 'driver_path', driver_path)
    config.set('Settings', 'reaction', reaction)
    config.set('Settings', 'delay', str(delay))
    config.set('Settings', 'headless', str(headless))

    with open(config_file, 'w') as configfile:
        config.write(configfile)

# Function to start the bot
def start_bot():
    global running
    running = True
    channel_link = channel_entry.get()
    driver_path = driver_path_entry.get()
    reaction = reaction_entry.get()
    delay = int(delay_entry.get())
    headless = headless_var.get()  # Get the state of the headless mode toggle

    if not channel_link or not driver_path or not reaction:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    # Save the config
    save_config(channel_link, driver_path, reaction, delay, headless)

    # Disable the start button to avoid multiple clicks
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)
    # Clear the skip status label initially
    skip_status_label.config(text="")

    # Call the bot thread to run in background
    threading.Thread(target=run_bot, args=(channel_link, driver_path, reaction, delay, headless)).start()

# Function to stop the bot
def stop_bot():
    global running
    running = False
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)

# The bot logic (running in a separate thread)
def run_bot(channel_link, driver_path, reaction, delay, headless):
    global last_reacted_message_id
    try:
        # Configure Chrome
        options = Options()
        options.add_argument("--user-data-dir=C:/Users/cammi/AppData/Local/Google/Chrome/User Data")
        options.add_argument("--profile-directory=Default")  # Uses logged-in Chrome session
        
        # Enable headless mode if the user has selected it
        if headless:
            options.add_argument("--headless")  # Run the browser in headless mode

        # Start Chrome with Selenium
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)

        # Open Discord channel
        driver.get(channel_link)
        time.sleep(10)  # Wait for Discord to fully load

        while running:
            try:
                # Find the latest message
                messages = driver.find_elements(By.CSS_SELECTOR, '[id^="chat-messages-"] div[data-list-item-id]')
                
                if messages:
                    last_message = messages[-1]
                    last_message_id = last_message.get_attribute("data-list-item-id")

                    # Check if we've already reacted to this message
                    if last_message_id == last_reacted_message_id:
                        update_skip_status("Already reacted, skipping...")
                    else:
                        # Right-click on the latest message
                        action = ActionChains(driver)
                        action.context_click(last_message).perform()
                        time.sleep(3)  # Ensure context menu loads

                        # Click "Add Reaction"
                        react_buttons = driver.find_elements(By.XPATH, '//div[contains(text(), "Add Reaction")]')
                        if react_buttons:
                            react_buttons[0].click()
                            time.sleep(3)  # Wait for reaction picker
                        else:
                            log_message("Could not find 'Add Reaction' button!")
                            continue

                        # Locate the emoji search bar (corrected XPATH)
                        emoji_search = driver.find_element(By.XPATH, '//input[@aria-label="Search"]')
                        emoji_search.send_keys(reaction)
                        time.sleep(2)  # Wait for search results

                        # Send the Enter key to confirm the selection
                        emoji_search.send_keys(Keys.RETURN)
                        time.sleep(2)  # Ensure reaction is applied

                        log_message(f"Reacted to message ID: {last_message_id}")
                        last_reacted_message_id = last_message_id  
                else:
                    log_message("No messages found.")
                
                # Wait for the next check
                time.sleep(delay)

            except Exception as e:
                log_message(f"Error: {str(e)}")
                break

        driver.quit()  # Close the browser once the bot stops
    except Exception as e:
        log_message(f"Error initializing bot: {str(e)}")

# Function to update log window
def log_message(message):
    log_output.insert(tk.END, f"{message}\n")
    log_output.yview(tk.END)  # Scroll to the bottom of the log

# Function to update skip status label
def update_skip_status(message):
    skip_status_label.config(text=message)
    skip_status_label.config(fg="gray")  # Set a lighter color to make it less intense

# Function to refresh the UI
def refresh_ui():
    global running
    if running:
        messagebox.showinfo("Info", "The bot is running. Stop it before refreshing.")
    else:
        log_output.delete(1.0, tk.END)  # Clear log output
        skip_status_label.config(text="")  # Clear skip status

# Function to open a file explorer for selecting ChromeDriver
def browse_driver():
    driver_path = filedialog.askopenfilename(
        title="Select ChromeDriver",
        filetypes=[("Executable Files", "*.exe")]
    )
    if driver_path:
        driver_path_entry.delete(0, tk.END)
        driver_path_entry.insert(0, driver_path)

# UI Setup
root = tk.Tk()
root.title("Discord Auto-Reactor Bot")

# Load last saved values
channel_link, driver_path, reaction, delay, headless = load_config()

# Channel Link
tk.Label(root, text="Discord Channel Link:").pack()
channel_entry = tk.Entry(root, width=50)
channel_entry.insert(0, channel_link)  # Set default value from config
channel_entry.pack()

# Driver Path
tk.Label(root, text="Path to ChromeDriver:").pack()
driver_path_entry = tk.Entry(root, width=50)
driver_path_entry.insert(0, driver_path)  # Set default value from config
driver_path_entry.pack()

# Button to browse and select ChromeDriver
browse_button = tk.Button(root, text="Browse", command=browse_driver)
browse_button.pack(pady=5)

# Reaction to Use
tk.Label(root, text="Reaction (e.g., ❤️):").pack()
reaction_entry = tk.Entry(root, width=50)
reaction_entry.insert(0, reaction)  # Set default value from config
reaction_entry.pack()

# Delay between checks
tk.Label(root, text="Delay Between Checks (seconds):").pack()
delay_entry = tk.Entry(root, width=50)
delay_entry.insert(0, str(delay))  # Set default value from config
delay_entry.pack()

# Headless Mode Toggle
headless_var = tk.BooleanVar(value=headless)
headless_checkbox = tk.Checkbutton(root, text="Enable Headless Mode", variable=headless_var)
headless_checkbox.pack(pady=5)

# Buttons
start_button = tk.Button(root, text="Start Bot", command=start_bot)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop Bot", command=stop_bot, state=tk.DISABLED)
stop_button.pack(pady=10)

refresh_button = tk.Button(root, text="Refresh", command=refresh_ui)
refresh_button.pack(pady=10)

# Skip Status Label
skip_status_label = tk.Label(root, text="", font=("Arial", 10, "italic"), fg="gray")
skip_status_label.pack(pady=5)

# Log Output
log_output = tk.Text(root, height=10, width=70)
log_output.pack(pady=10)
log_output.insert(tk.END, "Log Output:\n")

# Start the Tkinter event loop
root.mainloop()
