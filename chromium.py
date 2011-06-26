from zipfile import ZipFile
from os import rename, remove
from shutil import rmtree, copytree
from httplib2 import Http
from sys import argv, exit
import easygui


def getLatestVersion():
    verSite = ('http://build.chromium.org/f/chromium/snapshots/' +
            'Win/LATEST')
    re, ver = h.request(verSite)
    ver = str(ver, encoding='utf8')
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
    site = ('http://build.chromium.org/buildbot/snapshots/Win/'
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
    choice = easygui.indexbox('What do you want to do?',
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
        exit()
    gui()


def usage():
    print('-h         Display help text\n' +
            '-g         Launches the GUI Program\n' +
            '-v         Only gets the version\n' +
            '-r         Reverts to last backup\n' +
            '-b         Saves a new backup\n' +
            '-d         Specify save directory\n' +
            '-o         Specify version to download\n')


def main():
    if '-d' in argv:
        saveDir = argv.index('-d') + 1

    if '-g' in argv:
        gui()
        exit()
    elif '-h' in argv:
        usage()
        exit(2)
    elif '-r' in argv:
        revert()
        exit()

    if '-o' in argv:
        ver = argv.index('-o') + 1
    else:
        ver = getLatestVersion()
        print('Latest Version: ', ver)
    if '-v' in argv:
        exit()

    delCurrent()
    downloadChromium(ver)
    unzip()

    if '-b' in argv:
        backup()

if __name__ == "__main__":

    h = Http('.cache')
    saveDir = 'C:\\Program Files\\Chromium\\'
    main()
