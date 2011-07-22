import zipfile
import httplib2
import easygui
from lxml.html import fromstring
from sys import argv, version
from os import rename, remove, path, environ, system
from shutil import rmtree, copytree


class Settings(easygui.EgStore):
    def __init__(self, filename):
        self.save_dir = ''
        self.backup_ver = '0'
        self.current_ver = '0'
        self.filename = filename
        self.restore()


settingsFile = path.join('C:\\',
                   'Python' + version[:3].replace('.', ''), 'chromium.ini')
settings = Settings(settingsFile)
settings.save_dir = (settings.save_dir or
                    path.join(environ["ProgramFiles"], 'Chromium\\'))


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


def del_current(use_gui):
    if path.exists(path.join(settings.save_dir, 'Current')):
        try:
            rmtree(path.join(settings.save_dir, 'Current'))
        except WindowsError:
            close_chromium(use_gui)


def del_backup():
    if path.exists(path.join(settings.save_dir, 'Backup')):
        rmtree(path.join(settings.save_dir, 'Backup'))


def download_chromium(ver):
    connection = httplib2.Http('.cache')
    site = 'http://build.chromium.org/buildbot/snapshots/Win/' \
            '%s/chrome-win32.zip' % ver
    settings.current_ver = ver
    settings.store()
    re, chrome = connection.request(site)
    with open(path.join(settings.save_dir, 'latest.zip'), 'wb') as zfile:
        zfile.write(chrome)
    


def close_chromium(use_gui):
    if not use_gui:
        if input("Enter an character to close chromium: ")[:-1]:
            system("taskkill /F /IM chrome.exe > NUL")
    else:
        if easygui.ynbox("Do you want to close chromium?"):
            system("taskkill /F /IM chrome.exe > NUL")


def unzip():
    with zipfile.ZipFile(settings.save_dir + 'latest.zip', 'r') as zipped:
        zipped.extractall(settings.save_dir)

    rename(path.join(settings.save_dir, 'chrome-win32'), 
           path.join(settings.save_dir, 'Current'))

    remove(path.join(settings.save_dir, 'latest.zip'))
    print('Download Complete')


def revert():
    del_current(False)
    copytree(path.join(settings.save_dir, 'Backup'), 
             path.join(settings.save_dir, 'Current'))
    print('Revert Complete')


def backup(ver):
    del_backup()
    settings.backup_ver = ver
    settings.store()
    copytree(path.join(settings.save_dir, 'Current'), 
             path.join(settings.save_dir, 'Backup'))
    print('Backup Complete')


def gui():
    ver = get_latest_version()
    while True:
        choices = ['Download v%s' % ver, 'Specify Version',
                   'Backup v%s' % settings.current_ver, 'Revert to v%s'
                    % settings.backup_ver, 'Edit Save Dir', 'Exit']
        choice = easygui.indexbox('What do you want to do?',
                'Chromium Downloader', choices)
        if choice == 0:
            del_current(True)
            download_chromium(ver)
            unzip()
        elif choice == 1:
            ver = get_closest_version(easygui.integerbox(
                'Enter desired verson (The closest match will be used):',
                'Specify a version', int(ver)) or int(ver))
        elif choice == 2:
            backup(ver)
        elif choice == 3:
            revert()
        elif choice == 4:
            settings.save_dir = (easygui.enterbox("New Save Directory", "", "")
                        or path.join(environ["ProgramFiles"], 'Chromium\\'))
            settings.store()
        else:
            break


def usage():
    print('-h         Display help text\n' +
          '-g         Launches the GUI Program\n' +
          '-v         Only gets the version\n' +
          '-r         Reverts to last backup\n' +
          '-b         Saves a new backup\n' +
          '-o         Specify version to download\n')


def main():
    if '-o' in argv[1:]:
        ver = get_closest_version(argv[argv.index('-o') + 1])
    else:
        ver = get_latest_version()
        
    if '-g' in argv[1:]:
        gui()
        return
    elif '-h' in argv[1:]:
        usage()
        return
    elif '-r' in argv[1:]:
        revert()
        return
    elif '-b' in argv[1:]:
        backup(ver)
        return

    print('Latest Version: ', ver)

    if '-v' in argv[1:]:
        return

    del_current(False)
    download_chromium(ver)
    unzip()

if __name__ == "__main__":
    main()
