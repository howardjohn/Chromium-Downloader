from zipfile import ZipFile
from os import rename, remove
from shutil import rmtree, copytree
from httplib2 import Http
from msvcrt import getch
from sys import argv, exit
from easygui import *

h = Http('.cache')
saveDir = 'C:\\Program Files\\Chromium\\'


def getLatestVersion():
    verSite = ('http://build.chromium.org/f/chromium/snapshots/' +
            'chromium-rel-xp/LATEST')
    re, ver = h.request(verSite)
    ver = str(ver)
    return ver


def delCurrent():
    try:
        rmtree(saveDir + 'Current')
    except Exception:
        print('Chromium could not be removed.')


def delBackup():
    try:
        rmtree(saveDir + 'Backup')
    except Exception:
        print('Backup could not be removed.')


def downloadChromium(ver):
    site = ('http://build.chromium.org/buildbot/snapshots/chromium-rel-xp/'
            + ver + '/chrome-win32.zip')
    re, chrome = h.request(site)
    file = open(saveDir + 'latest.zip', 'wb')
    file.write(chrome)
    file.close()


def unzip():
    zip = ZipFile(saveDir + 'latest.zip', 'r')
    zip.extractall(saveDir)
    rename(saveDir + 'chrome-win32', saveDir + 'Current')
    zip.close()
    remove(saveDir + 'latest.zip')


def revert():
    delCurrent()
    copytree(saveDir + 'Backup', saveDir + 'Current')


def backup():
    delBackup()
    copytree(saveDir + 'Current', saveDir + 'Backup')


def gui():
    ver = getLatestVersion()
    choices = ['Download version %s' % ver, 'Backup', 'Revert', 'Exit']
    choice = indexbox('What do you want to do?',
            'Chromium Downloader', choices)
    if choice == 0:
        delCurrent()
        downloadChromium(ver)
        unzip()
    elif choice == 1:
        backup()
    elif choice == 2:
        revert()
    elif choice == 3:
        exit(2)
    gui()


def main():
    gui()
    exit(2)

if __name__ == "__main__":
    main()
