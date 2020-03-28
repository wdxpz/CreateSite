#!/usr/bin/env python3
import sys
import os
import getopt


import config
from utils import checkServer, deleteRemoteSite, createRemoteSite, saveMap

import logging
logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)

def createSite(sitename='test', description=''):
    if not checkServer('map_server'):
        logging.error('exit! Not found map_server')
    
    map_path = os.path.join(config.Map_Dir, sitename)

    if os.path.exists(map_path):
        choice = input('Find exited site with same name: {}, overwrite it, yes or nor? '.format(sitename))
        if not (choice.lower() == 'y' or choice.lower() == 'yes'):
            logging.info('exit! choose not to overwrite existed site!')
            return
    
    deleteRemoteSite(sitename)
    saveMap(map_path)
    createRemoteSite(sitename, description)
    
        
    
    
if __name__ == '__main__':
    sitename = 'test'
    description = ''

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "hs:d:", ['site=', 'desc='])
    except getopt.GetoptError:
        print('createsite.py -s <sitename> -d <desciption>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('createsite.py -s <sitename> -d <desciption>')
            sys.exit()
        elif opt in ('-s', '--site'):
            sitename = arg
        elif opt in ('-d', '--desc'):
            description = arg

    createSite(sitename, description)