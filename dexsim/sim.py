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
from dexsim.settings import DEBUG
from dexsim.driver import Driver
from dexsim.oracle import Oracle
from dexsim.utils import baksmali, smali


def dexsim_dex(dex_file, smali_dir, include_str, output_dex):
    driver = Driver()
    print('Cooking driver..')
    driver.cook()
    driver.start_dss()
    # print('Using driver: %s Pushing to dss..' % str(driver))
    driver.push_to_dss(dex_file)

    oracle = Oracle(smali_dir, driver, include_str)
    oracle.divine()

    output_dir = output_dex if output_dex else os.path.splitext(os.path.basename(dex_file))[0] + '.sim.dex'
    smali(smali_dir, output_dir)

    if not DEBUG:
        shutil.rmtree(smali_dir)


class DexSim(object):

    def __init__(self):
        self.smali_dir = os.path.join(os.path.abspath(os.curdir), 'smali') if DEBUG else tempfile.mkdtemp()

    def sim_apk(self, apk_path, output_path, include_str=None):
        # Temp dir
        tempdir = os.path.join(os.path.abspath(os.curdir), 'tmp_dir') if DEBUG else tempfile.mkdtemp()
        if not os.path.exists(tempdir):
            os.mkdir(tempdir)

        # Classes extraction
        print('Extracing classes...')
        count = 0
        ptn = re.compile(r'classes\d*.dex')
        zip_file = zipfile.ZipFile(apk_path)
        for item in zip_file.namelist():
            if ptn.match(item):
                output_path = zip_file.extract(item, tempdir)
                baksmali(output_path, self.smali_dir)
                count += 1

        zip_file.close()
        print('Extracted %i classes' % count)

        dexsim_dex(apk_path, self.smali_dir, include_str, output_path)
        if not DEBUG:
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
        print('File type: %s' % file_type)
        if file_type == 'apk':
            return self.sim_apk(input_path, output_path, include_str)

        elif file_type == 'dex':
            return self.sim_dex(input_path, output_path, include_str)

        print("Please give smali_dir/dex/apk.")
        return -1
