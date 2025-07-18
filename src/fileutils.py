import os
import json
import hashlib
from datetime import datetime

# Path to config file
CONFIG_PATH = r"C:/Program Files/Integrixa/config/sentinel_config.json"
#CONFIG_PATH = "C:/Users/Jeevan/Desktop/Integrixa/config/sentinel_config.json"

# Default skeleton for initial config file creation
SKELETON = {
    "userid": "",
    "password": "", 
    "bot_id": "",
    "chat_id": "",
    "log_start_time": "",
    "last_monitor_time": "",
    "daemon_status":"stop"
}

# Default salt for password hashing (for consistent, reversible comparison)
DEFAULT_SALT = "safesentinelSalt2025"   #change this salt

# This function ensure config file exists with skeleton
# and also ensures the sentinel_config.json file exists. If not, creates it using the default skeleton.
def initializeConfig():
    try:
        config_dir = os.path.dirname(CONFIG_PATH)
        os.makedirs(config_dir, exist_ok=True)     # Ensure config directory exists and if file dont present then creat the file and write it down.
        
        with open(CONFIG_PATH, "w") as file:
            json.dump(SKELETON, file, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to initialize config file: {e}")


#The function reads the configuration from sentinel_config.json. Returns the config as a dictionary. Falls back to SKELETON if file is unreadable or corrupted.
def readConfig():
    try:
        with open(CONFIG_PATH, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("[ERROR] Config file is corrupted. Resetting to default.")
        writeConfig(SKELETON)
    except Exception as e:
        print(f"[ERROR] Failed to read config file: {e}")

# This function overwrite the config file with provided dictionary
def writeConfig(data: dict):
    with open(CONFIG_PATH, "w") as file:
        json.dump(data, file, indent=2)

#Password Handling
#This function hashes the provided password using SHA-256 and a default salt. Returns the hashed string.
def hashPassword(password: str) -> str:
    salted = DEFAULT_SALT + password
    return hashlib.sha256(salted.encode()).hexdigest()

#This function updates the 'password' field in sentinel_config.json. Takes an already hashed password string. Returns True if successful, False on failure.
def updatePassword(password: str) -> bool:
    try:
        hashed_password= hashPassword(password)
        config = readConfig()
        config["password"] = hashed_password
        writeConfig(config)
        return True
    except:
        return False

#This function reads and returns the hashed password from config.
def readPassword() -> str:
    config = readConfig()
    return config.get("password", "")

#User ID Handling
#This function updates the 'userid' field in the config file. Returns True if successful, False on failure.
def updateUserID(userId: str) -> bool:
    try:
        config = readConfig()
        config["userid"] = userId
        writeConfig(config)
        return True
    except:
        return False

#This function reads and returns the 'userid' from config.
def readUserID() -> str:
    config = readConfig()
    return config.get("userid", "")


# Telegram Configuration
#This function sets or updates the Telegram bot ID and chat ID in the config file. Returns True if successful, False on failure.
def setTelegramId(botId: str, chatId: str) -> bool:
    try:
        config = readConfig()
        config["bot_id"] = botId
        config["chat_id"] = chatId
        writeConfig(config)
        return True
    except:
        return False
    
#This function fetches the Telegram bot ID and chat ID from the config file. Returns a dictionary
def getTelegramId() -> dict:
    config = readConfig()
    return {
        "bot_id": config.get("bot_id", ""),
        "chat_id": config.get("chat_id", "")
    }


# Log Time Handling
#This function current time in format of YYYY-MM-DD HH:MM:SS
def getCurrentTime() ->str:
   return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#This function reads and returns the log_start_time from the config file
def readTimeLogger() :
    config = readConfig()
    print(config)
    return config.get("log_start_time", "")

#This function updates the log_start_time field with the given timestamp. The timestamp must be in 'YYYY-MM-DD HH:MM:SS' format.
def updateTimeLogger():
    config = readConfig()
    config["log_start_time"] = getCurrentTime()
    writeConfig(config)
    return True


# Monitor Time Handling
#This function reads and returns the last_monitor_time from the config file
def readTimeMonitor() -> str:
    config = readConfig()
    return config.get("last_monitor_time", "")

#This function updates the last file monitored time i.e. last_monitor_time field with the given timestamp. The timestamp must be in 'YYYY-MM-DD HH:MM:SS' format.
def updateTimeMonitor() :
    config = readConfig()
    config["last_monitor_time"] = getCurrentTime()
    writeConfig(config)
    return True

#Deamon and watchdog status handling
#This function help to set the daemon which is monitoring the file.
def readDaemonStatus():
    config = readConfig()
    return config.get("daemon_status", "")

#Updates the last file monitored time i.e. last_monitor_time field with the given timestamp. The timestamp must be in 'YYYY-MM-DD HH:MM:SS' format.
def setDaemonStatus(status) :
    config = readConfig()
    config["daemon_status"] = status
    writeConfig(config)
    return True
