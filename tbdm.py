#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
'TBDM Moduel'
__author__ = 'Ken Zhao'
from logging import info,debug,error,warning,critical
import tracer
class Tbdm:
    def __init__(self, cmd_hdr):
        self.cmd_hdr = cmd_hdr+"\n"
        self.cmds = {}
    def add_io_cmd(self, data, port_str, port):
        self.cmds[port_str] = "//;$ at io read 0x%s set port 0x%04x to 0x%s\n"%(port_str, port ,data)
    def update_io_cmd(self,data, port_str, port):
        self.cmds[port_str] = self.cmds[port_str] + "//;$ then at io read 0x%s set port 0x%04x to 0x%s\n"%(port_str, port ,data)
    def add_reload_cmd(self, addr, data, offset):
        self.cmds[addr] = "//;$ at memory read 0x00%s set memory 0x00%s to 0x%s\n"%(addr, offset ,data)
    def update_reload_cmd(self, addr, data, offset):
        self.cmds[addr] = self.cmds[addr] + "//;$ then at memory read 0x00%s set memory 0x00%s to 0x%s\n"%(addr, offset, data)
    def add_smm_cmd(self, key, tr7, rip ,tr7_tbd, apic_base):
        self.cmds[key]["cmd"] = ""
        smm_cmd = "//sim: skip 0 at EIP 0x%s  TR7 0x%s delta 0x0000000F SMI\n"%(rip,tr7)
        smm_tbd_cmd = "//;$ at TARACER_TR7 0x%s issue priority transaction 0x%sFF000 0x09 0x00CA0300 0x1C 0x0000000000000200\n"%(tr7_tbd,apic_base)
        self.cmds[key]["cmd"] =  self.cmds[key]["cmd"] + smm_cmd + smm_tbd_cmd
        
    def store_smm(self, tr7, rip ,tr7_tbd, apic_base):
        self.cmds[tr7] = {}
        self.cmds[tr7]["rip"] = rip
        self.cmds[tr7]["apic_base"] = apic_base
        self.cmds[tr7]["tr7_tbd"] = tr7_tbd
        
    def print_io_cmds(self,file):
        file.write(self.cmd_hdr)
        for key in self.cmds:
            file.write(self.cmds[key])
    def print_reload_cmds(self,file):
        file.write(self.cmd_hdr)
        for key in sorted(self.cmds):
            file.write(self.cmds[key])
            
    def updata_smm_cmds(self,tr7,tr7_all):
        new_tr7 = "%016x"%(tr7_all - int(tr7,16))
        new_tr7_tbd = "%016x"%(tr7_all - int(self.cmds[tr7]["tr7_tbd"],16))
        self.add_smm_cmd(tr7, new_tr7, self.cmds[tr7]["rip"], new_tr7_tbd, self.cmds[tr7]["apic_base"])
        
    def print_smm_cmds(self,file,tr7_all):
        file.write(self.cmd_hdr)
        for key in sorted(self.cmds):
            self.updata_smm_cmds(key,tr7_all)
            file.write(self.cmds[key]["cmd"])
        