import collections
import itertools
import parse
import pathlib
import pyuac
import os
import re
import shutil
import stat
import string
import subprocess
import traceback

class WimInfo:
    ImageInfo = collections.namedtuple('ImageInfo','index, name, description, size')
    def __init__(self,wim:pathlib.Path):
        run = subprocess.run(
            args=(
                'dism',
                '/get-imageinfo',
                '/imagefile:'+str(wim),
            ),
            capture_output=True,
            text=True,
            check=True,
        )
        image_pattern = r'Index : (?P<index>\d*)\nName : (?P<name>.*)\nDescription : (?P<description>.*)\nSize : (?P<size>.*) bytes\n\n'
        wiminfo = re.fullmatch(
            pattern=r'\nDeployment Image Servicing and Management tool\nVersion: (?P<version>.*)\n\nDetails for image : (?P<path>.*)\n\n('+image_pattern+')*The operation completed successfully.\n',
            string=run.stdout,
            flags=re.MULTILINE,
        ).groupdict()
        self.version = wiminfo['version']
        self.path = pathlib.Path(wiminfo['path'])
        self.images = list()
        for imginfo in re.finditer(
            pattern=image_pattern,
            string=run.stdout,
            flags=re.MULTILINE,
        ):
            self.images.append(
                WimInfo.ImageInfo(**imginfo.groupdict())
            )
        assert self.path == wim
    def __repr__(self):
        return f'{self.__class__}(version={self.version!r},path={self.path!r},images={self.images!r})'

class WimMount:
    def __init__(self,wim:pathlib.Path,idx:int,mnt:pathlib.Path):
        self.wim = pathlib.Path(wim)
        self.idx = int(idx)
        self.mnt = pathlib.Path(mnt)
    def __enter__(self):
        print(f'\n## Mounting {self.wim} {self.idx} to {self.mnt} ...')
        subprocess.run(
            args=(
                'dism',
                '/mount-image',
                '/imagefile:'+str(self.wim),
                '/index:'+str(self.idx),
                '/mountdir:'+str(self.mnt),
            ),
            # capture_output=True,
            # text=True,
            check=True,
        )
        print('mounted.')
        return self
    def __exit__(self,*exc):
        print(f'\n## Unmounting {self.wim} {self.idx} from {self.mnt} ...')
        subprocess.run(
            args=(
                'dism',
                '/unmount-wim',
                '/mountdir:'+str(self.mnt),
                '/discard' if any(exc) else '/commit',
            ),
            # capture_output=True,
            # text=True,
            check=True,
        )
        print('discarded.' if any(exc) else 'commited')

@pyuac.main_requires_admin
def main():
    for letter in string.ascii_uppercase:
        wim = pathlib.WindowsPath(f'{letter}:/sources/install.wim')
        if wim.is_file(): break
    else:
        print('No drive with sources/install.wim found.')
        print('Did you insert a usb drive or mount a vhdx with windows installation media on it?')
        return -1
    print(wim)
    print(WimInfo(wim))
    with WimMount(
        wim=wim,
        idx=2,
        mnt='./mnt',
    ) as wimmount:
        try:
            print('\n## Chamfering Edge...')
            for edge in (
                list((wimmount.mnt/'Program Files (x86)'/'Microsoft').glob('Edge*'))+
                list((wimmount.mnt/'Windows'/'WinSxS').glob('amd64_microsoft-edge-webview_31bf3856ad364e35*'))+
                ([wimmount.mnt/'Windows'/'System32'/'Microsoft-Edge-Webview'] if (wimmount.mnt/'Windows'/'System32'/'Microsoft-Edge-Webview').exists() else [])
            ):
                print(f'removing {edge}...')
                shutil.rmtree(
                    path=edge,
                    onexc=lambda function,path,exception: (
                        os.chmod(path, stat.S_IWRITE),
                        function(path),
                    ) if pathlib.Path(path).exists() else None
                )
            print('Edge chamfered.')
        except:
            traceback.print_exc()
            raise
        else:
            input('press [enter] to continue...')
if __name__=='__main__': exit(main())
