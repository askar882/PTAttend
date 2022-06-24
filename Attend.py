#!/usr/bin/env python

import os
import sys
import json
from typing import Dict, List

import requests


def main() -> None:
    '''
    Main function
    '''
    config = []
    try:
        config = read_config()
    except Exception as e:
        print(e, file=sys.stderr)
        exit(1)
    for item in config:
        attend(item)


def read_config() -> List:
    '''
    Read config from './config.json'

    :return: PT config list.
    :rtype: List
    '''
    file_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(file_path) as config_file:
        config = json.load(config_file)
    return config


def attend(item: Dict) -> bool:
    '''
    Perform attendance.

    :param item: PT item.
    :type item: Dict
    :return: Attendance result.
    :rtype: bool
    '''
    print(f"Attending {item['name']}")
    try:
        res = requests.request(item['method'],
                               item['url'],
                               headers={
                                'User-Agent': '''\
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'''
                                },
                               cookies=cookies_to_jar(item['cookies']))
        if res.status_code != 200:
            print(f"Failed to attend {item['name']}, status: {res.status_code}")
            return False
    except Exception as e:
        print(e, file=sys.stderr)
        return False
    return True


def cookies_to_jar(cookies: Dict) -> requests.cookies.RequestsCookieJar:
    '''
    Convert cookies dict to CookieJar.

    :param cookies: Cookies dict.
    :type cookies: Dict
    :return: CookieJar.
    :rtype: requests.cookies.RequestsCookieJar
    '''
    jar = requests.cookies.RequestsCookieJar()
    for key, value in cookies.items():
        jar.set(key, value)
    return jar


if __name__ == '__main__':
    main()
