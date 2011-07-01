import zipfile
from os import rename, remove, path, environ
from shutil import rmtree, copytree
import httplib2
from sys import argv, exit
import easygui


SAVE_DIR = path.join(environ["ProgramFiles"], 'Chromium\\')


def get_latest_version():
    connection = httplib2.Http('.cache')
    verSite = ('http://build.chromium.org/f/chromium/snapshots/Win/LATEST')
    return connection.request(verSite)[1].decode('utf8')


def del_current():
    if path.exists(path.join(SAVE_DIR, 'Current')):
        rmtree(path.join(SAVE_DIR, 'Current'))


def del_backup():
    if path.exists(path.join(SAVE_DIR, 'Backup')):
        rmtree(path.join(SAVE_DIR, 'Backup'))


def download_chromium(ver):
    connection = httplib2.Http('.cache')
    site = 'http://build.chromium.org/buildbot/snapshots/Win/' \
            '%s/chrome-win32.zip' % ver
    re, chrome = connection.request(site)
    with open(path.join(SAVE_DIR, 'latest.zip'), 'wb') as zfile:
        zfile.write(chrome)


def unzip():
    with zipfile.ZipFile(SAVE_DIR + 'latest.zip', 'r') as zip:
        zip.extractall(SAVE_DIR)
    rename(path.join(SAVE_DIR, 'chrome-win32'), path.join(SAVE_DIR, 'Current'))
    remove(path.join(SAVE_DIR, 'latest.zip'))


def revert():
    del_current()
    copytree(path.join(SAVE_DIR, 'Backup'), path.join(SAVE_DIR, 'Current'))


def backup():
    del_backup()
    copytree(path.join(SAVE_DIR, 'Current'), path.join(SAVE_DIR, 'Backup'))


def gui():
    ver = get_latest_version()
    choices = ['Download version %s' % ver, 'Backup', 'Revert', 'Exit']
    while True:
        choice = easygui.indexbox('What do you want to do?',
                'Chromium Downloader', choices)
        if choice == 0:
            del_current()
            download_chromium(ver)
            unzip()
        elif choice == 1:
            backup()
        elif choice == 2:
            revert()
        elif choice == 3:
            break

def usage():
    print('-h         Display help text\n' +
          '-g         Launches the GUI Program\n' +
          '-v         Only gets the version\n' +
          '-r         Reverts to last backup\n' +
          '-b         Saves a new backup\n' +
          '-o         Specify version to download\n')


def main():
    if '-g' in argv:
        gui()
        return
    elif '-h' in argv:
        usage()
        return 2
    elif '-r' in argv:
        revert()
        return

    if '-o' in argv:
        ver = argv.index('-o') + 1
    else:
        ver = get_latest_version()
        print('Latest Version: ', ver)
    if '-v' in argv:
        return

    del_current()
    download_chromium(ver)
    unzip()

    if '-b' in argv:
        backup()

if __name__ == "__main__":
    exit(main())
