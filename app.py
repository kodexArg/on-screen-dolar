# This application initialize mutliple threads:
# 1. A 1st thread that initialize onscreen.py, playing the videos in a loop
# 2. A 2nd thread is a python telegram bot to write src/prices.json

import threading
import onscreen
import bot

