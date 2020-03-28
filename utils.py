#!/usr/bin/env python3

import os
import re
import time
import requests

from wand.image import Image
from subprocess import PIPE, run

import config

import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)


def shell_cmd(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    if result.returncode != 0:
        return 1, None
    return 0, result.stdout

def checkServer(name='map_server', timeout=3):
    cmd = 'rosnode ping -c 1 {}'.format(name)

    for i in range(timeout):
        _, output = shell_cmd(cmd)
        if len(re.findall('reply', output))>0:
            return True
        time.sleep(1)

    return False

def saveMap(map_path):
    if not os.path.exists(map_path):
        os.makedirs(map_path)
    
    #export map from ros map_server
    mapfilepath = os.path.join(map_path, 'map')
    cmd = 'rosrun map_server map_saver -f {}'.format(mapfilepath)
    result, output = shell_cmd(cmd)
    if result == 1:
        logging.error('saveMap: error in running ' + cmd)
        return None
    logging.info('saveMap: succeeded in export site map to path: {}'.format(map_path))
    
    mapfile = os.path.join(map_path, 'map.pgm')
    yamlfile = os.path.join(map_path, 'map.yaml')
    jpgfile = os.path.join(map_path, 'map.jpg')
    #conver jpg file form pgm file
    with Image(filename=mapfile) as img:
        img.format = 'jpeg'
        img.save(filename=jpgfile)
    if os.path.exists(jpgfile):
        logging.info('saveMap: succeeded in convert site map to jpeg into path: {}'.format(map_path))
        return (mapfile, yamlfile, jpgfile)
    else:
        logging.error('saveMap: failed in convert site map to jpeg into path: {}'.format(map_path))
        return None
        
def deleteRemoteSite(sitename):
    logging.info('utils: delete site {} from remote db'.format(sitename))
    endpoint = config.Delete_Site_Endpoint.format(sitename)
    response = requests.delete(endpoint)
    if response.status_code != 200:
        raise Exception('deleteRemoteSite Error!')
    logging.info('utils: succeeded in delete site {} from remote db'.format(sitename))


def createRemoteSite(sitename, description):
    logging.info('utils: create site {} in remote db'.format(sitename))
    jpgfile = 'map.jpg'
    jpgfilepath = os.path.join(config.Map_Dir, sitename, jpgfile)

    files = {
        'site_map': (jpgfile, open(jpgfilepath, 'rb'))
        #'site_map': open(jpgfilepath, 'rb')
    }
    values = {
        'site_name': sitename,
        'site_description': description
    }
    # headers = {
    #     'Content-type': 'multipart/form-data'
    # }

    responose = requests.post(config.Create_Site_Endoint, files=files, data=values)#, headers=headers)

    if responose.status_code != 200:
        raise Exception('createRemoteSite Error! status_code: {}'.format(responose.status_code))
    logging.info('utils: succeeded in create site {} from remote db'.format(sitename))


if __name__ == '__main__':
    # print(checkServer('rosout'))
    print(checkServer('map_server'))

    cmd = "rosrun map_server map_save -f {}".format('/home/sw/map')
    print(shell_cmd(cmd))

