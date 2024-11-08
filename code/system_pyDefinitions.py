import pyautogui
import pytesseract
import psutil  # For system information
import smtplib  # For email sending
import webbrowser  # For browser automation
import speech_recognition as sr  # For voice commands
from PIL import ImageGrab
import shutil
import pyperclip
from plyer import notification  # For desktop notifications
import os
import logging
import requests  # Ensure to import requests for external IP retrieval
import psutil
import os
import logging
import platform
import psutil
import logging
import time


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
ostype = 'mac'

def open_folder_in_explorer(folder_path):
    """Open a folder in the file explorer."""
    logging.info(f"Opening folder: {folder_path} for OS: {ostype}")
    try:
        if ostype == 'windows':
            os.startfile(folder_path)
        elif ostype == 'mac':
            os.system(f'open "{folder_path}"')
        logging.info("Folder opened successfully.")
    except Exception as e:
        logging.error(f"Error in open_folder_in_explorer: {str(e)}")


def open_application(app_path):
    """Open an application."""
    logging.info(f"Opening application: {app_path} for OS: {ostype}")
    try:
        if ostype == 'windows':
            os.startfile(app_path)
        elif ostype == 'mac':
            os.system(f'open "{app_path}"')
        logging.info("Application opened successfully.")
        # Verify if the application has started successfully
        if verify_application_open(app_path):
            logging.info(f"{app_path} is running successfully.")
        else:
            logging.warning(f"{app_path} did not start properly.")
    except Exception as e:
        logging.error(f"Error in open_application: {str(e)}")

def verify_application_open(app_path):
    """Verify if the application is running."""
    try:
        if ostype == 'windows':
            app_name = os.path.basename(app_path)  # Extract app name from path
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == app_name.lower():
                    return True
        elif ostype == 'mac':
            app_name = os.path.basename(app_path).split('.')[0]  # Extract app name for macOS
            for proc in psutil.process_iter(['name']):
                if app_name.lower() in proc.info['name'].lower():
                    return True
        return False
    except Exception as e:
        logging.error(f"Error in verify_application_open: {str(e)}")
        return False


def close_application(app_name):
    """Close an application."""
    logging.info(f"Closing application: {app_name} for OS: {ostype}")
    try:
        if ostype == 'windows':
            os.system(f'taskkill /im {app_name}.exe')
        elif ostype == 'mac':
            os.system(f'pkill {app_name}')
        logging.info("Application closed successfully.")
    except Exception as e:
        logging.error(f"Error in close_application: {str(e)}")


def kill_app_instance(app_name):
    """Forcefully kill an instance of an application."""
    logging.info(f"Forcefully killing app instance: {app_name} for OS: {ostype}")

    try:
        if ostype == 'windows':
            # Forcefully kill the process on Windows
            os.system(f'taskkill /f /im {app_name}.exe')
        elif ostype == 'mac':
            # Forcefully kill the process on macOS
            os.system(f'pkill -9 "{app_name}"')
        logging.info(f"App instance {app_name} killed successfully.")
    except Exception as e:
        logging.error(f"Error killing app instance {app_name}: {e}")


def take_screenshot(filename='screenshot.png'):
    """Take a screenshot and save it to a file."""
    logging.info("Taking a screenshot.")
    img = ImageGrab.grab()
    img.save(filename)
    logging.info(f"Screenshot saved as {filename}.")


# Clipboard Management Functions
def clear_clipboard():
    """Clear the clipboard."""
    logging.info("Clearing clipboard.")
    pyperclip.copy("")  # Set clipboard content to an empty string
    logging.info("Clipboard cleared.")


def get_clipboard_content():
    """Get the current content of the clipboard."""
    logging.info("Retrieving clipboard content.")
    content = pyperclip.paste()
    logging.info(f"Clipboard content: {content}")
    return content


# File Management Functions
def move_file(source, destination):
    """Move a file from source to destination."""
    logging.info(f"Moving file from {source} to {destination}.")
    try:
        shutil.move(source, destination)
        logging.info("File moved successfully.")
    except Exception as e:
        logging.error(f"Error moving file: {str(e)}")


def rename_file(old_name, new_name):
    """Rename a specified file."""
    logging.info(f"Renaming file from {old_name} to {new_name}.")
    try:
        os.rename(old_name, new_name)
        logging.info("File renamed successfully.")
    except Exception as e:
        logging.error(f"Error renaming file: {str(e)}")


def delete_file(file_path):
    """Delete a specified file."""
    logging.info(f"Deleting file: {file_path}.")
    try:
        os.remove(file_path)
        logging.info("File deleted successfully.")
    except Exception as e:
        logging.error(f"Error deleting file: {str(e)}")


def create_folder(folder_path):
    """Create a new folder at a specified path."""
    logging.info(f"Creating folder: {folder_path}.")
    try:
        os.makedirs(folder_path, exist_ok=True)
        logging.info("Folder created successfully.")
    except Exception as e:
        logging.error(f"Error creating folder: {str(e)}")


# Window Management Functions
def minimize_window():
    """Minimize the current active window."""
    logging.info("Minimizing current window.")
    if os.name == 'nt':  # Windows
        pyautogui.hotkey('win', 'd')  # Show desktop
    else:  # macOS
        pyautogui.hotkey('command', 'm')  # Minimize window


def maximize_window():
    """Maximize the current active window."""
    logging.info("Maximizing current window.")
    if os.name == 'nt':  # Windows
        pyautogui.hotkey('win', 'up')  # Maximize window
    else:  # macOS
        pyautogui.hotkey('control', 'command', 'f')  # Fullscreen


def close_window():
    """Close the current active window."""
    logging.info("Closing current window.")
    if os.name == 'nt':  # Windows
        pyautogui.hotkey('alt', 'f4')  # Close window
    else:  # macOS
        pyautogui.hotkey('command', 'w')  # Close window


# System Information Functions
def get_cpu_usage():
    """Get the current CPU usage percentage."""
    cpu_usage = psutil.cpu_percent(interval=1)
    logging.info(f"Current CPU usage: {cpu_usage}%")
    return cpu_usage


def get_memory_usage():
    """Get current memory usage statistics."""
    memory = psutil.virtual_memory()
    logging.info(f"Memory usage: {memory.percent}% used")
    return memory.percent


def get_disk_space(drive):
    """Check available disk space on a specified drive."""
    disk_usage = psutil.disk_usage(drive)
    logging.info(f"Available space on {drive}: {disk_usage.free / (1024 ** 3):.2f} GB")
    return disk_usage.free


# Network Operations Functions
def ping_host(host):
    """Ping a host to check its availability."""
    logging.info(f"Pinging host: {host}.")
    response = os.system(f"ping -c 1 {host}" if os.name != 'nt' else f"ping -n 1 {host}")
    logging.info(f"Ping response: {response}")
    return response == 0


def get_external_ip():
    """Retrieve the external IP address of the machine."""
    logging.info("Retrieving external IP address.")
    external_ip = requests.get('https://api.ipify.org').text.strip()
    logging.info(f"External IP: {external_ip}")
    return external_ip


# Browser Automation Functions
def open_url_in_browser(url):
    """Open a specific URL in the default web browser."""
    logging.info(f"Opening URL in browser: {url}.")
    webbrowser.open(url)


# Notification System Functions
def show_desktop_notification(title, message):
    """Show a desktop notification using plyer."""
    logging.info(f"Showing desktop notification: {title} - {message}.")
    notification.notify(title=title, message=message, timeout=10)


# Other Functions
def take_screenshot():
    """Take a screenshot and save it to a file."""
    logging.info("Taking screenshot.")
    img = ImageGrab.grab()
    img.save('screenshot.png')


def get_mouse_position():
    """Get the current mouse position."""
    logging.info("Getting mouse position.")
    x, y = pyautogui.position()
    logging.info(f"Mouse position: ({x}, {y})")
    return x, y


def get_screen_resolution():
    """Get the current screen resolution."""
    logging.info("Getting screen resolution.")
    width, height = pyautogui.size()
    logging.info(f"Screen resolution: ({width}, {height})")
    return width, height


def get_clipboard_image():
    """Get the current clipboard image."""
    logging.info("Getting clipboard image.")
    img = ImageGrab.grabclipboard()
    logging.info("Clipboard image retrieved.")
    return img

def copy_image_from_file_to_clipboard(image_path):
    """
    Copies an image to the clipboard.

    Args:
        image_path (str): The file path of the image to be copied.
    """
    try:
        # Ensure the file exists
        if not os.path.exists(image_path):
            logging.error(f"Image file not found at {image_path}")
            return

        # Open the image using Pillow
        image = Image.open(image_path)

        # On Windows, we can use ImageGrab to copy to clipboard (if the platform supports it)
        try:
            image.show()  # This automatically places the image in the clipboard on most platforms
            logging.info(f"Image from {image_path} copied to clipboard.")
        except Exception as e:
            logging.error(f"Failed to copy image to clipboard: {str(e)}")

    except Exception as e:
        logging.error(f"Error: {str(e)}")


def get_screen_brightness():
    """Get the current screen brightness."""
    logging.info("Getting screen brightness.")
    return 50  # Example value


def get_volume_level():
    """Get the current volume level."""
    logging.info("Getting volume level.")
    return 50  # Example value


# Brightness Control Functions
def increase_screen_brightness():
    """Increase the screen brightness using keyboard shortcuts."""
    logging.info("Increasing screen brightness.")
    if os.name == 'nt':  # Windows
        pyautogui.hotkey('fn', 'f2')  # Example for some laptops
    else:  # macOS
        pyautogui.hotkey('brightness_up')  # Adjust if necessary


def decrease_screen_brightness():
    """Decrease the screen brightness using keyboard shortcuts."""
    logging.info("Decreasing screen brightness.")
    if os.name == 'nt':  # Windows
        pyautogui.hotkey('fn', 'f1')  # Example for some laptops
    else:  # macOS
        pyautogui.hotkey('brightness_down')  # Adjust if necessary


# Volume Control Functions
def increase_volume():
    """Increase the system volume using keyboard shortcuts."""
    logging.info("Increasing volume.")
    if os.name == 'nt':  # Windows
        pyautogui.hotkey('volumeup')  # Windows volume up key
    else:  # macOS
        pyautogui.hotkey('volume_up')  # Adjust if necessary


def decrease_volume():
    """Decrease the system volume using keyboard shortcuts."""
    logging.info("Decreasing volume.")
    if os.name == 'nt':  # Windows
        pyautogui.hotkey('volumedown')  # Windows volume down key
    else:  # macOS
        pyautogui.hotkey('volume_down')  # Adjust if necessary


def get_cpu_usage_for_app(app_name):
    """Get the CPU usage percentage for a specific application."""
    logging.info(f"Getting CPU usage for {app_name}.")
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        if proc.info['name'] == app_name:
            # First, we need to call cpu_percent() once to initialize the measurement
            proc.info['cpu_percent']  # This triggers the first calculation, which is usually 0.0%
            time.sleep(2)  # Sleep for 100ms to allow accurate measurement
            cpu_usage = proc.cpu_percent()  # Now we get the actual CPU usage value
            logging.info(f"CPU usage for {app_name}: {cpu_usage}%")
            return cpu_usage
    logging.warning(f"{app_name} not found.")
    return None


def get_memory_usage_for_app(app_name):
    """Get the memory usage for a specific application."""
    logging.info(f"Getting memory usage for {app_name}.")

    # Loop through all processes
    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            # Check if the process name matches
            if proc.info['name'] == app_name:
                # Call memory_info to trigger initial measurement
                proc.memory_info()
                time.sleep(2)  # Sleep for a short period to allow accurate measurement

                # Now get the actual memory usage
                mem_usage = proc.memory_info().rss / (1024 ** 2)  # Convert bytes to MB
                logging.info(f"Memory usage for {app_name}: {mem_usage:.2f} MB")
                return mem_usage
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Handle any exceptions like process termination or permission issues
            continue

    logging.warning(f"{app_name} not found.")
    return None


def get_disk_space_for_app(app_name):
    """Get the disk space usage for a specific application."""
    logging.info(f"Getting disk space usage for {app_name}.")
    total_size = 0
    system_platform = platform.system()

    # Loop through the processes to find the application
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            # Check if process name matches
            if proc.info['name'] == app_name:
                exe_path = proc.info['exe']
                app_dir = os.path.dirname(exe_path)  # Directory of the application
                logging.debug(f"Found {app_name} at {exe_path}")

                # Trigger a file read for disk space usage
                proc.memory_info()  # This triggers disk-related stats
                time.sleep(2)  # Allow system to update stats

                # Now calculate the disk space usage of the application directory
                for dirpath, dirnames, filenames in os.walk(app_dir):
                    for filename in filenames:
                        file_path = os.path.join(dirpath, filename)
                        if os.path.isfile(file_path):
                            total_size += os.path.getsize(file_path)
                            logging.debug(f"File: {file_path}, Size: {os.path.getsize(file_path)} bytes")

                # Add disk space usage for common app data directories
                if system_platform == 'Darwin':  # macOS
                    app_data_dirs = [
                        os.path.expanduser('~/Library/Application Support'),
                        os.path.expanduser('~/Library/Caches'),
                        os.path.expanduser('~/Documents'),
                    ]
                elif system_platform == 'Windows':  # Windows
                    app_data_dirs = [
                        os.path.expanduser('~\\AppData\\Local'),
                        os.path.expanduser('~\\AppData\\Roaming'),
                        os.path.expanduser('~\\Documents'),
                    ]
                else:
                    app_data_dirs = []

                for app_data_dir in app_data_dirs:
                    if os.path.exists(app_data_dir):
                        for dirpath, dirnames, filenames in os.walk(app_data_dir):
                            if app_name.lower() in dirnames or app_name.lower() in filenames:
                                for filename in filenames:
                                    file_path = os.path.join(dirpath, filename)
                                    if os.path.isfile(file_path):
                                        total_size += os.path.getsize(file_path)
                                        logging.debug(
                                            f"File in App Data: {file_path}, Size: {os.path.getsize(file_path)} bytes")

                # Convert bytes to GB or MB based on the size
                if total_size >= 1024 ** 3:  # If size >= 1 GB
                    total_size_gb = total_size / (1024 ** 3)
                    logging.info(f"Disk space used by {app_name}: {total_size_gb:.2f} GB")
                else:  # If size is less than 1 GB, convert to MB
                    total_size_mb = total_size / (1024 ** 2)
                    logging.info(f"Disk space used by {app_name}: {total_size_mb:.2f} MB")

                return total_size  # Return the size in bytes for further processing if needed

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Handle any exceptions like process termination or permission issues
            continue
        except Exception as e:
            logging.error(f"Error calculating disk space for {app_name}: {str(e)}")

    logging.warning(f"{app_name} not found.")
    return None

# Email Sending Function
def send_email(subject, body, to_email, from_email, password, smtp_server='smtp.gmail.com', port=587):
    """Send an email using SMTP.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
        to_email (str): Recipient's email address.
        from_email (str): Sender's email address.
        password (str): Sender's email password.
        smtp_server (str): SMTP server address (default: Gmail).
        port (int): Port number (default: 587 for TLS).
    """
    logging.info(f"Sending email to {to_email} with subject '{subject}'.")
    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(from_email, password)
            message = f'Subject: {subject}\n\n{body}'
            server.sendmail(from_email, to_email, message)  # Corrected this line
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")


# Speech Recognition Function
def recognize_speech_from_mic():
    """Recognize speech from the microphone and return the recognized text.

    Returns:
        str: The recognized text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        logging.info("Listening for speech...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            logging.info(f"Recognized speech: {text}")
            return text
        except sr.UnknownValueError:
            logging.error("Could not understand audio.")
            return None
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Speech Recognition service; {e}")
            return None


# System Information Function
def get_system_info():
    """Get basic system information (CPU, memory, disk usage).

    Returns:
        dict: A dictionary containing CPU, memory, and disk usage.
    """
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    system_info = {
        'CPU Usage': f"{cpu_usage}%",
        'Memory Usage': f"{memory.percent}%",
        'Disk Usage': f"{disk.percent}%"
    }

    logging.info(f"System Information: {system_info}")
    return system_info

if __name__ == "__main__":
    ostype = 'mac'  # or 'mac'
    # get_cpu_usage_for_app('Dialpad')
    # get_memory_usage_for_app('Dialpad')
    # get_disk_space_for_app('Dialpad')
    # kill_app_instance('Dialpad', 'mac')
    # open_application('/Applications/Dialpad.app', 'mac')
    # verify_application_open('Dialpad', 'mac')
    # get_cpu_usage_for_app('Dialpad')
    # get_memory_usage_for_app('Dialpad')
    # get_disk_space_for_app('Dialpad')
