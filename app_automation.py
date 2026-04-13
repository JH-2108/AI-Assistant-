import os
import subprocess
import time
import psutil
import pyautogui
import pywinauto
from pathlib import Path
import json
import re
from typing import Dict, List, Optional, Tuple

# =========================
# APP AUTOMATION SYSTEM
# =========================

class AppAutomator:
    def __init__(self):
        self.running_apps = {}
        pyautogui.PAUSE = 0.5
        pyautogui.FAILSAFE = True
        
    def launch_app(self, app_name: str, args: List[str] = None) -> bool:
        """Launch an application by name or path"""
        try:
            app_paths = {
                "fusion360": [
                    r"C:\Program Files\Autodesk\Fusion 360\Fusion360.exe",
                    r"C:\Program Files (x86)\Autodesk\Fusion 360\Fusion360.exe"
                ],
                "netflix": ["chrome", "https://www.netflix.com"],
                "chrome": ["chrome"],
                "firefox": ["firefox"],
                "notepad": ["notepad.exe"],
                "calculator": ["calc.exe"],
                "paint": ["mspaint.exe"],
                "cmd": ["cmd.exe"],
                "explorer": ["explorer.exe"]
            }
            
            app_key = app_name.lower().replace(" ", "")
            
            if app_key in app_paths:
                paths = app_paths[app_key]
                for path in paths:
                    if os.path.exists(path) or path in ["chrome", "firefox", "calc.exe", "notepad.exe", "mspaint.exe", "cmd.exe", "explorer.exe"]:
                        try:
                            if args:
                                subprocess.Popen([path] + args)
                            else:
                                subprocess.Popen([path])
                            time.sleep(2)
                            return True
                        except Exception as e:
                            continue
            return False
        except Exception as e:
            print(f"Error launching {app_name}: {e}")
            return False
    
    def find_window(self, window_title: str) -> Optional:
        """Find a window by title"""
        try:
            from pywinauto.application import Application
            app = Application(backend="uia").connect(title_re=f".*{window_title}.*", timeout=5)
            return app
        except:
            try:
                from pywinauto.application import Application
                app = Application(backend="win32").connect(title_re=f".*{window_title}.*", timeout=5)
                return app
            except:
                return None
    
    def control_fusion360(self, action: str, params: Dict = None) -> str:
        """Control Fusion360 with specific actions"""
        try:
            if not self.is_app_running("Fusion360"):
                if not self.launch_app("fusion360"):
                    return "Failed to launch Fusion360"
                time.sleep(5)
            
            app = self.find_window("Fusion 360")
            if not app:
                return "Could not connect to Fusion360 window"
            
            window = app.window(title_re=".*Fusion 360.*")
            
            if action == "create_sketch":
                # Navigate to Sketch workspace
                window.type_keys("{VK_F1}")  # Design workspace
                time.sleep(1)
                window.type_keys("s")  # Sketch tool
                time.sleep(1)
                window.type_keys("{ENTER}")
                return "Created new sketch in Fusion360"
            
            elif action == "create_box":
                # Create a box sketch
                window.type_keys("r")  # Rectangle tool
                time.sleep(1)
                pyautogui.click(100, 100)  # Click start point
                pyautogui.dragTo(200, 200, duration=0.5)  # Drag to create rectangle
                window.type_keys("{ESC}")
                return "Created box sketch in Fusion360"
            
            elif action == "extrude":
                # Extrude the sketch
                window.type_keys("e")  # Extrude tool
                time.sleep(1)
                pyautogui.click(150, 150)  # Click on sketch
                pyautogui.dragTo(150, 100, duration=0.5)  # Drag up to extrude
                window.type_keys("{ENTER}")
                return "Extruded sketch in Fusion360"
            
            elif action == "save":
                window.type_keys("^s")  # Ctrl+S
                time.sleep(1)
                return "Opened save dialog in Fusion360"
            
            return f"Unknown Fusion360 action: {action}"
            
        except Exception as e:
            return f"Error controlling Fusion360: {str(e)}"
    
    def control_browser(self, action: str, params: Dict = None) -> str:
        """Control browser for Netflix, YouTube, etc."""
        try:
            if action == "open_netflix":
                self.launch_app("chrome", ["https://www.netflix.com"])
                time.sleep(3)
                return "Opened Netflix in Chrome"
            
            elif action == "search_movie":
                movie_name = params.get("movie", "") if params else ""
                if not movie_name:
                    return "Please specify a movie name"
                
                # Open Netflix and search
                self.launch_app("chrome", ["https://www.netflix.com"])
                time.sleep(3)
                
                # Try to find search box and type movie name
                pyautogui.hotkey('ctrl', 'f')
                time.sleep(1)
                pyautogui.typewrite(movie_name)
                pyautogui.press('enter')
                
                return f"Searching for {movie_name} on Netflix"
            
            elif action == "open_youtube":
                video = params.get("video", "") if params else ""
                url = f"https://www.youtube.com/results?search_query={video}" if video else "https://www.youtube.com"
                self.launch_app("chrome", [url])
                return f"Opened YouTube with search: {video}" if video else "Opened YouTube"
            
            return f"Unknown browser action: {action}"
            
        except Exception as e:
            return f"Error controlling browser: {str(e)}"
    
    def is_app_running(self, app_name: str) -> bool:
        """Check if an app is running"""
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if app_name.lower() in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False
    
    def get_running_apps(self) -> List[str]:
        """Get list of running applications"""
        apps = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                apps.append(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return list(set(apps))

# Global automator instance
automator = AppAutomator()

def handle_app_command(command: str) -> str:
    """Parse and handle app automation commands"""
    command = command.lower().strip()
    
    # Fusion360 commands
    if "fusion" in command or "fusion360" in command:
        if "create" in command and ("sketch" in command or "box" in command):
            return automator.control_fusion360("create_box")
        elif "sketch" in command:
            return automator.control_fusion360("create_sketch")
        elif "extrude" in command:
            return automator.control_fusion360("extrude")
        elif "save" in command:
            return automator.control_fusion360("save")
        else:
            return "Fusion360 commands: create sketch, create box, extrude, save"
    
    # Netflix commands
    elif "netflix" in command:
        if "open" in command or "launch" in command:
            return automator.control_browser("open_netflix")
        elif "search" in command or "find" in command:
            # Extract movie name
            movie_match = re.search(r'(?:movie|film|show)\s+(.+)', command)
            movie = movie_match.group(1) if movie_match else ""
            return automator.control_browser("search_movie", {"movie": movie})
        else:
            return "Netflix commands: open netflix, search movie [name]"
    
    # YouTube commands
    elif "youtube" in command:
        video_match = re.search(r'(?:video|song|music)\s+(.+)', command)
        video = video_match.group(1) if video_match else ""
        return automator.control_browser("open_youtube", {"video": video})
    
    # Generic app launch
    else:
        app_match = re.search(r'(?:open|launch|start)\s+(.+)', command)
        if app_match:
            app_name = app_match.group(1).strip()
            if automator.launch_app(app_name):
                return f"Launched {app_name}"
            else:
                return f"Could not launch {app_name}"
    
    return "App automation commands: Fusion360 design, Netflix, YouTube, or 'open [app name]'"
