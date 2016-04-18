#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
########################################################
# get_prolog is used for getting tracer prolog information
#
########################################################
import sys,os,re
from operator import eq
pram_prolog = {"pram_data_size": {"value":"0","position":0x0,"offset":0x0,"size":0x4,"DOC":"pram prolog data size "},\
               "pram_type":      {"value":"0","position":0x0,"offset":0x0,"size":0x4,"DOC":"pram prolog type "},\
               }
pram_prolog_start = 0
pram_prolog_end = 0
sig_name_cnt = 0
memread_cnt = 0
memread_start = 1
line_index = 0
last_sig_index = 0xFFFFFFF
cur_sig_index = 0
last_sig_name = ""
with open("pram_prolog","r") as fd:
    while True:
        line = fd.readline()
        if line:
            line = line.strip()
            line_index = line_index + 1
            if re.search(r'pram start',line):
                pram_prolog_start = 1
            if re.search(r'pram end',line):
                pram_prolog_end = 1
            if pram_prolog_start == 1 and pram_prolog_end == 0:
                m = re.search(r'// (\w+)_ADDR', line)
                if m:
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
                    print("position: %x and value: %s"%(int((int(m.group(1),16)-0x78)/4),m.group(2)))
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
