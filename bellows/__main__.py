import glob
import typing as ta

def find_cu(suf: str) -> ta.Sequence[str]:
    return list(glob.glob(f'/dev/cu.GoControl_{suf}*'))


import os
os.environ['EZSP_DEVICE'] = next(iter(find_cu('zigbee')))


from .cli import main

main.main()
