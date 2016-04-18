#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
'Avp Moduel'
__author__ = 'Ken Zhao'
import os, sys, re, tracer
from logging import info,debug,error,warning,critical
from mem import Mem
from operator import eq
#0x6000 is the mem space that used for this header. format is \t\tmem\taddr\tdata
#0x3FF00000 is tracer replay addr, 0x922F3AEF is msr 0x1523 eax passwd, 0x4D4653E3 is msr 0x1523 edx passwd
class Avp:
    def __init__(self):
        self.__replay_addr_h = "4000"
        self.__replay_addr_type2_h = "4002"
        self.__replay_addr_l = "0000"
        self.__passwd_eax_h = "922F"
        self.__passwd_edx_h = "4D46"
        self.__passwd_eax_l = "3AEF"
        self.__passwd_edx_l = "53E3"
        
    def gen_reset_code(self): 
        header = "test 0\n\
initial {\n\
\t//  RESET starts here\n\
        mem     0x0000006000    0x%sB866;\n\
        mem     0x0000006004    0xBA66%s;\n\
        mem     0x0000006008    0x%s%s;\n\
        mem     0x000000600C    0x1523B966;\n\
        mem     0x0000006010    0x300F0000;\n\
        mem     0x0000006014    0x0000B866;\n\
        mem     0x0000006018    0xBA66%s;\n\
        mem     0x000000601C    0x%s0000;\n\
        mem     0x0000006020    0x317BB966;\n\
        mem     0x0000006024    0x320F0000;\n\
        mem     0x00FFFFFFF0    0x006000EA;\n\
        mem     0x00FFFFFFF4    0x00000000;\n"\
        %(self.__passwd_eax_l, self.__passwd_eax_h,\
        self.__passwd_edx_h, self.__passwd_edx_l,\
        self.__replay_addr_h, self.__replay_addr_l)
        self.avp_handle.write(header)
        
    def adjust_data(self, size, data):
        new_data = ""
        for i in range(0,2*size,2):
            new_data = data[i:i+2] + new_data 
        return new_data
    
    def end_section(self): 
        self.avp_handle.write("}\n")
    
    def update_major_header(self,tracer_dump):
        
        tracer.MAJOR_HEADER["next_lip_h"]["value"] = tracer_dump["RIP"]["value_h"].upper()
        tracer.MAJOR_HEADER["next_lip_l"]["value"] = tracer_dump["RIP"]["value_l"].upper()
        tracer.MAJOR_HEADER["ctr_0_h"]["value"] = tracer_dump["TR7"]["value_h"].upper()
        tracer.MAJOR_HEADER["ctr_0_l"]["value"] = tracer_dump["TR7"]["value_l"].upper()
        tracer.MAJOR_HEADER["dump_vector"]["value"] = "%04x"%(tracer.TR3)
        
    def update_major_header_type2(self,tracer_dump):
        
        tracer.MAJOR_HEADER_type2["next_lip_h"]["value"] = tracer_dump["RIP"]["value_h"].upper()
        tracer.MAJOR_HEADER_type2["next_lip_l"]["value"] = tracer_dump["RIP"]["value_l"].upper()
        tracer.MAJOR_HEADER_type2["ctr_0_h"]["value"] = tracer_dump["TR7"]["value_h"].upper()
        tracer.MAJOR_HEADER_type2["ctr_0_l"]["value"] = tracer_dump["TR7"]["value_l"].upper()
        tracer.MAJOR_HEADER_type2["dump_vector"]["value"] = "%04x"%(tracer.TR3_2)
        tracer.MAJOR_HEADER_type2["hdr_details"]["value"] = "%04x"%(tracer.TR3_2)
        tracer.MAJOR_HEADER_type2["events"]["value"] = tracer_dump["EVENTS"]["value"].upper()
        
    def gen_major_header(self,tracer_dump): 
        
        self.update_major_header(tracer_dump)
        major_header = Mem(2);
        self.avp_handle.write("\t//  START OF Program & Data\n")
        tracer.total_size = tracer.major_header_size
        for key in tracer.MAJOR_HEADER:
            mem_addr = "%04x"%(tracer.MAJOR_HEADER[key]["position"]*4)
            
            if mem_addr in major_header.mem_lines:
                major_header.check_mem_line(mem_addr, tracer.MAJOR_HEADER[key]["offset"],tracer.MAJOR_HEADER[key]["size"],tracer.MAJOR_HEADER[key]["value"],tracer.MAJOR_HEADER[key]["DOC"])
            else:
                major_header.add_mem_line(mem_addr, tracer.MAJOR_HEADER[key]["offset"],tracer.MAJOR_HEADER[key]["size"],tracer.MAJOR_HEADER[key]["value"],tracer.MAJOR_HEADER[key]["DOC"])
        for key in sorted(major_header.mem_lines):
            
            self.avp_handle.write("\tmem\t0x00%s%s\t0x%s\n"%(self.__replay_addr_h,key,major_header.mem_lines[key]["value"]))
        del(major_header)
        
    def gen_major_header_type2(self,tracer_dump,replay_addr): 
        if not tracer_dump["occur"]:
            return
        self.update_major_header_type2(tracer_dump)
        major_header = Mem(2);
        self.avp_handle.write("\t//  TRACER DUMP TYPE 2\n")
        tracer.total_size = tracer.major_header_size
        for key in tracer.MAJOR_HEADER_type2:
            mem_addr = "%04x"%(tracer.MAJOR_HEADER_type2[key]["position"]*4)
            
            if mem_addr in major_header.mem_lines:
                major_header.check_mem_line(mem_addr, tracer.MAJOR_HEADER_type2[key]["offset"],tracer.MAJOR_HEADER_type2[key]["size"],tracer.MAJOR_HEADER_type2[key]["value"],tracer.MAJOR_HEADER_type2[key]["DOC"])
            else:
                major_header.add_mem_line(mem_addr, tracer.MAJOR_HEADER_type2[key]["offset"],tracer.MAJOR_HEADER_type2[key]["size"],tracer.MAJOR_HEADER_type2[key]["value"],tracer.MAJOR_HEADER_type2[key]["DOC"])
        for key in sorted(major_header.mem_lines):
            
            self.avp_handle.write("\tmem\t0x00%s%s\t0x%s\n"%(replay_addr,key,major_header.mem_lines[key]["value"]))
        del(major_header)
        
    def gen_sub_headers(self,subhdr,replay_addr):
        
        sub_hdr = Mem(2);
        for key in subhdr:
            if eq(key,"hdr_size") or eq(key,"offset"):
                continue
            else:
                mem_addr = "%04x"%(subhdr[key]["position"]*4 + tracer.total_size)
                
                if mem_addr in sub_hdr.mem_lines:
                    sub_hdr.check_mem_line(mem_addr,subhdr[key]["offset"],subhdr[key]["size"],subhdr[key]["value"],subhdr[key]["DOC"])
                else:
                    sub_hdr.add_mem_line(mem_addr,subhdr[key]["offset"],subhdr[key]["size"],subhdr[key]["value"],subhdr[key]["DOC"])
                
        for key in sorted(sub_hdr.mem_lines):
            self.avp_handle.write("\tmem\t0x00%s%s\t0x%s\n"%(replay_addr,key,sub_hdr.mem_lines[key]["value"]))
        del(sub_hdr)
        
    def update_sub_header_jwad_exception(self,tracer_dump):
        
        tracer.JWAD_EXCEPTION_SUBHDR["cr0"]["value"] = tracer_dump["CR0"]["value_l"]
        tracer.JWAD_EXCEPTION_SUBHDR["cr4"]["value"] = tracer_dump["CR4"]["value_l"]
        tracer.JWAD_EXCEPTION_SUBHDR["cr8"]["value"] = tracer_dump["CR8"]["value_l"]
        tracer.JWAD_EXCEPTION_SUBHDR["cr2_l"]["value"] = tracer_dump["CR2"]["value_l"]
        tracer.JWAD_EXCEPTION_SUBHDR["cr2_h"]["value"] = tracer_dump["CR2"]["value_h"]
        tracer.JWAD_EXCEPTION_SUBHDR["ecx"]["value"] = tracer_dump["RCX"]["value_l"]
        
    
    
    def update_sub_header_mperf(self,tracer_dump):
        pass
    
    def update_sub_header_nano_pebs(self,tracer_dump):
        pass
    
    def update_sub_header_pebs_jwad2(self,tracer_dump):
        tracer.PEBS_JWAD2_SUBHDR["rax_l"]["value"] = tracer_dump["RAX"]["value_l"]
        tracer.PEBS_JWAD2_SUBHDR["rax_h"]["value"] = tracer_dump["RAX"]["value_h"]
        tracer.PEBS_JWAD2_SUBHDR["rbx_l"]["value"] = tracer_dump["RBX"]["value_l"]
        tracer.PEBS_JWAD2_SUBHDR["rbx_h"]["value"] = tracer_dump["RBX"]["value_h"]
        tracer.PEBS_JWAD2_SUBHDR["rcx_l"]["value"] = tracer_dump["RCX"]["value_l"]
        tracer.PEBS_JWAD2_SUBHDR["rcx_h"]["value"] = tracer_dump["RCX"]["value_h"]
        tracer.PEBS_JWAD2_SUBHDR["rdx_l"]["value"] = tracer_dump["RDX"]["value_l"]
        tracer.PEBS_JWAD2_SUBHDR["rdx_h"]["value"] = tracer_dump["RDX"]["value_h"]
    
    def update_sub_headers(self,subhdr,tracer_dump,replay_addr):
        if not tracer_dump["occur"]:
            return
        
        if subhdr is tracer.JWAD_EXCEPTION_SUBHDR:
            self.update_sub_header_jwad_exception(tracer_dump)
            
        elif subhdr is tracer.MPERF_SUBHDR:
            self.update_sub_header_mperf(tracer_dump)
            
        elif subhdr is tracer.NANO_PEBS_SUBHDR:
            self.update_sub_header_nano_pebs(tracer_dump)
            
        elif subhdr is tracer.PEBS_JWAD2_SUBHDR:    
            self.update_sub_header_pebs_jwad2(tracer_dump)
            
        else:
            error("wrong sub header!")
        
        self.gen_sub_headers(subhdr,replay_addr)
        tracer.total_size = subhdr["hdr_size"] + tracer.total_size
        
    def update_fxsave_prolog(self,tracer_dump):
        pass
    
    def update_pram_prolog(self,tracer_dump):
        
        tracer.PRAM_PROLOG["TR1_l"]["value"] = tracer.TR1
        tracer.PRAM_PROLOG["TR3_l"]["value"] = "%04x%04x"%(tracer.TR3_1,tracer.TR3)
        tracer.PRAM_PROLOG["TR3_h"]["value"] = "%04x%04x"%(tracer.TR3_3,tracer.TR3_2)
        #tracer.PRAM_PROLOG["IO_RSTRT_ECX_l"]["value"] = tracer_dump["RCX"]["value_l"]
        #tracer.PRAM_PROLOG["IO_RSTRT_ECX_h"]["value"] = tracer_dump["RCX"]["value_h"]
        #tracer.PRAM_PROLOG["IO_RSTRT_ESI_l"]["value"] = tracer_dump["RSI"]["value_l"]
        #tracer.PRAM_PROLOG["IO_RSTRT_ESI_h"]["value"] = tracer_dump["RSI"]["value_h"]
        #tracer.PRAM_PROLOG["IO_RSTRT_EDI_l"]["value"] = tracer_dump["RDI"]["value_l"]
        #tracer.PRAM_PROLOG["IO_RSTRT_EDI_h"]["value"] = tracer_dump["RDI"]["value_h"]
#         tracer.PRAM_PROLOG["IO_RSTRT_EIP_l"]["value"] = tracer_dump["RIP"]["value_l"]
#         tracer.PRAM_PROLOG["IO_RSTRT_EIP_h"]["value"] = tracer_dump["RIP"]["value_h"]
        tracer.PRAM_PROLOG["CR2_l"]["value"] = tracer_dump["CR2"]["value_l"]
        tracer.PRAM_PROLOG["CR2_h"]["value"] = tracer_dump["CR2"]["value_h"]
        tracer.PRAM_PROLOG["CR3_l"]["value"] = tracer_dump["CR3"]["value_l"]
        tracer.PRAM_PROLOG["CR3_h"]["value"] = tracer_dump["CR3"]["value_h"]
        tracer.PRAM_PROLOG["HARDWARE_CR3_l"]["value"] = tracer_dump["CR3"]["value_l"]
        tracer.PRAM_PROLOG["HARDWARE_CR3_h"]["value"] = tracer_dump["CR3"]["value_h"]
        tracer.PRAM_PROLOG["ES_PRAM_CS_PRAM"]["value"] = tracer_dump["CS"]["value"] + tracer_dump["ES"]["value"]
        tracer.PRAM_PROLOG["SS_PRAM_DS_PRAM"]["value"] = tracer_dump["DS"]["value"] + tracer_dump["SS"]["value"]
        tracer.PRAM_PROLOG["FS_PRAM_GS_PRAM"]["value"] = tracer_dump["GS"]["value"] + tracer_dump["FS"]["value"]
        tracer.PRAM_PROLOG["TR_PRAM_LDT_PRAM"]["value"] = tracer_dump["LDTR"]["value"] + tracer_dump["TR"]["value"]
        #tracer.PRAM_PROLOG["MSR_IA32_TSC_ADJUST_l"]["value"] = tracer_dump["MSR_3b"]["value_l"]
        #tracer.PRAM_PROLOG["MSR_IA32_TSC_ADJUST_h"]["value"] = tracer_dump["MSR_3b"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE0_l"]["value"] = tracer_dump["MSR_200"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE0_h"]["value"] = tracer_dump["MSR_200"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK0_l"]["value"] = tracer_dump["MSR_201"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK0_h"]["value"] = tracer_dump["MSR_201"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE1_l"]["value"] = tracer_dump["MSR_202"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE1_h"]["value"] = tracer_dump["MSR_202"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK1_l"]["value"] = tracer_dump["MSR_203"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK1_h"]["value"] = tracer_dump["MSR_203"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE2_l"]["value"] = tracer_dump["MSR_204"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE2_h"]["value"] = tracer_dump["MSR_204"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK2_l"]["value"] = tracer_dump["MSR_205"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK2_h"]["value"] = tracer_dump["MSR_205"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE3_l"]["value"] = tracer_dump["MSR_206"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE3_h"]["value"] = tracer_dump["MSR_206"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK3_l"]["value"] = tracer_dump["MSR_207"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK3_h"]["value"] = tracer_dump["MSR_207"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE4_l"]["value"] = tracer_dump["MSR_208"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE4_h"]["value"] = tracer_dump["MSR_208"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK4_l"]["value"] = tracer_dump["MSR_209"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK4_h"]["value"] = tracer_dump["MSR_209"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE5_l"]["value"] = tracer_dump["MSR_20a"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE5_h"]["value"] = tracer_dump["MSR_20a"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK5_l"]["value"] = tracer_dump["MSR_20b"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK5_h"]["value"] = tracer_dump["MSR_20b"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE6_l"]["value"] = tracer_dump["MSR_20c"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE6_h"]["value"] = tracer_dump["MSR_20c"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK6_l"]["value"] = tracer_dump["MSR_20d"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK6_h"]["value"] = tracer_dump["MSR_20d"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE7_l"]["value"] = tracer_dump["MSR_20e"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSBASE7_h"]["value"] = tracer_dump["MSR_20e"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK7_l"]["value"] = tracer_dump["MSR_20f"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_PHYSMASK7_h"]["value"] = tracer_dump["MSR_20f"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_FIX64K_00000_l"]["value"] = tracer_dump["MSR_250"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_FIX64K_00000_h"]["value"] = tracer_dump["MSR_250"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_FIX16K_80000_l"]["value"] = tracer_dump["MSR_258"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_FIX16K_80000_h"]["value"] = tracer_dump["MSR_258"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_FIX16K_A0000_l"]["value"] = tracer_dump["MSR_259"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_FIX16K_A0000_h"]["value"] = tracer_dump["MSR_259"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_C0000_l"]["value"] = tracer_dump["MSR_268"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_C0000_h"]["value"] = tracer_dump["MSR_268"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_C8000_l"]["value"] = tracer_dump["MSR_269"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_C8000_h"]["value"] = tracer_dump["MSR_269"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_D0000_l"]["value"] = tracer_dump["MSR_26a"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_D0000_h"]["value"] = tracer_dump["MSR_26a"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_D8000_l"]["value"] = tracer_dump["MSR_26b"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_D8000_h"]["value"] = tracer_dump["MSR_26b"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_E0000_l"]["value"] = tracer_dump["MSR_26c"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_E0000_h"]["value"] = tracer_dump["MSR_26c"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_E8000_l"]["value"] = tracer_dump["MSR_26d"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_E8000_h"]["value"] = tracer_dump["MSR_26d"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_F0000_l"]["value"] = tracer_dump["MSR_26e"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_F0000_h"]["value"] = tracer_dump["MSR_26e"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_F8000_l"]["value"] = tracer_dump["MSR_26f"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_FIX4K_F8000_h"]["value"] = tracer_dump["MSR_26f"]["value_h"]
        tracer.PRAM_PROLOG["MTRR_DEF_TYPE_l"]["value"] = tracer_dump["MSR_2ff"]["value_l"]
        tracer.PRAM_PROLOG["MTRR_DEF_TYPE_h"]["value"] = tracer_dump["MSR_2ff"]["value_h"]
        tracer.PRAM_PROLOG["TR7_l"]["value"] = tracer_dump["_TR7"]["value_l"]
        tracer.PRAM_PROLOG["TR7_h"]["value"] = tracer_dump["_TR7"]["value_h"]
        tracer.PRAM_PROLOG["SMRR_BASE_l"]["value"] = "%08x"%(tracer.SMM_BASE+tracer.SMRAM_TYPE)
        tracer.PRAM_PROLOG["SMRR_MASK_l"]["value"] = "FFFF0800" # 0 indicate in, F indicate out
        tracer.PRAM_PROLOG["FCR5_h"]["value"] = "%08x"%(tracer.SMM_BASE)# CNR use FCR5[32-63] = SMM base address MSR 
        #instead of SMRR_BASE and SMRR_MASK if 30000, smm mode addr is 3fffc(+8000 +7ffc)
        #SMRR_BASE_l and SMRR_MASK_l only decide the attribute
        # bochs don't have this msr. need to sync every smm mode.
         #put the bochs code to cnsim CFF000000
    def update_core_prolog(self,tracer_dump):
        
        tracer.CORE_PROLOG["RAX_l"]["value"] = tracer_dump["RAX"]["value_l"]
        tracer.CORE_PROLOG["RAX_h"]["value"] = tracer_dump["RAX"]["value_h"]
        tracer.CORE_PROLOG["RBX_l"]["value"] = tracer_dump["RBX"]["value_l"]
        tracer.CORE_PROLOG["RBX_h"]["value"] = tracer_dump["RBX"]["value_h"]
        tracer.CORE_PROLOG["RCX_l"]["value"] = tracer_dump["RCX"]["value_l"]
        tracer.CORE_PROLOG["RCX_h"]["value"] = tracer_dump["RCX"]["value_h"]
        tracer.CORE_PROLOG["RDX_l"]["value"] = tracer_dump["RDX"]["value_l"]
        tracer.CORE_PROLOG["RDX_h"]["value"] = tracer_dump["RDX"]["value_h"]
        tracer.CORE_PROLOG["RSP_l"]["value"] = tracer_dump["RSP"]["value_l"]
        tracer.CORE_PROLOG["RSP_h"]["value"] = tracer_dump["RSP"]["value_h"]
        tracer.CORE_PROLOG["RBP_l"]["value"] = tracer_dump["RBP"]["value_l"]
        tracer.CORE_PROLOG["RBP_h"]["value"] = tracer_dump["RBP"]["value_h"]
        tracer.CORE_PROLOG["RDI_l"]["value"] = tracer_dump["RDI"]["value_l"]
        tracer.CORE_PROLOG["RDI_h"]["value"] = tracer_dump["RDI"]["value_h"]
        tracer.CORE_PROLOG["RSI_l"]["value"] = tracer_dump["RSI"]["value_l"]
        tracer.CORE_PROLOG["RSI_h"]["value"] = tracer_dump["RSI"]["value_h"]
        tracer.CORE_PROLOG["R8_l"]["value"] = tracer_dump["R8"]["value_l"]
        tracer.CORE_PROLOG["R8_h"]["value"] = tracer_dump["R8"]["value_h"]
        tracer.CORE_PROLOG["R9_l"]["value"] = tracer_dump["R9"]["value_l"]
        tracer.CORE_PROLOG["R9_h"]["value"] = tracer_dump["R9"]["value_h"]
        tracer.CORE_PROLOG["R10_l"]["value"] = tracer_dump["R10"]["value_l"]
        tracer.CORE_PROLOG["R10_h"]["value"] = tracer_dump["R10"]["value_h"]
        tracer.CORE_PROLOG["R11_l"]["value"] = tracer_dump["R11"]["value_l"]
        tracer.CORE_PROLOG["R11_h"]["value"] = tracer_dump["R11"]["value_h"]
        tracer.CORE_PROLOG["R12_l"]["value"] = tracer_dump["R12"]["value_l"]
        tracer.CORE_PROLOG["R12_h"]["value"] = tracer_dump["R12"]["value_h"]
        tracer.CORE_PROLOG["R13_l"]["value"] = tracer_dump["R13"]["value_l"]
        tracer.CORE_PROLOG["R13_h"]["value"] = tracer_dump["R13"]["value_h"]
        tracer.CORE_PROLOG["R14_l"]["value"] = tracer_dump["R14"]["value_l"]
        tracer.CORE_PROLOG["R14_h"]["value"] = tracer_dump["R14"]["value_h"]
        tracer.CORE_PROLOG["R15_l"]["value"] = tracer_dump["R15"]["value_l"]
        tracer.CORE_PROLOG["R15_h"]["value"] = tracer_dump["R15"]["value_h"]
        tracer.CORE_PROLOG["ESdesc_l"]["value"] = tracer_dump["ES"]["value_l"]
        tracer.CORE_PROLOG["ESdesc_h"]["value"] = tracer_dump["ES"]["value_h"]
        tracer.CORE_PROLOG["CSdesc_l"]["value"] = tracer_dump["CS"]["value_l"]
        tracer.CORE_PROLOG["CSdesc_h"]["value"] = tracer_dump["CS"]["value_h"]
        tracer.CORE_PROLOG["DSdesc_l"]["value"] = tracer_dump["DS"]["value_l"]
        tracer.CORE_PROLOG["DSdesc_h"]["value"] = tracer_dump["DS"]["value_h"]
        tracer.CORE_PROLOG["SSdesc_l"]["value"] = tracer_dump["SS"]["value_l"]
        tracer.CORE_PROLOG["SSdesc_h"]["value"] = tracer_dump["SS"]["value_h"]
        tracer.CORE_PROLOG["FSdesc_l"]["value"] = tracer_dump["FS"]["value_l"]
        tracer.CORE_PROLOG["FSdesc_h"]["value"] = tracer_dump["FS"]["value_h"]
        tracer.CORE_PROLOG["GSdesc_l"]["value"] = tracer_dump["GS"]["value_l"]
        tracer.CORE_PROLOG["GSdesc_h"]["value"] = tracer_dump["GS"]["value_h"]
        tracer.CORE_PROLOG["GDTdesc_l"]["value"] = tracer_dump["GDTR"]["base"][12:16] + tracer_dump["GDTR"]["limit"].zfill(4)
        tracer.CORE_PROLOG["GDTdesc_h"]["value"] = "000082"+tracer_dump["GDTR"]["base"][10:12] #sync with cnsim GTD_Descriptor
        tracer.CORE_PROLOG["IDTdesc_l"]["value"] = tracer_dump["IDTR"]["base"][12:16] + tracer_dump["IDTR"]["limit"].zfill(4)
        tracer.CORE_PROLOG["IDTdesc_h"]["value"] = "000082"+tracer_dump["IDTR"]["base"][10:12] #sync with cnsim ITD_Descriptor
        tracer.CORE_PROLOG["LDTdesc_l"]["value"] = tracer_dump["LDTR"]["value_l"]
        tracer.CORE_PROLOG["LDTdesc_h"]["value"] = tracer_dump["LDTR"]["value_h"]
        tracer.CORE_PROLOG["TSSdesc_l"]["value"] = tracer_dump["TR"]["value_l"]
        tracer.CORE_PROLOG["TSSdesc_h"]["value"] = tracer_dump["TR"]["value_h"]
        tracer.CORE_PROLOG["FP_SW"]["value"] = tracer_dump["STATUS_W"]["value"]
        tracer.CORE_PROLOG["FP_CW"]["value"] = tracer_dump["CONTROL_W"]["value"]
        tracer.CORE_PROLOG["FPTAG"]["value"] = tracer_dump["TAG_W"]["value"]
        tracer.CORE_PROLOG["FPCS"]["value"] = tracer_dump["FCS"]["value"]
        tracer.CORE_PROLOG["FPDS"]["value"] = tracer_dump["FDS"]["value"]
        tracer.CORE_PROLOG["FPLOP"]["value"] = tracer_dump["OPERAND"]["value"].zfill(8)
        tracer.CORE_PROLOG["FPLIP_l"]["value"] = tracer_dump["FIP"]["value_l"]
        tracer.CORE_PROLOG["FPLIP_h"]["value"] = tracer_dump["FIP"]["value_h"]
        tracer.CORE_PROLOG["FPLA_l"]["value"] = tracer_dump["FDP"]["value_l"]
        tracer.CORE_PROLOG["FPLA_h"]["value"] = tracer_dump["FDP"]["value_h"]
        tracer.CORE_PROLOG["MXCSR"]["value"] = tracer_dump["MXCSR"]["value"]
        tracer.CORE_PROLOG["st7_0"]["value"] = tracer_dump["FP7_ST7"]["value_l"]
        tracer.CORE_PROLOG["st7_1"]["value"] = tracer_dump["FP7_ST7"]["value_h"]
        tracer.CORE_PROLOG["st7_2"]["value"] = "0000"+tracer_dump["FP7_ST7"]["value"]
        tracer.CORE_PROLOG["st7_3"]["value"] = "00000000"
        tracer.CORE_PROLOG["st0_0"]["value"] = tracer_dump["FP1_ST1"]["value_l"]
        tracer.CORE_PROLOG["st0_1"]["value"] = tracer_dump["FP1_ST1"]["value_h"]
        tracer.CORE_PROLOG["st0_2"]["value"] = "0000"+tracer_dump["FP1_ST1"]["value"]
        tracer.CORE_PROLOG["st0_3"]["value"] = "00000000"
        tracer.CORE_PROLOG["st1_0"]["value"] = tracer_dump["FP2_ST2"]["value_l"]
        tracer.CORE_PROLOG["st1_1"]["value"] = tracer_dump["FP2_ST2"]["value_h"]
        tracer.CORE_PROLOG["st1_2"]["value"] = "0000"+tracer_dump["FP2_ST2"]["value"]
        tracer.CORE_PROLOG["st1_3"]["value"] = "00000000"
        tracer.CORE_PROLOG["st2_0"]["value"] = tracer_dump["FP2_ST2"]["value_l"]
        tracer.CORE_PROLOG["st2_1"]["value"] = tracer_dump["FP2_ST2"]["value_h"]
        tracer.CORE_PROLOG["st2_2"]["value"] = "0000"+tracer_dump["FP2_ST2"]["value"]
        tracer.CORE_PROLOG["st2_3"]["value"] = "00000000"
        tracer.CORE_PROLOG["st3_0"]["value"] = tracer_dump["FP3_ST3"]["value_l"]
        tracer.CORE_PROLOG["st3_1"]["value"] = tracer_dump["FP3_ST3"]["value_h"]
        tracer.CORE_PROLOG["st3_2"]["value"] = "0000"+tracer_dump["FP3_ST3"]["value"]
        tracer.CORE_PROLOG["st3_3"]["value"] = "00000000"
        tracer.CORE_PROLOG["st4_0"]["value"] = tracer_dump["FP4_ST4"]["value_l"]
        tracer.CORE_PROLOG["st4_1"]["value"] = tracer_dump["FP4_ST4"]["value_h"]
        tracer.CORE_PROLOG["st4_2"]["value"] = "0000"+tracer_dump["FP4_ST4"]["value"]
        tracer.CORE_PROLOG["st4_3"]["value"] = "00000000"
        tracer.CORE_PROLOG["st5_0"]["value"] = tracer_dump["FP5_ST5"]["value_l"]
        tracer.CORE_PROLOG["st5_1"]["value"] = tracer_dump["FP5_ST5"]["value_h"]
        tracer.CORE_PROLOG["st5_2"]["value"] = "0000"+tracer_dump["FP5_ST5"]["value"]
        tracer.CORE_PROLOG["st5_3"]["value"] = "00000000"
        tracer.CORE_PROLOG["st6_0"]["value"] = tracer_dump["FP6_ST6"]["value_l"]
        tracer.CORE_PROLOG["st6_1"]["value"] = tracer_dump["FP6_ST6"]["value_h"]
        tracer.CORE_PROLOG["st6_2"]["value"] = "0000"+tracer_dump["FP6_ST6"]["value"]
        tracer.CORE_PROLOG["st6_3"]["value"] = "00000000"
        
        tracer.CORE_PROLOG["xmm0_0"]["value"] = tracer_dump["VMM00"]["data_0"]
        tracer.CORE_PROLOG["xmm0_1"]["value"] = tracer_dump["VMM00"]["data_1"]
        tracer.CORE_PROLOG["xmm0_2"]["value"] = tracer_dump["VMM00"]["data_2"]
        tracer.CORE_PROLOG["xmm0_3"]["value"] = tracer_dump["VMM00"]["data_3"]
        tracer.CORE_PROLOG["xmm1_0"]["value"] = tracer_dump["VMM01"]["data_0"]
        tracer.CORE_PROLOG["xmm1_1"]["value"] = tracer_dump["VMM01"]["data_1"]
        tracer.CORE_PROLOG["xmm1_2"]["value"] = tracer_dump["VMM01"]["data_2"]
        tracer.CORE_PROLOG["xmm1_3"]["value"] = tracer_dump["VMM01"]["data_3"]
        tracer.CORE_PROLOG["xmm2_0"]["value"] = tracer_dump["VMM02"]["data_0"]
        tracer.CORE_PROLOG["xmm2_1"]["value"] = tracer_dump["VMM02"]["data_1"]
        tracer.CORE_PROLOG["xmm2_2"]["value"] = tracer_dump["VMM02"]["data_2"]
        tracer.CORE_PROLOG["xmm2_3"]["value"] = tracer_dump["VMM02"]["data_3"]
        tracer.CORE_PROLOG["xmm3_0"]["value"] = tracer_dump["VMM03"]["data_0"]
        tracer.CORE_PROLOG["xmm3_1"]["value"] = tracer_dump["VMM03"]["data_1"]
        tracer.CORE_PROLOG["xmm3_2"]["value"] = tracer_dump["VMM03"]["data_2"]
        tracer.CORE_PROLOG["xmm3_3"]["value"] = tracer_dump["VMM03"]["data_3"]
        tracer.CORE_PROLOG["xmm4_0"]["value"] = tracer_dump["VMM04"]["data_0"]
        tracer.CORE_PROLOG["xmm4_1"]["value"] = tracer_dump["VMM04"]["data_1"]
        tracer.CORE_PROLOG["xmm4_2"]["value"] = tracer_dump["VMM04"]["data_2"]
        tracer.CORE_PROLOG["xmm4_3"]["value"] = tracer_dump["VMM04"]["data_3"]
        tracer.CORE_PROLOG["xmm5_0"]["value"] = tracer_dump["VMM05"]["data_0"]
        tracer.CORE_PROLOG["xmm5_1"]["value"] = tracer_dump["VMM05"]["data_1"]
        tracer.CORE_PROLOG["xmm5_2"]["value"] = tracer_dump["VMM05"]["data_2"]
        tracer.CORE_PROLOG["xmm5_3"]["value"] = tracer_dump["VMM05"]["data_3"]
        tracer.CORE_PROLOG["xmm6_0"]["value"] = tracer_dump["VMM06"]["data_0"]
        tracer.CORE_PROLOG["xmm6_1"]["value"] = tracer_dump["VMM06"]["data_1"]
        tracer.CORE_PROLOG["xmm6_2"]["value"] = tracer_dump["VMM06"]["data_2"]
        tracer.CORE_PROLOG["xmm6_3"]["value"] = tracer_dump["VMM06"]["data_3"]
        tracer.CORE_PROLOG["xmm7_0"]["value"] = tracer_dump["VMM07"]["data_0"]
        tracer.CORE_PROLOG["xmm7_1"]["value"] = tracer_dump["VMM07"]["data_1"]
        tracer.CORE_PROLOG["xmm7_2"]["value"] = tracer_dump["VMM07"]["data_2"]
        tracer.CORE_PROLOG["xmm7_3"]["value"] = tracer_dump["VMM07"]["data_3"]
        tracer.CORE_PROLOG["xmm8_0"]["value"] = tracer_dump["VMM00"]["data_0"]
        tracer.CORE_PROLOG["xmm8_1"]["value"] = tracer_dump["VMM00"]["data_1"]
        tracer.CORE_PROLOG["xmm8_2"]["value"] = tracer_dump["VMM00"]["data_2"]
        tracer.CORE_PROLOG["xmm8_3"]["value"] = tracer_dump["VMM00"]["data_3"]
        tracer.CORE_PROLOG["xmm9_0"]["value"] = tracer_dump["VMM01"]["data_0"]
        tracer.CORE_PROLOG["xmm9_1"]["value"] = tracer_dump["VMM01"]["data_1"]
        tracer.CORE_PROLOG["xmm9_2"]["value"] = tracer_dump["VMM01"]["data_2"]
        tracer.CORE_PROLOG["xmm9_3"]["value"] = tracer_dump["VMM01"]["data_3"]
        tracer.CORE_PROLOG["xmm10_0"]["value"] = tracer_dump["VMM10"]["data_0"]
        tracer.CORE_PROLOG["xmm10_1"]["value"] = tracer_dump["VMM10"]["data_1"]
        tracer.CORE_PROLOG["xmm10_2"]["value"] = tracer_dump["VMM10"]["data_2"]
        tracer.CORE_PROLOG["xmm10_3"]["value"] = tracer_dump["VMM10"]["data_3"]
        tracer.CORE_PROLOG["xmm11_0"]["value"] = tracer_dump["VMM11"]["data_0"]
        tracer.CORE_PROLOG["xmm11_1"]["value"] = tracer_dump["VMM11"]["data_1"]
        tracer.CORE_PROLOG["xmm11_2"]["value"] = tracer_dump["VMM11"]["data_2"]
        tracer.CORE_PROLOG["xmm11_3"]["value"] = tracer_dump["VMM11"]["data_3"]
        tracer.CORE_PROLOG["xmm12_0"]["value"] = tracer_dump["VMM12"]["data_0"]
        tracer.CORE_PROLOG["xmm12_1"]["value"] = tracer_dump["VMM12"]["data_1"]
        tracer.CORE_PROLOG["xmm12_2"]["value"] = tracer_dump["VMM12"]["data_2"]
        tracer.CORE_PROLOG["xmm12_3"]["value"] = tracer_dump["VMM12"]["data_3"]
        tracer.CORE_PROLOG["xmm13_0"]["value"] = tracer_dump["VMM13"]["data_0"]
        tracer.CORE_PROLOG["xmm13_1"]["value"] = tracer_dump["VMM13"]["data_1"]
        tracer.CORE_PROLOG["xmm13_2"]["value"] = tracer_dump["VMM13"]["data_2"]
        tracer.CORE_PROLOG["xmm13_3"]["value"] = tracer_dump["VMM13"]["data_3"]
        tracer.CORE_PROLOG["xmm14_0"]["value"] = tracer_dump["VMM14"]["data_0"]
        tracer.CORE_PROLOG["xmm14_1"]["value"] = tracer_dump["VMM14"]["data_1"]
        tracer.CORE_PROLOG["xmm14_2"]["value"] = tracer_dump["VMM14"]["data_2"]
        tracer.CORE_PROLOG["xmm14_3"]["value"] = tracer_dump["VMM14"]["data_3"]
        tracer.CORE_PROLOG["xmm15_0"]["value"] = tracer_dump["VMM15"]["data_0"]
        tracer.CORE_PROLOG["xmm15_1"]["value"] = tracer_dump["VMM15"]["data_1"]
        tracer.CORE_PROLOG["xmm15_2"]["value"] = tracer_dump["VMM15"]["data_2"]
        tracer.CORE_PROLOG["xmm15_3"]["value"] = tracer_dump["VMM15"]["data_3"]
        
        
        tracer.CORE_PROLOG["ymm0_0"]["value"] = tracer_dump["VMM00"]["data_4"]
        tracer.CORE_PROLOG["ymm0_1"]["value"] = tracer_dump["VMM00"]["data_5"]
        tracer.CORE_PROLOG["ymm0_2"]["value"] = tracer_dump["VMM00"]["data_6"]
        tracer.CORE_PROLOG["ymm0_3"]["value"] = tracer_dump["VMM00"]["data_7"]
        tracer.CORE_PROLOG["ymm1_0"]["value"] = tracer_dump["VMM01"]["data_4"]
        tracer.CORE_PROLOG["ymm1_1"]["value"] = tracer_dump["VMM01"]["data_5"]
        tracer.CORE_PROLOG["ymm1_2"]["value"] = tracer_dump["VMM01"]["data_6"]
        tracer.CORE_PROLOG["ymm1_3"]["value"] = tracer_dump["VMM01"]["data_7"]
        tracer.CORE_PROLOG["ymm2_0"]["value"] = tracer_dump["VMM02"]["data_4"]
        tracer.CORE_PROLOG["ymm2_1"]["value"] = tracer_dump["VMM02"]["data_5"]
        tracer.CORE_PROLOG["ymm2_2"]["value"] = tracer_dump["VMM02"]["data_6"]
        tracer.CORE_PROLOG["ymm2_3"]["value"] = tracer_dump["VMM02"]["data_7"]
        tracer.CORE_PROLOG["ymm3_0"]["value"] = tracer_dump["VMM03"]["data_4"]
        tracer.CORE_PROLOG["ymm3_1"]["value"] = tracer_dump["VMM03"]["data_5"]
        tracer.CORE_PROLOG["ymm3_2"]["value"] = tracer_dump["VMM03"]["data_6"]
        tracer.CORE_PROLOG["ymm3_3"]["value"] = tracer_dump["VMM03"]["data_7"]
        tracer.CORE_PROLOG["ymm4_0"]["value"] = tracer_dump["VMM04"]["data_4"]
        tracer.CORE_PROLOG["ymm4_1"]["value"] = tracer_dump["VMM04"]["data_5"]
        tracer.CORE_PROLOG["ymm4_2"]["value"] = tracer_dump["VMM04"]["data_6"]
        tracer.CORE_PROLOG["ymm4_3"]["value"] = tracer_dump["VMM04"]["data_7"]
        tracer.CORE_PROLOG["ymm5_0"]["value"] = tracer_dump["VMM05"]["data_4"]
        tracer.CORE_PROLOG["ymm5_1"]["value"] = tracer_dump["VMM05"]["data_5"]
        tracer.CORE_PROLOG["ymm5_2"]["value"] = tracer_dump["VMM05"]["data_6"]
        tracer.CORE_PROLOG["ymm5_3"]["value"] = tracer_dump["VMM05"]["data_7"]
        tracer.CORE_PROLOG["ymm6_0"]["value"] = tracer_dump["VMM06"]["data_4"]
        tracer.CORE_PROLOG["ymm6_1"]["value"] = tracer_dump["VMM06"]["data_5"]
        tracer.CORE_PROLOG["ymm6_2"]["value"] = tracer_dump["VMM06"]["data_6"]
        tracer.CORE_PROLOG["ymm6_3"]["value"] = tracer_dump["VMM06"]["data_7"]
        tracer.CORE_PROLOG["ymm7_0"]["value"] = tracer_dump["VMM07"]["data_4"]
        tracer.CORE_PROLOG["ymm7_1"]["value"] = tracer_dump["VMM07"]["data_5"]
        tracer.CORE_PROLOG["ymm7_2"]["value"] = tracer_dump["VMM07"]["data_6"]
        tracer.CORE_PROLOG["ymm7_3"]["value"] = tracer_dump["VMM07"]["data_7"]
        tracer.CORE_PROLOG["ymm8_0"]["value"] = tracer_dump["VMM00"]["data_4"]
        tracer.CORE_PROLOG["ymm8_1"]["value"] = tracer_dump["VMM00"]["data_5"]
        tracer.CORE_PROLOG["ymm8_2"]["value"] = tracer_dump["VMM00"]["data_6"]
        tracer.CORE_PROLOG["ymm8_3"]["value"] = tracer_dump["VMM00"]["data_7"]
        tracer.CORE_PROLOG["ymm9_0"]["value"] = tracer_dump["VMM01"]["data_4"]
        tracer.CORE_PROLOG["ymm9_1"]["value"] = tracer_dump["VMM01"]["data_5"]
        tracer.CORE_PROLOG["ymm9_2"]["value"] = tracer_dump["VMM01"]["data_6"]
        tracer.CORE_PROLOG["ymm9_3"]["value"] = tracer_dump["VMM01"]["data_7"]
        tracer.CORE_PROLOG["ymm10_0"]["value"] = tracer_dump["VMM10"]["data_4"]
        tracer.CORE_PROLOG["ymm10_1"]["value"] = tracer_dump["VMM10"]["data_5"]
        tracer.CORE_PROLOG["ymm10_2"]["value"] = tracer_dump["VMM10"]["data_6"]
        tracer.CORE_PROLOG["ymm10_3"]["value"] = tracer_dump["VMM10"]["data_7"]
        tracer.CORE_PROLOG["ymm11_0"]["value"] = tracer_dump["VMM11"]["data_4"]
        tracer.CORE_PROLOG["ymm11_1"]["value"] = tracer_dump["VMM11"]["data_5"]
        tracer.CORE_PROLOG["ymm11_2"]["value"] = tracer_dump["VMM11"]["data_6"]
        tracer.CORE_PROLOG["ymm11_3"]["value"] = tracer_dump["VMM11"]["data_7"]
        tracer.CORE_PROLOG["ymm12_0"]["value"] = tracer_dump["VMM12"]["data_4"]
        tracer.CORE_PROLOG["ymm12_1"]["value"] = tracer_dump["VMM12"]["data_5"]
        tracer.CORE_PROLOG["ymm12_2"]["value"] = tracer_dump["VMM12"]["data_6"]
        tracer.CORE_PROLOG["ymm12_3"]["value"] = tracer_dump["VMM12"]["data_7"]
        tracer.CORE_PROLOG["ymm13_0"]["value"] = tracer_dump["VMM13"]["data_4"]
        tracer.CORE_PROLOG["ymm13_1"]["value"] = tracer_dump["VMM13"]["data_5"]
        tracer.CORE_PROLOG["ymm13_2"]["value"] = tracer_dump["VMM13"]["data_6"]
        tracer.CORE_PROLOG["ymm13_3"]["value"] = tracer_dump["VMM13"]["data_7"]
        tracer.CORE_PROLOG["ymm14_0"]["value"] = tracer_dump["VMM14"]["data_4"]
        tracer.CORE_PROLOG["ymm14_1"]["value"] = tracer_dump["VMM14"]["data_5"]
        tracer.CORE_PROLOG["ymm14_2"]["value"] = tracer_dump["VMM14"]["data_6"]
        tracer.CORE_PROLOG["ymm14_3"]["value"] = tracer_dump["VMM14"]["data_7"]
        tracer.CORE_PROLOG["ymm15_0"]["value"] = tracer_dump["VMM15"]["data_4"]
        tracer.CORE_PROLOG["ymm15_1"]["value"] = tracer_dump["VMM15"]["data_5"]
        tracer.CORE_PROLOG["ymm15_2"]["value"] = tracer_dump["VMM15"]["data_6"]
        tracer.CORE_PROLOG["ymm15_3"]["value"] = tracer_dump["VMM15"]["data_7"]
        
        tracer.CORE_PROLOG["CR0"]["value"] = tracer_dump["CR0"]["value_l"]
        tracer.CORE_PROLOG["CR4_l"]["value"] = tracer_dump["CR4"]["value_l"]
        tracer.CORE_PROLOG["CR4_h"]["value"] = tracer_dump["CR4"]["value_h"]
        tracer.CORE_PROLOG["EFER"]["value"] = tracer_dump["EFER"]["value_l"]
        tracer.CORE_PROLOG["IP_l"]["value"] = tracer_dump["RIP"]["value_l"]
        tracer.CORE_PROLOG["IP_h"]["value"] = tracer_dump["RIP"]["value_h"]
        tracer.CORE_PROLOG["EFLAGS"]["value"] = tracer_dump["EFLAGS"]["value"]
        tracer.CORE_PROLOG["APICBASE_l"]["value"] = tracer_dump["MSR_1b"]["value_l"]
        tracer.CORE_PROLOG["APICBASE_h"]["value"] = tracer_dump["MSR_1b"]["value_h"]
        
    def update_vmcs_stuff_prolog(self,tracer_dump):
        pass
    
    def update_smm_state_prolog(self,tracer_dump):
        pass
    
    def update_apic_prolog(self,tracer_dump):
        
        tracer.APIC_PROLOG["APIC_ID"]["value"] = tracer_dump["APIC_020"]["value"]
        tracer.APIC_PROLOG["APIC_VER"]["value"] = tracer_dump["APIC_030"]["value"]
        tracer.APIC_PROLOG["APIC_TPR"]["value"] = tracer_dump["APIC_080"]["value"]
        tracer.APIC_PROLOG["APIC_PPR"]["value"] = tracer_dump["APIC_0a0"]["value"]
        tracer.APIC_PROLOG["APIC_LDR"]["value"] = tracer_dump["APIC_0d0"]["value"]
        tracer.APIC_PROLOG["APIC_DFR"]["value"] = tracer_dump["APIC_0e0"]["value"]
        tracer.APIC_PROLOG["APIC_SVR"]["value"] = tracer_dump["APIC_0f0"]["value"]
        tracer.APIC_PROLOG["APIC_ISR_0"]["value"] = tracer_dump["APIC_100"]["value"]
        tracer.APIC_PROLOG["APIC_ISR_1"]["value"] = tracer_dump["APIC_110"]["value"]
        tracer.APIC_PROLOG["APIC_ISR_2"]["value"] = tracer_dump["APIC_120"]["value"]
        tracer.APIC_PROLOG["APIC_ISR_3"]["value"] = tracer_dump["APIC_130"]["value"]
        tracer.APIC_PROLOG["APIC_ISR_4"]["value"] = tracer_dump["APIC_140"]["value"]
        tracer.APIC_PROLOG["APIC_ISR_5"]["value"] = tracer_dump["APIC_150"]["value"]
        tracer.APIC_PROLOG["APIC_ISR_6"]["value"] = tracer_dump["APIC_160"]["value"]
        tracer.APIC_PROLOG["APIC_ISR_7"]["value"] = tracer_dump["APIC_170"]["value"]
        tracer.APIC_PROLOG["APIC_TMR_0"]["value"] = tracer_dump["APIC_180"]["value"]
        tracer.APIC_PROLOG["APIC_TMR_1"]["value"] = tracer_dump["APIC_190"]["value"]
        tracer.APIC_PROLOG["APIC_TMR_2"]["value"] = tracer_dump["APIC_1a0"]["value"]
        tracer.APIC_PROLOG["APIC_TMR_3"]["value"] = tracer_dump["APIC_1b0"]["value"]
        tracer.APIC_PROLOG["APIC_TMR_4"]["value"] = tracer_dump["APIC_1c0"]["value"]
        tracer.APIC_PROLOG["APIC_TMR_5"]["value"] = tracer_dump["APIC_1d0"]["value"]
        tracer.APIC_PROLOG["APIC_TMR_6"]["value"] = tracer_dump["APIC_1e0"]["value"]
        tracer.APIC_PROLOG["APIC_TMR_7"]["value"] = tracer_dump["APIC_1f0"]["value"]
        tracer.APIC_PROLOG["APIC_IRR_0"]["value"] = tracer_dump["APIC_200"]["value"]
        tracer.APIC_PROLOG["APIC_IRR_1"]["value"] = tracer_dump["APIC_210"]["value"]
        tracer.APIC_PROLOG["APIC_IRR_2"]["value"] = tracer_dump["APIC_220"]["value"]
        tracer.APIC_PROLOG["APIC_IRR_3"]["value"] = tracer_dump["APIC_230"]["value"]
        tracer.APIC_PROLOG["APIC_IRR_4"]["value"] = tracer_dump["APIC_240"]["value"]
        tracer.APIC_PROLOG["APIC_IRR_5"]["value"] = tracer_dump["APIC_250"]["value"]
        tracer.APIC_PROLOG["APIC_IRR_6"]["value"] = tracer_dump["APIC_260"]["value"]
        tracer.APIC_PROLOG["APIC_IRR_7"]["value"] = tracer_dump["APIC_270"]["value"]
        tracer.APIC_PROLOG["APIC_ESR"]["value"] = tracer_dump["APIC_280"]["value"]
        tracer.APIC_PROLOG["APIC_ICR0"]["value"] = tracer_dump["APIC_300"]["value"]
        tracer.APIC_PROLOG["APIC_ICR1"]["value"] = tracer_dump["APIC_310"]["value"]
        tracer.APIC_PROLOG["APIC_LVTT"]["value"] = tracer_dump["APIC_320"]["value"]
        tracer.APIC_PROLOG["APIC_LVTS"]["value"] = tracer_dump["APIC_330"]["value"]
        tracer.APIC_PROLOG["APIC_LVTP"]["value"] = tracer_dump["APIC_340"]["value"]
        tracer.APIC_PROLOG["APIC_LVT0"]["value"] = tracer_dump["APIC_350"]["value"]
        tracer.APIC_PROLOG["APIC_LVT1"]["value"] = tracer_dump["APIC_360"]["value"]
        tracer.APIC_PROLOG["APIC_LVTE"]["value"] = tracer_dump["APIC_370"]["value"]
        tracer.APIC_PROLOG["APIC_INIT_COUNT"]["value"] = tracer_dump["APIC_380"]["value"]
        tracer.APIC_PROLOG["APIC_TIMER"]["value"] = tracer_dump["APIC_390"]["value"]
        tracer.APIC_PROLOG["APIC_TIMER_DIV"]["value"] = tracer_dump["APIC_3e0"]["value"]
        
        
                
       
    def update_ctr_regs_prolog(self,tracer_dump):
        pass
    
    def update_uc_regs_prolog(self,tracer_dump):
        pass
    
    def update_uc_core_regs_prolog(self,tracer_dump):
        pass 
        
    def gen_prologs(self,prolog):
        
        avp_prolog = Mem(2);
        for key in prolog:
            if eq(key,"prolog_size") or eq(key,"offset"):
                continue
            else:
                mem_addr = "%04x"%(prolog[key]["position"]*4 + tracer.total_size)
                if mem_addr in avp_prolog.mem_lines:
                    #prolog[key]["value"]= self.adjust_data(prolog[key]["size"],prolog[key]["value"])
                    avp_prolog.check_mem_line(mem_addr,prolog[key]["offset"],prolog[key]["size"],prolog[key]["value"],prolog[key]["DOC"])
                else:
                    avp_prolog.add_mem_line(mem_addr,prolog[key]["offset"],prolog[key]["size"],prolog[key]["value"],prolog[key]["DOC"])
                
        for key in sorted(avp_prolog.mem_lines):
            self.avp_handle.write("\tmem\t0x00%s%s\t0x%s\n"%(self.__replay_addr_h,key,avp_prolog.mem_lines[key]["value"]))
            
        del(avp_prolog)
    def update_prologs(self,prolog,tracer_dump):
        if not tracer_dump["occur"]:
            return
        
        if prolog is tracer.FXSAVE_PROLOG:
            self.update_fxsave_prolog(tracer_dump)
            
        elif prolog is tracer.PRAM_PROLOG:
            self.update_pram_prolog(tracer_dump)
            
        elif prolog is tracer.CORE_PROLOG:
            self.update_core_prolog(tracer_dump)
            
        elif prolog is tracer.VMCS_STUFF_PROLOG:    
            self.update_vmcs_stuff_prolog(tracer_dump)
        
        elif prolog is tracer.SMM_STATE_PROLOG:
            self.update_smm_state_prolog(tracer_dump)
            
        elif prolog is tracer.APIC_PROLOG:
            self.update_apic_prolog(tracer_dump)
            
        elif prolog is tracer.CTR_REGS_PROLOG:    
            self.update_ctr_regs_prolog(tracer_dump)
            
        elif prolog is tracer.UC_REGS_PROLOG:
            self.update_uc_regs_prolog(tracer_dump)
            
        elif prolog is tracer.UC_CORE_REGS_PROLOG:    
            self.update_uc_core_regs_prolog(tracer_dump)
            
        else:
            error("wrong prolog!")
        
        self.gen_prologs(prolog)
        tracer.total_size = prolog["prolog_size"] + tracer.total_size
        
    def check_gen_sub_headers(self,tracer_dump,TR3,replay_addr):
        
        for i in range(0, len(tracer.SUBHDR)):
            if (0x1<<tracer.SUBHDR[i]["offset"]) & TR3:
                self.update_sub_headers(tracer.SUBHDR[i],tracer_dump,replay_addr)
                
    def check_gen_prologs(self,tracer_dump):
        
        for i in range(0, len(tracer.PROLOG)):
            if (0x1<<tracer.PROLOG[i]["offset"]) & tracer.TR3:
                self.update_prologs(tracer.PROLOG[i],tracer_dump)
        #self.avp_handle.write("\t//  Headers And Prologs End\n")
    
    def gen_program_mems(self,program):
        
        self.avp_handle.write("\t//  Code Mem\n")
        for key in sorted(program.mem_lines):
            self.avp_handle.write("\tmem\t0x00%s\t0x%s\n"%(key,program.mem_lines[key]["value"]))
            
    def check_gen_mems(self,avp_data_seg,program):
        mems = {}
        self.avp_handle.write("\t//  Code and Data Mems\n")
        mems.update(program.mem_lines)
        for key in sorted(mems):
            if key in avp_data_seg.mem_lines:
                new_mem = ""
                for i in range(0,4):
                    if eq(mems[key]["value"][i*2:i*2+2].upper(),"F4"): 
                        if not eq(avp_data_seg.mem_lines[key]["value"][i*2:i*2+2].upper(),"F4"): 
                            new_mem = new_mem + avp_data_seg.mem_lines[key]["value"][i*2:i*2+2]
                            continue
                    else:
                        if not eq(mems[key]["value"][i*2:i*2+2].upper(),avp_data_seg.mem_lines[key]["value"][i*2:i*2+2].upper()): 
                            if not eq(avp_data_seg.mem_lines[key]["value"][i*2:i*2+2].upper(),"F4"): 
                                warning("SMC may occur in mem %s, program data is %s and data seg data is %s, please check!"\
                                        %(key,mems[key]["value"][i*2:i*2+2].upper(),avp_data_seg.mem_lines[key]["value"][i*2:i*2+2].upper()))
                    new_mem = new_mem + mems[key]["value"][i*2:i*2+2]
                avp_data_seg.mem_lines[key]["value"] = new_mem + avp_data_seg.mem_lines[key]["value"][8:]
        mems.update(avp_data_seg.mem_lines)
        for key in sorted(mems):
            self.avp_handle.write("\tmem\t0x00%s\t0x%s\n"%(key,mems[key]["value"]))

    def gen_part(self,data, program, tracer_dump, cmd):
        tracer.total_size = 0
        if eq(cmd,"initial"):
            self.gen_reset_code()
            self.gen_major_header_type2(tracer.mini_dump_type2_result,self.__replay_addr_type2_h)
            self.check_gen_sub_headers(tracer.mini_dump_type2_initial,tracer.TR3_2,self.__replay_addr_type2_h)
            tracer.total_size = 0
        elif eq(cmd,"result"):
            self.avp_handle.write("results {\n")
            self.gen_major_header_type2(tracer.mini_dump_type2_result,self.__replay_addr_type2_h)
            self.check_gen_sub_headers(tracer.mini_dump_type2_result,tracer.TR3_2,self.__replay_addr_type2_h)
            tracer.total_size = 0
        self.gen_major_header(tracer_dump)
        self.check_gen_sub_headers(tracer_dump,tracer.TR3,self.__replay_addr_h)
        self.check_gen_prologs(tracer_dump)
        #self.gen_program_mems(program)
        self.check_gen_mems(data, program)
        self.end_section()
        if eq(cmd,"result"):
            self.avp_handle.write("end\n")
    
    def __del__(self):
        del(self.avp_handle)