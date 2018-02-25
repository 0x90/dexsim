#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
import re
import shutil
import tempfile
import zipfile
#
from cigam import Magic
#
from dexsim import settings
from dexsim import Driver, Oracle
from dexsim.utils import baksmali, smali


def dexsim_dex(dex_file, smali_dir, include_str, output_dex):
    def dexsim(dex_file, smali_dir, include_str):
        driver = Driver()
        driver.push_to_dss(dex_file)
        oracle = Oracle(smali_dir, driver, include_str)
        oracle.divine()

    dexsim(dex_file, smali_dir, include_str)
    output_dir = output_dex if output_dex else os.path.splitext(os.path.basename(dex_file))[0] + '.sim.dex'
    smali(smali_dir, output_dir)

    if not settings.DEBUG:
        shutil.rmtree(smali_dir)


class DexSim(object):

    def __init__(self):
        self.smali_dir = os.path.join(os.path.abspath(os.curdir), 'smali') if settings.DEBUG else tempfile.mkdtemp()

    def sim_apk(self, apk_path, output_path, include_str=None):
        tempdir = os.path.join(os.path.abspath(os.curdir), 'tmp_dir') if settings.DEBUG else tempfile.mkdtemp()
        if not os.path.exists(tempdir):
            os.mkdir(tempdir)

        ptn = re.compile(r'classes\d*.dex')
        zip_file = zipfile.ZipFile(apk_path)
        for item in zip_file.namelist():
            if ptn.match(item):
                output_path = zip_file.extract(item, tempdir)
                baksmali(output_path, self.smali_dir)

        zip_file.close()

        dexsim_dex(apk_path, self.smali_dir, include_str, output_path)
        if not settings.DEBUG:
            shutil.rmtree(tempdir)

    def sim_dex(self, dex_path, output_path, include_str=None):
        baksmali(dex_path, self.smali_dir)
        dexsim_dex(dex_path, self.smali_dir, include_str, output_path)

    def sim_dir(self, input_path, output_path, include_str=None):
        smali_dir = input_path[:-1] if input_path.endswith('\\') or input_path.endswith('/') else input_path
        dex_file = smali(smali_dir, os.path.basename(smali_dir) + '.dex')
        dexsim_dex(dex_file, smali_dir, include_str, output_path)

    def run(self, input_path, output_path, include_str):

        if os.path.isdir(input_path):
            return self.sim_dir(input_path, output_path, include_str)

        file_type = Magic(input_path).get_type()
        if file_type == 'apk':
            return self.sim_apk(input_path, output_path, include_str)

        elif file_type == 'dex':
            return self.sim_dex(input_path, output_path, include_str)

        print("Please give smali_dir/dex/apk.")
        return -1
