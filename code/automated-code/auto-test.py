
import time
from common_imports import *

kill_app_instance('Dialpad')
open_application('/Applications/Dialpad.app')
verify_application_open('Dialpad')
time.sleep(7)
get_cpu_usage_for_app('Dialpad')
get_memory_usage_for_app('Dialpad')
get_disk_space_for_app('Dialpad')

wait_for_seconds(sec='4')
locate_and_click(image_path='/Users/swapnil/PycharmProjects/CodeLess Automation/code/ui-locators/cta-call-button.png')
click_on_text(text='type a name or number')
write_on_ui(text='9599066811')
wait_for_seconds(sec='1')
press_single_key(key='enter')
wait_for_seconds(sec='5')
locate_and_click(image_path='/Users/swapnil/PycharmProjects/CodeLess Automation/code/ui-locators/new-message.png')
wait_for_seconds(sec='1')
write_on_ui(text='Hello Buddy')
press_single_key(key='enter')