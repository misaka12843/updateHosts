#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import urllib.request
import platform
import datetime
import time
import re
import os
import shutil
import configparser
import sys
import socket
import logging

# 设置日志记录
logging.basicConfig(filename='errorLog.txt', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

config_path = 'config.ini' 
# default setting 
hosts_folder = ""
hosts_location = hosts_folder + "hosts"

source_list = ['https://raw.hellogithub.com/hosts']
not_block_sites = 0
always_on = 0
# default setting 

def get_cur_info():
    return sys._getframe().f_back.f_code.co_name

def exit_this():
    sys.exit()

def check_connection():
    sleep_seconds = 1200
    for i in range(sleep_seconds):
        try:
            socket.gethostbyname("www.baidu.com")
            break
        except socket.gaierror:
            time.sleep(1)
    else:
        logging.error(f'{get_cur_info()} - Unable to connect to the internet after {sleep_seconds} seconds.')
        exit_this()

def check_system_and_config():
    global hosts_folder, hosts_location, source_list, not_block_sites, always_on

    # 检查系统并设置hosts文件路径
    if platform.system() == 'Windows':
        hosts_folder = os.environ['SYSTEMROOT'] + "\\System32\\drivers\\etc\\"
    elif platform.system() in ['Linux', 'Darwin']:  # Linux 或 macOS
        hosts_folder = "/etc/"
    else:
        logging.error(f'{get_cur_info()} - Unsupported operating system: {platform.system()}')
        exit_this()

    hosts_location = hosts_folder + "hosts"

    # 读取配置文件
    if os.path.exists(config_path):
        try:
            # 清除Windows记事本自动添加的BOM
            with open(config_path, 'r+', encoding='utf-8') as f:
                content = f.read()
                content = re.sub(r"\xfe\xff", "", content)  # 删除 BOM
                content = re.sub(r"\xff\xfe", "", content)
                content = re.sub(r"\xef\xbb\xbf", "", content)
                f.seek(0)
                f.write(content)

            config = configparser.ConfigParser()
            config.read(config_path)
            source_id = config.get('source_select', 'source_id')
            source_list = source_id.split(",")
            for i in range(len(source_list)):
                source_list[i] = config.get('source_select', f'source{i + 1}')

            not_block_sites = config.get("function", "not_block_sites")
            always_on = config.get("function", "always_on")
        except Exception as e:
            logging.error(f'{get_cur_info()} - Error reading configuration: {e}')
            exit_this()
    else:
        logging.error(f'{get_cur_info()} - Configuration file not found: {config_path}')
        exit_this()

def backup_hosts():
    try:
        if not os.path.isfile(hosts_folder + 'backup_hosts_original_by_updateHosts') and \
                os.path.isfile(hosts_folder + 'hosts'):
            shutil.copy(hosts_folder + 'hosts', hosts_folder + 'backup_hosts_original_by_updateHosts')
        if os.path.isfile(hosts_folder + 'hosts'):
            shutil.copy(hosts_folder + 'hosts', hosts_folder + 'backup_hosts_last_by_updateHosts')
    except Exception as e:
        logging.error(f'{get_cur_info()} - Error backing up hosts file: {e}')
        exit_this()

def download_hosts():
    try:
        with open("hosts_from_web", "w", encoding='utf-8') as hosts_from_web:
            for x in source_list:
                response = urllib.request.urlopen(x)
                hosts_from_web.write(response.read().decode('utf-8'))
    except Exception as e:
        logging.error(f'{get_cur_info()} - Error downloading hosts file: {e}')
        exit_this()

def process_hosts():
    try:
        with open('hosts', 'w', encoding='utf-8') as hosts_content:
            with open('hosts_from_web', 'r', encoding='utf-8') as file_from_web:
                hosts_from_web = file_from_web.read()
            with open('hosts_user_defined.txt', 'r', encoding='utf-8') as file_user_defined:
                hosts_user_defined = file_user_defined.read()

            hosts_content.write('#hosts_user_defined\n')
            hosts_content.write(hosts_user_defined)
            hosts_content.write('\n#hosts_user_defined\n')
            hosts_content.write('\n\n#hosts_by_hostsUpdate\n\n')

            if not_block_sites == "1":
                hosts_from_web = re.sub("127.0.0.1", "#not_block_sites", hosts_from_web)

            hosts_content.write(hosts_from_web)
            hosts_content.write('\n#hosts_by_hostsUpdate')

        os.remove('hosts_from_web')
    except Exception as e:
        logging.error(f'{get_cur_info()} - Error processing hosts file: {e}')
        exit_this()

def move_hosts():
    try:
        shutil.move("hosts", hosts_location)
    except Exception as e:
        logging.error(f'{get_cur_info()} - Error moving hosts file: {e}')
        exit_this()

def main():
    check_connection()
    check_system_and_config()
    backup_hosts()
    download_hosts()
    process_hosts()
    move_hosts()

if __name__ == '__main__':
    main()

if always_on == "1":
    while True:
        time.sleep(3600)
        main()