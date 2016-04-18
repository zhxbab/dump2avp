#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
########################################################
# get_prolog is used for getting tracer prolog information
#
########################################################
import sys,os,re
from operator import eq
sig_name_base = ""
position = 0x0
value = ""
p_flag = 0
with open("apic_prolog_log","r") as fd:
    while True:
        line = fd.readline()
        if line:
            line = line.strip()
            m = re.search(r'name: (APIC\s\w+)', line)
            if m:
                if p_flag:
                    
                    print("\t\"%s\": {\"value\":\"%s\",\"position\":0x%x,\"offset\":0x0,\"size\":0x4,\"DOC\":\"%s \"},\\"%(sig_name_base, value, position, sig_name_base))
                    p_flag = 0
                    sig_name_base = m.group(1)
                else:
                    if eq(sig_name_base,""):
                        sig_name_base = sig_name_base + m.group(1)
                    else:
                        sig_name_base = sig_name_base + "_"+m.group(1)
                    continue
            else:
                m = re.search(r'position: (\w+) and value: (\w+)', line)
                if m:
                    if p_flag :
                        
                        print("\t\"%s_l\": {\"value\":\"%s\",\"position\":0x%x,\"offset\":0x0,\"size\":0x4,\"DOC\":\"%s l \"},\\"%(sig_name_base, value, position, sig_name_base))
                        position = int(m.group(1),16)
                        value = m.group(2)
                        
                        print("\t\"%s_h\": {\"value\":\"%s\",\"position\":0x%x,\"offset\":0x0,\"size\":0x4,\"DOC\":\"%s h \"},\\"%(sig_name_base, value, position, sig_name_base))
                        p_flag = 0
                        sig_name_base = ""
                    else:
                        position = int(m.group(1),16)
                        value = m.group(2)
                        p_flag = 1
                        continue
                    

        else:
            break;
#print(pram_prolog)
