import re

import PyInstaller.__main__
from main import __package_name__, __version__
import shutil
import subprocess as sbp

if __name__ == '__main__':
    #update pakcages
    pkgs = eval(str(sbp.run("pip list -o --format=json", shell=True,
                            stdout=sbp.PIPE).stdout, encoding='utf-8'))
    for pkg in pkgs:
        sbp.run("pip install --upgrade " + pkg['name'], shell=True)


    try:
        shutil.rmtree('dist')
    except FileNotFoundError:
        pass
    with open("file_version_info.txt", 'r+') as f:
        data = f.read()
        ver = __version__.split('.')
        f.seek(0)
        f.write(re.sub(r"(.*=*\((u'.*)*)(\d+)([.,]\s*)(\d+)([.,]\s*)(\d+)(.*)", fr"\g<1>{ver[0]}\g<4>{ver[1]}\g<6>{ver[2]}\g<8>", data))
        f.truncate()

    PyInstaller.__main__.run([
        f'--name={__package_name__}',
        '--onefile',
        '--clean',
        '--noconfirm',
        '--icon=icon.ico',
        '--version-file=file_version_info.txt',
        '--add-binary=libcpdf\libpycpdf.dll:libcpdf',
        'main.py',
    ])
    # shutil.copyfile('config-sample.ini', '{0}/config.ini'.format('dist'))
    # # shutil.copyfile('logging.yaml', '{0}/logging.yaml'.format('dist'))
    # shutil.copyfile('README.md', '{0}/README.md'.format('dist'))
    # print("zipping")
    # shutil.make_archive(f'zip/{__package_name__} v.{__version__}', 'zip', 'dist')


