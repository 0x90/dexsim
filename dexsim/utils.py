import os
import subprocess
import shutil

from dexsim import settings, Driver, Oracle


def baksmali(dex_file, output_dir='out'):
    """
    dex to smali
    """
    cmd = '{} -jar {} d {} -o {}'.format(settings.JAVA_PATH,
                                         settings.BAKSMALI_PATH, dex_file, output_dir)
    print(cmd)

    subprocess.call(cmd, shell=True)

    for line in settings.FILTERS_LIST:
        clz = line.split('#')[0]
        xpath = output_dir + os.sep + clz.replace('.', os.sep).strip('\n')
        if os.path.exists(xpath):
            shutil.rmtree(xpath)

    return output_dir


def smali(smali_dir, output_file='out.dex'):
    """
    smali to dex
    """
    cmd = '{} -jar {} a {} -o {}'.format(settings.JAVA_PATH,
                                         settings.SMALI_PATH, smali_dir, output_file)
    print(cmd)

    subprocess.call(cmd, shell=True)

    return output_file

