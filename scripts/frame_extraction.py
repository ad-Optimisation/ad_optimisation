# Imports the required library for frame extraction
from typing import Tuple
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from os import path
from subprocess import Popen, call
import pyautogui
import ffmpeg

class CreativeFrameExtractor:
    '''
    Class responsible for Extracting Creative Start and End Frames.
    It requires a chrome webdriver compatible with selenium to be
    installed/included in the run environment path.
    '''
def __init__(self, preview_url: str, 
                 engagement_type: str, 
                 save_location: str = '',
                 browser_edges: Tuple[float, float] = (70, 1039)) -> None:
        
        self.preview_url = preview_url
        self.engagement_type = engagement_type
        self.browser_edges = browser_edges
        self.file_name = '-'.join(preview_url.split('/')[-3:-1])
        self.save_location = save_location
        self.video_name = path.join(self.save_location, self.file_name)
        self.cmd = f"ffmpeg -f gdigrab -draw_mouse 0 -framerate 60 -i desktop -vcodec libx264rgb {self.video_name}.mkv -y"
        