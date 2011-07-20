import zipfile
import httplib2
import easygui
from lxml.html import fromstring
from sys import argv
from os import rename, remove, path, environ
from shutil import rmtree, copytree

SAVE_DIR = path.join(environ["ProgramFiles"], 'Chromium\\')


def get_latest_version():
    connection = httplib2.Http('.cache')
    verSite = ('http://build.chromium.org/f/chromium/snapshots/Win/LATEST')
    return connection.request(verSite)[1].decode('utf8')


def get_closest_version(ver):
    connection = httplib2.Http('.cache')
    versSite = ('http://build.chromium.org/f/chromium/snapshots/Win/')
    doc = fromstring(connection.request(versSite)[1].decode('utf8'))
    return min([int(a.text_content()[:-1]) for a in doc.cssselect('a')
           if a.text_content()[:-1].isdigit()], key=lambda x: abs(x - ver))


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
    print('Done')


def revert():
    del_current()
    copytree(path.join(SAVE_DIR, 'Backup'), path.join(SAVE_DIR, 'Current'))


def backup():
    del_backup()
    copytree(path.join(SAVE_DIR, 'Current'), path.join(SAVE_DIR, 'Backup'))


def gui():
    ver = get_latest_version()
    while True:
        choices = ['Download version %s' % ver, 'Specify Version',
                   'Backup', 'Revert', 'Exit']
        choice = easygui.indexbox('What do you want to do?',
                'Chromium Downloader', choices)
        if choice == 0:
            del_current()
            download_chromium(ver)
            unzip()
        elif choice == 1:
            ver = get_closest_version(easygui.integerbox(
                'Enter desired verson (The closest match will be used):',
                'Specify a version', int(ver), 0, 999999))
        elif choice == 2:
            backup()
        elif choice == 3:
            revert()
        elif choice == 4:
            break


def usage():
    print('-h         Display help text\n' +
          '-g         Launches the GUI Program\n' +
          '-v         Only gets the version\n' +
          '-r         Reverts to last backup\n' +
          '-b         Saves a new backup\n' +
          '-o         Specify version to download\n')


def main():
    if '-g' in argv[1:]:
        gui()
        return
    elif '-h' in argv[1:]:
        usage()
        return
    elif '-r' in argv[1:]:
        revert()
        return
    elif 'b' in argv[1:]:
        backup()
        return

    if '-o' in argv[1:]:
        ver = get_closest_version(argv[argv.index('-o') + 1])
    else:
        ver = get_latest_version()
    print('Latest Version: ', ver)

    if '-v' in argv[1:]:
        return

    del_current()
    download_chromium(ver)
    unzip()

if __name__ == "__main__":
    main()
