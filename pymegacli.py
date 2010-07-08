#
# Copyright (c) 2010, Giovanni P. Tirloni <gtirloni@sysdroid.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#  - Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#
#  - Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from subprocess import Popen, PIPE

MEGACLI='/usr/local/sas/utilities/MegaCli'

class Adapter:
    device_id = 0
    product_name = ''
    serial_number = ''
    fw_package_build = ''
    fw_version = ''
    bios_version = ''
    webbios_version = ''
    preboot_cli_version = ''
    boot_block_version = ''
    sas_address = ''
    bbu_present = False
    alarm_present = False
    nvram_present = False
    serial_debugger_present = False
    memory_present = False
    flash_present = False
    memory_size = ''

    def load(self, adapter_id):

        try:
            ret = megacli('-AdpAllInfo -a%i -NoLog' % adapter_id)
        except OSError:
            print 'Failed to get adapter information (MegaCli -AdpAllInfo)'
            return 0

        for line in ret.readlines():
            if line[0:9] == 'Adapter #':
                self.device_id = int(clean_nl(line[9:]))
            if line[0:12] == 'Product Name':
                self.product_name = clean_nl(line[18:])
            elif line[0:9] == 'Serial No':
                self.serial_number = clean_nl(line[18:])
            elif line[0:16] == 'FW Package Build':
                self.fw_package_build = clean_nl(line[18:])
            elif line[0:10] == 'FW Version':
                self.fw_version = clean_nl(line[21:])
            elif line[0:12] == 'BIOS Version':
                self.bios_version = clean_nl(line[21:])
            elif line[0:15] == 'WebBIOS Version':
                self.webbios_version = clean_nl(line[21:])
            elif line[0:19] == 'Preboot CLI Version':
                self.preboot_cli_version = clean_nl(line[21:])
            elif line[0:18] == 'Boot Block Version':
                self.boot_block_version = clean_nl(line[21:])
            elif line[0:11] == 'SAS Address':
                self.sas_address = clean_nl(line[18:])
            elif line[0:3] == 'BBU':
                self.bbu_present = is_present(line[18:])
            elif line[0:5] == 'Alarm':
                self.alarm_present = is_present(line[18:])
            elif line[0:5] == 'NVRAM':
                self.nvram_present = is_present(line[18:])
            elif line[0:15] == 'Serial Debugger':
                self.serial_debugger_present = is_present(line[18:])
            elif line[0:8] == 'Memory  ':
                self.memory_present = is_present(line[18:])
            elif line[0:11] == 'Memory Size':
                self.memory_size = clean_nl(line[18:])

    def show(self):

        ret = """Device ID                     : %d
Product Name                  : %s
Serial Number                 : %s
FW Package Build              : %s
FW Version                    : %s
BIOS Version                  : %s
WebBIOS Version               : %s
Preboot CLI Version           : %s
Boot Block Version            : %s
SAS Address                   : %s
BBU Present                   : %s
Alarm Present                 : %s
NVRAM Present                 : %s
Serial Debugger Present       : %s
Memory Present                : %s
Flash Present                 : %s
Memory Size                   : %s""" % (self.device_id, self.product_name, \
        self.serial_number, self.fw_package_build, self.fw_version, \
        self.bios_version, self.webbios_version, self.preboot_cli_version, \
        self.boot_block_version, self.sas_address, self.bbu_present, \
        self.alarm_present, self.nvram_present, self.serial_debugger_present, \
        self.memory_present, self.flash_present, self.memory_size)

        print ret


class Enclosure:
    device_id = 0
    number_of_slots = 0
    number_of_power_supplies = 0
    number_of_fans = 0
    number_of_temperature_sensors = 0
    number_of_alarms = 0
    number_of_sim_modules = 0
    number_of_physical_drives = 0
    status = ''
    position = 0
    connector_name = ''
    partner_device_id = 0

    def load_from_text(self, input):

        for line in input:
            if line[4:13] == 'Device ID':
                self.device_id = int(clean_nl(line[36:]))
            if line[4:19] == 'Number of Slots':
                self.number_of_slots = int(clean_nl(line[36:]))
            elif line[4:28] == 'Number of Power Supplies':
                self.number_of_power_supplies = int(clean_nl(line[36:]))
            elif line[4:18] == 'Number of Fans':
                self.number_of_fans = int(clean_nl(line[36:]))
            elif line[4:33] == 'Number of Temperature Sensors':
                self.number_of_temperature_sensors = int(clean_nl(line[36:]))
            elif line[4:20] == 'Number of Alarms':
                self.number_of_alarms = int(clean_nl(line[36:]))
            elif line[4:25] == 'Number of SIM Modules':
                self.number_of_sim_modules = int(clean_nl(line[36:]))
            elif line[4:29] == 'Number of Physical Drives':
                self.number_of_physical_drives = int(clean_nl(line[36:]))
            elif line[4:10] == 'Status':
                self.status = clean_nl(line[36:])
            elif line[4:12] == 'Position':
                self.position = clean_nl(line[36:])
            elif line[4:18] == 'Connector Name':
                self.connector_name = clean_nl(line[36:])
            elif line[4:21] == 'Partner Device Id':
                self.partner_device_id = int(clean_nl(line[36:]))

    def show(self):

        ret = """Device ID                     : %i
Number of Slots               : %i
Number of Power Supplies      : %i
Number of Fans                : %i
Number of Temperature Sensors : %i
Number of Alarms              : %i
Number of SIM Modules         : %i
Number of Physical Drives     : %i
Status                        : %s
Position                      : %s
Connector Name                : %s
Partner Device Id             : %i""" % (self.device_id, self.number_of_slots, \
        self.number_of_power_supplies, self.number_of_fans, \
        self.number_of_temperature_sensors, self.number_of_alarms, \
        self.number_of_sim_modules, self.number_of_physical_drives, \
        self.status, self.position, self.connector_name, self.partner_device_id)

        print ret


class PhysicalDevice:
    adapter_id = 0
    enclosure_id = 0
    slot_id = 0
    device_id = 0
    sequence_number = 0
    media_errors = 0
    other_errors = 0
    predictive_failures = 0
    last_predictive_seq_number = 0
    pd_type = ''
    raw_size = ''
    non_coerced_size = ''
    coerced_size = ''
    firmware_state = ''
    sas_address = ''
    connected_port_number = ''
    inquiry_data = ''
    fde_capable = ''
    fde_enable = ''
    secured = ''
    locked = ''
    foreign_state = ''
    device_speed = ''
    link_speed = ''
    media_type = ''

    def led_on(self):

        try:
            ret = megacli('-PdLocate -Start -PhysDrv[%i:%i] -a%i'
                % (self.enclosure_id, self.slot_id, self.adapter_id))
        except OSError:
            print 'Failed to turn location LED on (MegaCli -PdLocate -Start)'
            return False

        return True


    def led_off(self):

        try:
            ret = megacli('-PdLocate -Stop -PhysDrv[%i:%i] -a%i'
                % (self.enclosure_id, self.slot_id, self.adapter_id))
        except OSError:
            print 'Failed to turn location LED on (MegaCli -PdLocate -Stop)'
            return False

        return True


    def load_from_text(self, input):

        for line in input:

            if line[0:19] == 'Enclosure Device ID':
                self.enclosure_id = int(clean_nl(line[21:]))
            if line[0:11] == 'Slot Number':
                self.slot_id = int(clean_nl(line[13:]))
            elif line[0:9] == 'Device Id':
                self.device_id = int(clean_nl(line[11:]))
            elif line[0:15] == 'Sequence Number':
                self.sequence_number = int(clean_nl(line[17:]))
            elif line[0:17] == 'Media Error Count':
                self.media_errors = int(clean_nl(line[19:]))
            elif line[0:17] == 'Other Error Count':
                self.other_errors = int(clean_nl(line[19:]))
            elif line[0:24] == 'Predictive Failure Count':
                self.predictive_failures = int(clean_nl(line[26:]))
            elif line[0:40] == 'Last Predictive Failure Event Seq Number':
                self.last_predictive_failure_seq_number = int(clean_nl(line[42:]))
            elif line[0:7] == 'PD Type':
                self.pd_type = clean_nl(line[9:])
            elif line[0:8] == 'Raw Size':
                delim = line.find('[') - 4
                self.raw_size = float(clean_nl(line[10:delim]))
            elif line[0:16] == 'Non Coerced Size':
                delim = line.find('[') - 4
                self.non_coerced_size = float(clean_nl(line[18:delim]))
            elif line[0:12] == 'Coerced Size':
                delim = line.find('[') - 4
                self.coerced_size = float(clean_nl(line[14:delim]))
            elif line[0:14] == 'Firmware state':
                self.firmware_state = clean_nl(line[16:])
            elif line[0:11] == 'SAS Address':
                self.sas_address = clean_nl(line[16:])
            elif line[0:21] == 'Connected Port Number':
                self.connected_port_number = clean_nl(line[23:])
            elif line[0:12] == 'Inquiry Data':
                self.inquiry_data = clean_nl(line[14:])
            elif line[0:11] == 'FDE Capable':
                self.fde_capable = clean_nl(line[13:])
            elif line[0:10] == 'FDE Enable':
                self.fde_enable = clean_nl(line[12:])
            elif line[0:7] == 'Secured':
                self.secured = clean_nl(line[9:])
            elif line[0:6] == 'Locked':
                self.locked = clean_nl(line[8:])
            elif line[0:13] == 'Foreign State':
                self.foreign_state = clean_nl(line[15:])
            elif line[0:12] == 'Device Speed':
                self.device_speed = clean_nl(line[14:])
            elif line[0:10] == 'Link Speed':
                self.link_speed = clean_nl(line[12:])
            elif line[0:10] == 'Media Type':
                self.media_type = clean_nl(line[12:])

    def load(self, adapter_id, enclosure_id, slot_id):

        try:
            ret = megacli('-PdInfo -PhysDrv[%i:%i] -a%i' % (enclosure_id, slot_id, adapter_id))
        except OSError:
            print 'Failed to get physical device information (MegaCli -PdInfo)'
            return []

        self.adapter_id = adapter_id
        ret_lines = ret.readlines()
        self.load_from_text(ret_lines)

    def show(self):

        ret = """Adapter ID: %s
Enclosure Device ID: %s
Slot Number: %s
Device Id: %s
Sequence Number: %s
Media Error Count: %s
Other Error Count: %s
Predictive Failure Count: %s
Last Predictive Failure Event Seq Number: %s
PD Type: %s
Raw Size: %s
Non Coerced Size: %s
Coerced Size: %s
Firmware state: %s
SAS Address(0): %s
Connected Port Number: %s
Inquiry Data: %s
FDE Capable: %s
FDE Enable: %s
Secured: %s
Locked: %s
Foreign State: %s
Device Speed: %s
Link Speed: %s
Media Type: %s""" % (self.adapter_id, self.enclosure_id, self.slot_id, self.device_id, \
        self.sequence_number, self.media_errors, self.other_errors, \
        self.predictive_failures, \
        self.last_predictive_seq_number, \
        self.pd_type, self.raw_size, self.non_coerced_size, \
        self.coerced_size, \
        self.firmware_state, self.sas_address, self.connected_port_number, \
        self.inquiry_data, self.fde_capable, self.fde_enable, \
        self.secured, self.locked, self.foreign_state, self.device_speed, \
        self.link_speed, self.media_type)

        print ret


class VirtualDrive:
    virtualdisk_id = 0
    name = ''
    raid_level = ''
    size = ''
    state = ''
    stripe_size = ''
    number_of_drives = 0
    span_depth = 0
    default_cache_policy = ''
    current_cache_policy = ''
    access_policy = ''
    disk_cache_policy = ''
    encryption = ''


    def load_from_text(self, input):

        for line in input:
            if line[0:12] == 'Virtual Disk':
                offset = line.find('(')
                self.virtualdisk_id = int(clean_nl(line[14:offset-1]))
            if line[0:4] == 'Name':
                self.name = clean_nl(line[6:])
            elif line[0:10] == 'RAID Level':
                self.raid_level = clean_nl(line[12:])
            elif line[0:4] == 'Size':
                delim = line.find(' GB')
                self.size = clean_nl(line[5:delim])
            elif line[0:5] == 'State':
                self.state = clean_nl(line[7:])
            elif line[0:11] == 'Stripe Size':
                delim = line.find(' KB')
                self.stripe_size = clean_nl(line[13:delim])
            elif line[0:16] == 'Number Of Drives':
                self.number_of_drives = int(clean_nl(line[17:]))
            elif line[0:10] == 'Span Depth':
                self.span_depth = int(clean_nl(line[11:]))
            elif line[0:20] == 'Default Cache Policy':
                self.default_cache_policy = clean_nl(line[22:])
            elif line[0:20] == 'Current Cache Policy':
                self.current_cache_policy = clean_nl(line[22:])
            elif line[0:13] == 'Access Policy':
                self.access_policy = clean_nl(line[15:])
            elif line[0:17] == 'Disk Cache Policy':
                self.disk_cache_policy = clean_nl(line[19:])
            elif line[0:10] == 'Encryption':
                self.encryption = clean_nl(line[12:])


    def show(self):

        ret = """Virtual Disk: %d
Name: %s
RAID Level: %s
Size: %s
State: %s
Strip Size: %s
Number Of Drives: %d
Span Depth: %d
Default Cache Policy: %s
Current Cache Policy: %s
Access Policy: %s
Disk Cache Policy: %s
Encryption: %s""" % (self.virtualdisk_id, self.name, self.raid_level, \
    self.size, self.state, self.stripe_size, self.number_of_drives, \
    self.span_depth, self.default_cache_policy, self.current_cache_policy, \
    self.access_policy, self.disk_cache_policy, self.encryption)

        print ret


def adp_list():

    try:
        ret = megacli('-AdpCount -NoLog')
    except OSError:
        print 'Failed to get adapter count (MegaCli -AdpCount)'
        return []

    adp_count = 0

    for line in ret.readlines():
        if line[0:16] == 'Controller Count':
            adp_count = int(clean_nl(line[17:]).replace('.',''))

    adp_list = []
    adp = Adapter()

    for adp_id in range(0, adp_count):
                adp.load(adp_id)
                adp_list.append(adp)
                adp = Adapter()

    return adp_list


def enc_list(adapter_id):

    try:
        ret = megacli('-EncInfo -a%i' % adapter_id)
    except OSError:
        print 'Failed to get enclosure information (MegaCli -EncInfo)'
        return []

    ret_lines = ret.readlines()

    enc_list = []
    enc = Enclosure()

    # Go through all lines looking for the Enclosure identifier line
    for line in range(0, len(ret_lines)):
        if ret_lines[line][0:13] == '    Enclosure':

            # Feed the enclosure's block of text to the Enclosure object
            enc.load_from_text(ret_lines[line:line+13])

            # Add Enclosure to the enc_list and reset it
            enc_list.append(enc)
            enc = Enclosure()

    return enc_list


def pd_list(adapter_id):

    try:
        ret = megacli('-PdList -a%i' % adapter_id)
    except OSError:
        print 'Failed to get physical device information (MegaCli -PdList)'
        return []

    ret_lines = ret.readlines()

    pd_list = []
    pd = PhysicalDevice()

    # Go through all lines looking for the first line in the disk info
    for line in range(0, len(ret_lines)):
        if ret_lines[line][0:19] == 'Enclosure Device ID':

            # Feed disk info to the PhysicalDevice object
            pd.load_from_text(ret_lines[line:line+24])

            # Add PhysicalDevice to the pd_list and reset it
            pd_list.append(pd)
            pd = PhysicalDevice()

    return pd_list


def vd_list(adapter_id):

    try:
        ret = megacli('-LdInfo -Lall -a%i' % adapter_id)
    except OSError:
        print 'Failed to get virtual drive information (MegaCli -LDInfo -Lall)'
        return []

    ret_lines = ret.readlines()

    vd_list = []
    vd = VirtualDrive()

    # Go through all lines looking for the Virtual Disk line
    for line in range(0, len(ret_lines)):
        if ret_lines[line][0:12] == 'Virtual Disk':

            # Feed the virtual drive's block of text to the VirtualDrive object
            vd.load_from_text(ret_lines[line:line+13])

            # Add VirtualDrive to the vd_list and create a new one
            vd_list.append(vd)
            vd = VirtualDrive()

    return vd_list

def clean_nl(str):
    return str.replace('\n', '')

def is_present(str):
    if clean_nl(str) == 'Present':
        return True
    else:
        return False

def megacli(args):
    cmd = MEGACLI + ' ' + args
    out = Popen(cmd, shell=True, stdout=PIPE).stdout
    return out