#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
'Mem Moduel'
__author__ = 'Ken Zhao'
from logging import info,debug,error,warning,critical
from operator import eq
class Mem:
    def __init__(self,mem_flag=0x0):
        self.mem_lines = {}
        self.mem_flag = mem_flag    # mem_flag: 0 indicate a data seg in avp, 
                                    # and 1 indicate a code seg in avp
                                    # and 2 indicate hdrs or prologs in avp
    def add_mem_line(self,mem_addr,offset,size,data,doc=""):
        self.mem_lines[mem_addr] = {}
        if size == 0x1:
            if offset == 0x0:
                self.mem_lines[mem_addr]["value"] = "F4F4F4%s; //%s"%(data,doc)
                self.mem_lines[mem_addr]["raw_data"] = "F4F4F4%s"%(data)
                self.mem_lines[mem_addr]["update_flag"] = 0x1
            elif offset == 0x1:
                self.mem_lines[mem_addr]["value"] = "F4F4%sF4; //%s"%(data,doc)
                self.mem_lines[mem_addr]["raw_data"] = "F4F4%sF4"%(data)
                self.mem_lines[mem_addr]["update_flag"] = 0x2
            elif offset == 0x2:
                self.mem_lines[mem_addr]["value"] = "F4%sF4F4; //%s"%(data,doc)
                self.mem_lines[mem_addr]["raw_data"] = "F4%sF4F4"%(data)
                self.mem_lines[mem_addr]["update_flag"] = 0x4
            elif offset == 0x3:
                self.mem_lines[mem_addr]["value"] = "%sF4F4F4; //%s"%(data,doc)
                self.mem_lines[mem_addr]["raw_data"] = "%sF4F4F4"%(data)
                self.mem_lines[mem_addr]["update_flag"] = 0x8
            else:
                error("size is 1, mem addr is %s, but offset %s is invalid"%(mem_addr,offset))
        elif size == 0x2:
            if offset == 0x0:
                self.mem_lines[mem_addr]["value"] = "F4F4%s; //%s"%(data,doc)
                self.mem_lines[mem_addr]["raw_data"] = "F4F4%s"%(data)
                self.mem_lines[mem_addr]["update_flag"] = 0x3
            elif offset == 0x1:
                self.mem_lines[mem_addr]["value"] = "F4%sF4; //%s"%(data,doc)
                self.mem_lines[mem_addr]["raw_data"] = "F4%sF4"%(data)
                self.mem_lines[mem_addr]["update_flag"] = 0x6
            elif offset == 0x2:
                self.mem_lines[mem_addr]["value"] = "%sF4F4; //%s"%(data,doc)
                self.mem_lines[mem_addr]["raw_data"] = "%sF4F4"%(data)
                self.mem_lines[mem_addr]["update_flag"] = 0xc
            else:
                error("size is 2, mem addr is %s, but offset %s is invalid"%(mem_addr,offset))
        elif size == 0x3:
            if offset == 0x0:
                self.mem_lines[mem_addr]["value"] = "F4%s; //%s"%(data,doc)
                self.mem_lines[mem_addr]["raw_data"] = "F4%s"%(data)
                self.mem_lines[mem_addr]["update_flag"] = 0x7
            elif offset == 0x1:
                self.mem_lines[mem_addr]["value"] = "%sF4; //%s"%(data,doc)
                self.mem_lines[mem_addr]["raw_data"] = "%sF4"%(data)
                self.mem_lines[mem_addr]["update_flag"] = 0xe
            else:
                error("size is 3, mem addr is %s, but offset %s is invalid"%(mem_addr,offset))
        elif size == 0x4:
            if offset == 0x0:
                self.mem_lines[mem_addr]["value"] = "%s; //%s"%(data,doc)
                self.mem_lines[mem_addr]["raw_data"] = "%s"%(data)
                self.mem_lines[mem_addr]["update_flag"] = 0xff
            else:
                error("size is 4, mem addr is %s, but offset %s is invalid"%(mem_addr,offset))
        else:
            error("size is %x invalid, mem addr is %s"%(size, mem_addr))
                
    def update_mem_line(self,mem_addr,offset,size,data,doc=""):
        
        if size == 0x1:
            if offset == 0x0:
                self.mem_lines[mem_addr]["value"] = self.mem_lines[mem_addr]["value"][0:6] + data + self.mem_lines[mem_addr]["value"][8:]
                self.mem_lines[mem_addr]["raw_data"] = self.mem_lines[mem_addr]["raw_data"][0:6] + data + self.mem_lines[mem_addr]["raw_data"][8:]
                self.mem_lines[mem_addr]["update_flag"] = self.mem_lines[mem_addr]["update_flag"] | 0x1
            elif offset == 0x1:
                self.mem_lines[mem_addr]["value"] = self.mem_lines[mem_addr]["value"][0:4] + data + self.mem_lines[mem_addr]["value"][6:]
                self.mem_lines[mem_addr]["raw_data"] = self.mem_lines[mem_addr]["raw_data"][0:4] + data + self.mem_lines[mem_addr]["raw_data"][6:]
                self.mem_lines[mem_addr]["update_flag"] = self.mem_lines[mem_addr]["update_flag"] | 0x2
            elif offset == 0x2:
                self.mem_lines[mem_addr]["value"] = self.mem_lines[mem_addr]["value"][0:2] + data + self.mem_lines[mem_addr]["value"][4:]
                self.mem_lines[mem_addr]["raw_data"] = self.mem_lines[mem_addr]["raw_data"][0:2] + data + self.mem_lines[mem_addr]["raw_data"][4:]
                self.mem_lines[mem_addr]["update_flag"] = self.mem_lines[mem_addr]["update_flag"] | 0x4
            elif offset == 0x3:
                self.mem_lines[mem_addr]["value"] = data + self.mem_lines[mem_addr]["value"][2:]
                self.mem_lines[mem_addr]["raw_data"] = data + self.mem_lines[mem_addr]["raw_data"][2:]
                self.mem_lines[mem_addr]["update_flag"] = self.mem_lines[mem_addr]["update_flag"] | 0x8
            else:
                error("updata_mem: size is 1, mem addr is %s, but offset %s is invalid"%(mem_addr,offset))
        elif size == 0x2:
            if offset == 0x0:
                self.mem_lines[mem_addr]["value"] = self.mem_lines[mem_addr]["value"][0:4] + data + self.mem_lines[mem_addr]["value"][8:]
                self.mem_lines[mem_addr]["raw_data"] = self.mem_lines[mem_addr]["raw_data"][0:4] + data + self.mem_lines[mem_addr]["raw_data"][8:]
                self.mem_lines[mem_addr]["update_flag"] = self.mem_lines[mem_addr]["update_flag"] | 0x3
            elif offset == 0x1:
                self.mem_lines[mem_addr]["value"] = self.mem_lines[mem_addr]["value"][0:2]+ data + self.mem_lines[mem_addr]["value"][6:]
                self.mem_lines[mem_addr]["raw_data"] = self.mem_lines[mem_addr]["raw_data"][0:2]+ data + self.mem_lines[mem_addr]["raw_data"][6:]
                self.mem_lines[mem_addr]["update_flag"] = self.mem_lines[mem_addr]["update_flag"] | 0x6
            elif offset == 0x2:
                self.mem_lines[mem_addr]["value"] = data + self.mem_lines[mem_addr]["value"][4:]
                self.mem_lines[mem_addr]["raw_data"] = data + self.mem_lines[mem_addr]["raw_data"][4:]
                self.mem_lines[mem_addr]["update_flag"] = self.mem_lines[mem_addr]["update_flag"] | 0xc
            else:
                error("updata size is 2, mem addr is %s, but offset %s is invalid"%(mem_addr,offset))
        elif size == 0x3:
            if offset == 0x0:
                self.mem_lines[mem_addr]["value"] = self.mem_lines[mem_addr]["value"][0:2] + data + self.mem_lines[mem_addr]["value"][8:]
                self.mem_lines[mem_addr]["raw_data"] = self.mem_lines[mem_addr]["raw_data"][0:2] + data + self.mem_lines[mem_addr]["raw_data"][8:]
                self.mem_lines[mem_addr]["update_flag"] = self.mem_lines[mem_addr]["update_flag"] | 0x7
            elif offset == 0x1:
                self.mem_lines[mem_addr]["value"] = data + self.mem_lines[mem_addr]["value"][6:]
                self.mem_lines[mem_addr]["raw_data"] = data + self.mem_lines[mem_addr]["raw_data"][6:]
                self.mem_lines[mem_addr]["update_flag"] = self.mem_lines[mem_addr]["update_flag"] | 0xe
            else:
                error("updata size is 3, mem addr is %s, but offset %s is invalid"%(mem_addr,offset))
                 
        elif size == 0x4:
            if offset == 0x0:
                self.mem_lines[mem_addr]["value"] = data + self.mem_lines[mem_addr]["value"][8:]
                self.mem_lines[mem_addr]["raw_data"] = data
                self.mem_lines[mem_addr]["update_flag"] = self.mem_lines[mem_addr]["update_flag"] | 0xf
            else:
                error("update size 4, mem addr is %s, but offset %s is invalid"%(mem_addr,offset)) 
        else:
            error("updata_mem: size %x is invalid"%(size))
            
        self.mem_lines[mem_addr]["value"] = self.mem_lines[mem_addr]["value"] + doc
        
    def check_mem_line(self,mem_addr,offset,size,data,doc=""):
        if size<=4 and size>=1:
            for i in range(size):
                new_offset = offset+size-i-1
                #if eq(mem_addr,"F40f0ca0"):
                    #info("update_flag is 0x%02x"%(self.mem_lines[mem_addr]["update_flag"]))
                if not ((self.mem_lines[mem_addr]["update_flag"] >> (new_offset)) & 0x1):
                    if i == 0:
                        self.update_mem_line(mem_addr,new_offset,1,data[i*2:(i+1)*2],doc)#i*2:(i+1)*2
                    else:
                        self.update_mem_line(mem_addr,new_offset,1,data[i*2:(i+1)*2],"")
                else:
                    self.check_smc(self.mem_lines[mem_addr]["raw_data"][2*(3-new_offset):2*(4-new_offset)],data[i*2:(i+1)*2],\
                                   mem_addr,new_offset,self.mem_lines[mem_addr]["raw_data"], size, self.mem_lines[mem_addr]["update_flag"])
        else:
            error("check_mem_line: size is %x invalid, mem addr is %s"%(size, mem_addr))
            
    def check_smc(self,raw_data,new_data,mem_addr,offset,raw_data_all,size,update_flag):
        if not eq(raw_data,new_data):
            if self.mem_flag == 0x1:
                warning("Maybe code mem %s, offset 0x%02x, data %s, new_data %s, raw_data_all %s size 0x%02x, updata_flag 0x%02x occur self-modified code, please check!"\
                %(mem_addr,offset, raw_data, new_data,raw_data_all, size, update_flag))
            elif self.mem_flag == 0x2:
                error("Hdrs and Prologs cannot be recoverd mem %s, offset 0x%02x, data %s, new_data %s, raw_data_all %s size 0x%02x, updata_flag 0x%02x, please check!"\
                %(mem_addr,offset, raw_data, new_data,raw_data_all, size, update_flag))

        