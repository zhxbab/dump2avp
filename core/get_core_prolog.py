#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
########################################################
# get_prolog is used for getting tracer prolog information
#
########################################################
import sys,os,re
from operator import eq
core_prolog = {"core_data_size": {"value":"00000528","position":0x0,"offset":0x0,"size":0x4,"DOC":"core_data_size data "},\
               "core_type":      {"value":"00000040","position":0x0,"offset":0x0,"size":0x4,"DOC":"core_type prolog "},\
               }
core_prolog_start = 0
core_prolog_end = 0
with open("core_prolog","r") as fd:
    while True:
        line = fd.readline()
        if line:
            line = line.strip()
            if re.search(r'core start',line):
                core_prolog_start = 1
            if re.search(r'core end',line):
                core_prolog_end = 1
            if core_prolog_start == 1 and core_prolog_end == 0:
                m = re.search(r'// (\w+)', line)
                if m:
                    if eq("WB",m.group(1)) or eq("Load",m.group(1)) :
                          pass
                    else:
                        print("name: %s"%(m.group(1)))
#                    cur_sig_index = line_index 
#                    if cur_sig_index > last_sig_index + 1:
#                        pram_prolog[m.group(1)] = {"value":"0","position":0x0,"offset":0x0,"size":0x4,"DOC":"%s "%(m.group(1))}
#                    else:
#                        
#                last_sig_index = cur_sig_index
#                last_sig_name = m.group(1)
                m = re.search(r'memread    0x003FF0(\w+)    0x(\w+)', line)
                if m:
                    print("position: %x and value: %s"%(int((int(m.group(1),16)-0x78-0x6C8)/4),m.group(2)))
#                    memread_cnt = memread_cnt + 1
#                    if memread_cnt == 1:
#                        pram_prolog["pram_data_size"]["value"] = m.group(2)
#                        pram_prolog["pram_data_size"]["postion"] = 
#                    elif memread_cnt == 2:
#                        pram_prolog["pram_type"]["value"] = m.group(2)
#                        pram_prolog["pram_type"]["postion"] = int((int(m.group(1),16)-0x78)/4)
#                    else:
#                        pass
#                
        else:
            break;
