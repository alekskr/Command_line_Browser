#  запускать программу из командной строки

import argparse, os, sys, requests
from collections import deque
from bs4 import BeautifulSoup
from colorama import Fore
from colorama import init
# init()

# FOR INPUT IN COMMAND LINE
# первый вариант создания папки с помощью argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('new_dir', help='Directory for new files')
# args = parser.parse_args()
# work_dir = 'D:\\Python projects\\Text-Based Browser my\\' + args.new_dir

# второй вариант создания папки с помощью sys
args = sys.argv
work_dir = 'D:\\Python projects\\Text-Based Browser my\\' + args[-1]

try:
    os.mkdir(work_dir)
except FileExistsError:
    print('Error: Directory already exists. Enter web-site name:')

# GLOBALS
stack = deque()
tags = ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li')


def delete_ending(url):
    file_name = url.replace('https://', '')
    file_name_reverse = file_name[::-1]
    index_of_dot = file_name_reverse.find('.')
    file_name_reverse_delete_ending = file_name_reverse[index_of_dot + 1:]
    file_name_delete_ending = file_name_reverse_delete_ending[::-1]
    return file_name_delete_ending


def creating_file(content, name):
    file_name = work_dir + '\\' + name
    with open(file_name, 'w', encoding='UTF-8') as f:
        f.write(str(content))
    web_sites_stack(name)


def web_sites_stack(file_name):
    global stack
    stack.append(file_name)
    return stack


def previous_page(stack):
    if len(stack) < 2:
        pass
    else:
        stack.pop()
        file_name = work_dir + '\\' + stack.pop()
        with open(file_name, 'r', encoding='UTF-8') as f:
            print(f.read())


def processing_request(request):
    if request.startswith('https://'):
        link = request
    else:
        link = 'https://' + request
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')
    p = soup.find_all(tags)
    content = ''

    for i in p:
        if i.name == 'a':
        # if i.has_attr('href'):
        # if str(i).startswith('<a'):
            print(Fore.BLUE + i.text.strip().replace('\n', " "))
        else:
            print(i.text.strip().replace('\n', " "))
        content += i.text
    return content


while True:
    user_request = input()
    try:
        if user_request == 'exit':
            exit()
        elif user_request == 'back':
            previous_page(stack)
        else:
            site_content = processing_request(user_request)
            site_name = delete_ending(user_request)
            creating_file(site_content, site_name)
    except requests.exceptions.ConnectionError:
        print('Incorrect URL')
