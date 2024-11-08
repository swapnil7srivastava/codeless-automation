import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import inspect
import logging
import platform
import subprocess
import os
from system_pyDefinitions import *  # Ensure these are your actual modules
from pyDefinitions import *  # Ensure these are your actual modules
import inspect

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define categorized functions (ensure these functions are defined in the imported modules)
automation_functions = {
    "Search & Open Application": search_and_open_app,
    "Write Text in UI": write_on_ui,
    "Find Text on Screen": find_text_on_screen,
    "Hover Over Text": hover_on_text,
    "Click on Text": click_on_text,
    "Right Click on Text": right_click_on_text,
    "Verify Text on Screen": verify_text_on_screen,
    "Double Click on Text": double_click_on_text,
    "Press Single Key": press_single_key,
    "Press Double Keys": press_double_key,
    "Press Triple Keys": press_triple_key,
    "Press Quadruple Keys": press_quadruple_key,
    "Read Text on Screen": read_text_on_screen,
    "Locate and Click Image": locate_and_click,
    "Wait for Seconds": wait_for_seconds,
    "Click Coordinates in UI": click_on_coordinates_in_ui,
    "Write File Path in UI": write_file_path,
    "Zoom In": zoom_in_ui,
    "Zoom Out": zoom_out_ui,
    "Scroll Up": scroll_up_ui,
    "Scroll Down": scroll_down_ui,
    "Keep Pressing a Key": pressed_key,
    "Release Key": released_key,
    "Copy Text": copy_text,
    "Paste Text": paste_text,
    "Wait for Image on Screen": wait_for_image,
    "Hover Over Coordinates": hover_on_coordinates,
    "Get Screen Resolution": get_screen_resolution,
}

system_functions = {
    "Kill Application Instance": kill_app_instance,
    "Get CPU Usage for App": get_cpu_usage_for_app,
    "Get Memory Usage for App": get_memory_usage_for_app,
    "Get Disk Space for App": get_disk_space_for_app,
    "Get Clipboard Image": get_clipboard_image,
    "Copy Image From File": copy_image_from_file_to_clipboard,
    "Get Clipboard Content": get_clipboard_content,
    "Get Volume Level": get_volume_level,
    "Increase Volume": increase_volume,
    "Decrease Volume": decrease_volume,
    "Open Application": open_application,
    "Open Folder": open_folder_in_explorer,
    "Close Application": close_application,
    "Take Screenshot": take_screenshot,
    "Clear Clipboard": clear_clipboard,
    "Move File": move_file,
    "Rename File": rename_file,
    "Delete File": delete_file,
    "Create Folder": create_folder,
    "Minimize Window": minimize_window,
    "Maximize Window": maximize_window,
    "Close Window": close_window,
    "Get CPU Usage": get_cpu_usage,
    "Get Memory Usage": get_memory_usage,
    "Get Disk Space": get_disk_space,
    "Ping Host": ping_host,
    "Get External IP": get_external_ip,
    "Open URL in Browser": open_url_in_browser,
    "Show Desktop Notification": show_desktop_notification,
    "Get Mouse Position": get_mouse_position,
    "Get Screen Brightness": get_screen_brightness,
    "Increase Screen Brightness": increase_screen_brightness,
    "Decrease Screen Brightness": decrease_screen_brightness,
    "Send Email": send_email,
}

# Assuming you have a function that determines the OS type
def get_os_type():
    import platform
    os_type = platform.system().lower()  # Returns 'windows' or 'darwin' for Mac
    return "windows" if os_type == "windows" else "mac"

# Initialize main app window
app = tk.Tk()
app.title("Codeless Automation")
app.geometry("500x350")  # Adjusted size to fit buttons below the text block
app.config(bg="#f0f0f0")

# Apply styles for a modern look
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Helvetica", 10), background="#f0f0f0", foreground="black")
style.configure("TButton", font=("Helvetica", 9, "bold"), background="#8c8c8c", foreground="white", padding=5)
style.map("TButton", background=[("active", "#6f6f6f")])
style.configure("TCombobox", font=("Helvetica", 10), padding=5, width=20)  # Set a thinner width
style.configure("TCheckbutton", font=("Helvetica", 10))

# Frame for radio buttons and dropdown
selection_frame = ttk.Frame(app)
selection_frame.pack(pady=5)

# Create radio buttons for selecting function categories
selected_category = tk.StringVar(value="Automation Functions")
automation_radio = ttk.Radiobutton(selection_frame, text="Automation Functions", variable=selected_category, value="Automation Functions", command=lambda: update_dropdown())
automation_radio.pack(side=tk.LEFT, padx=5, pady=5)

system_tasks_radio = ttk.Radiobutton(selection_frame, text="System Tasks", variable=selected_category, value="System Tasks", command=lambda: update_dropdown())
system_tasks_radio.pack(side=tk.LEFT, padx=5, pady=5)

# Create the dropdown for selecting functions
func_dropdown = ttk.Combobox(app, values=list(automation_functions.keys()), state="readonly", width=20)  # Set a thinner width
func_dropdown.pack(pady=10, padx=5, in_=selection_frame)

# Frame for input fields and button
input_frame = ttk.Frame(app)
input_frame.pack(pady=5, fill="x", anchor="center")

# Text block for displaying selected functions and parameters
text_block_frame = ttk.Frame(app, padding=10)
text_block_frame.pack(fill="both", expand=True)

text_block = scrolledtext.ScrolledText(text_block_frame, wrap=tk.WORD, width=70, height=3)  # Reduced height
text_block.pack(expand=True, fill=tk.BOTH)

# Selected functions list to store function details
selected_functions = []

# Entry references for dynamic fields
entries = {}

# Define the integer validation function
def is_integer(value):
    # Allow empty strings to prevent errors during typing
    if value == "":
        return True
    try:
        int(value)
        return True
    except ValueError:
        return False

# Function to create input fields dynamically in a single line and center-align
def create_input_fields(selected_function):
    # Clear previous input fields
    for widget in input_frame.winfo_children():
        widget.destroy()

    if selected_function is None:
        print("No function selected.")
        return

    parameters = inspect.signature(selected_function).parameters
    entries.clear()  # Clear previous entry references

    # Set consistent width for entries and set max columns per row
    entry_width = 15
    col = 0

    # Calculate total columns needed for center alignment
    total_columns = len(parameters) * 2

    # Place each input field in a single line with center alignment
    for param in parameters.values():
        label_text = f"{param.name} ({param.annotation if param.annotation != inspect._empty else 'Any'}):"
        label = ttk.Label(input_frame, text=label_text)
        label.grid(row=0, column=col, padx=(5, 2), pady=5, sticky="e")

        # Configure input based on parameter type
        if param.annotation == str and "file" in param.name.lower():
            entry = ttk.Button(input_frame, text="Browse File", command=lambda e=param.name: browse_file(e), width=entry_width)
        elif param.annotation == str and "folder" in param.name.lower():
            entry = ttk.Button(input_frame, text="Browse Folder", command=lambda e=param.name: browse_folder(e), width=entry_width)
        elif param.annotation == int:
            entry = ttk.Entry(input_frame, validate="key", validatecommand=(input_frame.register(is_integer), "%P"), width=entry_width)
        elif param.annotation == bool:
            entry = ttk.Checkbutton(input_frame, text=param.name)
            entry.grid(row=0, column=col + 1, padx=(0, 10), pady=5)
            col += 2
            entries[param.name] = entry
            continue
        else:
            entry = ttk.Entry(input_frame, width=entry_width)

        entry.grid(row=0, column=col + 1, padx=(0, 10), pady=5)
        entries[param.name] = entry
        col += 2

    # Configure grid to center-align all columns
    for i in range(total_columns):
        input_frame.grid_columnconfigure(i, weight=1)

# Function for file browsing (updates the entry field with file path)
def browse_file(entry_name):
    file_path = filedialog.askopenfilename()
    if file_path:
        print(f"Selected file path for {entry_name}: {file_path}")

# Function for folder browsing
def browse_folder(entry_name):
    folder_path = filedialog.askdirectory()
    if folder_path:
        print(f"Selected folder path for {entry_name}: {folder_path}")

# Function to enter input and update the text block
def enter_input():
    selected_func_name = func_dropdown.get()  # Get selected function from dropdown
    selected_func = automation_functions.get(
        selected_func_name) if selected_category.get() == "Automation Functions" else system_functions.get(
        selected_func_name)

    # Ensure there's a valid function selected
    if not selected_func:
        return  # Exit if no function is selected

    func_call = f"{selected_func.__name__}("

    # Loop through parameters and gather their input values
    for param_name, entry in entries.items():
        # Check if the parameter is "ostype"
        if param_name == "ostype":
            # Call the get_os_type function to get the OS type
            os_type = get_os_type()
            value = os_type  # Pre-fill the entry with the OS type value

            # If the entry is a tk.Entry, set the value directly
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)  # Clear the current value
                entry.insert(0, value)  # Insert the new value (mac/windows)

        else:
            value = entry.get() if isinstance(entry, tk.Entry) else entry.var.get()  # Get value from entry or Checkbutton

            # If it's an Entry field, you can set its value here too if needed
            if isinstance(entry, tk.Entry):
                entry.delete(0, tk.END)
                entry.insert(0, value)

        func_call += f"{param_name}='{value}', "

    # Remove trailing comma and space, then close the function call
    func_call = func_call.rstrip(", ") + ")"

    # Add the function call to the selected functions list only if it's valid
    if all(entry.get() or isinstance(entry, tk.Checkbutton) for entry in entries.values()):
        selected_functions.append(func_call)

    # Show new input fields for the selected function
    create_input_fields(selected_func)


# Function to add the selected function to the text block
def add_to_text_block():
    selected_func_name = func_dropdown.get()
    selected_func = (
        automation_functions.get(selected_func_name)
        if selected_category.get() == "Automation Functions"
        else system_functions.get(selected_func_name)
    )

    if selected_func:
        func_call = f"{selected_func.__name__}("
        parameters = inspect.signature(selected_func).parameters

        # Loop through parameters to build the function call string
        for param_name, entry in entries.items():
            value = entry.get() if isinstance(entry, tk.Entry) else entry.var.get()
            if not value and isinstance(entry, tk.Entry):
                messagebox.showerror("Input Error", f"Field for '{param_name}' cannot be blank.")
                return  # Exit if any required field is blank
            func_call += f"{param_name}='{value}', "  # Build function call string

        # Format the function call, add to list, and insert into text block
        func_call = func_call.rstrip(", ") + ")"
        selected_functions.append(func_call)  # Directly append the function call

        # Insert formatted function call with scrolling capability
        text_block.insert(tk.END, func_call + "\n")
        text_block.yview(tk.END)  # Scroll to the bottom to show the latest step

        # Display new input fields if required for the next function
        create_input_fields(selected_func)

# Function to save the script
def save_script():
    # Remove the first item if it exists
    if selected_functions:
        selected_functions.pop(0)  # Remove the first item

    script_content = "\n".join(selected_functions)  # Join function calls
    file = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
    if file:
        try:
            with open(file, 'w') as f:
                f.write(script_content)
            logging.info("Script saved successfully.")
        except Exception as e:
            logging.error(f"Error saving script: {e}")
            messagebox.showerror("Save Error", f"Error saving script: {e}")

# The rest of your code remains unchanged...

# Function to execute the script
def execute_script():
    script_content = "\n".join(selected_functions)
    temp_file = "temp_script.py"
    try:
        with open(temp_file, 'w') as f:
            f.write(script_content)
        subprocess.run(["python", temp_file], check=True)
        logging.info("Script executed successfully.")
    except Exception as e:
        logging.error(f"Error executing script: {e}")
        messagebox.showerror("Execution Error", f"Error executing script: {e}")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

# Function to update the dropdown based on the selected category
def update_dropdown():
    if selected_category.get() == "Automation Functions":
        func_dropdown.config(values=list(automation_functions.keys()))
    else:
        func_dropdown.config(values=list(system_functions.keys()))

# Create styles for the buttons
style_default = ttk.Style()
style_default.configure("Default.TButton", background="lightgray", foreground="black", padding=5)

style_light_green = ttk.Style()
style_light_green.configure("LightGreen.TButton", background="lightgreen", foreground="black", padding=5)

# Creating the "Enter Input" button with the default style
btn_enter_input = ttk.Button(app, text="Enter Input", command=enter_input, style="Default.TButton")
btn_enter_input.pack(side=tk.LEFT, padx=10, pady=10)

# Creating the "Add Step" button with the default style
btn_add_step = ttk.Button(app, text="Add Step", command=add_to_text_block, style="Default.TButton")
btn_add_step.pack(side=tk.LEFT, padx=10, pady=10)

# Creating the "Save Script" button with the light green style
btn_save_script = ttk.Button(app, text="Save Script", command=save_script, style="LightGreen.TButton")
btn_save_script.pack(side=tk.RIGHT, padx=10, pady=10)

# Creating the "Save & Execute" button with the light green style
btn_save_execute = ttk.Button(app, text="Save & Execute", command=lambda: [save_script(), execute_script()], style="LightGreen.TButton")
btn_save_execute.pack(side=tk.RIGHT, padx=10, pady=10)

# Create the initial input fields for the first dropdown item
create_input_fields(automation_functions.get(func_dropdown.get()))  # Default automation function selected

# Start the application
app.mainloop()