import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import PhotoImage
import logging
import pyautogui
from PIL import ImageGrab, ImageTk
import io
from datetime import datetime
import os
import time
import subprocess
from pyDefinitions import (locate_and_click, locate_and_right_click, wait_for_seconds,
                           click_on_coordinates_in_ui, write_on_ui, write_file_path,
                           zoom_in_ui, zoom_out_ui, scroll_up_ui, scroll_down_ui,
                           open_folder_in_explorer, pressed_key, released_key,
                           take_screenshot, open_application, close_application,
                           wait_for_image)

# Configure logging
logging.basicConfig(filename='automation.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CodelessAutomationApp:
    def __init__(self, root):
        self.root = root
        self.steps = []
        self.operations = ["Locate and Click", "Wait For Seconds", "Write On UI"]  # Example operations
        self.operation_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        logging.debug("Creating widgets")
        self.operation_var.set(self.operations[0])  # Default value
        tk.Label(self.root, text="Select Operation:").pack()
        self.operation_dropdown = tk.OptionMenu(self.root, self.operation_var, *self.operations)
        self.operation_dropdown.pack()
        logging.debug("Operation dropdown created")

        self.snap_location_button = tk.Button(self.root, text="Snap Coordinates",
                                              command=self.capture_and_display_screenshot)
        self.snap_location_button.pack()
        logging.debug("Snap Coordinates button created")

        tk.Label(self.root, text="Image Name (leave blank for timestamp):").pack()
        self.image_name_entry = tk.Entry(self.root, width=50)
        self.image_name_entry.pack()
        logging.debug("Image Name entry created")

        tk.Label(self.root, text="Text (if applicable):").pack()
        self.text_entry = tk.Entry(self.root, width=50)
        self.text_entry.pack()
        logging.debug("Text entry created")

        # Buttons for Snap Coordinates functionality
        self.enter_time_button = tk.Button(self.root, text="Enter Time", command=self.show_time_entry)
        self.enter_time_button.pack()

        self.time_entry = tk.Entry(self.root, width=50)

        self.enter_text_button = tk.Button(self.root, text="Enter Text", command=self.show_text_entry)
        self.enter_text_button.pack()

        self.text_input_entry = tk.Entry(self.root, width=50)

        self.add_snippet_button = tk.Button(self.root, text="Add Snippet", command=self.show_snippet_entry)
        self.add_snippet_button.pack()

        self.snippet_entry = tk.Entry(self.root, width=50)

        self.add_step_button = tk.Button(self.root, text="+ Add New Step", command=self.add_new_step)
        self.add_step_button.pack()
        logging.debug("Add New Step button created")

        self.step_list = scrolledtext.ScrolledText(self.root, width=60, height=15)
        self.step_list.pack()
        logging.debug("Step list created")

        self.save_button = tk.Button(self.root, text="Save", command=self.save_flow)
        self.save_button.pack(side=tk.LEFT)
        logging.debug("Save button created")

        self.save_run_button = tk.Button(self.root, text="Save and Run", command=self.save_and_run)
        self.save_run_button.pack(side=tk.RIGHT)
        logging.debug("Save and Run button created")

        # Initially hide the additional entry fields
        self.time_entry.pack_forget()
        self.text_input_entry.pack_forget()
        self.snippet_entry.pack_forget()

    def show_time_entry(self):
        """Show the time entry field when the Enter Time button is pressed."""
        self.time_entry.pack()
        self.text_input_entry.pack_forget()
        self.snippet_entry.pack_forget()
        logging.debug("Time entry field displayed.")

    def show_text_entry(self):
        """Show the text entry field when the Enter Text button is pressed."""
        self.text_input_entry.pack()
        self.time_entry.pack_forget()
        self.snippet_entry.pack_forget()
        logging.debug("Text entry field displayed.")

    def show_snippet_entry(self):
        """Show the snippet entry field when the Add Snippet button is pressed."""
        self.snippet_entry.pack()
        self.time_entry.pack_forget()
        self.text_input_entry.pack_forget()
        logging.debug("Snippet entry field displayed.")

    def send_keyboard_combination(self):
        """Simulate the keyboard combination COMMAND+CONTROL+SHIFT+4 using AppleScript."""
        logging.debug("Sending keyboard combination COMMAND+CONTROL+SHIFT+4 using AppleScript")

        # AppleScript to simulate the key presses
        script = '''
                tell application "System Events"
                    key down command
                    key down control
                    key down shift
                    keystroke "4"
                    key up shift
                    key up control
                    key up command
                end tell
                '''
        # Run the AppleScript
        subprocess.run(['osascript', '-e', script])
        # Wait for the user to take the screenshot
        time.sleep(10)  # Adjust this delay if necessary

    def capture_and_display_screenshot(self):
        logging.debug("Capturing screenshot from clipboard")
        self.send_keyboard_combination()  # Trigger the screenshot capture

        # Allow some time for the user to take the screenshot
        time.sleep(1)  # Adjust this delay if necessary

        # Capture the image from the clipboard
        screenshot = ImageGrab.grabclipboard()
        if screenshot is None:
            messagebox.showwarning("Warning",
                                   "No image found in clipboard. Please use COMMAND+CONTROL+SHIFT+4 to capture a part of the screen.")
            return

        # Save screenshot to a specified location
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_name = self.image_name_entry.get().strip() or f"screenshot_{timestamp}.png"
        self.screenshot_path = os.path.join("ui-locators", image_name)

        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.screenshot_path), exist_ok=True)

        # Save the screenshot
        screenshot.save(self.screenshot_path, "PNG")
        logging.debug(f"Screenshot saved as: {self.screenshot_path}")

        # Display a thumbnail of the image
        self.display_thumbnail(screenshot)

    def display_thumbnail(self, image):
        """Display a thumbnail of the captured image."""
        # Convert the image to PhotoImage for display
        image.thumbnail((100, 100))
        photo = ImageTk.PhotoImage(image)

        thumbnail_label = tk.Label(self.root, image=photo)
        thumbnail_label.image = photo  # Keep a reference to avoid garbage collection
        thumbnail_label.pack()

        logging.debug("Thumbnail displayed.")

    def add_new_step(self):
        logging.debug("Adding new step")
        operation = self.operation_var.get()
        if hasattr(self, 'screenshot_path') and self.screenshot_path:
            text = self.text_entry.get()
            time_value = self.time_entry.get()
            snippet = self.snippet_entry.get()

            # Construct the step based on the inputs
            step = f"{operation}('{self.screenshot_path}', '{text}', '{time_value}', '{snippet}')\n"

            self.steps.append(step)
            self.step_list.insert(tk.END, step.strip())
            logging.debug(f"Added step: {step.strip()}")
        else:
            messagebox.showwarning("Warning", "Please capture a screenshot before adding a step.")
            logging.warning("No screenshot captured")

    def save_flow(self):
        logging.debug("Saving flow")
        flow_name = filedialog.asksaveasfilename(defaultextension=".py", initialdir="automated-code")
        if flow_name:
            os.makedirs(os.path.dirname(flow_name), exist_ok=True)
            with open(flow_name, "w") as f:
                f.writelines(self.steps)
            messagebox.showinfo("Success", "Flow saved successfully!")
            logging.debug("Flow saved successfully")

    def save_and_run(self):
        logging.debug("Saving and running flow")
        self.save_flow()
        # Code to run the saved flow
        self.run_steps()

    def run_steps(self):
        for step in self.steps:
            operation, args = self.parse_step(step)
            if operation:
                try:
                    self.execute_operation(operation, *args)
                except Exception as e:
                    logging.error(f"Error executing step {step.strip()}: {e}")
                    messagebox.showerror("Execution Error", f"Error executing step: {str(e)}")

    def parse_step(self, step):
        try:
            operation_name, args = step.split('(', 1)
            operation_name = operation_name.strip()
            args = args.rstrip(')\n').split(', ')
            args = [arg.strip().strip("'") for arg in args]  # Clean up arguments
            operation = self.get_operation_function(operation_name)
            return operation, args
        except Exception as e:
            logging.error(f"Error parsing step {step.strip()}: {e}")
            return None, None

    def get_operation_function(self, operation_name):
        operations_map = {
            "Locate and Click": locate_and_click,
            "Locate and Right Click": locate_and_right_click,
            "Wait For Seconds": wait_for_seconds,
            "Click On Coordinates In UI": click_on_coordinates_in_ui,
            "Write On UI": write_on_ui,
            "Write File Path": write_file_path,
            "Zoom In UI": zoom_in_ui,
            "Zoom Out UI": zoom_out_ui,
            "Scroll Up UI": scroll_up_ui,
            "Scroll Down UI": scroll_down_ui,
            "Open Folder In Explorer": open_folder_in_explorer,
            "Pressed Key": pressed_key,
            "Released Key": released_key,
            "Take Screenshot": take_screenshot,
            "Open Application": open_application,
            "Close Application": close_application,
            "Wait for Image": wait_for_image,
            # Add other operations as needed
        }
        return operations_map.get(operation_name)

    def execute_operation(self, operation, *args):
        logging.info(f"Executing operation: {operation} with arguments: {args}")
        try:
            if operation == locate_and_click:
                locate_and_click(args[0], args[1])  # Assuming args[0] is image_path and args[1] is text
            elif operation == locate_and_right_click:
                locate_and_right_click(args[0], args[1])
            elif operation == "Wait For Seconds":
                time.sleep(float(args[0]))  # Here args[0] is treated as seconds
            elif operation == "Click On Coordinates In UI":
                click_on_coordinates_in_ui(int(args[0]), int(args[1]))
            elif operation == "Write On UI":
                write_on_ui(int(args[0]), int(args[1]), args[2])
            elif operation == "Write File Path":
                write_file_path(int(args[0]), int(args[1]), args[2])
            elif operation == "Zoom In UI":
                zoom_in_ui(int(args[0]), int(args[1]))
            elif operation == "Zoom Out UI":
                zoom_out_ui(int(args[0]), int(args[1]))
            elif operation == "Scroll Up UI":
                scroll_up_ui(int(args[0]))  # Here args[0] is treated as scroll units
            elif operation == "Scroll Down UI":
                scroll_down_ui(int(args[0]))  # Here args[0] is treated as scroll units
            elif operation == "Open Folder In Explorer":
                open_folder_in_explorer(args[0])  # Here args[0] is treated as a folder path
            elif operation == "Pressed Key":
                pressed_key(args[0])  # Here args[0] is treated as a key code
            elif operation == "Released Key":
                released_key(args[0])  # Here args[0] is treated as a key code
            elif operation == "Take Screenshot":
                take_screenshot(args[0])  # Here args[0] is treated as a file path
            elif operation == "Open Application":
                open_application(args[0])  # Here args[0] is treated as the application path
            elif operation == "Close Application":
                close_application(args[0])  # Here args[0] is treated as the application name
            elif operation == "Wait for Image":
                wait_for_image(args[0])  # Here args[0] is treated as the image path
            else:
                logging.error(f"Unknown operation: {operation}")
                raise ValueError(f"Unknown operation: {operation}")
        except Exception as e:
            logging.error(f"Error executing operation {operation}: {e}")
            raise e  # Re-raise the exception for handling in the caller

            # Main application execution block
if __name__ == "__main__":
    logging.debug("Starting application")
    root = tk.Tk()
    app = CodelessAutomationApp(root)
    root.mainloop()
    logging.debug("Application closed")