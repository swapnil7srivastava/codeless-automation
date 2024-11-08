import time
import logging
import pyautogui
import pyperclip
import pytesseract
from PIL import ImageGrab, ImageEnhance
import logging
from PIL import ImageGrab
import pytesseract
import pyautogui
import logging
import pytesseract
import pyautogui
from PIL import ImageGrab
import AppKit

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
ostype = 'mac'

def get_screen_resolution():
    """Get the screen resolution based on the operating system."""
    resolution = pyautogui.size()
    logging.info(f"Screen resolution: {resolution}")
    return resolution

scale_factor = 2

def locate_and_click(image_path):
    """Locate an image on the screen and click it with Retina display support.

    Args:
        image_path (str): The path of the image to locate.
    """
    max_retries = 5
    wait_time = 2  # Wait time in seconds between each retry

    for attempt in range(max_retries):
        try:
            logging.info(f"Attempt {attempt + 1} to locate and click on: {image_path} with scale factor {scale_factor}")
            # Locate image
            location = pyautogui.locateOnScreen(image_path, confidence=0.9)  # Adjust confidence if needed
            if location:
                # Scale coordinates for Retina display
                x, y = location.left / scale_factor, location.top / scale_factor
                pyautogui.click(x, y)
                logging.info(f"Clicked on {image_path} at scaled location ({x}, {y})")
                return  # Exit the function if click is successful
            else:
                logging.warning(f"Image {image_path} not found on screen. Retrying in {wait_time} seconds...")

            # Wait before the next attempt
            time.sleep(wait_time)

        except Exception as e:
            logging.error(f"Error in locate_and_click on attempt {attempt + 1}: {str(e)}")

    # If the image was not found after all retries, raise an exception
    error_message = f"Failed to locate and click on image {image_path} after {max_retries} attempts."
    logging.error(error_message)
    raise RuntimeError(error_message)

def wait_for_seconds(sec):
    """Wait for a specified number of seconds.

    Args:
        seconds (int or float): The number of seconds to wait.
    """
    seconds = int(sec)
    if seconds < 0:
        logging.warning("Wait time cannot be negative. Setting to 0.")
        seconds = 0
    logging.info(f"Waiting for {seconds} seconds.")
    time.sleep(seconds)


def click_on_coordinates_in_ui(x, y):
    """Click on specific coordinates in the UI.

    Args:
        x (int): The x-coordinate to click.
        y (int): The y-coordinate to click.
        ostype (str): The operating system type ('windows' or 'mac').
    """
    if not isinstance(x, int) or not isinstance(y, int):
        logging.error("Coordinates must be integers.")
        return

    logging.info(f"Clicking on coordinates: ({x}, {y}) for OS: {ostype}")
    try:
        pyautogui.click(x, y)
        logging.info(f"Clicked at ({x}, {y})")
    except Exception as e:
        logging.error(f"Error in click_on_coordinates_in_ui: {str(e)}")


def write_on_ui(text):
    """Write text on the UI.

    Args:
        text (str): The text to write.
    """
    if not isinstance(text, str):
        logging.error("Text must be a string.")
        return

    logging.info(f"Writing text: {text}")
    try:
        pyautogui.typewrite(text)
        logging.info("Text written successfully.")
    except Exception as e:
        logging.error(f"Error in write_on_ui: {str(e)}")


def write_file_path(file_path):
    """Write a file path on the UI.

    Args:
        file_path (str): The file path to write.
    """
    if not isinstance(file_path, str):
        logging.error("File path must be a string.")
        return

    logging.info(f"Writing file path: {file_path}")
    try:
        pyautogui.typewrite(file_path)
        logging.info("File path written successfully.")
    except Exception as e:
        logging.error(f"Error in write_file_path: {str(e)}")


def zoom_in_ui():
    """Zoom in the UI.

    Args:
        ostype (str): The operating system type ('windows' or 'mac').
    """
    logging.info(f"Zooming in for OS: {ostype}")
    if ostype == 'windows':
        pyautogui.hotkey('ctrl', '+')
    else:
        pyautogui.hotkey('command', '+')


def zoom_out_ui():
    """Zoom out the UI.

    Args:
        ostype (str): The operating system type ('windows' or 'mac').
    """
    logging.info(f"Zooming out for OS: {ostype}")
    if ostype == 'windows':
        pyautogui.hotkey('ctrl', '-')
    else:
        pyautogui.hotkey('command', '-')


def scroll_up_ui(pixels):
    """Scroll up in the UI.

    Args:
        pixels (int): The number of pixels to scroll up.
    """
    logging.info(f"Scrolling up {pixels} pixels.")
    pyautogui.scroll(pixels)


def scroll_down_ui(pixels):
    """Scroll down in the UI.

    Args:
        pixels (int ): The number of pixels to scroll down.
    """
    logging.info(f"Scrolling down {pixels} pixels.")
    pyautogui.scroll(-pixels)


def pressed_key(key):
    """Press a key.

    Args:
        key (str): The key to press.
    """
    if not isinstance(key, str):
        logging.error("Key must be a string.")
        return

    logging.info(f"Pressing key: {key}")
    pyautogui.press(key)


def released_key(key):
    """Release a key.

    Args:
        key (str): The key to release.
    """
    if not isinstance(key, str):
        logging.error("Key must be a string.")
        return

    logging.info(f"Releasing key: {key}")
    pyautogui.release(key)


def read_text_on_screen():
    """Read text on the screen using Tesseract.

    Args:
        ostype (str): The operating system type ('windows' or 'mac').

    Returns:
        str: The text on the screen.
    """
    logging.info("Reading text on the screen.")
    img = ImageGrab.grab()
    text = pytesseract.image_to_string(img)
    logging.info(f"Text on screen: {text}")
    return text

# Uncomment the following line and provide the path if needed
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'  # macOS with Homebrew
# pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'  # Windows

max_retries = 5
wait_time = 1  # Seconds between retries

def get_dpi_scaling_factor():
    return scale_factor

def find_text_on_screen(text):
    """Find the coordinates of specific text on the screen using OCR with Retina display support and image enhancement.

    Args:
        text (str): The text to search for on the screen.

    Returns:
        tuple: Adjusted x, y coordinates of the text center, or (None, None) if not found.
    """
    if not isinstance(text, str):
        logging.error("Text must be a string.")
        return None, None

    dpi_scaling_factor = get_dpi_scaling_factor()

    for attempt in range(max_retries):
        logging.info(f"Attempt {attempt + 1}: Finding text: '{text}' on the screen.")
        try:
            # Capture screen image (potentially at Retina resolution)
            img = ImageGrab.grab()

            # Convert to grayscale and enhance contrast for better OCR accuracy
            img = img.convert("L")  # Convert to grayscale
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2)  # Increase contrast (try different values if needed)

            # Extract OCR data
            text_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

            # Loop through OCR data to locate the text
            for i, word in enumerate(text_data['text']):
                if word.lower() == text.lower():
                    # Get bounding box coordinates of the found word
                    x, y, w, h = (text_data['left'][i], text_data['top'][i],
                                  text_data['width'][i], text_data['height'][i])

                    # Calculate center coordinates of the text box
                    center_x = x + w // 2
                    center_y = y + h // 2

                    # Adjust for DPI scaling to match physical screen resolution
                    adjusted_x = int(center_x / dpi_scaling_factor)
                    adjusted_y = int(center_y / dpi_scaling_factor)

                    logging.info(f"Text '{text}' found at scaled coordinates ({adjusted_x}, {adjusted_y})")
                    return adjusted_x, adjusted_y

            logging.warning(f"Text '{text}' not found on screen. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)  # Wait before retrying

        except Exception as e:
            logging.error(f"Error in find_text_on_screen on attempt {attempt + 1}: {e}")

    # logging.error(f"Failed to find text '{text}' on the screen after {max_retries} attempts.")
    return None, None

def hover_on_text(text):
    """Hover over a specific text on the screen.

    Args:
        text (str): The text to hover over.
        ostype (str): The operating system type ('windows' or 'mac').
    """
    x, y = find_text_on_screen(text)
    if x is not None and y is not None:
        pyautogui.moveTo(x, y)
        logging.info(f"Hovered over text {text} at ({x}, {y})")


def click_on_text(text):
    """Click on a specific text on the screen.

    Args:
        text (str): The text to click.
        ostype (str): The operating system type ('windows' or 'mac').
    """
    x, y = find_text_on_screen(text)
    if x is not None and y is not None:
        pyautogui.click(x, y)
        logging.info(f"Clicked on text {text} at ({x}, {y})")


def right_click_on_text(text):
    """Right-click on a specific text on the screen.

    Args:
        text (str): The text to right-click.
        ostype (str): The operating system type ('windows' or 'mac').
    """
    x, y = find_text_on_screen(text)
    if x is not None and y is not None:
        pyautogui.rightClick(x, y)
        logging.info(f"Right-clicked on text {text} at ({x}, {y})")


def verify_text_on_screen(text):
    """Verify if a specific text is present on the screen.

    Args:
        text (str): The text to verify.
        ostype (str): The operating system type ('windows' or 'mac').

    Returns:
        bool: True if the text is found, False otherwise.
    """
    img = ImageGrab.grab()
    text_on_screen = pytesseract.image_to_string(img)
    if text in text_on_screen:
        logging.info(f"Text {text} found on screen.")
        return True
    else:
        logging.warning(f"Text {text} not found on screen.")
        return False


def double_click_on_text(text):
    """Double-click on a specific text on the screen.

    Args:
        text (str): The text to double-click.
        ostype (str): The operating system type ('windows' or 'mac').
    """
    x, y = find_text_on_screen(text)
    if x is not None and y is not None:
        pyautogui.doubleClick(x, y)
        logging.info(f"Double-clicked on text {text} at ({x}, {y})")


def search_and_open_app(app_name):
    """Search for an application in the start menu or spotlight.

    Args:
        app_name (str): The name of the application to search for.
        ostype (str): The operating system type ('windows' or 'mac').
    """
    if not isinstance(app_name, str):
        logging.error("App name must be a string.")
        return

    logging.info(f"Searching for app: {app_name} for OS: {ostype}")
    if ostype == 'windows':
        pyautogui.press('winleft')
        pyautogui.typewrite(app_name)
        pyautogui.press('enter')
    elif ostype == 'mac':
        pyautogui.hotkey('command', 'space')
        pyautogui.typewrite(app_name)
        pyautogui.press('enter')
    logging.info(f"Searched for app {app_name} successfully.")


def copy_text():
    """Copy text using the clipboard.

    Args:
        ostype (str): The operating system type ('windows' or 'mac').
    """
    logging.info(f"Copying text for OS: {ostype}")
    if ostype == 'windows':
        pyautogui.hotkey('ctrl', 'c')
    else:
        pyautogui.hotkey('command', 'c')
    logging.info("Text copied successfully.")


def paste_text():
    """Paste text using the clipboard.

    Args:
        ostype (str): The operating system type ('windows' or 'mac').
    """
    logging.info(f"Pasting text for OS: {ostype}")
    if ostype == 'windows':
        pyautogui.hotkey('ctrl', 'v')
    else:
        pyautogui.hotkey('command', 'v')
    logging.info("Text pasted successfully.")


def wait_for_image(image_path):
    """Wait for an image to appear on the screen.

    Args:
        image_path (str): The path of the image to wait for.
        ostype (str): The operating system type ('windows' or 'mac').
    """
    logging.info(f"Waiting for image: {image_path} for OS: {ostype}")
    try:
        while True:
            location = pyautogui.locateOnScreen(image_path)
            if location:
                logging.info(f"Image {image_path} found at {location}")
                break
            time.sleep(1)  # Wait for 1 second before checking again
    except Exception as e:
        logging.error(f"Error in wait_for_image: {str(e)}")


def scroll_up_ui(pixels):
    """Scroll up in the UI.

    Args:
        pixels (int): The number of pixels to scroll up.
    """
    logging.info(f"Scrolling up {pixels} pixels.")
    pyautogui.scroll(pixels)

"""
Common Key Names:
Function Keys: f1, f2, f3, ..., f12
Control Keys: ctrl, shift, alt, capslock, esc, tab, backspace, enter, space, delete, insert
Arrow Keys: up, down, left, right
Number Keys: 0, 1, 2, ..., 9
Special Characters: !, ", #, $, %, &, ', (, ), *, +, ,, -, ., /, :, ;, <, =, >, ?, @, [, \, ], ^, _, `, {, |, }, ~
Alphabet Keys: a, b, c, ..., z
Other Keys: numlock, scrolllock, pause, printscreen
"""

def press_single_key(key):
    """Press a single key, log the action, and release it."""
    pyautogui.keyDown(key)  # Press the key
    logging.info(f"Pressed key: {key}")
    pyautogui.keyUp(key)  # Release the key
    logging.info(f"Released key: {key}")

def press_double_key(key1, key2):
    """Press a double key combination, log the action, and release the keys."""
    pyautogui.keyDown(key1)  # Press the first key
    pyautogui.keyDown(key2)  # Press the second key
    logging.info(f"Pressed key combination: {key1} + {key2}")
    pyautogui.keyUp(key2)  # Release the second key
    pyautogui.keyUp(key1)  # Release the first key
    logging.info(f"Released key combination: {key1} + {key2}")

def press_triple_key(key1, key2, key3):
    """Press a triple key combination, log the action, and release the keys."""
    pyautogui.keyDown(key1)  # Press the first key
    pyautogui.keyDown(key2)  # Press the second key
    pyautogui.keyDown(key3)  # Press the third key
    logging.info(f"Pressed key combination: {key1} + {key2} + {key3}")
    pyautogui.keyUp(key3)  # Release the third key
    pyautogui.keyUp(key2)  # Release the second key
    pyautogui.keyUp(key1)  # Release the first key
    logging.info(f"Released key combination: {key1} + {key2} + {key3}")

def press_quadruple_key(key1, key2, key3, key4):
    """Press a quadruple key combination, log the action, and release the keys."""
    pyautogui.keyDown(key1)  # Press the first key
    pyautogui.keyDown(key2)  # Press the second key
    pyautogui.keyDown(key3)  # Press the third key
    pyautogui.keyDown(key4)  # Press the fourth key
    logging.info(f"Pressed key combination: {key1} + {key2} + {key3} + {key4}")
    pyautogui.keyUp(key4)  # Release the fourth key
    pyautogui.keyUp(key3)  # Release the third key
    pyautogui.keyUp(key2)  # Release the second key
    pyautogui.keyUp(key1)  # Release the first key
    logging.info(f"Released key combination: {key1} + {key2} + {key3} + {key4}")

def scroll_down_ui(pixels):
    """Scroll down in the UI.

    Args:
        pixels (int): The number of pixels to scroll down.
    """
    logging.info(f"Scrolling down {pixels} pixels.")
    pyautogui.scroll(-pixels)


def hover_on_coordinates(x, y):
    """Hover over specific coordinates in the UI.

    Args:
        x (int): The x-coordinate to hover.
        y (int): The y-coordinate to hover.
    """
    if not isinstance(x, int) or not isinstance(y, int):
        logging.error("Coordinates must be integers.")
        return

    logging.info(f"Hovering over coordinates: ({x}, {y})")
    pyautogui.moveTo(x, y)
    logging.info(f"Hovered over coordinates: ({x}, {y})")


def drag_and_drop(start_x, start_y, end_x, end_y):
    """Drag and drop from one coordinate to another.

    Args:
        start_x (int): The x-coordinate to start dragging from.
        start_y (int): The y-coordinate to start dragging from.
        end_x (int): The x-coordinate to drop at.
        end_y (int): The y-coordinate to drop at.
    """
    if not (isinstance(start_x, int) and isinstance(start_y, int) and
            isinstance(end_x, int) and isinstance(end_y, int)):
        logging.error("Coordinates must be integers.")
        return

    logging.info(f"Dragging from ({start_x}, {start_y}) to ({end_x}, {end_y})")
    pyautogui.moveTo(start_x, start_y)
    pyautogui.dragTo(end_x, end_y, duration=1)
    logging.info("Drag and drop completed.")


def double_click_on_coordinates(x, y):
    """Double-click on specific coordinates in the UI.

    Args :
        x (int): The x-coordinate to double-click.
        y (int): The y-coordinate to double-click.
    """
    if not isinstance(x, int) or not isinstance(y, int):
        logging.error("Coordinates must be integers.")
        return

    logging.info(f"Double-clicking on coordinates: ({x}, {y})")
    pyautogui.doubleClick(x, y)
    logging.info(f"Double-clicked at ({x}, {y})")


def right_click_on_coordinates(x, y):
    """Right-click on specific coordinates in the UI.

    Args:
        x (int): The x-coordinate to right-click.
        y (int): The y-coordinate to right-click.
    """
    if not isinstance(x, int) or not isinstance(y, int):
        logging.error("Coordinates must be integers.")
        return

    logging.info(f"Right-clicking on coordinates: ({x}, {y})")
    pyautogui.rightClick(x, y)
    logging.info(f"Right-clicked at ({x}, {y})")


def type_text_with_delay(text, delay=0.1):
    """Type text with a delay between each character.

    Args:
        text (str): The text to type.
        delay (float): The delay between each character (default: 0.1 seconds).
    """
    if not isinstance(text, str):
        logging.error("Text must be a string.")
        return

    logging.info(f"Typing text with delay: {text}")
    for char in text:
        pyautogui.typewrite(char)
        time.sleep(delay)
    logging.info("Text typed successfully.")


def wait_for_text_on_screen(text):
    """Wait for specific text to appear on the screen.

    Args:
        text (str): The text to wait for.
        ostype (str): The operating system type ('windows' or 'mac').

    Returns:
        bool: True if the text is found, False otherwise.
    """
    logging.info(f"Waiting for text: {text} on the screen for OS: {ostype}")
    try:
        while True:
            img = ImageGrab.grab()
            text_on_screen = pytesseract.image_to_string(img)
            if text in text_on_screen:
                logging.info(f"Text {text} found on screen.")
                return True
            time.sleep(1)  # Wait for 1 second before checking again
    except Exception as e:
        logging.error(f"Error in wait_for_text_on_screen: {str(e)}")
        return False


def find_and_click_text(text):
    """Find specific text on the screen and click it.

    Args:
        text (str): The text to find and click.
        ostype (str): The operating system type ('windows' or 'mac').
    """
    x, y = find_text_on_screen(text)
    if x is not None and y is not None:
        pyautogui.click(x, y)
        logging.info(f"Clicked on text {text} at ({x}, {y})")


def capture_and_save_screenshot(filename='screenshot.png'):
    """Capture a screenshot and save it to a specified file.

    Args:
        filename (str): The filename to save the screenshot as (default: 'screenshot.png').
    """
    logging.info("Capturing screenshot.")
    img = ImageGrab.grab()
    img.save(filename)
    logging.info(f"Screenshot saved as {filename}.")


def clear_clipboard():
    """Clear the clipboard."""
    logging.info("Clearing clipboard.")
    pyperclip.copy("")  # Set clipboard content to an empty string
    logging.info("Clipboard cleared.")


def get_clipboard_content():
    """Get the current content of the clipboard.

    Returns:
        str: The current clipboard content.
    """
    logging.info("Retrieving clipboard content.")
    content = pyperclip.paste()
    logging.info(f"Clipboard content: {content}")
    return content


if __name__ == "__main__":
    ostype = 'mac'  # or 'mac'
    # # Example usage of automation functions
    # get_screen_resolution()
    # wait_for_seconds(2)
    # wait_for_image("example_image.png")
    # click_on_coordinates_in_ui(200, 300)
    # write_on_ui("Sample text for typing.")
    # type_text_with_delay("Hello with delay!", delay=0.2)
    # capture_and_save_screenshot("my_screenshot.png")
    # clear_clipboard()
    # copy_text(ostype)
    # pasted_content = get_clipboard_content()
    # logging.info(f"Pasted content: {pasted_content}")