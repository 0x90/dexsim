import os
import time
import json
import logging
import tempfile

#
from dexsim.adbwrapper import ADB
from dexsim import settings

logger = logging.getLogger(__name__)


DSS_PATH = '/data/local/dss'
DSS_APK_PATH = '/data/local/dss/tmp.apk'
DSS_DATA_PATH = '/data/local/dss_data'
DSS_OUTPUT_PATH = '/data/local/dss_data/od-output.json'
DSS_TARGETS_PATH = '/data/local/dss_data/od-targets.json'
DSS_EXCEPTION_PATH = '/data/local/dss_data/od-targets.json'
DSS_NEW_PATH = '/data/local/dss_data/new'
DSS_FINISH_PATH = '/data/local/dss_data/finish'


class Driver:

    def __init__(self, adb_path='adb'):
        """Init adb and command.

        export CLASSPATH=/data/local/od.zip;
        app_process /system/bin org.cf.oracle.Driver
        @/data/local/od-targets.json;
        """
        self.adb = ADB(adb_path)

    def set_new_dss(self):
        self.adb.shell_command(['echo', 'Yes', '>', DSS_NEW_PATH])

    def create_dss_folders(self):
        self.adb.shell_command(['mkdir', DSS_PATH, DSS_DATA_PATH])

    def install_dss(self):
        self.adb.install(reinstall=True, pkgapp=settings.DSS_SERVER_PATH)

    def uninstall_dss(self):
        self.adb.uninstall('me.mikusjelly.dss')

    def cook(self):
        self.create_dss_folders()
        self.set_new_dss()
        self.stop_dss()
        self.uninstall_dss()
        self.install_dss()

    def start_dss(self):
        self.adb.shell_command(['echo', 'No', '>', DSS_FINISH_PATH])
        self.adb.su_command(['am', 'broadcast', '-a', 'dss.start'])
        self.adb.su_command(['am', 'startservice', 'me.mikusjelly.dss/.DSService'])

    def stop_dss(self):
        self.adb.su_command(['am', 'force-stop', 'me.mikusjelly.dss'])

    def push_to_dss(self, apk_path):
        self.adb.run_cmd(['push', apk_path, DSS_APK_PATH])
        output = self.adb.get_output().decode('utf-8', errors='ignore')
        if 'failed' in output:
            print(output)
            return False

        return True

    def decode(self, targets):
        self.adb.run_cmd(['push', targets, DSS_TARGETS_PATH])
        output = self.adb.get_output().decode('utf-8', errors='ignore')
        if 'failed' in output:
            # print(output)
            return False

        self.start_dss()

        counter = 0
        while 1:
            time.sleep(3)
            counter += 3

            self.adb.su_command(['cat', DSS_FINISH_PATH])
            output = self.adb.get_output().decode('utf-8', errors='ignore')
            if 'Yes' in output:
                break

            if counter > 180:
                print("Driver time out", output)
                self.stop_dss()
                return

        tempdir = tempfile.gettempdir()
        output_path = os.path.join(tempdir, 'output.json')
        self.adb.run_cmd(
            ['pull', DSS_OUTPUT_PATH, output_path])

        result = None
        with open(output_path, mode='r+', encoding='utf-8') as ofile:
            size = len(ofile.read())
            if not size:
                self.adb.run_cmd(['pull', DSS_EXCEPTION_PATH, 'exception.txt'])
                self.adb.shell_command(['rm', DSS_EXCEPTION_PATH])
            else:
                ofile.seek(0)
                result = json.load(ofile)

        if not settings.DEBUG:
            self.adb.shell_command(['rm', DSS_OUTPUT_PATH])
            self.adb.shell_command(['rm', DSS_TARGETS_PATH])
        else:
            self.adb.shell_command(['pull', DSS_TARGETS_PATH])

        os.unlink(output_path)
        self.stop_dss()

        return result
