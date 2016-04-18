#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
'Tracer Moduel'
__author__ = 'Ken Zhao'
#################### Global Vars ####################
major_header_size = 0x28
total_size = 0x0
sub_header_mask = 0x4
TR3 = 0xB249 #tracer type 0
TR3_1 = 0x0000 #tracer type 1
TR3_2 = 0x0005 #tracer type 2 use PEBS_JWAD2_subhdr for reload ecx
TR3_3 = 0x0000 #tracer type 3
TR1 = "8000021c"
#bit 1: wrmsr
#bit 2: rdmsr
#bit 3: rdtsc
#bit 4: rdpmc
#bit 9: cpuid
delta = 0xF
SMM_BASE = 0xCFF00000
SMRAM_TYPE = 0x4 # 4 WT, 0 UC, 6 WB

major_dump_initial = {"RAX":{"value_h":"0","value_l":"0"},\
                      "RBX":{"value_h":"0","value_l":"0"},\
                      "RCX":{"value_h":"0","value_l":"0"},\
                      "RDX":{"value_h":"0","value_l":"0"},\
                      "RSP":{"value_h":"0","value_l":"0"},\
                      "RBP":{"value_h":"0","value_l":"0"},\
                      "RSI":{"value_h":"0","value_l":"0"},\
                      "RDI":{"value_h":"0","value_l":"0"},\
                      "R8":{"value_h":"0","value_l":"0"},\
                      "R9":{"value_h":"0","value_l":"0"},\
                      "R10":{"value_h":"0","value_l":"0"},\
                      "R11":{"value_h":"0","value_l":"0"},\
                      "R12":{"value_h":"0","value_l":"0"},\
                      "R13":{"value_h":"0","value_l":"0"},\
                      "R14":{"value_h":"0","value_l":"0"},\
                      "R15":{"value_h":"0","value_l":"0"},\
                      "RIP":{"value_h":"0","value_l":"0"},\
                      "TR7":{"value_h":"0","value_l":"0"},\
                      "CR0":{"value_h":"0","value_l":"0"},\
                      "CR2":{"value_h":"0","value_l":"0"},\
                      "CR3":{"value_h":"0","value_l":"0"},\
                      "CR4":{"value_h":"0","value_l":"0"},\
                      "CR8":{"value_h":"0","value_l":"0"},\
                      "EFLAGS":{"value":"0"},\
                      "STATUS_W":{"value":"0"},\
                      "CONTROL_W":{"value":"0"},\
                      "TAG_W":{"value":"0"},\
                      "OPERAND":{"value":"0"},\
                      "FIP":{"value_h":"0","value_l":"0"},\
                      "FCS":{"value":"0"},\
                      "FDP":{"value_h":"0","value_l":"0"},\
                      "FDS":{"value":"0"},\
                      "FP0_ST0":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP1_ST1":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP2_ST2":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP3_ST3":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP4_ST4":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP5_ST5":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP6_ST6":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP7_ST7":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "XCR0":{"value_h":"0","value_l":"0"},\
                      "EFER":{"value_h":"0","value_l":"0"},\
                      "MXCSR":{"value":"0"},\
                      "CS":{"value":"0","value_h":"0", "value_l":"0"},\
                      "DS":{"value":"0","value_h":"0", "value_l":"0"},\
                      "ES":{"value":"0","value_h":"0", "value_l":"0"},\
                      "SS":{"value":"0","value_h":"0", "value_l":"0"},\
                      "FS":{"value":"0","value_h":"0", "value_l":"0"},\
                      "GS":{"value":"0","value_h":"0", "value_l":"0"},\
                      "LDTR":{"value":"0","value_h":"0", "value_l":"0"},\
                      "TR":{"value":"0","value_h":"0", "value_l":"0"},\
                      "GDTR":{"base":"0","limit":"0"},\
                      "IDTR":{"base":"0","limit":"0"},\
                      "MM0":{"value_h":"0","value_l":"0"},\
                      "MM1":{"value_h":"0","value_l":"0"},\
                      "MM2":{"value_h":"0","value_l":"0"},\
                      "MM3":{"value_h":"0","value_l":"0"},\
                      "MM4":{"value_h":"0","value_l":"0"},\
                      "MM5":{"value_h":"0","value_l":"0"},\
                      "MM6":{"value_h":"0","value_l":"0"},\
                      "MM7":{"value_h":"0","value_l":"0"},\
                      "VMM00":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM01":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM02":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM03":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM04":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM05":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM06":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM07":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM08":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM09":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM10":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM11":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM12":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM13":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM14":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM15":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "MSR_10":{"value_h":"0","value_l":"0"},\
                      "MSR_1b":{"value_h":"0","value_l":"0"},\
                      "MSR_174":{"value_h":"0","value_l":"0"},\
                      "MSR_175":{"value_h":"0","value_l":"0"},\
                      "MSR_176":{"value_h":"0","value_l":"0"},\
                      "MSR_fe":{"value_h":"0","value_l":"0"},\
                      "MSR_200":{"value_h":"0","value_l":"0"},\
                      "MSR_201":{"value_h":"0","value_l":"0"},\
                      "MSR_202":{"value_h":"0","value_l":"0"},\
                      "MSR_203":{"value_h":"0","value_l":"0"},\
                      "MSR_204":{"value_h":"0","value_l":"0"},\
                      "MSR_205":{"value_h":"0","value_l":"0"},\
                      "MSR_206":{"value_h":"0","value_l":"0"},\
                      "MSR_207":{"value_h":"0","value_l":"0"},\
                      "MSR_208":{"value_h":"0","value_l":"0"},\
                      "MSR_209":{"value_h":"0","value_l":"0"},\
                      "MSR_20a":{"value_h":"0","value_l":"0"},\
                      "MSR_20b":{"value_h":"0","value_l":"0"},\
                      "MSR_20c":{"value_h":"0","value_l":"0"},\
                      "MSR_20d":{"value_h":"0","value_l":"0"},\
                      "MSR_20e":{"value_h":"0","value_l":"0"},\
                      "MSR_20f":{"value_h":"0","value_l":"0"},\
                      "MSR_250":{"value_h":"0","value_l":"0"},\
                      "MSR_258":{"value_h":"0","value_l":"0"},\
                      "MSR_259":{"value_h":"0","value_l":"0"},\
                      "MSR_268":{"value_h":"0","value_l":"0"},\
                      "MSR_269":{"value_h":"0","value_l":"0"},\
                      "MSR_26a":{"value_h":"0","value_l":"0"},\
                      "MSR_26b":{"value_h":"0","value_l":"0"},\
                      "MSR_26c":{"value_h":"0","value_l":"0"},\
                      "MSR_26d":{"value_h":"0","value_l":"0"},\
                      "MSR_26e":{"value_h":"0","value_l":"0"},\
                      "MSR_26f":{"value_h":"0","value_l":"0"},\
                      "MSR_277":{"value_h":"0","value_l":"0"},\
                      "MSR_2ff":{"value_h":"0","value_l":"0"},\
                      "MSR_6e0":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000080":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000081":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000082":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000083":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000084":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000100":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000101":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000102":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000103":{"value_h":"0","value_l":"0"},\
                      "MSR_480":{"value_h":"0","value_l":"0"},\
                      "MSR_481":{"value_h":"0","value_l":"0"},\
                      "MSR_482":{"value_h":"0","value_l":"0"},\
                      "MSR_483":{"value_h":"0","value_l":"0"},\
                      "MSR_484":{"value_h":"0","value_l":"0"},\
                      "MSR_485":{"value_h":"0","value_l":"0"},\
                      "MSR_486":{"value_h":"0","value_l":"0"},\
                      "MSR_487":{"value_h":"0","value_l":"0"},\
                      "MSR_488":{"value_h":"0","value_l":"0"},\
                      "MSR_489":{"value_h":"0","value_l":"0"},\
                      "MSR_48a":{"value_h":"0","value_l":"0"},\
                      "MSR_48b":{"value_h":"0","value_l":"0"},\
                      "MSR_3a":{"value_h":"0","value_l":"0"},\
                      "APIC_020":{"value":"0"},\
                      "APIC_030":{"value":"0"},\
                      "APIC_080":{"value":"0"},\
                      "APIC_090":{"value":"0"},\
                      "APIC_0a0":{"value":"0"},\
                      "APIC_0b0":{"value":"0"},\
                      "APIC_0c0":{"value":"0"},\
                      "APIC_0d0":{"value":"0"},\
                      "APIC_0e0":{"value":"0"},\
                      "APIC_0f0":{"value":"0"},\
                      "APIC_100":{"value":"0"},\
                      "APIC_110":{"value":"0"},\
                      "APIC_120":{"value":"0"},\
                      "APIC_130":{"value":"0"},\
                      "APIC_140":{"value":"0"},\
                      "APIC_150":{"value":"0"},\
                      "APIC_160":{"value":"0"},\
                      "APIC_170":{"value":"0"},\
                      "APIC_180":{"value":"0"},\
                      "APIC_190":{"value":"0"},\
                      "APIC_1a0":{"value":"0"},\
                      "APIC_1b0":{"value":"0"},\
                      "APIC_1c0":{"value":"0"},\
                      "APIC_1d0":{"value":"0"},\
                      "APIC_1e0":{"value":"0"},\
                      "APIC_1f0":{"value":"0"},\
                      "APIC_200":{"value":"0"},\
                      "APIC_210":{"value":"0"},\
                      "APIC_220":{"value":"0"},\
                      "APIC_230":{"value":"0"},\
                      "APIC_240":{"value":"0"},\
                      "APIC_250":{"value":"0"},\
                      "APIC_260":{"value":"0"},\
                      "APIC_270":{"value":"0"},\
                      "APIC_280":{"value":"0"},\
                      "APIC_2f0":{"value":"0"},\
                      "APIC_300":{"value":"0"},\
                      "APIC_310":{"value":"0"},\
                      "APIC_320":{"value":"0"},\
                      "APIC_330":{"value":"0"},\
                      "APIC_340":{"value":"0"},\
                      "APIC_350":{"value":"0"},\
                      "APIC_360":{"value":"0"},\
                      "APIC_370":{"value":"0"},\
                      "APIC_380":{"value":"0"},\
                      "APIC_390":{"value":"0"},\
                      "APIC_3e0":{"value":"0"},\
                      "APIC_3f0":{"value":"0"},\
                      "occur":0x1,
}

major_dump_result = {"RAX":{"value_h":"0","value_l":"0"},\
                      "RBX":{"value_h":"0","value_l":"0"},\
                      "RCX":{"value_h":"0","value_l":"0"},\
                      "RDX":{"value_h":"0","value_l":"0"},\
                      "RSP":{"value_h":"0","value_l":"0"},\
                      "RBP":{"value_h":"0","value_l":"0"},\
                      "RSI":{"value_h":"0","value_l":"0"},\
                      "RDI":{"value_h":"0","value_l":"0"},\
                      "R8":{"value_h":"0","value_l":"0"},\
                      "R9":{"value_h":"0","value_l":"0"},\
                      "R10":{"value_h":"0","value_l":"0"},\
                      "R11":{"value_h":"0","value_l":"0"},\
                      "R12":{"value_h":"0","value_l":"0"},\
                      "R13":{"value_h":"0","value_l":"0"},\
                      "R14":{"value_h":"0","value_l":"0"},\
                      "R15":{"value_h":"0","value_l":"0"},\
                      "RIP":{"value_h":"0","value_l":"0"},\
                      "TR7":{"value_h":"0","value_l":"0"},\
                      "CR0":{"value_h":"0","value_l":"0"},\
                      "CR2":{"value_h":"0","value_l":"0"},\
                      "CR3":{"value_h":"0","value_l":"0"},\
                      "CR4":{"value_h":"0","value_l":"0"},\
                      "CR8":{"value_h":"0","value_l":"0"},\
                      "EFLAGS":{"value":"0"},\
                      "STATUS_W":{"value":"0"},\
                      "CONTROL_W":{"value":"0"},\
                      "TAG_W":{"value":"0"},\
                      "OPERAND":{"value":"0"},\
                      "FIP":{"value_h":"0","value_l":"0"},\
                      "FCS":{"value":"0"},\
                      "FDP":{"value_h":"0","value_l":"0"},\
                      "FDS":{"value":"0"},\
                      "FP0_ST0":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP1_ST1":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP2_ST2":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP3_ST3":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP4_ST4":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP5_ST5":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP6_ST6":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "FP7_ST7":{"value":"0", "value_h":"0", "value_l":"0"},\
                      "XCR0":{"value_h":"0","value_l":"0"},\
                      "EFER":{"value_h":"0","value_l":"0"},\
                      "MXCSR":{"value":"0"},\
                      "CS":{"value":"0","value_h":"0", "value_l":"0"},\
                      "DS":{"value":"0","value_h":"0", "value_l":"0"},\
                      "ES":{"value":"0","value_h":"0", "value_l":"0"},\
                      "SS":{"value":"0","value_h":"0", "value_l":"0"},\
                      "FS":{"value":"0","value_h":"0", "value_l":"0"},\
                      "GS":{"value":"0","value_h":"0", "value_l":"0"},\
                      "LDTR":{"value":"0","value_h":"0", "value_l":"0"},\
                      "TR":{"value":"0","value_h":"0", "value_l":"0"},\
                      "GDTR":{"base":"0","limit":"0"},\
                      "IDTR":{"base":"0","limit":"0"},\
                      "MM0":{"value_h":"0","value_l":"0"},\
                      "MM1":{"value_h":"0","value_l":"0"},\
                      "MM2":{"value_h":"0","value_l":"0"},\
                      "MM3":{"value_h":"0","value_l":"0"},\
                      "MM4":{"value_h":"0","value_l":"0"},\
                      "MM5":{"value_h":"0","value_l":"0"},\
                      "MM6":{"value_h":"0","value_l":"0"},\
                      "MM7":{"value_h":"0","value_l":"0"},\
                      "VMM00":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM01":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM02":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM03":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM04":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM05":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM06":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM07":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM08":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM09":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM10":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM11":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM12":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM13":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM14":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "VMM15":{"data_7":"0","data_6":"0","data_5":"0","data_4":"0","data_3":"0","data_2":"0","data_1":"0","data_0":"0"},\
                      "MSR_10":{"value_h":"0","value_l":"0"},\
                      "MSR_1b":{"value_h":"0","value_l":"0"},\
                      "MSR_174":{"value_h":"0","value_l":"0"},\
                      "MSR_175":{"value_h":"0","value_l":"0"},\
                      "MSR_176":{"value_h":"0","value_l":"0"},\
                      "MSR_fe":{"value_h":"0","value_l":"0"},\
                      "MSR_200":{"value_h":"0","value_l":"0"},\
                      "MSR_201":{"value_h":"0","value_l":"0"},\
                      "MSR_202":{"value_h":"0","value_l":"0"},\
                      "MSR_203":{"value_h":"0","value_l":"0"},\
                      "MSR_204":{"value_h":"0","value_l":"0"},\
                      "MSR_205":{"value_h":"0","value_l":"0"},\
                      "MSR_206":{"value_h":"0","value_l":"0"},\
                      "MSR_207":{"value_h":"0","value_l":"0"},\
                      "MSR_208":{"value_h":"0","value_l":"0"},\
                      "MSR_209":{"value_h":"0","value_l":"0"},\
                      "MSR_20a":{"value_h":"0","value_l":"0"},\
                      "MSR_20b":{"value_h":"0","value_l":"0"},\
                      "MSR_20c":{"value_h":"0","value_l":"0"},\
                      "MSR_20d":{"value_h":"0","value_l":"0"},\
                      "MSR_20e":{"value_h":"0","value_l":"0"},\
                      "MSR_20f":{"value_h":"0","value_l":"0"},\
                      "MSR_250":{"value_h":"0","value_l":"0"},\
                      "MSR_258":{"value_h":"0","value_l":"0"},\
                      "MSR_259":{"value_h":"0","value_l":"0"},\
                      "MSR_268":{"value_h":"0","value_l":"0"},\
                      "MSR_269":{"value_h":"0","value_l":"0"},\
                      "MSR_26a":{"value_h":"0","value_l":"0"},\
                      "MSR_26b":{"value_h":"0","value_l":"0"},\
                      "MSR_26c":{"value_h":"0","value_l":"0"},\
                      "MSR_26d":{"value_h":"0","value_l":"0"},\
                      "MSR_26e":{"value_h":"0","value_l":"0"},\
                      "MSR_26f":{"value_h":"0","value_l":"0"},\
                      "MSR_277":{"value_h":"0","value_l":"0"},\
                      "MSR_2ff":{"value_h":"0","value_l":"0"},\
                      "MSR_6e0":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000080":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000081":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000082":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000083":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000084":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000100":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000101":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000102":{"value_h":"0","value_l":"0"},\
                      "MSR_c0000103":{"value_h":"0","value_l":"0"},\
                      "MSR_480":{"value_h":"0","value_l":"0"},\
                      "MSR_481":{"value_h":"0","value_l":"0"},\
                      "MSR_482":{"value_h":"0","value_l":"0"},\
                      "MSR_483":{"value_h":"0","value_l":"0"},\
                      "MSR_484":{"value_h":"0","value_l":"0"},\
                      "MSR_485":{"value_h":"0","value_l":"0"},\
                      "MSR_486":{"value_h":"0","value_l":"0"},\
                      "MSR_487":{"value_h":"0","value_l":"0"},\
                      "MSR_488":{"value_h":"0","value_l":"0"},\
                      "MSR_489":{"value_h":"0","value_l":"0"},\
                      "MSR_48a":{"value_h":"0","value_l":"0"},\
                      "MSR_48b":{"value_h":"0","value_l":"0"},\
                      "MSR_3a":{"value_h":"0","value_l":"0"},\
                      "APIC_020":{"value":"0"},\
                      "APIC_030":{"value":"0"},\
                      "APIC_080":{"value":"0"},\
                      "APIC_090":{"value":"0"},\
                      "APIC_0a0":{"value":"0"},\
                      "APIC_0b0":{"value":"0"},\
                      "APIC_0c0":{"value":"0"},\
                      "APIC_0d0":{"value":"0"},\
                      "APIC_0e0":{"value":"0"},\
                      "APIC_0f0":{"value":"0"},\
                      "APIC_100":{"value":"0"},\
                      "APIC_110":{"value":"0"},\
                      "APIC_120":{"value":"0"},\
                      "APIC_130":{"value":"0"},\
                      "APIC_140":{"value":"0"},\
                      "APIC_150":{"value":"0"},\
                      "APIC_160":{"value":"0"},\
                      "APIC_170":{"value":"0"},\
                      "APIC_180":{"value":"0"},\
                      "APIC_190":{"value":"0"},\
                      "APIC_1a0":{"value":"0"},\
                      "APIC_1b0":{"value":"0"},\
                      "APIC_1c0":{"value":"0"},\
                      "APIC_1d0":{"value":"0"},\
                      "APIC_1e0":{"value":"0"},\
                      "APIC_1f0":{"value":"0"},\
                      "APIC_200":{"value":"0"},\
                      "APIC_210":{"value":"0"},\
                      "APIC_220":{"value":"0"},\
                      "APIC_230":{"value":"0"},\
                      "APIC_240":{"value":"0"},\
                      "APIC_250":{"value":"0"},\
                      "APIC_260":{"value":"0"},\
                      "APIC_270":{"value":"0"},\
                      "APIC_280":{"value":"0"},\
                      "APIC_2f0":{"value":"0"},\
                      "APIC_300":{"value":"0"},\
                      "APIC_310":{"value":"0"},\
                      "APIC_320":{"value":"0"},\
                      "APIC_330":{"value":"0"},\
                      "APIC_340":{"value":"0"},\
                      "APIC_350":{"value":"0"},\
                      "APIC_360":{"value":"0"},\
                      "APIC_370":{"value":"0"},\
                      "APIC_380":{"value":"0"},\
                      "APIC_390":{"value":"0"},\
                      "APIC_3e0":{"value":"0"},\
                      "APIC_3f0":{"value":"0"},\
                      "occur":0x1,          
}

mini_dump_type2_initial ={"RAX":{"value_h":"0","value_l":"0"},\
                      "RBX":{"value_h":"0","value_l":"0"},\
                      "RCX":{"value_h":"0","value_l":"0"},\
                      "RDX":{"value_h":"0","value_l":"0"}, \
                      "RIP":{"value_h":"0","value_l":"0"}, \
                      "TR7":{"value_h":"00000000","value_l":"0"}, \
                      "EVENTS":{"value":"0"}, \
                      "occur":0x0,\
                      }

mini_dump_type2_result ={"RAX":{"value_h":"0","value_l":"0"},\
                      "RBX":{"value_h":"0","value_l":"0"},\
                      "RCX":{"value_h":"0","value_l":"0"},\
                      "RDX":{"value_h":"0","value_l":"0"}, \
                      "RIP":{"value_h":"0","value_l":"0"}, \
                      "TR7":{"value_h":"00000000","value_l":"0"}, \
                      "EVENTS":{"value":"0"}, \
                      "occur":0x0,\
                      }

MAJOR_HEADER = {"magic":                    {"value":"DEAD","position":0x0,"offset":0x0,"size":0x2,"DOC":"magic number = 0xDEAD "},\
                "tracer_version":           {"value":"36","position":0x0,"offset":0x2,"size":0x1,"DOC":"CNQ = 0x34, CNR = 0x36 "},\
                "cn_version":               {"value":"00","position":0x0,"offset":0x3,"size":0x1,"DOC":"0x01 "},\
                "hdr_details":              {"value":"0049","position":0x1,"offset":0x0,"size":0x2,"DOC":"TR3[0:15] "},\
                "action_vector":            {"value":"2180","position":0x1,"offset":0x2,"size":0x2,"DOC":"TR6[0:15] "},\
                "events":                   {"value":"80000000","position":0x2,"offset":0x0,"size":0x4,"DOC":"TR1,Event of dump is caused "},\
                "dump_vector":              {"value":"B249","position":0x3,"offset":0x0,"size":0x2,"DOC":"Dump vector,TR3[0:15] "},\
                "last_exception_vector":    {"value":"00","position":0x3,"offset":0x2,"size":0x1,"DOC":"last_exception_vector "},\
                "last_swint_vector":        {"value":"00","position":0x3,"offset":0x3,"size":0x1,"DOC":"last_swint_vector "},\
                "next_lip_l":               {"value":"0","position":0x4,"offset":0x0,"size":0x4,"DOC":"Next instr RIP l "},\
                "next_lip_h":               {"value":"0","position":0x5,"offset":0x0,"size":0x4,"DOC":"Next instr RIP h "},\
                "ctr_0_l":                  {"value":"0","position":0x6,"offset":0x0,"size":0x4,"DOC":"Current TR7 l "},\
                "ctr_0_h":                  {"value":"0","position":0x7,"offset":0x0,"size":0x4,"DOC":"Current TR7 h "},\
                "last_lip_l":               {"value":"00000000","position":0x8,"offset":0x0,"size":0x4,"DOC":"last instr RIP l "},\
                "last_lip_h":               {"value":"00000000","position":0x9,"offset":0x0,"size":0x4,"DOC":"last instr RIP h "},\
               }#position is related to the Nth 4Byte from the header start,name is key, 
                #and data is [offset size(byte) description]
                #last_exception_vector and last_swint_vector can't get from bochs
                #last_lip_h and last_lip_l can't get from bochs
                
MAJOR_HEADER_type2 = {"magic":                    {"value":"DEAD","position":0x0,"offset":0x0,"size":0x2,"DOC":"magic number = 0xDEAD "},\
                "tracer_version":           {"value":"36","position":0x0,"offset":0x2,"size":0x1,"DOC":"CNQ = 0x34, CNR = 0x36 "},\
                "cn_version":               {"value":"00","position":0x0,"offset":0x3,"size":0x1,"DOC":"0x01 "},\
                "hdr_details":              {"value":"0049","position":0x1,"offset":0x0,"size":0x2,"DOC":"TR3[0:15] "},\
                "action_vector":            {"value":"0800","position":0x1,"offset":0x2,"size":0x2,"DOC":"TR6[0:15] "},\
                "events":                   {"value":"80000000","position":0x2,"offset":0x0,"size":0x4,"DOC":"TR1,Event of dump is caused "},\
                "dump_vector":              {"value":"B249","position":0x3,"offset":0x0,"size":0x2,"DOC":"Dump vector,TR3[0:15] "},\
                "last_exception_vector":    {"value":"00","position":0x3,"offset":0x2,"size":0x1,"DOC":"last_exception_vector "},\
                "last_swint_vector":        {"value":"00","position":0x3,"offset":0x3,"size":0x1,"DOC":"last_swint_vector "},\
                "next_lip_l":               {"value":"0","position":0x4,"offset":0x0,"size":0x4,"DOC":"Next instr RIP l "},\
                "next_lip_h":               {"value":"0","position":0x5,"offset":0x0,"size":0x4,"DOC":"Next instr RIP h "},\
                "ctr_0_l":                  {"value":"0","position":0x6,"offset":0x0,"size":0x4,"DOC":"Current TR7 l "},\
                "ctr_0_h":                  {"value":"0","position":0x7,"offset":0x0,"size":0x4,"DOC":"Current TR7 h "},\
                "last_lip_l":               {"value":"00000000","position":0x8,"offset":0x0,"size":0x4,"DOC":"last instr RIP l "},\
                "last_lip_h":               {"value":"00000000","position":0x9,"offset":0x0,"size":0x4,"DOC":"last instr RIP h "},\
               }#position is related to the Nth 4Byte from the header start,name is key, 
                #and data is [offset size(byte) description]
                #last_exception_vector and last_swint_vector can't get from bochs
                #last_lip_h and last_lip_l can't get from bochs
NANO_PEBS_SUBHDR = {"eax":                  {"value":0x0,"position":0x0, "offset":0x0,"size":0x4,"DOC":"eax"},\
                    "ebx":                  {"value":0x0,"position":0x0,"offset":0x4,"size":0x4,"DOC":"ebx"},\
                    "edx":                  {"value":0x0,"position":0x1, "offset":0x0,"size":0x4,"DOC":"edx"},\
                    "eflags":               {"value":0x0,"position":0x1,"offset":0x4,"size":0x4,"DOC":"eflags"},\
                    "offset":                 0x1
                }
PEBS_JWAD2_SUBHDR = {"eflags":              {"value":"00000000","position":0x0,"offset":0x0,"size":0x4,"DOC":"eflags"},\
               "Nodefined":                 {"value":"00000000","position":0x1,"offset":0x0,"size":0x4,"DOC":"Nodefined"},\
               "rax_l":                       {"value":"00000000","position":0x2, "offset":0x0,"size":0x4,"DOC":"rax_l"},\
               "rax_h":                       {"value":"00000000","position":0x3, "offset":0x0,"size":0x4,"DOC":"rax_h"},\
               "rbx_l":                       {"value":"00000000","position":0x4, "offset":0x0,"size":0x4,"DOC":"rbx_l"},\
               "rbx_h":                       {"value":"00000000","position":0x5, "offset":0x0,"size":0x4,"DOC":"rbx_h"},\
               "rcx_l":                       {"value":"00000000","position":0x6, "offset":0x0,"size":0x4,"DOC":"rcx_l"},\
               "rcx_h":                       {"value":"00000000","position":0x7, "offset":0x0,"size":0x4,"DOC":"rcx_h"},\
               "rdx_l":                       {"value":"00000000","position":0x8, "offset":0x0,"size":0x4,"DOC":"rdx_l"},\
               "rdx_h":                       {"value":"00000000","position":0x9, "offset":0x0,"size":0x4,"DOC":"rdx_h"},\
               "rsi_l":                       {"value":"00000000","position":0xa, "offset":0x0,"size":0x4,"DOC":"rsi_l"},\
               "rsi_h":                       {"value":"00000000","position":0xb, "offset":0x0,"size":0x4,"DOC":"rsi_h"},\
               "rdi_l":                       {"value":"00000000","position":0xc, "offset":0x0,"size":0x4,"DOC":"rdi_l"},\
               "rdi_h":                       {"value":"00000000","position":0xd, "offset":0x0,"size":0x4,"DOC":"rdi_h"},\
               "rbp_l":                       {"value":"00000000","position":0xe, "offset":0x0,"size":0x4,"DOC":"rbp_l"},\
               "rbp_h":                       {"value":"00000000","position":0xf, "offset":0x0,"size":0x4,"DOC":"rbp_h"},\
               "rsp_l":                       {"value":"00000000","position":0x10, "offset":0x0,"size":0x4,"DOC":"rsp_l"},\
               "rsp_h":                       {"value":"00000000","position":0x11, "offset":0x0,"size":0x4,"DOC":"rsp_h"},\
               "perf_ctr0_l":                 {"value":"00000000","position":0x12, "offset":0x0,"size":0x4,"DOC":"perf ctr0_l"},\
               "perf_ctr0_h":                 {"value":"00000000","position":0x13, "offset":0x0,"size":0x4,"DOC":"perf ctr0_h"},\
               "perf_ctr1_l":                 {"value":"00000000","position":0x14, "offset":0x0,"size":0x4,"DOC":"perf ctr1_l"},\
               "perf_ctr2_h":                 {"value":"00000000","position":0x15, "offset":0x0,"size":0x4,"DOC":"perf ctr1_h"},\
               "real_hwd_tsc_l":              {"value":"00000000","position":0x16,"offset":0x0,"size":0x4,"DOC":"the real hdw tsc_l)"},\
               "real_hwd_tsc_h":              {"value":"00000000","position":0x17, "offset":0x0,"size":0x4,"DOC":"the real hdw tsc_h"},\
               "hdr_size":                     0x60,\
               "offset":                        0x2
               }
JWAD_EXCEPTION_SUBHDR = {"c2_iir_l":          {"value":"00000000","position":0x0,"offset":0x0,"size":0x4,"DOC":"c2_iir(about the last inst) l "},\
                         "c2_iir_h":          {"value":"00000000","position":0x1,"offset":0x0,"size":0x4,"DOC":"c2_iir(about the last inst) h "},\
               "c2_xcr_l":                    {"value":"00000000","position":0x2,"offset":0x0,"size":0x4,"DOC":"c2_xcr(interrput/exception causes stuff) l "},\
               "c2_xcr_h":                    {"value":"00000000","position":0x3,"offset":0x0,"size":0x4,"DOC":"c2_xcr(interrput/exception causes stuff) h "},\
               "msr_misc_enable_l":           {"value":"00153C89","position":0x4, "offset":0x0,"size":0x4,"DOC":"msr_misc_enable l "},\
               "msr_misc_enable_h":           {"value":"00000000","position":0x5, "offset":0x0,"size":0x4,"DOC":"msr_misc_enable h "},\
               "c1_jcr":                      {"value":"1063FD00","position":0x6,"offset":0x0,"size":0x4,"DOC":"c1_jcr(vmx state) "},\
               "gstate":                      {"value":"80000000","position":0x7, "offset":0x0,"size":0x4,"DOC":"misc state "},\
               "c2_xmr":                      {"value":"00000003","position":0x8, "offset":0x0,"size":0x4,"DOC":"c2_xmr(interrupt mask) "},\
               "last_intr_xcr_lo":            {"value":"00000000","position":0x9,"offset":0x0,"size":0x4,"DOC":"last_intr_xcr_lo(CNQ used to be efer) "},\
               "cr0":                         {"value":"0","position":0x0a, "offset":0x0,"size":0x4,"DOC":"cr0 "},\
               "cr4":                         {"value":"0","position":0x0b,"offset":0x0,"size":0x4,"DOC":"cr4 "},\
               "apic_ctrl":                   {"value":"002002B4","position":0x0c, "offset":0x0,"size":0x4,"DOC":"apic_ctrl "},\
               "cr8":                         {"value":"0","position":0x0d, "offset":0x0,"size":0x4,"DOC":"cr8 "},\
               "c2_ipr":                      {"value":"00008000","position":0x0e,"offset":0x0,"size":0x4,"DOC":"c2_ipr(pending interrupts used to be rcx) "},\
               "ecx":                         {"value":"0","position":0x0f,"offset":0x0,"size":0x4,"DOC":"ecx "},\
               "cr2_l":                       {"value":"0","position":0x10, "offset":0x0,"size":0x4,"DOC":"cr2 l "},\
               "cr2_h":                       {"value":"0","position":0x11, "offset":0x0,"size":0x4,"DOC":"cr2 h "},\
               "uexcept_state_l":             {"value":"00000000","position":0x12, "offset":0x0,"size":0x4,"DOC":"uexcept_state l "},\
               "uexcept_state_h":             {"value":"00000000","position":0x13, "offset":0x0,"size":0x4,"DOC":"uexcept_state h "},\
               "hdr_size":                     0x50,\
               "offset":                        0x3
               }
# c2_iir_h, c2_iir_l, c2_xcr_l, c2_xcr_h, c1_jcr can't get from bochs
# bochs debugger don't have msr_misc_enable 0x1a0

MPERF_SUBHDR = {"raw_mperf":                     {"value":0x0,"position":0x0,"offset":0x0,"size":0x8,"DOC":"bus count"},\
               "apic_timer":                      {"value":0x0,"position":0x1,"offset":0x0,"size":0x8,"DOC":"apic_timer(new in 0B)"},\
               "offset":                        0x4
               }
FXSAVE_PROLOG = {"offset":                      0x8,\
                 "prolog_size":                 0x2C8,\
                 }
PRAM_PROLOG = {"offset":                      0x9,\
               "prolog_size":                 0x6C8,\
               "pram_data_size": {"value":"000006C0","position":0x0,"offset":0x0,"size":0x4,"DOC":"pram prolog data size "},\
               "pram_type":      {"value":"00000200","position":0x1,"offset":0x0,"size":0x4,"DOC":"pram prolog type "},\
"CR2_l": {"value":"08F07000","position":0x2,"offset":0x0,"size":0x4,"DOC":"CR2 l "},\
"CR2_h": {"value":"FFFFF980","position":0x3,"offset":0x0,"size":0x4,"DOC":"CR2 h "},\
"IA32_LSTAR_l": {"value":"02E86BC0","position":0x4,"offset":0x0,"size":0x4,"DOC":"IA32_LSTAR l "},\
"IA32_LSTAR_h": {"value":"FFFFF800","position":0x5,"offset":0x0,"size":0x4,"DOC":"IA32_LSTAR h "},\
"SYSEXIT_CSDESC_32_l": {"value":"0000FFFF","position":0x6,"offset":0x0,"size":0x4,"DOC":"SYSEXIT_CSDESC_32 l "},\
"SYSEXIT_CSDESC_32_h": {"value":"00CFFB00","position":0x7,"offset":0x0,"size":0x4,"DOC":"SYSEXIT_CSDESC_32 h "},\
"SYSEXIT_CSDESC_64_l": {"value":"0000FFFF","position":0x8,"offset":0x0,"size":0x4,"DOC":"SYSEXIT_CSDESC_64 l "},\
"SYSEXIT_CSDESC_64_h": {"value":"00AFFB00","position":0x9,"offset":0x0,"size":0x4,"DOC":"SYSEXIT_CSDESC_64 h "},\
"SYSENTER_CS": {"value":"00000000","position":0xa,"offset":0x0,"size":0x4,"DOC":"SYSENTER_CS "},\
"LA_DESC0_LA_DESC1": {"value":"00007EFF","position":0xb,"offset":0x0,"size":0x4,"DOC":"LA_DESC0_LA_DESC1 "},\
"FSR0_l": {"value":"01030000","position":0xc,"offset":0x0,"size":0x4,"DOC":"FSR0 l "},\
"FSR0_h": {"value":"00000000","position":0xd,"offset":0x0,"size":0x4,"DOC":"FSR0 h "},\
"ES_PRAM_CS_PRAM": {"value":"0010002B","position":0xe,"offset":0x0,"size":0x4,"DOC":"ES_PRAM_CS_PRAM "},\
"SS_PRAM_DS_PRAM": {"value":"002B0018","position":0xf,"offset":0x0,"size":0x4,"DOC":"SS_PRAM_DS_PRAM "},\
"FS_PRAM_GS_PRAM": {"value":"002B0053","position":0x10,"offset":0x0,"size":0x4,"DOC":"FS_PRAM_GS_PRAM "},\
"TR_PRAM_LDT_PRAM": {"value":"00000040","position":0x11,"offset":0x0,"size":0x4,"DOC":"TR_PRAM_LDT_PRAM "},\
"ALT_BOOT_ADDR_l": {"value":"00000000","position":0x12,"offset":0x0,"size":0x4,"DOC":"ALT_BOOT_ADDR l "},\
"ALT_BOOT_ADDR_h": {"value":"00000000","position":0x13,"offset":0x0,"size":0x4,"DOC":"ALT_BOOT_ADDR h "},\
"CR3_l": {"value":"00187000","position":0x14,"offset":0x0,"size":0x4,"DOC":"CR3 l "},\
"CR3_h": {"value":"00000000","position":0x15,"offset":0x0,"size":0x4,"DOC":"CR3 h "},\
"LOCAL_CONTEXT_ENT0_l": {"value":"00187000","position":0x16,"offset":0x0,"size":0x4,"DOC":"LOCAL_CONTEXT_ENT0 l "},\
"LOCAL_CONTEXT_ENT0_h": {"value":"40000000","position":0x17,"offset":0x0,"size":0x4,"DOC":"LOCAL_CONTEXT_ENT0 h "},\
"LOCAL_CONTEXT_ENT1_l": {"value":"00000000","position":0x18,"offset":0x0,"size":0x4,"DOC":"LOCAL_CONTEXT_ENT1 l "},\
"LOCAL_CONTEXT_ENT1_h": {"value":"00010000","position":0x19,"offset":0x0,"size":0x4,"DOC":"LOCAL_CONTEXT_ENT1 h "},\
"LOCAL_CONTEXT_ENT2_l": {"value":"00000000","position":0x1a,"offset":0x0,"size":0x4,"DOC":"LOCAL_CONTEXT_ENT2 l "},\
"LOCAL_CONTEXT_ENT2_h": {"value":"00020000","position":0x1b,"offset":0x0,"size":0x4,"DOC":"LOCAL_CONTEXT_ENT2 h "},\
"LOCAL_CONTEXT_ENT3_l": {"value":"00000000","position":0x1c,"offset":0x0,"size":0x4,"DOC":"LOCAL_CONTEXT_ENT3 l "},\
"LOCAL_CONTEXT_ENT3_h": {"value":"00030000","position":0x1d,"offset":0x0,"size":0x4,"DOC":"LOCAL_CONTEXT_ENT3 h "},\
"DR7_l": {"value":"00000400","position":0x1e,"offset":0x0,"size":0x4,"DOC":"DR7 l "},\
"DR7_h": {"value":"00000000","position":0x1f,"offset":0x0,"size":0x4,"DOC":"DR7 h "},\
"FCR4_l": {"value":"00000474","position":0x20,"offset":0x0,"size":0x4,"DOC":"FCR4 l "},\
"FCR4_h": {"value":"000006FE","position":0x21,"offset":0x0,"size":0x4,"DOC":"FCR4 h "},\
"FCR5_l": {"value":"00000001","position":0x22,"offset":0x0,"size":0x4,"DOC":"FCR5 l "},\
"FCR5_h": {"value":"CFEF8000","position":0x23,"offset":0x0,"size":0x4,"DOC":"FCR5 h "},\
"FCR0_l": {"value":"BFCBFBFF","position":0x24,"offset":0x0,"size":0x4,"DOC":"FCR0 l "},\
"FCR0_h": {"value":"77FA63EB","position":0x25,"offset":0x0,"size":0x4,"DOC":"FCR0 h "},\
"FCR1_l": {"value":"2C100800","position":0x26,"offset":0x0,"size":0x4,"DOC":"FCR1 l "},\
"FCR1_h": {"value":"00000121","position":0x27,"offset":0x0,"size":0x4,"DOC":"FCR1 h "},\
"FCR46_l": {"value":"00000000","position":0x28,"offset":0x0,"size":0x4,"DOC":"FCR46 l "},\
"FCR46_h": {"value":"00000000","position":0x29,"offset":0x0,"size":0x4,"DOC":"FCR46 h "},\
"FCR2_l": {"value":"00003DFC","position":0x2a,"offset":0x0,"size":0x4,"DOC":"FCR2 l "},\
"FCR2_h": {"value":"00000000","position":0x2b,"offset":0x0,"size":0x4,"DOC":"FCR2 h "},\
"TPM_CTRL_l": {"value":"00000000","position":0x2c,"offset":0x0,"size":0x4,"DOC":"TPM_CTRL l "},\
"TPM_CTRL_h": {"value":"01000006","position":0x2d,"offset":0x0,"size":0x4,"DOC":"TPM_CTRL h "},\
"PWR_CTRL_LO_l": {"value":"00090820","position":0x2e,"offset":0x0,"size":0x4,"DOC":"PWR_CTRL_LO l "},\
"PWR_CTRL_LO_h": {"value":"169B060A","position":0x2f,"offset":0x0,"size":0x4,"DOC":"PWR_CTRL_LO h "},\
"MFG_ID_l": {"value":"240EC6F2","position":0x30,"offset":0x0,"size":0x4,"DOC":"MFG_ID l "},\
"MFG_ID_h": {"value":"B4180C59","position":0x31,"offset":0x0,"size":0x4,"DOC":"MFG_ID h "},\
"PSN_LO_l": {"value":"A02FE6BA","position":0x32,"offset":0x0,"size":0x4,"DOC":"PSN_LO l "},\
"PSN_LO_h": {"value":"0E5C1901","position":0x33,"offset":0x0,"size":0x4,"DOC":"PSN_LO h "},\
"PSN_HI_l": {"value":"C4295CCD","position":0x34,"offset":0x0,"size":0x4,"DOC":"PSN_HI l "},\
"PSN_HI_h": {"value":"F22655C2","position":0x35,"offset":0x0,"size":0x4,"DOC":"PSN_HI h "},\
"MSR_PASSWD_LO_l": {"value":"73AC1757","position":0x36,"offset":0x0,"size":0x4,"DOC":"MSR_PASSWD_LO l "},\
"MSR_PASSWD_LO_h": {"value":"3675828B","position":0x37,"offset":0x0,"size":0x4,"DOC":"MSR_PASSWD_LO h "},\
"PATCHX_ID": {"value":"00005005","position":0x38,"offset":0x0,"size":0x4,"DOC":"PATCHX_ID "},\
"HIGHEST_PATCHRAM_USED": {"value":"0000FFFF","position":0x39,"offset":0x0,"size":0x4,"DOC":"HIGHEST_PATCHRAM_USED "},\
"TR0_l": {"value":"00000005","position":0x3a,"offset":0x0,"size":0x4,"DOC":"TR0 l "},\
"TR0_h": {"value":"00000000","position":0x3b,"offset":0x0,"size":0x4,"DOC":"TR0 h "},\
"GLOBAL_CONTEXT_EPTP_ENT0_l": {"value":"00000000","position":0x3c,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CONTEXT_EPTP_ENT0 l "},\
"GLOBAL_CONTEXT_EPTP_ENT0_h": {"value":"00000000","position":0x3d,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CONTEXT_EPTP_ENT0 h "},\
"GLOBAL_CONTEXT_EPTP_ENT1_l": {"value":"00000000","position":0x3e,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CONTEXT_EPTP_ENT1 l "},\
"GLOBAL_CONTEXT_EPTP_ENT1_h": {"value":"40000000","position":0x3f,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CONTEXT_EPTP_ENT1 h "},\
"GLOBAL_CONTEXT_EPTP_ENT2_l": {"value":"00000000","position":0x40,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CONTEXT_EPTP_ENT2 l "},\
"GLOBAL_CONTEXT_EPTP_ENT2_h": {"value":"80000000","position":0x41,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CONTEXT_EPTP_ENT2 h "},\
"GLOBAL_CONTEXT_EPTP_ENT3_l": {"value":"00000000","position":0x42,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CONTEXT_EPTP_ENT3 l "},\
"GLOBAL_CONTEXT_EPTP_ENT3_h": {"value":"C0000000","position":0x43,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CONTEXT_EPTP_ENT3 h "},\
"HARDWARE_CR3_l": {"value":"00187000","position":0x44,"offset":0x0,"size":0x4,"DOC":"HARDWARE_CR3 l "},\
"HARDWARE_CR3_h": {"value":"00000000","position":0x45,"offset":0x0,"size":0x4,"DOC":"HARDWARE_CR3 h "},\
"VPID_GLOBAL_CONTEXT_VPID_ENT0": {"value":"00000000","position":0x46,"offset":0x0,"size":0x4,"DOC":"VPID_GLOBAL_CONTEXT_VPID_ENT0 "},\
"GLOBAL_CONTEXT_VPID_ENT1_GLOBAL_CONTEXT_VPID_ENT2": {"value":"00000000","position":0x47,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CONTEXT_VPID_ENT1_GLOBAL_CONTEXT_VPID_ENT2 "},\
"GLOBAL_CONTEXT_VPID_ENT3_l": {"value":"00000000","position":0x48,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CONTEXT_VPID_ENT3 l "},\
"GLOBAL_CONTEXT_VPID_ENT3_h": {"value":"00000000","position":0x49,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CONTEXT_VPID_ENT3 h "},\
"FCR17_l": {"value":"000C25AB","position":0x4a,"offset":0x0,"size":0x4,"DOC":"FCR17 l "},\
"FCR17_h": {"value":"00000007","position":0x4b,"offset":0x0,"size":0x4,"DOC":"FCR17 h "},\
"KERNEL_GS_BASE_l": {"value":"FFFAC000","position":0x4c,"offset":0x0,"size":0x4,"DOC":"KERNEL_GS_BASE l "},\
"KERNEL_GS_BASE_h": {"value":"000007FF","position":0x4d,"offset":0x0,"size":0x4,"DOC":"KERNEL_GS_BASE h "},\
"SYSENTER_ESP_l": {"value":"00000000","position":0x4e,"offset":0x0,"size":0x4,"DOC":"SYSENTER_ESP l "},\
"SYSENTER_ESP_h": {"value":"00000000","position":0x4f,"offset":0x0,"size":0x4,"DOC":"SYSENTER_ESP h "},\
"IA32_STAR_l": {"value":"00000000","position":0x50,"offset":0x0,"size":0x4,"DOC":"IA32_STAR l "},\
"IA32_STAR_h": {"value":"00230010","position":0x51,"offset":0x0,"size":0x4,"DOC":"IA32_STAR h "},\
"IA32_CSTAR_l": {"value":"02E86900","position":0x52,"offset":0x0,"size":0x4,"DOC":"IA32_CSTAR l "},\
"IA32_CSTAR_h": {"value":"FFFFF800","position":0x53,"offset":0x0,"size":0x4,"DOC":"IA32_CSTAR h "},\
"IA32_BIOS_SIG_l": {"value":"00000000","position":0x54,"offset":0x0,"size":0x4,"DOC":"IA32_BIOS_SIG l "},\
"IA32_BIOS_SIG_h": {"value":"00005005","position":0x55,"offset":0x0,"size":0x4,"DOC":"IA32_BIOS_SIG h "},\
"VMX_BASIC_l": {"value":"00000007","position":0x56,"offset":0x0,"size":0x4,"DOC":"VMX_BASIC l "},\
"VMX_BASIC_h": {"value":"00D80400","position":0x57,"offset":0x0,"size":0x4,"DOC":"VMX_BASIC h "},\
"VMX_PINBASED_CTLS_l": {"value":"00000016","position":0x58,"offset":0x0,"size":0x4,"DOC":"VMX_PINBASED_CTLS l "},\
"VMX_PINBASED_CTLS_h": {"value":"0000003F","position":0x59,"offset":0x0,"size":0x4,"DOC":"VMX_PINBASED_CTLS h "},\
"VMX_PROCBASED_CTLS_l": {"value":"0401E172","position":0x5a,"offset":0x0,"size":0x4,"DOC":"VMX_PROCBASED_CTLS l "},\
"VMX_PROCBASED_CTLS_h": {"value":"FFF9FFFE","position":0x5b,"offset":0x0,"size":0x4,"DOC":"VMX_PROCBASED_CTLS h "},\
"VMX_PROCBASED_CTLS2_l": {"value":"00000000","position":0x5c,"offset":0x0,"size":0x4,"DOC":"VMX_PROCBASED_CTLS2 l "},\
"VMX_PROCBASED_CTLS2_h": {"value":"00001CFE","position":0x5d,"offset":0x0,"size":0x4,"DOC":"VMX_PROCBASED_CTLS2 h "},\
"VMX_EXIT_CTLS_l": {"value":"00036DFF","position":0x5e,"offset":0x0,"size":0x4,"DOC":"VMX_EXIT_CTLS l "},\
"VMX_EXIT_CTLS_h": {"value":"003FFFFF","position":0x5f,"offset":0x0,"size":0x4,"DOC":"VMX_EXIT_CTLS h "},\
"VMX_ENTRY_CTLS_l": {"value":"000011FF","position":0x60,"offset":0x0,"size":0x4,"DOC":"VMX_ENTRY_CTLS l "},\
"VMX_ENTRY_CTLS_h": {"value":"0000FFFF","position":0x61,"offset":0x0,"size":0x4,"DOC":"VMX_ENTRY_CTLS h "},\
"VMX_EPT_VPID_CAP_l": {"value":"06134141","position":0x62,"offset":0x0,"size":0x4,"DOC":"VMX_EPT_VPID_CAP l "},\
"VMX_EPT_VPID_CAP_h": {"value":"00000F01","position":0x63,"offset":0x0,"size":0x4,"DOC":"VMX_EPT_VPID_CAP h "},\
"VMX_TRUE_PINBASED_CTLS_l": {"value":"00000016","position":0x64,"offset":0x0,"size":0x4,"DOC":"VMX_TRUE_PINBASED_CTLS l "},\
"VMX_TRUE_PINBASED_CTLS_h": {"value":"0000003F","position":0x65,"offset":0x0,"size":0x4,"DOC":"VMX_TRUE_PINBASED_CTLS h "},\
"VMX_TRUE_PROCBASED_CTLS_l": {"value":"04006172","position":0x66,"offset":0x0,"size":0x4,"DOC":"VMX_TRUE_PROCBASED_CTLS l "},\
"VMX_TRUE_PROCBASED_CTLS_h": {"value":"FFF9FFFE","position":0x67,"offset":0x0,"size":0x4,"DOC":"VMX_TRUE_PROCBASED_CTLS h "},\
"VMX_TRUE_EXIT_CTLS_l": {"value":"00036DFB","position":0x68,"offset":0x0,"size":0x4,"DOC":"VMX_TRUE_EXIT_CTLS l "},\
"VMX_TRUE_EXIT_CTLS_h": {"value":"003FFFFF","position":0x69,"offset":0x0,"size":0x4,"DOC":"VMX_TRUE_EXIT_CTLS h "},\
"VMX_TRUE_ENTRY_CTLS_l": {"value":"000011FB","position":0x6a,"offset":0x0,"size":0x4,"DOC":"VMX_TRUE_ENTRY_CTLS l "},\
"VMX_TRUE_ENTRY_CTLS_h": {"value":"0000FFFF","position":0x6b,"offset":0x0,"size":0x4,"DOC":"VMX_TRUE_ENTRY_CTLS h "},\
"VMX_MISC_l": {"value":"000401E0","position":0x6c,"offset":0x0,"size":0x4,"DOC":"VMX_MISC l "},\
"VMX_MISC_h": {"value":"00000000","position":0x6d,"offset":0x0,"size":0x4,"DOC":"VMX_MISC h "},\
"VMX_CR0_FIXED0_l": {"value":"80000021","position":0x6e,"offset":0x0,"size":0x4,"DOC":"VMX_CR0_FIXED0 l "},\
"VMX_CR0_FIXED0_h": {"value":"00000000","position":0x6f,"offset":0x0,"size":0x4,"DOC":"VMX_CR0_FIXED0 h "},\
"VMX_CR0_FIXED1_l": {"value":"FFFFFFFF","position":0x70,"offset":0x0,"size":0x4,"DOC":"VMX_CR0_FIXED1 l "},\
"VMX_CR0_FIXED1_h": {"value":"00000000","position":0x71,"offset":0x0,"size":0x4,"DOC":"VMX_CR0_FIXED1 h "},\
"VMX_CR4_FIXED0_l": {"value":"00002000","position":0x72,"offset":0x0,"size":0x4,"DOC":"VMX_CR4_FIXED0 l "},\
"VMX_CR4_FIXED0_h": {"value":"00000000","position":0x73,"offset":0x0,"size":0x4,"DOC":"VMX_CR4_FIXED0 h "},\
"VMX_CR4_FIXED1_l": {"value":"003727FF","position":0x74,"offset":0x0,"size":0x4,"DOC":"VMX_CR4_FIXED1 l "},\
"VMX_CR4_FIXED1_h": {"value":"00000000","position":0x75,"offset":0x0,"size":0x4,"DOC":"VMX_CR4_FIXED1 h "},\
"VMX_VMCS_ENUM_l": {"value":"0000002A","position":0x76,"offset":0x0,"size":0x4,"DOC":"VMX_VMCS_ENUM l "},\
"VMX_VMCS_ENUM_h": {"value":"00000000","position":0x77,"offset":0x0,"size":0x4,"DOC":"VMX_VMCS_ENUM h "},\
"FCR6_l": {"value":"68532020","position":0x78,"offset":0x0,"size":0x4,"DOC":"FCR6 l "},\
"FCR6_h": {"value":"68676E61","position":0x79,"offset":0x0,"size":0x4,"DOC":"FCR6 h "},\
"FCR8_l": {"value":"00000000","position":0x7a,"offset":0x0,"size":0x4,"DOC":"FCR8 l "},\
"FCR8_h": {"value":"00000000","position":0x7b,"offset":0x0,"size":0x4,"DOC":"FCR8 h "},\
"FCR9_l": {"value":"00000000","position":0x7c,"offset":0x0,"size":0x4,"DOC":"FCR9 l "},\
"FCR9_h": {"value":"00000000","position":0x7d,"offset":0x0,"size":0x4,"DOC":"FCR9 h "},\
"FCR10_l": {"value":"00000000","position":0x7e,"offset":0x0,"size":0x4,"DOC":"FCR10 l "},\
"FCR10_h": {"value":"00000000","position":0x7f,"offset":0x0,"size":0x4,"DOC":"FCR10 h "},\
"FCR11_l": {"value":"00000000","position":0x80,"offset":0x0,"size":0x4,"DOC":"FCR11 l "},\
"FCR11_h": {"value":"00000000","position":0x81,"offset":0x0,"size":0x4,"DOC":"FCR11 h "},\
"FCR12_l": {"value":"00000000","position":0x82,"offset":0x0,"size":0x4,"DOC":"FCR12 l "},\
"FCR12_h": {"value":"00000000","position":0x83,"offset":0x0,"size":0x4,"DOC":"FCR12 h "},\
"FCR13_l": {"value":"00000000","position":0x84,"offset":0x0,"size":0x4,"DOC":"FCR13 l "},\
"FCR13_h": {"value":"00000000","position":0x85,"offset":0x0,"size":0x4,"DOC":"FCR13 h "},\
"TURBO_MODE_CONFIG_2_l": {"value":"00000000","position":0x86,"offset":0x0,"size":0x4,"DOC":"TURBO_MODE_CONFIG_2 l "},\
"TURBO_MODE_CONFIG_2_h": {"value":"00000000","position":0x87,"offset":0x0,"size":0x4,"DOC":"TURBO_MODE_CONFIG_2 h "},\
"PAD67_l": {"value":"00000000","position":0x88,"offset":0x0,"size":0x4,"DOC":"PAD67 l "},\
"PAD67_h": {"value":"00000000","position":0x89,"offset":0x0,"size":0x4,"DOC":"PAD67 h "},\
"FCR7_l": {"value":"20206961","position":0x8a,"offset":0x0,"size":0x4,"DOC":"FCR7 l "},\
"FCR7_h": {"value":"00000000","position":0x8b,"offset":0x0,"size":0x4,"DOC":"FCR7 h "},\
"PERF_GLOBAL_CTRL_l": {"value":"0000000F","position":0x8c,"offset":0x0,"size":0x4,"DOC":"PERF_GLOBAL_CTRL l "},\
"PERF_GLOBAL_CTRL_h": {"value":"00000007","position":0x8d,"offset":0x0,"size":0x4,"DOC":"PERF_GLOBAL_CTRL h "},\
"TR2_l": {"value":"77FBF2AC","position":0x8e,"offset":0x0,"size":0x4,"DOC":"TR2 l "},\
"TR2_h": {"value":"01000005","position":0x8f,"offset":0x0,"size":0x4,"DOC":"TR2 h "},\
"TR3_l": {"value":"000BB249","position":0x90,"offset":0x0,"size":0x4,"DOC":"TR3 l "},\
"TR3_h": {"value":"000B0003","position":0x91,"offset":0x0,"size":0x4,"DOC":"TR3 h "},\
"TR4_l": {"value":"00000000","position":0x92,"offset":0x0,"size":0x4,"DOC":"TR4 l "},\
"TR4_h": {"value":"00000000","position":0x93,"offset":0x0,"size":0x4,"DOC":"TR4 h "},\
"TR5_l": {"value":"40000000","position":0x94,"offset":0x0,"size":0x4,"DOC":"TR5 l "},\
"TR5_h": {"value":"00000000","position":0x95,"offset":0x0,"size":0x4,"DOC":"TR5 h "},\
"TR6_l": {"value":"00002180","position":0x96,"offset":0x0,"size":0x4,"DOC":"TR6 l "},\
"TR6_h": {"value":"00000800","position":0x97,"offset":0x0,"size":0x4,"DOC":"TR6 h "},\
"TR7_l": {"value":"FFFC0000","position":0x98,"offset":0x0,"size":0x4,"DOC":"TR7 l "},\
"TR7_h": {"value":"FFFFFFFF","position":0x99,"offset":0x0,"size":0x4,"DOC":"TR7 h "},\
"TR1_l": {"value":"80000000","position":0x9a,"offset":0x0,"size":0x4,"DOC":"TR1 l "},\
"TR1_h": {"value":"00000000","position":0x9b,"offset":0x0,"size":0x4,"DOC":"TR1 h "},\
"DS_AREA_l": {"value":"00000000","position":0x9c,"offset":0x0,"size":0x4,"DOC":"DS_AREA l "},\
"DS_AREA_h": {"value":"00000000","position":0x9d,"offset":0x0,"size":0x4,"DOC":"DS_AREA h "},\
"FCR0_FUSES_l": {"value":"00000000","position":0x9e,"offset":0x0,"size":0x4,"DOC":"FCR0_FUSES l "},\
"FCR0_FUSES_h": {"value":"00000000","position":0x9f,"offset":0x0,"size":0x4,"DOC":"FCR0_FUSES h "},\
"FCR1_FUSES_l": {"value":"00000000","position":0xa0,"offset":0x0,"size":0x4,"DOC":"FCR1_FUSES l "},\
"FCR1_FUSES_h": {"value":"00000000","position":0xa1,"offset":0x0,"size":0x4,"DOC":"FCR1_FUSES h "},\
"FCR3_RESET_l": {"value":"00000018","position":0xa2,"offset":0x0,"size":0x4,"DOC":"FCR3_RESET l "},\
"FCR3_RESET_h": {"value":"00000000","position":0xa3,"offset":0x0,"size":0x4,"DOC":"FCR3_RESET h "},\
"SYSEXIT_SSDESC_l": {"value":"0000FFFF","position":0xa4,"offset":0x0,"size":0x4,"DOC":"SYSEXIT_SSDESC l "},\
"SYSEXIT_SSDESC_h": {"value":"00CFF300","position":0xa5,"offset":0x0,"size":0x4,"DOC":"SYSEXIT_SSDESC h "},\
"VMXON_PTR_l": {"value":"00000000","position":0xa6,"offset":0x0,"size":0x4,"DOC":"VMXON_PTR l "},\
"VMXON_PTR_h": {"value":"00000000","position":0xa7,"offset":0x0,"size":0x4,"DOC":"VMXON_PTR h "},\
"CURRENT_VMCS_DESC_l": {"value":"0000FFFF","position":0xa8,"offset":0x0,"size":0x4,"DOC":"CURRENT_VMCS_DESC l "},\
"CURRENT_VMCS_DESC_h": {"value":"00008B00","position":0xa9,"offset":0x0,"size":0x4,"DOC":"CURRENT_VMCS_DESC h "},\
"VMX_IIR_SAVE_l": {"value":"00000000","position":0xaa,"offset":0x0,"size":0x4,"DOC":"VMX_IIR_SAVE l "},\
"VMX_IIR_SAVE_h": {"value":"00000000","position":0xab,"offset":0x0,"size":0x4,"DOC":"VMX_IIR_SAVE h "},\
"VMX_EXCEPTION_CS_DESC_l": {"value":"00000000","position":0xac,"offset":0x0,"size":0x4,"DOC":"VMX_EXCEPTION_CS_DESC l "},\
"VMX_EXCEPTION_CS_DESC_h": {"value":"00000000","position":0xad,"offset":0x0,"size":0x4,"DOC":"VMX_EXCEPTION_CS_DESC h "},\
"CR4_ALLOWED_MASK_l": {"value":"003767FF","position":0xae,"offset":0x0,"size":0x4,"DOC":"CR4_ALLOWED_MASK l "},\
"CR4_ALLOWED_MASK_h": {"value":"00000000","position":0xaf,"offset":0x0,"size":0x4,"DOC":"CR4_ALLOWED_MASK h "},\
"FCR0_ALLOWED_MASK_l": {"value":"FFFFFFFF","position":0xb0,"offset":0x0,"size":0x4,"DOC":"FCR0_ALLOWED_MASK l "},\
"FCR0_ALLOWED_MASK_h": {"value":"FFFFFFFF","position":0xb1,"offset":0x0,"size":0x4,"DOC":"FCR0_ALLOWED_MASK h "},\
"FCR1_ALLOWED_MASK_l": {"value":"2E100800","position":0xb2,"offset":0x0,"size":0x4,"DOC":"FCR1_ALLOWED_MASK l "},\
"FCR1_ALLOWED_MASK_h": {"value":"00000121","position":0xb3,"offset":0x0,"size":0x4,"DOC":"FCR1_ALLOWED_MASK h "},\
"IO_RSTRT_ECX_l": {"value":"00000000","position":0xb4,"offset":0x0,"size":0x4,"DOC":"IO_RSTRT_ECX l "},\
"IO_RSTRT_ECX_h": {"value":"00000000","position":0xb5,"offset":0x0,"size":0x4,"DOC":"IO_RSTRT_ECX h "},\
"IO_RSTRT_ESI_l": {"value":"00000000","position":0xb6,"offset":0x0,"size":0x4,"DOC":"IO_RSTRT_ESI l "},\
"IO_RSTRT_ESI_h": {"value":"00000000","position":0xb7,"offset":0x0,"size":0x4,"DOC":"IO_RSTRT_ESI h "},\
"IO_RSTRT_EDI_l": {"value":"00000000","position":0xb8,"offset":0x0,"size":0x4,"DOC":"IO_RSTRT_EDI l "},\
"IO_RSTRT_EDI_h": {"value":"00000000","position":0xb9,"offset":0x0,"size":0x4,"DOC":"IO_RSTRT_EDI h "},\
"IO_RSTRT_EIP_l": {"value":"00000000","position":0xba,"offset":0x0,"size":0x4,"DOC":"IO_RSTRT_EIP l "},\
"IO_RSTRT_EIP_h": {"value":"00000000","position":0xbb,"offset":0x0,"size":0x4,"DOC":"IO_RSTRT_EIP h "},\
"IO_RSTRT_MEM_l": {"value":"00000000","position":0xbc,"offset":0x0,"size":0x4,"DOC":"IO_RSTRT_MEM l "},\
"IO_RSTRT_MEM_h": {"value":"00000000","position":0xbd,"offset":0x0,"size":0x4,"DOC":"IO_RSTRT_MEM h "},\
"FCR82_l": {"value":"00000040","position":0xbe,"offset":0x0,"size":0x4,"DOC":"FCR82 l "},\
"FCR82_h": {"value":"10004000","position":0xbf,"offset":0x0,"size":0x4,"DOC":"FCR82 h "},\
"POWER_CTL_l": {"value":"00000000","position":0xc0,"offset":0x0,"size":0x4,"DOC":"POWER_CTL l "},\
"POWER_CTL_h": {"value":"00000000","position":0xc1,"offset":0x0,"size":0x4,"DOC":"POWER_CTL h "},\
"SMM_TRANSFER_PTR_l": {"value":"00000000","position":0xc2,"offset":0x0,"size":0x4,"DOC":"SMM_TRANSFER_PTR l "},\
"SMM_TRANSFER_PTR_h": {"value":"00000000","position":0xc3,"offset":0x0,"size":0x4,"DOC":"SMM_TRANSFER_PTR h "},\
"VMX_EXCEPTION_SS_DESC_l": {"value":"00000000","position":0xc4,"offset":0x0,"size":0x4,"DOC":"VMX_EXCEPTION_SS_DESC l "},\
"VMX_EXCEPTION_SS_DESC_h": {"value":"00000000","position":0xc5,"offset":0x0,"size":0x4,"DOC":"VMX_EXCEPTION_SS_DESC h "},\
"TR18_l": {"value":"00000000","position":0xc6,"offset":0x0,"size":0x4,"DOC":"TR18 l "},\
"TR18_h": {"value":"00000000","position":0xc7,"offset":0x0,"size":0x4,"DOC":"TR18 h "},\
"SP_CTRL0_l": {"value":"00000000","position":0xc8,"offset":0x0,"size":0x4,"DOC":"SP_CTRL0 l "},\
"SP_CTRL0_h": {"value":"00000000","position":0xc9,"offset":0x0,"size":0x4,"DOC":"SP_CTRL0 h "},\
"SP_CTRL1_l": {"value":"00000000","position":0xca,"offset":0x0,"size":0x4,"DOC":"SP_CTRL1 l "},\
"SP_CTRL1_h": {"value":"00000000","position":0xcb,"offset":0x0,"size":0x4,"DOC":"SP_CTRL1 h "},\
"TR14_l": {"value":"FFFFFFFF","position":0xcc,"offset":0x0,"size":0x4,"DOC":"TR14 l "},\
"TR14_h": {"value":"FFFFFFFF","position":0xcd,"offset":0x0,"size":0x4,"DOC":"TR14 h "},\
"PROC_NAME_BANK_0_l": {"value":"20202020","position":0xce,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_0 l "},\
"PROC_NAME_BANK_0_h": {"value":"20202020","position":0xcf,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_0 h "},\
"PROC_NAME_BANK_1_l": {"value":"20202020","position":0xd0,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_1 l "},\
"PROC_NAME_BANK_1_h": {"value":"20202020","position":0xd1,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_1 h "},\
"PROC_NAME_BANK_2_l": {"value":"20202020","position":0xd2,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_2 l "},\
"PROC_NAME_BANK_2_h": {"value":"43202020","position":0xd3,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_2 h "},\
"PROC_NAME_BANK_3_l": {"value":"6175512D","position":0xd4,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_3 l "},\
"PROC_NAME_BANK_3_h": {"value":"726F4364","position":0xd5,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_3 h "},\
"PROC_NAME_BANK_4_l": {"value":"43204D65","position":0xd6,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_4 l "},\
"PROC_NAME_BANK_4_h": {"value":"30303634","position":0xd7,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_4 h "},\
"PROC_NAME_BANK_5_l": {"value":"302E3240","position":0xd8,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_5 l "},\
"PROC_NAME_BANK_5_h": {"value":"007A4847","position":0xd9,"offset":0x0,"size":0x4,"DOC":"PROC_NAME_BANK_5 h "},\
"SP_CTRL2_l": {"value":"00000000","position":0xda,"offset":0x0,"size":0x4,"DOC":"SP_CTRL2 l "},\
"SP_CTRL2_h": {"value":"00000000","position":0xdb,"offset":0x0,"size":0x4,"DOC":"SP_CTRL2 h "},\
"FCR35_l": {"value":"00000000","position":0xdc,"offset":0x0,"size":0x4,"DOC":"FCR35 l "},\
"FCR35_h": {"value":"00000000","position":0xdd,"offset":0x0,"size":0x4,"DOC":"FCR35 h "},\
"TURBO_MODE_CONFIG_1_l": {"value":"00000000","position":0xde,"offset":0x0,"size":0x4,"DOC":"TURBO_MODE_CONFIG_1 l "},\
"TURBO_MODE_CONFIG_1_h": {"value":"00000000","position":0xdf,"offset":0x0,"size":0x4,"DOC":"TURBO_MODE_CONFIG_1 h "},\
"TR_EVENT_CAUSE_l": {"value":"80000000","position":0xe0,"offset":0x0,"size":0x4,"DOC":"TR_EVENT_CAUSE l "},\
"TR_EVENT_CAUSE_h": {"value":"00000000","position":0xe1,"offset":0x0,"size":0x4,"DOC":"TR_EVENT_CAUSE h "},\
"LAST_PAUSE_TIME_l": {"value":"00000000","position":0xe2,"offset":0x0,"size":0x4,"DOC":"LAST_PAUSE_TIME l "},\
"LAST_PAUSE_TIME_h": {"value":"00000000","position":0xe3,"offset":0x0,"size":0x4,"DOC":"LAST_PAUSE_TIME h "},\
"FIRST_PAUSE_TIME_l": {"value":"00000000","position":0xe4,"offset":0x0,"size":0x4,"DOC":"FIRST_PAUSE_TIME l "},\
"FIRST_PAUSE_TIME_h": {"value":"00000000","position":0xe5,"offset":0x0,"size":0x4,"DOC":"FIRST_PAUSE_TIME h "},\
"RESTART_IP_SAVE_l": {"value":"00000000","position":0xe6,"offset":0x0,"size":0x4,"DOC":"RESTART_IP_SAVE l "},\
"RESTART_IP_SAVE_h": {"value":"00000000","position":0xe7,"offset":0x0,"size":0x4,"DOC":"RESTART_IP_SAVE h "},\
"PWR_CTRL_HI_l": {"value":"3E9D2E9C","position":0xe8,"offset":0x0,"size":0x4,"DOC":"PWR_CTRL_HI l "},\
"PWR_CTRL_HI_h": {"value":"00003E9D","position":0xe9,"offset":0x0,"size":0x4,"DOC":"PWR_CTRL_HI h "},\
"DYNAMIC_PWR_CTRL_l": {"value":"00010042","position":0xea,"offset":0x0,"size":0x4,"DOC":"DYNAMIC_PWR_CTRL l "},\
"DYNAMIC_PWR_CTRL_h": {"value":"00020001","position":0xeb,"offset":0x0,"size":0x4,"DOC":"DYNAMIC_PWR_CTRL h "},\
"IDT_EFLAGS_TO_SAVE_SHADOW_l": {"value":"00000287","position":0xec,"offset":0x0,"size":0x4,"DOC":"IDT_EFLAGS_TO_SAVE_SHADOW l "},\
"IDT_EFLAGS_TO_SAVE_SHADOW_h": {"value":"00000000","position":0xed,"offset":0x0,"size":0x4,"DOC":"IDT_EFLAGS_TO_SAVE_SHADOW h "},\
"MSR_IA32_TSC_ADJUST_l": {"value":"E7ECC16E","position":0xee,"offset":0x0,"size":0x4,"DOC":"MSR_IA32_TSC_ADJUST l "},\
"MSR_IA32_TSC_ADJUST_h": {"value":"FFFFFFE6","position":0xef,"offset":0x0,"size":0x4,"DOC":"MSR_IA32_TSC_ADJUST h "},\
"PRNG_CNTRL_l": {"value":"00000000","position":0xf0,"offset":0x0,"size":0x4,"DOC":"PRNG_CNTRL l "},\
"PRNG_CNTRL_h": {"value":"00000000","position":0xf1,"offset":0x0,"size":0x4,"DOC":"PRNG_CNTRL h "},\
"PRNG_DATA0_l": {"value":"00000000","position":0xf2,"offset":0x0,"size":0x4,"DOC":"PRNG_DATA0 l "},\
"PRNG_DATA0_h": {"value":"00000000","position":0xf3,"offset":0x0,"size":0x4,"DOC":"PRNG_DATA0 h "},\
"PRNG_DATA1_l": {"value":"00000000","position":0xf4,"offset":0x0,"size":0x4,"DOC":"PRNG_DATA1 l "},\
"PRNG_DATA1_h": {"value":"00000000","position":0xf5,"offset":0x0,"size":0x4,"DOC":"PRNG_DATA1 h "},\
"PRNG_SEED_l": {"value":"240EC6F2","position":0xf6,"offset":0x0,"size":0x4,"DOC":"PRNG_SEED l "},\
"PRNG_SEED_h": {"value":"B4180C59","position":0xf7,"offset":0x0,"size":0x4,"DOC":"PRNG_SEED h "},\
"PRNG_SEED_DETERMINED_l": {"value":"00000000","position":0xf8,"offset":0x0,"size":0x4,"DOC":"PRNG_SEED_DETERMINED l "},\
"PRNG_SEED_DETERMINED_h": {"value":"00000000","position":0xf9,"offset":0x0,"size":0x4,"DOC":"PRNG_SEED_DETERMINED h "},\
"PRNG_KEY1_l": {"value":"240EC6F2","position":0xfa,"offset":0x0,"size":0x4,"DOC":"PRNG_KEY1 l "},\
"PRNG_KEY1_h": {"value":"B4180C59","position":0xfb,"offset":0x0,"size":0x4,"DOC":"PRNG_KEY1 h "},\
"PRNG_KEY2_l": {"value":"240EC6F2","position":0xfc,"offset":0x0,"size":0x4,"DOC":"PRNG_KEY2 l "},\
"PRNG_KEY2_h": {"value":"B4180C59","position":0xfd,"offset":0x0,"size":0x4,"DOC":"PRNG_KEY2 h "},\
"SAVED_UEXCEPT_l": {"value":"00000000","position":0xfe,"offset":0x0,"size":0x4,"DOC":"SAVED_UEXCEPT l "},\
"SAVED_UEXCEPT_h": {"value":"00000000","position":0xff,"offset":0x0,"size":0x4,"DOC":"SAVED_UEXCEPT h "},\
"PATCH_OVERLAY_START_l": {"value":"F8400384","position":0x100,"offset":0x0,"size":0x4,"DOC":"PATCH_OVERLAY_START l "},\
"PATCH_OVERLAY_START_h": {"value":"000000C8","position":0x101,"offset":0x0,"size":0x4,"DOC":"PATCH_OVERLAY_START h "},\
"MSR_CORE_SCRATCH_BIOS_l": {"value":"00000000","position":0x102,"offset":0x0,"size":0x4,"DOC":"MSR_CORE_SCRATCH_BIOS l "},\
"MSR_CORE_SCRATCH_BIOS_h": {"value":"00000000","position":0x103,"offset":0x0,"size":0x4,"DOC":"MSR_CORE_SCRATCH_BIOS h "},\
"MSR_CORE_SCRATCH_0_l": {"value":"00000000","position":0x104,"offset":0x0,"size":0x4,"DOC":"MSR_CORE_SCRATCH_0 l "},\
"MSR_CORE_SCRATCH_0_h": {"value":"00000000","position":0x105,"offset":0x0,"size":0x4,"DOC":"MSR_CORE_SCRATCH_0 h "},\
"OLD_XCR_l": {"value":"00000000","position":0x106,"offset":0x0,"size":0x4,"DOC":"OLD_XCR l "},\
"OLD_XCR_h": {"value":"00000000","position":0x107,"offset":0x0,"size":0x4,"DOC":"OLD_XCR h "},\
"DR7_SAVE": {"value":"00000000","position":0x108,"offset":0x0,"size":0x4,"DOC":"DR7_SAVE "},\
"MSR_IO_BASE_P": {"value":"00000814","position":0x109,"offset":0x0,"size":0x4,"DOC":"MSR_IO_BASE_P "},\
"MSR_IO_CAPT_P": {"value":"00030814","position":0x10a,"offset":0x0,"size":0x4,"DOC":"MSR_IO_CAPT_P "},\
"FSR1": {"value":"F8400380","position":0x10b,"offset":0x0,"size":0x4,"DOC":"FSR1 "},\
"IA32_FMASK": {"value":"00004700","position":0x10c,"offset":0x0,"size":0x4,"DOC":"IA32_FMASK "},\
"IA32_SMM_MONITOR_CTL": {"value":"00000000","position":0x10d,"offset":0x0,"size":0x4,"DOC":"IA32_SMM_MONITOR_CTL "},\
"VMX_JCR_SAVE": {"value":"00615D00","position":0x10e,"offset":0x0,"size":0x4,"DOC":"VMX_JCR_SAVE "},\
"VMX_EFLAGS_SAVE": {"value":"00000000","position":0x10f,"offset":0x0,"size":0x4,"DOC":"VMX_EFLAGS_SAVE "},\
"VMX_INTERRUPTION_INFO": {"value":"000000B4","position":0x110,"offset":0x0,"size":0x4,"DOC":"VMX_INTERRUPTION_INFO "},\
"IO_RSTRT_STATE": {"value":"00640012","position":0x111,"offset":0x0,"size":0x4,"DOC":"IO_RSTRT_STATE "},\
"SMM_XMR": {"value":"00000003","position":0x112,"offset":0x0,"size":0x4,"DOC":"SMM_XMR "},\
"CST_CONTROL": {"value":"01000401","position":0x113,"offset":0x0,"size":0x4,"DOC":"CST_CONTROL "},\
"TR8": {"value":"00000000","position":0x114,"offset":0x0,"size":0x4,"DOC":"TR8 "},\
"CURRENT_VMCS_DESC_EXT": {"value":"00000000","position":0x115,"offset":0x0,"size":0x4,"DOC":"CURRENT_VMCS_DESC_EXT "},\
"TURBO_MODE_HCR3_SAVE": {"value":"2A750090","position":0x116,"offset":0x0,"size":0x4,"DOC":"TURBO_MODE_HCR3_SAVE "},\
"SMI_CNT": {"value":"00000560","position":0x117,"offset":0x0,"size":0x4,"DOC":"SMI_CNT "},\
"INTR_CNT": {"value":"005E1B8E","position":0x118,"offset":0x0,"size":0x4,"DOC":"INTR_CNT "},\
"NMI_CNT": {"value":"00000000","position":0x119,"offset":0x0,"size":0x4,"DOC":"NMI_CNT "},\
"A20_CNT": {"value":"00000000","position":0x11a,"offset":0x0,"size":0x4,"DOC":"A20_CNT "},\
"MC_CNT": {"value":"00000000","position":0x11b,"offset":0x0,"size":0x4,"DOC":"MC_CNT "},\
"SKIP_MSRGP_CNT": {"value":"00000004","position":0x11c,"offset":0x0,"size":0x4,"DOC":"SKIP_MSRGP_CNT "},\
"TRACER_DEADLOCK_RESTART_CNT": {"value":"00000000","position":0x11d,"offset":0x0,"size":0x4,"DOC":"TRACER_DEADLOCK_RESTART_CNT "},\
"WBINVD_DEADLOCK_RESTART_CNT": {"value":"00000000","position":0x11e,"offset":0x0,"size":0x4,"DOC":"WBINVD_DEADLOCK_RESTART_CNT "},\
"MWAIT_DEADLOCK_BLOWOFF_CNT": {"value":"00000000","position":0x11f,"offset":0x0,"size":0x4,"DOC":"MWAIT_DEADLOCK_BLOWOFF_CNT "},\
"PATCH_DEADLOCK_BLOWOFF_CNT": {"value":"00000000","position":0x120,"offset":0x0,"size":0x4,"DOC":"PATCH_DEADLOCK_BLOWOFF_CNT "},\
"LAST_SYNC_CODE": {"value":"00800411","position":0x121,"offset":0x0,"size":0x4,"DOC":"LAST_SYNC_CODE "},\
"TR9": {"value":"00000000","position":0x122,"offset":0x0,"size":0x4,"DOC":"TR9 "},\
"AUX_TSC": {"value":"00000000","position":0x123,"offset":0x0,"size":0x4,"DOC":"AUX_TSC "},\
"EFER_ALLOWED_MASK": {"value":"00002D01","position":0x124,"offset":0x0,"size":0x4,"DOC":"EFER_ALLOWED_MASK "},\
"PWR_ACTION": {"value":"00000000","position":0x125,"offset":0x0,"size":0x4,"DOC":"PWR_ACTION "},\
"LAST_INTR_IPR": {"value":"00009000","position":0x126,"offset":0x0,"size":0x4,"DOC":"LAST_INTR_IPR "},\
"MWAIT_EF_SAVE": {"value":"00000000","position":0x127,"offset":0x0,"size":0x4,"DOC":"MWAIT_EF_SAVE "},\
"HCR2_PRAM": {"value":"0000C800","position":0x128,"offset":0x0,"size":0x4,"DOC":"HCR2_PRAM "},\
"HCR7_PRAM": {"value":"00000000","position":0x129,"offset":0x0,"size":0x4,"DOC":"HCR7_PRAM "},\
"LAST_SLEEP_CODE": {"value":"00000000","position":0x12a,"offset":0x0,"size":0x4,"DOC":"LAST_SLEEP_CODE "},\
"PERF_STATUS_UP": {"value":"00000000","position":0x12b,"offset":0x0,"size":0x4,"DOC":"PERF_STATUS_UP "},\
"IA32_FEATURE_CONTROL_IA32_MONITOR_FILTER_SIZE": {"value":"00400005","position":0x12c,"offset":0x0,"size":0x4,"DOC":"IA32_FEATURE_CONTROL_IA32_MONITOR_FILTER_SIZE "},\
"SMI_CR4_SAVE_SMI_MTF_SAVE": {"value":"000006F8","position":0x12d,"offset":0x0,"size":0x4,"DOC":"SMI_CR4_SAVE_SMI_MTF_SAVE "},\
"PERF_CTRL0_PERF_CTRL1": {"value":"00000000","position":0x12e,"offset":0x0,"size":0x4,"DOC":"PERF_CTRL0_PERF_CTRL1 "},\
"PERF_CTRL2_ROM_VERSION_INSTALLED": {"value":"00000000","position":0x12f,"offset":0x0,"size":0x4,"DOC":"PERF_CTRL2_ROM_VERSION_INSTALLED "},\
"REAL_PSRUP_MAX_AES_VALID": {"value":"00000C63","position":0x130,"offset":0x0,"size":0x4,"DOC":"REAL_PSRUP_MAX_AES_VALID "},\
"PRAM_OVERLAY_BASE_XCR0_MCG_STATUS": {"value":"00010000","position":0x131,"offset":0x0,"size":0x4,"DOC":"PRAM_OVERLAY_BASE_XCR0_MCG_STATUS "},\
"VMX_CPL_SAVE_MAX_RATIO_PADDR_SIZE_FSB_FREQ": {"value":"04240C00","position":0x132,"offset":0x0,"size":0x4,"DOC":"VMX_CPL_SAVE_MAX_RATIO_PADDR_SIZE_FSB_FREQ "},\
"FUSE_ECC_RESULT_TR1_SUB_FIELD_NAP_VID_OFFSET_COMPOSITE_CST": {"value":"00000000","position":0x133,"offset":0x0,"size":0x4,"DOC":"FUSE_ECC_RESULT_TR1_SUB_FIELD_NAP_VID_OFFSET_COMPOSITE_CST "},\
"ORIG_VRM_RCVRY_DEL_TR_SWINT_VECTOR_UC_WAKEUP_DELAY_VDD_DEAD_FLG": {"value":"0014B400","position":0x134,"offset":0x0,"size":0x4,"DOC":"ORIG_VRM_RCVRY_DEL_TR_SWINT_VECTOR_UC_WAKEUP_DELAY_VDD_DEAD_FLG "},\
"PHYS_CORE_ID_VIRT_CORE_ID_VIRT_NUM_CORES_GLOBAL_CONTEXT": {"value":"00040000","position":0x135,"offset":0x0,"size":0x4,"DOC":"PHYS_CORE_ID_VIRT_CORE_ID_VIRT_NUM_CORES_GLOBAL_CONTEXT "},\
"IA32_ENERGY_PERF_BIAS_NUM_IO_TRANSLATE_DESC_PATCH_OVERLAY_INSTALLED_PATCH_STATE": {"value":"02000000","position":0x136,"offset":0x0,"size":0x4,"DOC":"IA32_ENERGY_PERF_BIAS_NUM_IO_TRANSLATE_DESC_PATCH_OVERLAY_INSTALLED_PATCH_STATE "},\
"FUSE_CTRLS_REPAIR_REBLOW_CTR": {"value":"003C0000","position":0x137,"offset":0x0,"size":0x4,"DOC":"FUSE_CTRLS_REPAIR_REBLOW_CTR "},\
"MTRR_PHYSBASE0_l": {"value":"00000006","position":0x138,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE0 l "},\
"MTRR_PHYSBASE0_h": {"value":"00000000","position":0x139,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE0 h "},\
"MTRR_PHYSMASK0_l": {"value":"80000800","position":0x13a,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK0 l "},\
"MTRR_PHYSMASK0_h": {"value":"0000000F","position":0x13b,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK0 h "},\
"MTRR_PHYSBASE1_l": {"value":"80000006","position":0x13c,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE1 l "},\
"MTRR_PHYSBASE1_h": {"value":"00000000","position":0x13d,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE1 h "},\
"MTRR_PHYSMASK1_l": {"value":"C0000800","position":0x13e,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK1 l "},\
"MTRR_PHYSMASK1_h": {"value":"0000000F","position":0x13f,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK1 h "},\
"MTRR_PHYSBASE2_l": {"value":"C0000006","position":0x140,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE2 l "},\
"MTRR_PHYSBASE2_h": {"value":"00000000","position":0x141,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE2 h "},\
"MTRR_PHYSMASK2_l": {"value":"F0000800","position":0x142,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK2 l "},\
"MTRR_PHYSMASK2_h": {"value":"0000000F","position":0x143,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK2 h "},\
"MTRR_PHYSBASE3_l": {"value":"40000000","position":0x144,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE3 l "},\
"MTRR_PHYSBASE3_h": {"value":"00000000","position":0x145,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE3 h "},\
"MTRR_PHYSMASK3_l": {"value":"F0000800","position":0x146,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK3 l "},\
"MTRR_PHYSMASK3_h": {"value":"0000000F","position":0x147,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK3 h "},\
"MTRR_PHYSBASE4_l": {"value":"00000006","position":0x148,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE4 l "},\
"MTRR_PHYSBASE4_h": {"value":"00000001","position":0x149,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE4 h "},\
"MTRR_PHYSMASK4_l": {"value":"E0000800","position":0x14a,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK4 l "},\
"MTRR_PHYSMASK4_h": {"value":"0000000F","position":0x14b,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK4 h "},\
"MTRR_PHYSBASE5_l": {"value":"00000000","position":0x14c,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE5 l "},\
"MTRR_PHYSBASE5_h": {"value":"00000000","position":0x14d,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE5 h "},\
"MTRR_PHYSMASK5_l": {"value":"00000000","position":0x14e,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK5 l "},\
"MTRR_PHYSMASK5_h": {"value":"00000000","position":0x14f,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK5 h "},\
"MTRR_PHYSBASE6_l": {"value":"00000000","position":0x150,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE6 l "},\
"MTRR_PHYSBASE6_h": {"value":"00000000","position":0x151,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE6 h "},\
"MTRR_PHYSMASK6_l": {"value":"00000000","position":0x152,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK6 l "},\
"MTRR_PHYSMASK6_h": {"value":"00000000","position":0x153,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK6 h "},\
"MTRR_PHYSBASE7_l": {"value":"00000000","position":0x154,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE7 l "},\
"MTRR_PHYSBASE7_h": {"value":"00000000","position":0x155,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSBASE7 h "},\
"MTRR_PHYSMASK7_l": {"value":"00000000","position":0x156,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK7 l "},\
"MTRR_PHYSMASK7_h": {"value":"00000000","position":0x157,"offset":0x0,"size":0x4,"DOC":"MTRR_PHYSMASK7 h "},\
"MTRR_FIX64K_00000_l": {"value":"06060606","position":0x158,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX64K_00000 l "},\
"MTRR_FIX64K_00000_h": {"value":"06060606","position":0x159,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX64K_00000 h "},\
"MTRR_FIX16K_80000_l": {"value":"06060606","position":0x15a,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX16K_80000 l "},\
"MTRR_FIX16K_80000_h": {"value":"06060606","position":0x15b,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX16K_80000 h "},\
"MTRR_FIX16K_A0000_l": {"value":"00000000","position":0x15c,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX16K_A0000 l "},\
"MTRR_FIX16K_A0000_h": {"value":"00000000","position":0x15d,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX16K_A0000 h "},\
"MTRR_FIX4K_C0000_l": {"value":"05050505","position":0x15e,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_C0000 l "},\
"MTRR_FIX4K_C0000_h": {"value":"05050505","position":0x15f,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_C0000 h "},\
"MTRR_FIX4K_C8000_l": {"value":"05050505","position":0x160,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_C8000 l "},\
"MTRR_FIX4K_C8000_h": {"value":"05050505","position":0x161,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_C8000 h "},\
"MTRR_FIX4K_D0000_l": {"value":"00000000","position":0x162,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_D0000 l "},\
"MTRR_FIX4K_D0000_h": {"value":"00000000","position":0x163,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_D0000 h "},\
"MTRR_FIX4K_D8000_l": {"value":"00000000","position":0x164,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_D8000 l "},\
"MTRR_FIX4K_D8000_h": {"value":"00000000","position":0x165,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_D8000 h "},\
"MTRR_FIX4K_E0000_l": {"value":"00000000","position":0x166,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_E0000 l "},\
"MTRR_FIX4K_E0000_h": {"value":"00000000","position":0x167,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_E0000 h "},\
"MTRR_FIX4K_E8000_l": {"value":"05050505","position":0x168,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_E8000 l "},\
"MTRR_FIX4K_E8000_h": {"value":"05050505","position":0x169,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_E8000 h "},\
"MTRR_FIX4K_F0000_l": {"value":"05050505","position":0x16a,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_F0000 l "},\
"MTRR_FIX4K_F0000_h": {"value":"05050505","position":0x16b,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_F0000 h "},\
"MTRR_FIX4K_F8000_l": {"value":"05050505","position":0x16c,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_F8000 l "},\
"MTRR_FIX4K_F8000_h": {"value":"05050505","position":0x16d,"offset":0x0,"size":0x4,"DOC":"MTRR_FIX4K_F8000 h "},\
"MTRR_DEF_TYPE_l": {"value":"00000C00","position":0x16e,"offset":0x0,"size":0x4,"DOC":"MTRR_DEF_TYPE l "},\
"MTRR_DEF_TYPE_h": {"value":"00000000","position":0x16f,"offset":0x0,"size":0x4,"DOC":"MTRR_DEF_TYPE h "},\
"SMRR_BASE_l": {"value":"CFF00004","position":0x170,"offset":0x0,"size":0x4,"DOC":"SMRR_BASE l "},\
"SMRR_BASE_h": {"value":"00000000","position":0x171,"offset":0x0,"size":0x4,"DOC":"SMRR_BASE h "},\
"SMRR_MASK_l": {"value":"FFF00800","position":0x172,"offset":0x0,"size":0x4,"DOC":"SMRR_MASK l "},\
"SMRR_MASK_h": {"value":"FFFFFFFF","position":0x173,"offset":0x0,"size":0x4,"DOC":"SMRR_MASK h "},\
"MTRR_DEF_TYPE_SHADOW_l": {"value":"00000000","position":0x174,"offset":0x0,"size":0x4,"DOC":"MTRR_DEF_TYPE_SHADOW l "},\
"MTRR_DEF_TYPE_SHADOW_h": {"value":"00000000","position":0x175,"offset":0x0,"size":0x4,"DOC":"MTRR_DEF_TYPE_SHADOW h "},\
"PDPT0_l": {"value":"00000000","position":0x176,"offset":0x0,"size":0x4,"DOC":"PDPT0 l "},\
"PDPT0_h": {"value":"00000000","position":0x177,"offset":0x0,"size":0x4,"DOC":"PDPT0 h "},\
"PDPT1_l": {"value":"00000000","position":0x178,"offset":0x0,"size":0x4,"DOC":"PDPT1 l "},\
"PDPT1_h": {"value":"00000000","position":0x179,"offset":0x0,"size":0x4,"DOC":"PDPT1 h "},\
"PDPT2_l": {"value":"00000000","position":0x17a,"offset":0x0,"size":0x4,"DOC":"PDPT2 l "},\
"PDPT2_h": {"value":"00000000","position":0x17b,"offset":0x0,"size":0x4,"DOC":"PDPT2 h "},\
"PDPT3_l": {"value":"00000000","position":0x17c,"offset":0x0,"size":0x4,"DOC":"PDPT3 l "},\
"PDPT3_h": {"value":"00000000","position":0x17d,"offset":0x0,"size":0x4,"DOC":"PDPT3 h "},\
"DR0_l": {"value":"00000000","position":0x17e,"offset":0x0,"size":0x4,"DOC":"DR0 l "},\
"DR0_h": {"value":"00000000","position":0x17f,"offset":0x0,"size":0x4,"DOC":"DR0 h "},\
"DR1_l": {"value":"74E2650C","position":0x180,"offset":0x0,"size":0x4,"DOC":"DR1 l "},\
"DR1_h": {"value":"00000000","position":0x181,"offset":0x0,"size":0x4,"DOC":"DR1 h "},\
"DR2_l": {"value":"77BFFEF0","position":0x182,"offset":0x0,"size":0x4,"DOC":"DR2 l "},\
"DR2_h": {"value":"00000000","position":0x183,"offset":0x0,"size":0x4,"DOC":"DR2 h "},\
"DR3_l": {"value":"77702A30","position":0x184,"offset":0x0,"size":0x4,"DOC":"DR3 l "},\
"DR3_h": {"value":"00000000","position":0x185,"offset":0x0,"size":0x4,"DOC":"DR3 h "},\
"PAT_l": {"value":"00070106","position":0x186,"offset":0x0,"size":0x4,"DOC":"PAT l "},\
"PAT_h": {"value":"00070106","position":0x187,"offset":0x0,"size":0x4,"DOC":"PAT h "},\
"HARDWARE_EPTP_l": {"value":"00000000","position":0x188,"offset":0x0,"size":0x4,"DOC":"HARDWARE_EPTP l "},\
"HARDWARE_EPTP_h": {"value":"00000000","position":0x189,"offset":0x0,"size":0x4,"DOC":"HARDWARE_EPTP h "},\
"ACFLAGS_l": {"value":"00000001","position":0x18a,"offset":0x0,"size":0x4,"DOC":"ACFLAGS l "},\
"ACFLAGS_h": {"value":"00000064","position":0x18b,"offset":0x0,"size":0x4,"DOC":"ACFLAGS h "},\
"GETSEC_PARAM_1_MASK": {"value":"00000000","position":0x18c,"offset":0x0,"size":0x4,"DOC":"GETSEC_PARAM_1_MASK "},\
"GETSEC_PARAM_1_VERSION": {"value":"00000000","position":0x18d,"offset":0x0,"size":0x4,"DOC":"GETSEC_PARAM_1_VERSION "},\
"GETSEC_PARAM_2_SIZE": {"value":"00000800","position":0x18e,"offset":0x0,"size":0x4,"DOC":"GETSEC_PARAM_2_SIZE "},\
"GETSEC_PARAM_3_GETSEC_PARAM_4_GETSEC_PARAM_5": {"value":"00010003","position":0x18f,"offset":0x0,"size":0x4,"DOC":"GETSEC_PARAM_3_GETSEC_PARAM_4_GETSEC_PARAM_5 "},\
"SPI_PREFIX_OPCODE_MENU_SPI_OPCODE_TYPE": {"value":"0000FEF0","position":0x190,"offset":0x0,"size":0x4,"DOC":"SPI_PREFIX_OPCODE_MENU_SPI_OPCODE_TYPE "},\
"SPI_BASE": {"value":"00010000","position":0x191,"offset":0x0,"size":0x4,"DOC":"SPI_BASE "},\
"SPI_OPCODE_MENU_l": {"value":"00000000","position":0x192,"offset":0x0,"size":0x4,"DOC":"SPI_OPCODE_MENU l "},\
"SPI_OPCODE_MENU_h": {"value":"00000000","position":0x193,"offset":0x0,"size":0x4,"DOC":"SPI_OPCODE_MENU h "},\
"CORE_C2_RESIDENCY_l": {"value":"00000000","position":0x194,"offset":0x0,"size":0x4,"DOC":"CORE_C2_RESIDENCY l "},\
"CORE_C2_RESIDENCY_h": {"value":"00000000","position":0x195,"offset":0x0,"size":0x4,"DOC":"CORE_C2_RESIDENCY h "},\
"CORE_C3_RESIDENCY_l": {"value":"00000000","position":0x196,"offset":0x0,"size":0x4,"DOC":"CORE_C3_RESIDENCY l "},\
"CORE_C3_RESIDENCY_h": {"value":"00000000","position":0x197,"offset":0x0,"size":0x4,"DOC":"CORE_C3_RESIDENCY h "},\
"CORE_C4_RESIDENCY_l": {"value":"00000000","position":0x198,"offset":0x0,"size":0x4,"DOC":"CORE_C4_RESIDENCY l "},\
"CORE_C4_RESIDENCY_h": {"value":"00000000","position":0x199,"offset":0x0,"size":0x4,"DOC":"CORE_C4_RESIDENCY h "},\
"CORE_C5_RESIDENCY_l": {"value":"00000000","position":0x19a,"offset":0x0,"size":0x4,"DOC":"CORE_C5_RESIDENCY l "},\
"CORE_C5_RESIDENCY_h": {"value":"00000000","position":0x19b,"offset":0x0,"size":0x4,"DOC":"CORE_C5_RESIDENCY h "},\
"CORE_C6_RESIDENCY_l": {"value":"00000000","position":0x19c,"offset":0x0,"size":0x4,"DOC":"CORE_C6_RESIDENCY l "},\
"CORE_C6_RESIDENCY_h": {"value":"00000000","position":0x19d,"offset":0x0,"size":0x4,"DOC":"CORE_C6_RESIDENCY h "},\
"TEMP_DEBUG_SAVE0_l": {"value":"00000000","position":0x19e,"offset":0x0,"size":0x4,"DOC":"TEMP_DEBUG_SAVE0 l "},\
"TEMP_DEBUG_SAVE0_h": {"value":"00000000","position":0x19f,"offset":0x0,"size":0x4,"DOC":"TEMP_DEBUG_SAVE0 h "},\
"IO_TRANSLATE_DESC0_l": {"value":"00000000","position":0x1a0,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC0 l "},\
"IO_TRANSLATE_DESC0_h": {"value":"00000000","position":0x1a1,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC0 h "},\
"IO_TRANSLATE_DESC1_l": {"value":"00000000","position":0x1a2,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC1 l "},\
"IO_TRANSLATE_DESC1_h": {"value":"00000000","position":0x1a3,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC1 h "},\
"IO_TRANSLATE_DESC2_l": {"value":"00000000","position":0x1a4,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC2 l "},\
"IO_TRANSLATE_DESC2_h": {"value":"00000000","position":0x1a5,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC2 h "},\
"IO_TRANSLATE_DESC3_l": {"value":"00000000","position":0x1a6,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC3 l "},\
"IO_TRANSLATE_DESC3_h": {"value":"00000000","position":0x1a7,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC3 h "},\
"IO_TRANSLATE_DESC4_l": {"value":"00000000","position":0x1a8,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC4 l "},\
"IO_TRANSLATE_DESC4_h": {"value":"00000000","position":0x1a9,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC4 h "},\
"IO_TRANSLATE_DESC5_l": {"value":"00000000","position":0x1aa,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC5 l "},\
"IO_TRANSLATE_DESC5_h": {"value":"00000000","position":0x1ab,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC5 h "},\
"IO_TRANSLATE_DESC6_l": {"value":"00000000","position":0x1ac,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC6 l "},\
"IO_TRANSLATE_DESC6_h": {"value":"00000000","position":0x1ad,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC6 h "},\
"IO_TRANSLATE_DESC7_l": {"value":"00000000","position":0x1ae,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC7 l "},\
"IO_TRANSLATE_DESC7_h": {"value":"00000000","position":0x1af,"offset":0x0,"size":0x4,"DOC":"IO_TRANSLATE_DESC7 h "},\
"LA_DESC2_LA_DESC3_l": {"value":"00000000","position":0x1b0,"offset":0x0,"size":0x4,"DOC":"LA_DESC2_LA_DESC3 l "},\
"LA_DESC2_LA_DESC3_h": {"value":"00000000","position":0x1b1,"offset":0x0,"size":0x4,"DOC":"LA_DESC2_LA_DESC3 h "},\
}

CORE_PROLOG = {"offset":                      0x6,\
                "prolog_size":                 0x530,\
                "core_data_size": {"value":"00000528","position":0x0,"offset":0x0,"size":0x4,"DOC":"core_data_size data "},\
                "core_type":      {"value":"00000040","position":0x1,"offset":0x0,"size":0x4,"DOC":"core_type prolog "},\
                    "UCODE_FLGS_l": {"value":"00001805","position":0x2,"offset":0x0,"size":0x4,"DOC":"UCODE_FLGS l "},\
    "UCODE_FLGS_h": {"value":"00000000","position":0x3,"offset":0x0,"size":0x4,"DOC":"UCODE_FLGS h "},\
    "g10_l": {"value":"00000049","position":0x4,"offset":0x0,"size":0x4,"DOC":"g10 l "},\
    "g10_h": {"value":"00000000","position":0x5,"offset":0x0,"size":0x4,"DOC":"g10 h "},\
    "g15_l": {"value":"00000000","position":0x6,"offset":0x0,"size":0x4,"DOC":"g15 l "},\
    "g15_h": {"value":"00000000","position":0x7,"offset":0x0,"size":0x4,"DOC":"g15 h "},\
    "GSTATE_l": {"value":"80000000","position":0x8,"offset":0x0,"size":0x4,"DOC":"GSTATE l "},\
    "GSTATE_h": {"value":"00000000","position":0x9,"offset":0x0,"size":0x4,"DOC":"GSTATE h "},\
    "LSTATE_l": {"value":"00002000","position":0xa,"offset":0x0,"size":0x4,"DOC":"LSTATE l "},\
    "LSTATE_h": {"value":"00000000","position":0xb,"offset":0x0,"size":0x4,"DOC":"LSTATE h "},\
    "TSTATE_l": {"value":"9003FFDE","position":0xc,"offset":0x0,"size":0x4,"DOC":"TSTATE l "},\
    "TSTATE_h": {"value":"00000000","position":0xd,"offset":0x0,"size":0x4,"DOC":"TSTATE h "},\
    "UEXCEPT_STATE_l": {"value":"00000000","position":0xe,"offset":0x0,"size":0x4,"DOC":"UEXCEPT_STATE l "},\
    "UEXCEPT_STATE_h": {"value":"00000000","position":0xf,"offset":0x0,"size":0x4,"DOC":"UEXCEPT_STATE h "},\
    "SHADOW_RSP_l": {"value":"40000000","position":0x10,"offset":0x0,"size":0x4,"DOC":"SHADOW_RSP l "},\
    "SHADOW_RSP_h": {"value":"00000000","position":0x11,"offset":0x0,"size":0x4,"DOC":"SHADOW_RSP h "},\
    "RAX_l": {"value":"3B8248A1","position":0x12,"offset":0x0,"size":0x4,"DOC":"RAX l "},\
    "RAX_h": {"value":"00000000","position":0x13,"offset":0x0,"size":0x4,"DOC":"RAX h "},\
    "RCX_l": {"value":"00000000","position":0x14,"offset":0x0,"size":0x4,"DOC":"RCX l "},\
    "RCX_h": {"value":"00000000","position":0x15,"offset":0x0,"size":0x4,"DOC":"RCX h "},\
    "RDX_l": {"value":"00000046","position":0x16,"offset":0x0,"size":0x4,"DOC":"RDX l "},\
    "RDX_h": {"value":"00000000","position":0x17,"offset":0x0,"size":0x4,"DOC":"RDX h "},\
    "RBX_l": {"value":"00000014","position":0x18,"offset":0x0,"size":0x4,"DOC":"RBX l "},\
    "RBX_h": {"value":"00000000","position":0x19,"offset":0x0,"size":0x4,"DOC":"RBX h "},\
    "RSP_l": {"value":"03598600","position":0x1a,"offset":0x0,"size":0x4,"DOC":"RSP l "},\
    "RSP_h": {"value":"FFFFF880","position":0x1b,"offset":0x0,"size":0x4,"DOC":"RSP h "},\
    "RBP_l": {"value":"03598CD0","position":0x1c,"offset":0x0,"size":0x4,"DOC":"RBP l "},\
    "RBP_h": {"value":"FFFFF880","position":0x1d,"offset":0x0,"size":0x4,"DOC":"RBP h "},\
    "RSI_l": {"value":"00000000","position":0x1e,"offset":0x0,"size":0x4,"DOC":"RSI l "},\
    "RSI_h": {"value":"00000000","position":0x1f,"offset":0x0,"size":0x4,"DOC":"RSI h "},\
    "RDI_l": {"value":"00000014","position":0x20,"offset":0x0,"size":0x4,"DOC":"RDI l "},\
    "RDI_h": {"value":"00000000","position":0x21,"offset":0x0,"size":0x4,"DOC":"RDI h "},\
    "R8_l": {"value":"00000000","position":0x22,"offset":0x0,"size":0x4,"DOC":"R8 l "},\
    "R8_h": {"value":"00000000","position":0x23,"offset":0x0,"size":0x4,"DOC":"R8 h "},\
    "R9_l": {"value":"3B82478C","position":0x24,"offset":0x0,"size":0x4,"DOC":"R9 l "},\
    "R9_h": {"value":"00000000","position":0x25,"offset":0x0,"size":0x4,"DOC":"R9 h "},\
    "R10_l": {"value":"03017588","position":0x26,"offset":0x0,"size":0x4,"DOC":"R10 l "},\
    "R10_h": {"value":"FFFFF800","position":0x27,"offset":0x0,"size":0x4,"DOC":"R10 h "},\
    "R11_l": {"value":"03598BC8","position":0x28,"offset":0x0,"size":0x4,"DOC":"R11 l "},\
    "R11_h": {"value":"FFFFF880","position":0x29,"offset":0x0,"size":0x4,"DOC":"R11 h "},\
    "R12_l": {"value":"00000001","position":0x2a,"offset":0x0,"size":0x4,"DOC":"R12 l "},\
    "R12_h": {"value":"00000000","position":0x2b,"offset":0x0,"size":0x4,"DOC":"R12 h "},\
    "R13_l": {"value":"00000000","position":0x2c,"offset":0x0,"size":0x4,"DOC":"R13 l "},\
    "R13_h": {"value":"00000000","position":0x2d,"offset":0x0,"size":0x4,"DOC":"R13 h "},\
    "R14_l": {"value":"00000001","position":0x2e,"offset":0x0,"size":0x4,"DOC":"R14 l "},\
    "R14_h": {"value":"00000000","position":0x2f,"offset":0x0,"size":0x4,"DOC":"R14 h "},\
    "R15_l": {"value":"00000001","position":0x30,"offset":0x0,"size":0x4,"DOC":"R15 l "},\
    "R15_h": {"value":"00000000","position":0x31,"offset":0x0,"size":0x4,"DOC":"R15 h "},\
    "ESdesc_l": {"value":"0000FFFF","position":0x32,"offset":0x0,"size":0x4,"DOC":"ESdesc l "},\
    "ESdesc_h": {"value":"00CFF300","position":0x33,"offset":0x0,"size":0x4,"DOC":"ESdesc h "},\
    "CSdesc_l": {"value":"00000000","position":0x34,"offset":0x0,"size":0x4,"DOC":"CSdesc l "},\
    "CSdesc_h": {"value":"00209B00","position":0x35,"offset":0x0,"size":0x4,"DOC":"CSdesc h "},\
    "SSdesc_l": {"value":"0000FFFF","position":0x36,"offset":0x0,"size":0x4,"DOC":"SSdesc l "},\
    "SSdesc_h": {"value":"00CF9300","position":0x37,"offset":0x0,"size":0x4,"DOC":"SSdesc h "},\
    "DSdesc_l": {"value":"0000FFFF","position":0x38,"offset":0x0,"size":0x4,"DOC":"DSdesc l "},\
    "DSdesc_h": {"value":"00CFF300","position":0x39,"offset":0x0,"size":0x4,"DOC":"DSdesc h "},\
    "FSdesc_l": {"value":"E0003C00","position":0x3a,"offset":0x0,"size":0x4,"DOC":"FSdesc l "},\
    "FSdesc_h": {"value":"FF40F3FA","position":0x3b,"offset":0x0,"size":0x4,"DOC":"FSdesc h "},\
    "GSdesc_l": {"value":"2D00FFFF","position":0x3c,"offset":0x0,"size":0x4,"DOC":"GSdesc l "},\
    "GSdesc_h": {"value":"03CFF300","position":0x3d,"offset":0x0,"size":0x4,"DOC":"GSdesc h "},\
    "TSSdesc_l": {"value":"90800067","position":0x3e,"offset":0x0,"size":0x4,"DOC":"TSSdesc l "},\
    "TSSdesc_h": {"value":"04008B3E","position":0x3f,"offset":0x0,"size":0x4,"DOC":"TSSdesc h "},\
    "GDTdesc_l": {"value":"8000007F","position":0x40,"offset":0x0,"size":0x4,"DOC":"GDTdesc l "},\
    "GDTdesc_h": {"value":"0400823E","position":0x41,"offset":0x0,"size":0x4,"DOC":"GDTdesc h "},\
    "IDTdesc_l": {"value":"80800FFF","position":0x42,"offset":0x0,"size":0x4,"DOC":"IDTdesc l "},\
    "IDTdesc_h": {"value":"0400823E","position":0x43,"offset":0x0,"size":0x4,"DOC":"IDTdesc h "},\
    "LDTdesc_l": {"value":"0000FFFF","position":0x44,"offset":0x0,"size":0x4,"DOC":"LDTdesc l "},\
    "LDTdesc_h": {"value":"00CF0000","position":0x45,"offset":0x0,"size":0x4,"DOC":"LDTdesc h "},\
    "VMCSdesc_l": {"value":"0000FFFF","position":0x46,"offset":0x0,"size":0x4,"DOC":"VMCSdesc l "},\
    "VMCSdesc_h": {"value":"00008B00","position":0x47,"offset":0x0,"size":0x4,"DOC":"VMCSdesc h "},\
    "FSdesc_ext": {"value":"00000000","position":0x48,"offset":0x0,"size":0x4,"DOC":"FSdesc_ext "},\
    "GSdesc_ext": {"value":"00000000","position":0x49,"offset":0x0,"size":0x4,"DOC":"GSdesc_ext "},\
    "TSSdesc_ext": {"value":"00000000","position":0x4a,"offset":0x0,"size":0x4,"DOC":"TSSdesc_ext "},\
    "GDTdesc_ext": {"value":"00000000","position":0x4b,"offset":0x0,"size":0x4,"DOC":"GDTdesc_ext "},\
    "LDTdesc_ext": {"value":"00000000","position":0x4c,"offset":0x0,"size":0x4,"DOC":"LDTdesc_ext "},\
    "VMCSdesc_ext": {"value":"00000000","position":0x4d,"offset":0x0,"size":0x4,"DOC":"VMCSdesc_ext "},\
    "IDTdesc_ext_l": {"value":"00000000","position":0x4e,"offset":0x0,"size":0x4,"DOC":"IDTdesc_ext l "},\
    "IDTdesc_ext_h": {"value":"00000000","position":0x4f,"offset":0x0,"size":0x4,"DOC":"IDTdesc_ext h "},\
    "FP_SW": {"value":"3800","position":0x50,"offset":0x0,"size":0x2,"DOC":"FP_SW "},\
    "FP_CW": {"value":"027F","position":0x50,"offset":0x2,"size":0x2,"DOC":"FP_CW "},\
    "FPTAG": {"value":"0080","position":0x51,"offset":0x0,"size":0x2,"DOC":"FPTAG "},\
    "MXCSR": {"value":"1F80","position":0x51,"offset":0x2,"size":0x2,"DOC":"MXCSR "},\
    "FPDS": {"value":"0000","position":0x52,"offset":0x0,"size":0x2,"DOC":"FPDS "},\
    "FPCS": {"value":"0000","position":0x52,"offset":0x2,"size":0x2,"DOC":"FPCS "},\
    "FPLOP": {"value":"00000301","position":0x53,"offset":0x0,"size":0x4,"DOC":"FPLOP "},\
    "FPLA_l": {"value":"0209BE00","position":0x54,"offset":0x0,"size":0x4,"DOC":"FPLA l "},\
    "FPLA_h": {"value":"FFFFF880","position":0x55,"offset":0x0,"size":0x4,"DOC":"FPLA h "},\
    "FPLIP_l": {"value":"02E8ADC3","position":0x56,"offset":0x0,"size":0x4,"DOC":"FPLIP l "},\
    "FPLIP_h": {"value":"0000F800","position":0x57,"offset":0x0,"size":0x4,"DOC":"FPLIP h "},\
    "xmm0_0": {"value":"00000000","position":0x58,"offset":0x0,"size":0x4,"DOC":"xmm0_0 "},\
    "xmm0_1": {"value":"00000000","position":0x59,"offset":0x0,"size":0x4,"DOC":"xmm0_1 "},\
    "xmm0_2": {"value":"00000000","position":0x5a,"offset":0x0,"size":0x4,"DOC":"xmm0_2 "},\
    "xmm0_3": {"value":"00000000","position":0x5b,"offset":0x0,"size":0x4,"DOC":"xmm0_3 "},\
    "xmm1_0": {"value":"00000000","position":0x5c,"offset":0x0,"size":0x4,"DOC":"xmm1_0 "},\
    "xmm1_1": {"value":"00000000","position":0x5d,"offset":0x0,"size":0x4,"DOC":"xmm1_1 "},\
    "xmm1_2": {"value":"00000000","position":0x5e,"offset":0x0,"size":0x4,"DOC":"xmm1_2 "},\
    "xmm1_3": {"value":"00000000","position":0x5f,"offset":0x0,"size":0x4,"DOC":"xmm1_3 "},\
    "xmm2_0": {"value":"00000000","position":0x60,"offset":0x0,"size":0x4,"DOC":"xmm2_0 "},\
    "xmm2_1": {"value":"00000000","position":0x61,"offset":0x0,"size":0x4,"DOC":"xmm2_1 "},\
    "xmm2_2": {"value":"00000000","position":0x62,"offset":0x0,"size":0x4,"DOC":"xmm2_2 "},\
    "xmm2_3": {"value":"00000000","position":0x63,"offset":0x0,"size":0x4,"DOC":"xmm2_3 "},\
    "xmm3_0": {"value":"00000000","position":0x64,"offset":0x0,"size":0x4,"DOC":"xmm3_0 "},\
    "xmm3_1": {"value":"00000000","position":0x65,"offset":0x0,"size":0x4,"DOC":"xmm3_1 "},\
    "xmm3_2": {"value":"00000000","position":0x66,"offset":0x0,"size":0x4,"DOC":"xmm3_2 "},\
    "xmm3_3": {"value":"00000000","position":0x67,"offset":0x0,"size":0x4,"DOC":"xmm3_3 "},\
    "xmm4_0": {"value":"00000000","position":0x68,"offset":0x0,"size":0x4,"DOC":"xmm4_0 "},\
    "xmm4_1": {"value":"00000000","position":0x69,"offset":0x0,"size":0x4,"DOC":"xmm4_1 "},\
    "xmm4_2": {"value":"00000000","position":0x6a,"offset":0x0,"size":0x4,"DOC":"xmm4_2 "},\
    "xmm4_3": {"value":"00000000","position":0x6b,"offset":0x0,"size":0x4,"DOC":"xmm4_3 "},\
    "xmm5_0": {"value":"00000000","position":0x6c,"offset":0x0,"size":0x4,"DOC":"xmm5_0 "},\
    "xmm5_1": {"value":"00000000","position":0x6d,"offset":0x0,"size":0x4,"DOC":"xmm5_1 "},\
    "xmm5_2": {"value":"00000000","position":0x6e,"offset":0x0,"size":0x4,"DOC":"xmm5_2 "},\
    "xmm5_3": {"value":"00000000","position":0x6f,"offset":0x0,"size":0x4,"DOC":"xmm5_3 "},\
    "xmm6_0": {"value":"00000000","position":0x70,"offset":0x0,"size":0x4,"DOC":"xmm6_0 "},\
    "xmm6_1": {"value":"00000000","position":0x71,"offset":0x0,"size":0x4,"DOC":"xmm6_1 "},\
    "xmm6_2": {"value":"00000000","position":0x72,"offset":0x0,"size":0x4,"DOC":"xmm6_2 "},\
    "xmm6_3": {"value":"00000000","position":0x73,"offset":0x0,"size":0x4,"DOC":"xmm6_3 "},\
    "xmm7_0": {"value":"00000000","position":0x74,"offset":0x0,"size":0x4,"DOC":"xmm7_0 "},\
    "xmm7_1": {"value":"00000000","position":0x75,"offset":0x0,"size":0x4,"DOC":"xmm7_1 "},\
    "xmm7_2": {"value":"00000000","position":0x76,"offset":0x0,"size":0x4,"DOC":"xmm7_2 "},\
    "xmm7_3": {"value":"00000000","position":0x77,"offset":0x0,"size":0x4,"DOC":"xmm7_3 "},\
    "xmm8_0": {"value":"00000000","position":0x78,"offset":0x0,"size":0x4,"DOC":"xmm8_0 "},\
    "xmm8_1": {"value":"00000000","position":0x79,"offset":0x0,"size":0x4,"DOC":"xmm8_1 "},\
    "xmm8_2": {"value":"00000000","position":0x7a,"offset":0x0,"size":0x4,"DOC":"xmm8_2 "},\
    "xmm8_3": {"value":"00000000","position":0x7b,"offset":0x0,"size":0x4,"DOC":"xmm8_3 "},\
    "xmm9_0": {"value":"00000000","position":0x7c,"offset":0x0,"size":0x4,"DOC":"xmm9_0 "},\
    "xmm9_1": {"value":"00000000","position":0x7d,"offset":0x0,"size":0x4,"DOC":"xmm9_1 "},\
    "xmm9_2": {"value":"00000000","position":0x7e,"offset":0x0,"size":0x4,"DOC":"xmm9_2 "},\
    "xmm9_3": {"value":"00000000","position":0x7f,"offset":0x0,"size":0x4,"DOC":"xmm9_3 "},\
    "xmm10_0": {"value":"00000000","position":0x80,"offset":0x0,"size":0x4,"DOC":"xmm10_0 "},\
    "xmm10_1": {"value":"00000000","position":0x81,"offset":0x0,"size":0x4,"DOC":"xmm10_1 "},\
    "xmm10_2": {"value":"00000000","position":0x82,"offset":0x0,"size":0x4,"DOC":"xmm10_2 "},\
    "xmm10_3": {"value":"00000000","position":0x83,"offset":0x0,"size":0x4,"DOC":"xmm10_3 "},\
    "xmm11_0": {"value":"00000000","position":0x84,"offset":0x0,"size":0x4,"DOC":"xmm11_0 "},\
    "xmm11_1": {"value":"00000000","position":0x85,"offset":0x0,"size":0x4,"DOC":"xmm11_1 "},\
    "xmm11_2": {"value":"00000000","position":0x86,"offset":0x0,"size":0x4,"DOC":"xmm11_2 "},\
    "xmm11_3": {"value":"00000000","position":0x87,"offset":0x0,"size":0x4,"DOC":"xmm11_3 "},\
    "xmm12_0": {"value":"00000000","position":0x88,"offset":0x0,"size":0x4,"DOC":"xmm12_0 "},\
    "xmm12_1": {"value":"00000000","position":0x89,"offset":0x0,"size":0x4,"DOC":"xmm12_1 "},\
    "xmm12_2": {"value":"00000000","position":0x8a,"offset":0x0,"size":0x4,"DOC":"xmm12_2 "},\
    "xmm12_3": {"value":"00000000","position":0x8b,"offset":0x0,"size":0x4,"DOC":"xmm12_3 "},\
    "xmm13_0": {"value":"00000000","position":0x8c,"offset":0x0,"size":0x4,"DOC":"xmm13_0 "},\
    "xmm13_1": {"value":"00000000","position":0x8d,"offset":0x0,"size":0x4,"DOC":"xmm13_1 "},\
    "xmm13_2": {"value":"00000000","position":0x8e,"offset":0x0,"size":0x4,"DOC":"xmm13_2 "},\
    "xmm13_3": {"value":"00000000","position":0x8f,"offset":0x0,"size":0x4,"DOC":"xmm13_3 "},\
    "xmm14_0": {"value":"00000000","position":0x90,"offset":0x0,"size":0x4,"DOC":"xmm14_0 "},\
    "xmm14_1": {"value":"00000000","position":0x91,"offset":0x0,"size":0x4,"DOC":"xmm14_1 "},\
    "xmm14_2": {"value":"00000000","position":0x92,"offset":0x0,"size":0x4,"DOC":"xmm14_2 "},\
    "xmm14_3": {"value":"00000000","position":0x93,"offset":0x0,"size":0x4,"DOC":"xmm14_3 "},\
    "xmm15_0": {"value":"00000000","position":0x94,"offset":0x0,"size":0x4,"DOC":"xmm15_0 "},\
    "xmm15_1": {"value":"00000000","position":0x95,"offset":0x0,"size":0x4,"DOC":"xmm15_1 "},\
    "xmm15_2": {"value":"00000000","position":0x96,"offset":0x0,"size":0x4,"DOC":"xmm15_2 "},\
    "xmm15_3": {"value":"00000000","position":0x97,"offset":0x0,"size":0x4,"DOC":"xmm15_3 "},\
    "st7_0": {"value":"00000000","position":0x98,"offset":0x0,"size":0x4,"DOC":"st7_0 "},\
    "st7_1": {"value":"00000000","position":0x99,"offset":0x0,"size":0x4,"DOC":"st7_1 "},\
    "st7_2": {"value":"00000000","position":0x9a,"offset":0x0,"size":0x4,"DOC":"st7_2 "},\
    "st7_3": {"value":"00000000","position":0x9b,"offset":0x0,"size":0x4,"DOC":"st7_3 "},\
    "st0_0": {"value":"00000000","position":0x9c,"offset":0x0,"size":0x4,"DOC":"st0_0 "},\
    "st0_1": {"value":"00000000","position":0x9d,"offset":0x0,"size":0x4,"DOC":"st0_1 "},\
    "st0_2": {"value":"00000000","position":0x9e,"offset":0x0,"size":0x4,"DOC":"st0_2 "},\
    "st0_3": {"value":"00000000","position":0x9f,"offset":0x0,"size":0x4,"DOC":"st0_3 "},\
    "st1_0": {"value":"00000000","position":0xa0,"offset":0x0,"size":0x4,"DOC":"st1_0 "},\
    "st1_1": {"value":"00000000","position":0xa1,"offset":0x0,"size":0x4,"DOC":"st1_1 "},\
    "st1_2": {"value":"00000000","position":0xa2,"offset":0x0,"size":0x4,"DOC":"st1_2 "},\
    "st1_3": {"value":"00000000","position":0xa3,"offset":0x0,"size":0x4,"DOC":"st1_3 "},\
    "st2_0": {"value":"00000000","position":0xa4,"offset":0x0,"size":0x4,"DOC":"st2_0 "},\
    "st2_1": {"value":"00000000","position":0xa5,"offset":0x0,"size":0x4,"DOC":"st2_1 "},\
    "st2_2": {"value":"00000000","position":0xa6,"offset":0x0,"size":0x4,"DOC":"st2_2 "},\
    "st2_3": {"value":"00000000","position":0xa7,"offset":0x0,"size":0x4,"DOC":"st2_3 "},\
    "st3_0": {"value":"00000000","position":0xa8,"offset":0x0,"size":0x4,"DOC":"st3_0 "},\
    "st3_1": {"value":"00000000","position":0xa9,"offset":0x0,"size":0x4,"DOC":"st3_1 "},\
    "st3_2": {"value":"00000000","position":0xaa,"offset":0x0,"size":0x4,"DOC":"st3_2 "},\
    "st3_3": {"value":"00000000","position":0xab,"offset":0x0,"size":0x4,"DOC":"st3_3 "},\
    "st4_0": {"value":"00000000","position":0xac,"offset":0x0,"size":0x4,"DOC":"st4_0 "},\
    "st4_1": {"value":"00000000","position":0xad,"offset":0x0,"size":0x4,"DOC":"st4_1 "},\
    "st4_2": {"value":"00000000","position":0xae,"offset":0x0,"size":0x4,"DOC":"st4_2 "},\
    "st4_3": {"value":"00000000","position":0xaf,"offset":0x0,"size":0x4,"DOC":"st4_3 "},\
    "st5_0": {"value":"00000000","position":0xb0,"offset":0x0,"size":0x4,"DOC":"st5_0 "},\
    "st5_1": {"value":"00000000","position":0xb1,"offset":0x0,"size":0x4,"DOC":"st5_1 "},\
    "st5_2": {"value":"00000000","position":0xb2,"offset":0x0,"size":0x4,"DOC":"st5_2 "},\
    "st5_3": {"value":"00000000","position":0xb3,"offset":0x0,"size":0x4,"DOC":"st5_3 "},\
    "st6_0": {"value":"00000000","position":0xb4,"offset":0x0,"size":0x4,"DOC":"st6_0 "},\
    "st6_1": {"value":"00000000","position":0xb5,"offset":0x0,"size":0x4,"DOC":"st6_1 "},\
    "st6_2": {"value":"00000000","position":0xb6,"offset":0x0,"size":0x4,"DOC":"st6_2 "},\
    "st6_3": {"value":"00000000","position":0xb7,"offset":0x0,"size":0x4,"DOC":"st6_3 "},\
    "ymm0_0": {"value":"00000000","position":0xb8,"offset":0x0,"size":0x4,"DOC":"ymm0_0 "},\
    "ymm0_1": {"value":"00000000","position":0xb9,"offset":0x0,"size":0x4,"DOC":"ymm0_1 "},\
    "ymm0_2": {"value":"00000000","position":0xba,"offset":0x0,"size":0x4,"DOC":"ymm0_2 "},\
    "ymm0_3": {"value":"00000000","position":0xbb,"offset":0x0,"size":0x4,"DOC":"ymm0_3 "},\
    "ymm1_0": {"value":"00000000","position":0xbc,"offset":0x0,"size":0x4,"DOC":"ymm1_0 "},\
    "ymm1_1": {"value":"00000000","position":0xbd,"offset":0x0,"size":0x4,"DOC":"ymm1_1 "},\
    "ymm1_2": {"value":"00000000","position":0xbe,"offset":0x0,"size":0x4,"DOC":"ymm1_2 "},\
    "ymm1_3": {"value":"00000000","position":0xbf,"offset":0x0,"size":0x4,"DOC":"ymm1_3 "},\
    "ymm2_0": {"value":"00000000","position":0xc0,"offset":0x0,"size":0x4,"DOC":"ymm2_0 "},\
    "ymm2_1": {"value":"00000000","position":0xc1,"offset":0x0,"size":0x4,"DOC":"ymm2_1 "},\
    "ymm2_2": {"value":"00000000","position":0xc2,"offset":0x0,"size":0x4,"DOC":"ymm2_2 "},\
    "ymm2_3": {"value":"00000000","position":0xc3,"offset":0x0,"size":0x4,"DOC":"ymm2_3 "},\
    "ymm3_0": {"value":"00000000","position":0xc4,"offset":0x0,"size":0x4,"DOC":"ymm3_0 "},\
    "ymm3_1": {"value":"00000000","position":0xc5,"offset":0x0,"size":0x4,"DOC":"ymm3_1 "},\
    "ymm3_2": {"value":"00000000","position":0xc6,"offset":0x0,"size":0x4,"DOC":"ymm3_2 "},\
    "ymm3_3": {"value":"00000000","position":0xc7,"offset":0x0,"size":0x4,"DOC":"ymm3_3 "},\
    "ymm4_0": {"value":"00000000","position":0xc8,"offset":0x0,"size":0x4,"DOC":"ymm4_0 "},\
    "ymm4_1": {"value":"00000000","position":0xc9,"offset":0x0,"size":0x4,"DOC":"ymm4_1 "},\
    "ymm4_2": {"value":"00000000","position":0xca,"offset":0x0,"size":0x4,"DOC":"ymm4_2 "},\
    "ymm4_3": {"value":"00000000","position":0xcb,"offset":0x0,"size":0x4,"DOC":"ymm4_3 "},\
    "ymm5_0": {"value":"00000000","position":0xcc,"offset":0x0,"size":0x4,"DOC":"ymm5_0 "},\
    "ymm5_1": {"value":"00000000","position":0xcd,"offset":0x0,"size":0x4,"DOC":"ymm5_1 "},\
    "ymm5_2": {"value":"00000000","position":0xce,"offset":0x0,"size":0x4,"DOC":"ymm5_2 "},\
    "ymm5_3": {"value":"00000000","position":0xcf,"offset":0x0,"size":0x4,"DOC":"ymm5_3 "},\
    "ymm6_0": {"value":"00000000","position":0xd0,"offset":0x0,"size":0x4,"DOC":"ymm6_0 "},\
    "ymm6_1": {"value":"00000000","position":0xd1,"offset":0x0,"size":0x4,"DOC":"ymm6_1 "},\
    "ymm6_2": {"value":"00000000","position":0xd2,"offset":0x0,"size":0x4,"DOC":"ymm6_2 "},\
    "ymm6_3": {"value":"00000000","position":0xd3,"offset":0x0,"size":0x4,"DOC":"ymm6_3 "},\
    "ymm7_0": {"value":"00000000","position":0xd4,"offset":0x0,"size":0x4,"DOC":"ymm7_0 "},\
    "ymm7_1": {"value":"00000000","position":0xd5,"offset":0x0,"size":0x4,"DOC":"ymm7_1 "},\
    "ymm7_2": {"value":"00000000","position":0xd6,"offset":0x0,"size":0x4,"DOC":"ymm7_2 "},\
    "ymm7_3": {"value":"00000000","position":0xd7,"offset":0x0,"size":0x4,"DOC":"ymm7_3 "},\
    "ymm8_0": {"value":"00000000","position":0xd8,"offset":0x0,"size":0x4,"DOC":"ymm8_0 "},\
    "ymm8_1": {"value":"00000000","position":0xd9,"offset":0x0,"size":0x4,"DOC":"ymm8_1 "},\
    "ymm8_2": {"value":"00000000","position":0xda,"offset":0x0,"size":0x4,"DOC":"ymm8_2 "},\
    "ymm8_3": {"value":"00000000","position":0xdb,"offset":0x0,"size":0x4,"DOC":"ymm8_3 "},\
    "ymm9_0": {"value":"00000000","position":0xdc,"offset":0x0,"size":0x4,"DOC":"ymm9_0 "},\
    "ymm9_1": {"value":"00000000","position":0xdd,"offset":0x0,"size":0x4,"DOC":"ymm9_1 "},\
    "ymm9_2": {"value":"00000000","position":0xde,"offset":0x0,"size":0x4,"DOC":"ymm9_2 "},\
    "ymm9_3": {"value":"00000000","position":0xdf,"offset":0x0,"size":0x4,"DOC":"ymm9_3 "},\
    "ymm10_0": {"value":"00000000","position":0xe0,"offset":0x0,"size":0x4,"DOC":"ymm10_0 "},\
    "ymm10_1": {"value":"00000000","position":0xe1,"offset":0x0,"size":0x4,"DOC":"ymm10_1 "},\
    "ymm10_2": {"value":"00000000","position":0xe2,"offset":0x0,"size":0x4,"DOC":"ymm10_2 "},\
    "ymm10_3": {"value":"00000000","position":0xe3,"offset":0x0,"size":0x4,"DOC":"ymm10_3 "},\
    "ymm11_0": {"value":"00000000","position":0xe4,"offset":0x0,"size":0x4,"DOC":"ymm11_0 "},\
    "ymm11_1": {"value":"00000000","position":0xe5,"offset":0x0,"size":0x4,"DOC":"ymm11_1 "},\
    "ymm11_2": {"value":"00000000","position":0xe6,"offset":0x0,"size":0x4,"DOC":"ymm11_2 "},\
    "ymm11_3": {"value":"00000000","position":0xe7,"offset":0x0,"size":0x4,"DOC":"ymm11_3 "},\
    "ymm12_0": {"value":"00000000","position":0xe8,"offset":0x0,"size":0x4,"DOC":"ymm12_0 "},\
    "ymm12_1": {"value":"00000000","position":0xe9,"offset":0x0,"size":0x4,"DOC":"ymm12_1 "},\
    "ymm12_2": {"value":"00000000","position":0xea,"offset":0x0,"size":0x4,"DOC":"ymm12_2 "},\
    "ymm12_3": {"value":"00000000","position":0xeb,"offset":0x0,"size":0x4,"DOC":"ymm12_3 "},\
    "ymm13_0": {"value":"00000000","position":0xec,"offset":0x0,"size":0x4,"DOC":"ymm13_0 "},\
    "ymm13_1": {"value":"00000000","position":0xed,"offset":0x0,"size":0x4,"DOC":"ymm13_1 "},\
    "ymm13_2": {"value":"00000000","position":0xee,"offset":0x0,"size":0x4,"DOC":"ymm13_2 "},\
    "ymm13_3": {"value":"00000000","position":0xef,"offset":0x0,"size":0x4,"DOC":"ymm13_3 "},\
    "ymm14_0": {"value":"00000000","position":0xf0,"offset":0x0,"size":0x4,"DOC":"ymm14_0 "},\
    "ymm14_1": {"value":"00000000","position":0xf1,"offset":0x0,"size":0x4,"DOC":"ymm14_1 "},\
    "ymm14_2": {"value":"00000000","position":0xf2,"offset":0x0,"size":0x4,"DOC":"ymm14_2 "},\
    "ymm14_3": {"value":"00000000","position":0xf3,"offset":0x0,"size":0x4,"DOC":"ymm14_3 "},\
    "ymm15_0": {"value":"00000000","position":0xf4,"offset":0x0,"size":0x4,"DOC":"ymm15_0 "},\
    "ymm15_1": {"value":"00000000","position":0xf5,"offset":0x0,"size":0x4,"DOC":"ymm15_1 "},\
    "ymm15_2": {"value":"00000000","position":0xf6,"offset":0x0,"size":0x4,"DOC":"ymm15_2 "},\
    "ymm15_3": {"value":"00000000","position":0xf7,"offset":0x0,"size":0x4,"DOC":"ymm15_3 "},\
    "C0_MOB_CTRL_l": {"value":"04003100","position":0xf8,"offset":0x0,"size":0x4,"DOC":"C0_MOB_CTRL l "},\
    "C0_MOB_CTRL_h": {"value":"00000080","position":0xf9,"offset":0x0,"size":0x4,"DOC":"C0_MOB_CTRL h "},\
    "FCR56_l": {"value":"00000000","position":0xfa,"offset":0x0,"size":0x4,"DOC":"FCR56 l "},\
    "FCR56_h": {"value":"00020000","position":0xfb,"offset":0x0,"size":0x4,"DOC":"FCR56 h "},\
    "APICBASE_l": {"value":"FEE00900","position":0xfc,"offset":0x0,"size":0x4,"DOC":"APICBASE l "},\
    "APICBASE_h": {"value":"00000000","position":0xfd,"offset":0x0,"size":0x4,"DOC":"APICBASE h "},\
    "FCR55_l": {"value":"00000000","position":0xfe,"offset":0x0,"size":0x4,"DOC":"FCR55 l "},\
    "FCR55_h": {"value":"00000420","position":0xff,"offset":0x0,"size":0x4,"DOC":"FCR55 h "},\
    "TCR": {"value":"00000000","position":0x100,"offset":0x0,"size":0x4,"DOC":"TCR "},\
    "JCR": {"value":"00617D00","position":0x101,"offset":0x0,"size":0x4,"DOC":"JCR "},\
    "CR0": {"value":"80050031","position":0x102,"offset":0x0,"size":0x4,"DOC":"CR0 "},\
    "FCR16": {"value":"00000000","position":0x103,"offset":0x0,"size":0x4,"DOC":"FCR16 "},\
    "EFER": {"value":"00000D01","position":0x104,"offset":0x0,"size":0x4,"DOC":"EFER "},\
    "CRC32_POLY": {"value":"05EC76F1","position":0x105,"offset":0x0,"size":0x4,"DOC":"CRC32_POLY "},\
    "MISC_ENABLE_l": {"value":"00153C89","position":0x106,"offset":0x0,"size":0x4,"DOC":"MISC_ENABLE l "},\
    "MISC_ENABLE_h": {"value":"00000000","position":0x107,"offset":0x0,"size":0x4,"DOC":"MISC_ENABLE h "},\
    "FCR14_l": {"value":"00002100","position":0x108,"offset":0x0,"size":0x4,"DOC":"FCR14 l "},\
    "FCR14_h": {"value":"01800700","position":0x109,"offset":0x0,"size":0x4,"DOC":"FCR14 h "},\
    "FCR3_l": {"value":"00040018","position":0x10a,"offset":0x0,"size":0x4,"DOC":"FCR3 l "},\
    "FCR3_h": {"value":"00000000","position":0x10b,"offset":0x0,"size":0x4,"DOC":"FCR3 h "},\
    "FCR15_l": {"value":"88100000","position":0x10c,"offset":0x0,"size":0x4,"DOC":"FCR15 l "},\
    "FCR15_h": {"value":"20000800","position":0x10d,"offset":0x0,"size":0x4,"DOC":"FCR15 h "},\
    "CR4_l": {"value":"000006F8","position":0x10e,"offset":0x0,"size":0x4,"DOC":"CR4 l "},\
    "CR4_h": {"value":"00000000","position":0x10f,"offset":0x0,"size":0x4,"DOC":"CR4 h "},\
    "SYSENTER_EIP_64_l": {"value":"00000000","position":0x110,"offset":0x0,"size":0x4,"DOC":"SYSENTER_EIP_64 l "},\
    "SYSENTER_EIP_64_h": {"value":"00000000","position":0x111,"offset":0x0,"size":0x4,"DOC":"SYSENTER_EIP_64 h "},\
    "FCR57_l": {"value":"F8400384","position":0x112,"offset":0x0,"size":0x4,"DOC":"FCR57 l "},\
    "FCR57_h": {"value":"000000C8","position":0x113,"offset":0x0,"size":0x4,"DOC":"FCR57 h "},\
    "IP_l": {"value":"03406A2C","position":0x114,"offset":0x0,"size":0x4,"DOC":"IP l "},\
    "IP_h": {"value":"FFFFF800","position":0x115,"offset":0x0,"size":0x4,"DOC":"IP h "},\
    "TERRY_CONTROL_l": {"value":"02007B7F","position":0x116,"offset":0x0,"size":0x4,"DOC":"TERRY_CONTROL l "},\
    "TERRY_CONTROL_h": {"value":"00000040","position":0x117,"offset":0x0,"size":0x4,"DOC":"TERRY_CONTROL h "},\
    "TIMEOUT_CTR_l": {"value":"FFF00000","position":0x118,"offset":0x0,"size":0x4,"DOC":"TIMEOUT_CTR l "},\
    "TIMEOUT_CTR_h": {"value":"00000000","position":0x119,"offset":0x0,"size":0x4,"DOC":"TIMEOUT_CTR h "},\
    "ICR": {"value":"00000000","position":0x11a,"offset":0x0,"size":0x4,"DOC":"ICR "},\
    "IMR": {"value":"00000003","position":0x11b,"offset":0x0,"size":0x4,"DOC":"IMR "},\
    "DR6": {"value":"FFFF0FF0","position":0x11c,"offset":0x0,"size":0x4,"DOC":"DR6 "},\
    "DUMMY": {"value":"00000000","position":0x11d,"offset":0x0,"size":0x4,"DOC":"DUMMY "},\
    "PERF_CNT_0_H_l": {"value":"00000000","position":0x11e,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_0_H l "},\
    "PERF_CNT_0_H_h": {"value":"00000000","position":0x11f,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_0_H h "},\
    "PERF_CNT_1_H_l": {"value":"FFFC0000","position":0x120,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_1_H l "},\
    "PERF_CNT_1_H_h": {"value":"000000FF","position":0x121,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_1_H h "},\
    "PERF_CNT_2_H_l": {"value":"00000000","position":0x122,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_2_H l "},\
    "PERF_CNT_2_H_h": {"value":"00000000","position":0x123,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_2_H h "},\
    "DISPATCH_CTR_H_l": {"value":"00000000","position":0x124,"offset":0x0,"size":0x4,"DOC":"DISPATCH_CTR_H l "},\
    "DISPATCH_CTR_H_h": {"value":"00000000","position":0x125,"offset":0x0,"size":0x4,"DOC":"DISPATCH_CTR_H h "},\
    "DUMMY_1_l": {"value":"00000000","position":0x126,"offset":0x0,"size":0x4,"DOC":"DUMMY_1 l "},\
    "DUMMY_1_h": {"value":"00000000","position":0x127,"offset":0x0,"size":0x4,"DOC":"DUMMY_1 h "},\
    "PERF_CNT_5_H_l": {"value":"00000000","position":0x128,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_5_H l "},\
    "PERF_CNT_5_H_h": {"value":"00000000","position":0x129,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_5_H h "},\
    "PERF_CNT_6_H_l": {"value":"00000000","position":0x12a,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_6_H l "},\
    "PERF_CNT_6_H_h": {"value":"00000000","position":0x12b,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_6_H h "},\
    "PERF_CNT_7_H_l": {"value":"00000000","position":0x12c,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_7_H l "},\
    "PERF_CNT_7_H_h": {"value":"00000000","position":0x12d,"offset":0x0,"size":0x4,"DOC":"PERF_CNT_7_H h "},\
    "PERF_CCCR_0_H_l": {"value":"00000700","position":0x12e,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_0_H l "},\
    "PERF_CCCR_0_H_h": {"value":"00000000","position":0x12f,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_0_H h "},\
    "PERF_CCCR_1_H_l": {"value":"08431000","position":0x130,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_1_H l "},\
    "PERF_CCCR_1_H_h": {"value":"00000000","position":0x131,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_1_H h "},\
    "PERF_CCCR_2_H_l": {"value":"00002700","position":0x132,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_2_H l "},\
    "PERF_CCCR_2_H_h": {"value":"00000000","position":0x133,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_2_H h "},\
    "DUMMY_2_l": {"value":"00000000","position":0x134,"offset":0x0,"size":0x4,"DOC":"DUMMY_2 l "},\
    "DUMMY_2_h": {"value":"00000000","position":0x135,"offset":0x0,"size":0x4,"DOC":"DUMMY_2 h "},\
    "DUMMY_3_l": {"value":"00000000","position":0x136,"offset":0x0,"size":0x4,"DOC":"DUMMY_3 l "},\
    "DUMMY_3_h": {"value":"00000000","position":0x137,"offset":0x0,"size":0x4,"DOC":"DUMMY_3 h "},\
    "PERF_CCCR_5_H_l": {"value":"00405000","position":0x138,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_5_H l "},\
    "PERF_CCCR_5_H_h": {"value":"00000000","position":0x139,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_5_H h "},\
    "PERF_CCCR_6_H_l": {"value":"00406082","position":0x13a,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_6_H l "},\
    "PERF_CCCR_6_H_h": {"value":"00000000","position":0x13b,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_6_H h "},\
    "PERF_CCCR_7_H_l": {"value":"00407083","position":0x13c,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_7_H l "},\
    "PERF_CCCR_7_H_h": {"value":"00000000","position":0x13d,"offset":0x0,"size":0x4,"DOC":"PERF_CCCR_7_H h "},\
    "APERF_CTR_H_l": {"value":"00000000","position":0x13e,"offset":0x0,"size":0x4,"DOC":"APERF_CTR_H l "},\
    "APERF_CTR_H_h": {"value":"00000000","position":0x13f,"offset":0x0,"size":0x4,"DOC":"APERF_CTR_H h "},\
    "MPERF_CTR_H_l": {"value":"00000000","position":0x140,"offset":0x0,"size":0x4,"DOC":"MPERF_CTR_H l "},\
    "MPERF_CTR_H_h": {"value":"00000000","position":0x141,"offset":0x0,"size":0x4,"DOC":"MPERF_CTR_H h "},\
    "FIXED_CTRL_H_l": {"value":"00000000","position":0x142,"offset":0x0,"size":0x4,"DOC":"FIXED_CTRL_H l "},\
    "FIXED_CTRL_H_h": {"value":"00000000","position":0x143,"offset":0x0,"size":0x4,"DOC":"FIXED_CTRL_H h "},\
    "GLOBAL_STATUS_H_l": {"value":"00000000","position":0x144,"offset":0x0,"size":0x4,"DOC":"GLOBAL_STATUS_H l "},\
    "GLOBAL_STATUS_H_h": {"value":"00000000","position":0x145,"offset":0x0,"size":0x4,"DOC":"GLOBAL_STATUS_H h "},\
    "GLOBAL_CTRL_H_l": {"value":"0000000F","position":0x146,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CTRL_H l "},\
    "GLOBAL_CTRL_H_h": {"value":"00000007","position":0x147,"offset":0x0,"size":0x4,"DOC":"GLOBAL_CTRL_H h "},\
    "GLOBAL_OVF_CTRL_H_l": {"value":"00000000","position":0x148,"offset":0x0,"size":0x4,"DOC":"GLOBAL_OVF_CTRL_H l "},\
    "GLOBAL_OVF_CTRL_H_h": {"value":"00000000","position":0x149,"offset":0x0,"size":0x4,"DOC":"GLOBAL_OVF_CTRL_H h "},\
    "EFLAGS": {"value":"00000297","position":0x14a,"offset":0x0,"size":0x4,"DOC":"EFLAGS "},\

               }


VMCS_STUFF_PROLOG = {"offset":                      0xa,\
                 "prolog_size":                 0x38,\
                 }
SMM_STATE_PROLOG = {"offset":                      0xb,\
                 "prolog_size":                 0x300,\
                 }
APIC_PROLOG = {"offset":                      0xd,\
                 "prolog_size":                 0x108,\
                 "apic_data_size": {"value":"000000100","position":0x0,"offset":0x0,"size":0x4,"DOC":"apic data size "},\
               "apic_type":      {"value":"000002000","position":0x1,"offset":0x0,"size":0x4,"DOC":"apic  type "},\
               "undefined_0":      {"value":"000000000","position":0x2,"offset":0x0,"size":0x4,"DOC":"apic  type "},\
               "undefined_1":      {"value":"000000000","position":0x3,"offset":0x0,"size":0x4,"DOC":"apic  type "},\
               "APIC_ID": {"value":"00000000","position":0x4,"offset":0x0,"size":0x4,"DOC":"APIC ID "},\
    "APIC_VER": {"value":"01050015","position":0x5,"offset":0x0,"size":0x4,"DOC":"APIC VER "},\
    "APIC_RESVD_0": {"value":"00000000","position":0x6,"offset":0x0,"size":0x4,"DOC":"APIC RESVD 0"},\
    "APIC_RESVD_1": {"value":"012000FF","position":0x7,"offset":0x0,"size":0x4,"DOC":"APIC RESVD 1"},\
    "APIC_RESVD_2": {"value":"00011422","position":0x8,"offset":0x0,"size":0x4,"DOC":"APIC RESVD 2"},\
    "APIC_TPR": {"value":"00000000","position":0xa,"offset":0x0,"size":0x4,"DOC":"APIC TPR "},\
    "APIC_PPR": {"value":"00000000","position":0xc,"offset":0x0,"size":0x4,"DOC":"APIC PPR "},\
    "APIC_LDR": {"value":"01000000","position":0xf,"offset":0x0,"size":0x4,"DOC":"APIC LDR "},\
    "APIC_DFR": {"value":"FFFFFFFF","position":0x10,"offset":0x0,"size":0x4,"DOC":"APIC DFR "},\
    "APIC_SVR": {"value":"0000013F","position":0x11,"offset":0x0,"size":0x4,"DOC":"APIC SVR "},\
    "APIC_ISR_0": {"value":"00000000","position":0x12,"offset":0x0,"size":0x4,"DOC":"APIC ISR_0 "},\
    "APIC_ISR_1": {"value":"00000000","position":0x13,"offset":0x0,"size":0x4,"DOC":"APIC ISR_1 "},\
    "APIC_ISR_2": {"value":"00000000","position":0x14,"offset":0x0,"size":0x4,"DOC":"APIC ISR_2 "},\
    "APIC_ISR_3": {"value":"00000000","position":0x15,"offset":0x0,"size":0x4,"DOC":"APIC ISR_3 "},\
    "APIC_ISR_4": {"value":"00000000","position":0x16,"offset":0x0,"size":0x4,"DOC":"APIC ISR_4 "},\
    "APIC_ISR_5": {"value":"00000000","position":0x17,"offset":0x0,"size":0x4,"DOC":"APIC ISR_5 "},\
    "APIC_ISR_6": {"value":"00000000","position":0x18,"offset":0x0,"size":0x4,"DOC":"APIC ISR_6 "},\
    "APIC_ISR_7": {"value":"00000000","position":0x19,"offset":0x0,"size":0x4,"DOC":"APIC ISR_7 "},\
    "APIC_TMR_0": {"value":"00000000","position":0x1a,"offset":0x0,"size":0x4,"DOC":"APIC TMR_0 "},\
    "APIC_TMR_1": {"value":"00000000","position":0x1b,"offset":0x0,"size":0x4,"DOC":"APIC TMR_1 "},\
    "APIC_TMR_2": {"value":"00000000","position":0x1c,"offset":0x0,"size":0x4,"DOC":"APIC TMR_2 "},\
    "APIC_TMR_3": {"value":"00040004","position":0x1d,"offset":0x0,"size":0x4,"DOC":"APIC TMR_3 "},\
    "APIC_TMR_4": {"value":"00060004","position":0x1e,"offset":0x0,"size":0x4,"DOC":"APIC TMR_4 "},\
    "APIC_TMR_5": {"value":"000A0006","position":0x1f,"offset":0x0,"size":0x4,"DOC":"APIC TMR_5 "},\
    "APIC_TMR_6": {"value":"00000000","position":0x20,"offset":0x0,"size":0x4,"DOC":"APIC TMR_6 "},\
    "APIC_TMR_7": {"value":"00000000","position":0x21,"offset":0x0,"size":0x4,"DOC":"APIC TMR_7 "},\
    "APIC_IRR_0": {"value":"00000000","position":0x22,"offset":0x0,"size":0x4,"DOC":"APIC IRR_0 "},\
    "APIC_IRR_1": {"value":"00000000","position":0x23,"offset":0x0,"size":0x4,"DOC":"APIC IRR_1 "},\
    "APIC_IRR_2": {"value":"00000000","position":0x24,"offset":0x0,"size":0x4,"DOC":"APIC IRR_2 "},\
    "APIC_IRR_3": {"value":"00000000","position":0x25,"offset":0x0,"size":0x4,"DOC":"APIC IRR_3 "},\
    "APIC_IRR_4": {"value":"00000000","position":0x26,"offset":0x0,"size":0x4,"DOC":"APIC IRR_4 "},\
    "APIC_IRR_5": {"value":"00000000","position":0x27,"offset":0x0,"size":0x4,"DOC":"APIC IRR_5 "},\
    "APIC_IRR_6": {"value":"00000000","position":0x28,"offset":0x0,"size":0x4,"DOC":"APIC IRR_6 "},\
    "APIC_IRR_7": {"value":"00000000","position":0x29,"offset":0x0,"size":0x4,"DOC":"APIC IRR_7 "},\
    "APIC_ESR": {"value":"00000000","position":0x2a,"offset":0x0,"size":0x4,"DOC":"APIC ESR "},\
    "APIC_ICR0": {"value":"0004002F","position":0x32,"offset":0x0,"size":0x4,"DOC":"APIC ICR0 "},\
    "APIC_ICR1": {"value":"01000000","position":0x33,"offset":0x0,"size":0x4,"DOC":"APIC ICR1 "},\
    "APIC_LVTT": {"value":"000300FD","position":0x34,"offset":0x0,"size":0x4,"DOC":"APIC LVTT "},\
    "APIC_LVTS": {"value":"00010000","position":0x35,"offset":0x0,"size":0x4,"DOC":"APIC LVTS "},\
    "APIC_LVTP": {"value":"000000FE","position":0x36,"offset":0x0,"size":0x4,"DOC":"APIC LVTP "},\
    "APIC_LVT0": {"value":"0001003F","position":0x37,"offset":0x0,"size":0x4,"DOC":"APIC LVT0 "},\
    "APIC_LVT1": {"value":"000004FF","position":0x38,"offset":0x0,"size":0x4,"DOC":"APIC LVT1 "},\
    "APIC_LVTE": {"value":"000000E3","position":0x39,"offset":0x0,"size":0x4,"DOC":"APIC LVTE "},\
    "APIC_INIT_COUNT": {"value":"00000000","position":0x3a,"offset":0x0,"size":0x4,"DOC":"APIC INIT_COUNT "},\
    "APIC_TIMER": {"value":"00000000","position":0x3b,"offset":0x0,"size":0x4,"DOC":"APIC TIMER "},\
    "APIC_TIMER_DIV": {"value":"0000000B","position":0x40,"offset":0x0,"size":0x4,"DOC":"APIC TIMER_DIV "},\
    "APIC_RESVD_3": {"value":"00000001","position":0x41,"offset":0x0,"size":0x4,"DOC":"APIC RESVD 3"},\
                 }
CTR_REGS_PROLOG = {"offset":                      0xe,\
                 "prolog_size":                 0x400,\
                 }
UC_REGS_PROLOG = {"offset":                      0xf,\
                 "prolog_size":                 0x3E8,\
                 "uncore_data_size": {"value":"000003E0","position":0x0,"offset":0x0,"size":0x4,"DOC":"uncore_data_size "},\
               "uncore_type":      {"value":"00008000","position":0x1,"offset":0x0,"size":0x4,"DOC":"uncore_type "},\
                   "uncore_1_HCR8_l": {"value":"7004001C","position":0x2,"offset":0x0,"size":0x4,"DOC":"uncore_1_HCR8 l "},\
    "uncore_1_HCR8_h": {"value":"00000000","position":0x3,"offset":0x0,"size":0x4,"DOC":"uncore_1_HCR8 h "},\
    "uncore_undefined_0": {"value":"00000000","position":0x4,"offset":0x0,"size":0x4,"DOC":"uncore_undefined_0 "},\
    "uncore_undefined_1": {"value":"00000000","position":0x5,"offset":0x0,"size":0x4,"DOC":"uncore_undefined_1 "},\
    "uncore_undefined_2": {"value":"00000000","position":0x6,"offset":0x0,"size":0x4,"DOC":"uncore_undefined_2 "},\
    "uncore_undefined_3": {"value":"00000000","position":0x7,"offset":0x0,"size":0x4,"DOC":"uncore_undefined_3 "},\
    "uncore_4_BMR_l": {"value":"03000002","position":0x8,"offset":0x0,"size":0x4,"DOC":"uncore_4_BMR l "},\
    "uncore_4_BMR_h": {"value":"00000000","position":0x9,"offset":0x0,"size":0x4,"DOC":"uncore_4_BMR h "},\
    "uncore_7_HCR4_l": {"value":"08570000","position":0xe,"offset":0x0,"size":0x4,"DOC":"uncore_7_HCR4 l "},\
    "uncore_7_HCR4_h": {"value":"00000000","position":0xf,"offset":0x0,"size":0x4,"DOC":"uncore_7_HCR4 h "},\
    "uncore_8_HCR5_l": {"value":"08000847","position":0x10,"offset":0x0,"size":0x4,"DOC":"uncore_8_HCR5 l "},\
    "uncore_8_HCR5_h": {"value":"00000000","position":0x11,"offset":0x0,"size":0x4,"DOC":"uncore_8_HCR5 h "},\
    "uncore_9_HCR6_l": {"value":"0000004F","position":0x12,"offset":0x0,"size":0x4,"DOC":"uncore_9_HCR6 l "},\
    "uncore_9_HCR6_h": {"value":"00000000","position":0x13,"offset":0x0,"size":0x4,"DOC":"uncore_9_HCR6 h "},\
    "uncore_10_RING_OSCILLATOR_MSR_l": {"value":"00000000","position":0x14,"offset":0x0,"size":0x4,"DOC":"uncore_10_RING_OSCILLATOR_MSR l "},\
    "uncore_10_RING_OSCILLATOR_MSR_h": {"value":"00000000","position":0x15,"offset":0x0,"size":0x4,"DOC":"uncore_10_RING_OSCILLATOR_MSR h "},\
    "uncore_12_PERF_CTL_MSR_l": {"value":"00000C63","position":0x18,"offset":0x0,"size":0x4,"DOC":"uncore_12_PERF_CTL_MSR l "},\
    "uncore_12_PERF_CTL_MSR_h": {"value":"00000000","position":0x19,"offset":0x0,"size":0x4,"DOC":"uncore_12_PERF_CTL_MSR h "},\
    "uncore_13_HCR3_l": {"value":"2A750090","position":0x1a,"offset":0x0,"size":0x4,"DOC":"uncore_13_HCR3 l "},\
    "uncore_13_HCR3_h": {"value":"00000000","position":0x1b,"offset":0x0,"size":0x4,"DOC":"uncore_13_HCR3 h "},\
    "uncore_14_NCR_l": {"value":"00000000","position":0x1c,"offset":0x0,"size":0x4,"DOC":"uncore_14_NCR l "},\
    "uncore_14_NCR_h": {"value":"00000000","position":0x1d,"offset":0x0,"size":0x4,"DOC":"uncore_14_NCR h "},\
    "uncore_15_BSR_l": {"value":"00008CC9","position":0x1e,"offset":0x0,"size":0x4,"DOC":"uncore_15_BSR l "},\
    "uncore_15_BSR_h": {"value":"00000000","position":0x1f,"offset":0x0,"size":0x4,"DOC":"uncore_15_BSR h "},\
    "uncore_18_HARD_POWERONHARD_POWERON_MSR_l": {"value":"03000000","position":0x24,"offset":0x0,"size":0x4,"DOC":"uncore_18_HARD_POWERONHARD_POWERON_MSR l "},\
    "uncore_18_HARD_POWERONHARD_POWERON_MSR_h": {"value":"00000000","position":0x25,"offset":0x0,"size":0x4,"DOC":"uncore_18_HARD_POWERONHARD_POWERON_MSR h "},\
    "uncore_21_BUS_IDLE_MSR_l": {"value":"000800FF","position":0x2a,"offset":0x0,"size":0x4,"DOC":"uncore_21_BUS_IDLE_MSR l "},\
    "uncore_21_BUS_IDLE_MSR_h": {"value":"00000000","position":0x2b,"offset":0x0,"size":0x4,"DOC":"uncore_21_BUS_IDLE_MSR h "},\
    "uncore_22_CLOCK_MODULATION_MSR_l": {"value":"00000002","position":0x2c,"offset":0x0,"size":0x4,"DOC":"uncore_22_CLOCK_MODULATION_MSR l "},\
    "uncore_22_CLOCK_MODULATION_MSR_h": {"value":"00000000","position":0x2d,"offset":0x0,"size":0x4,"DOC":"uncore_22_CLOCK_MODULATION_MSR h "},\
    "uncore_24_PERF_STATUS_MSR_l": {"value":"08000C63","position":0x30,"offset":0x0,"size":0x4,"DOC":"uncore_24_PERF_STATUS_MSR l "},\
    "uncore_24_PERF_STATUS_MSR_h": {"value":"00000000","position":0x31,"offset":0x0,"size":0x4,"DOC":"uncore_24_PERF_STATUS_MSR h "},\
    "uncore_25_PERF_STATUS_UP_MSR_l": {"value":"08570C63","position":0x32,"offset":0x0,"size":0x4,"DOC":"uncore_25_PERF_STATUS_UP_MSR l "},\
    "uncore_25_PERF_STATUS_UP_MSR_h": {"value":"00000000","position":0x33,"offset":0x0,"size":0x4,"DOC":"uncore_25_PERF_STATUS_UP_MSR h "},\
    "uncore_26_THERM2_CTL_MSR_l": {"value":"00000857","position":0x34,"offset":0x0,"size":0x4,"DOC":"uncore_26_THERM2_CTL_MSR l "},\
    "uncore_26_THERM2_CTL_MSR_h": {"value":"00000000","position":0x35,"offset":0x0,"size":0x4,"DOC":"uncore_26_THERM2_CTL_MSR h "},\
    "uncore_28_HCR_l": {"value":"00800000","position":0x38,"offset":0x0,"size":0x4,"DOC":"uncore_28_HCR l "},\
    "uncore_28_HCR_h": {"value":"00000000","position":0x39,"offset":0x0,"size":0x4,"DOC":"uncore_28_HCR h "},\
    "uncore_30_MSR_FSB_FREQ_l": {"value":"00000000","position":0x3c,"offset":0x0,"size":0x4,"DOC":"uncore_30_MSR_FSB_FREQ l "},\
    "uncore_30_MSR_FSB_FREQ_h": {"value":"00000000","position":0x3d,"offset":0x0,"size":0x4,"DOC":"uncore_30_MSR_FSB_FREQ h "},\
    "uncore_32_VRMCount_l": {"value":"00001388","position":0x40,"offset":0x0,"size":0x4,"DOC":"uncore_32_VRMCount l "},\
    "uncore_32_VRMCount_h": {"value":"00000000","position":0x41,"offset":0x0,"size":0x4,"DOC":"uncore_32_VRMCount h "},\
    "uncore_33_PLLCount_l": {"value":"00000CF0","position":0x42,"offset":0x0,"size":0x4,"DOC":"uncore_33_PLLCount l "},\
    "uncore_33_PLLCount_h": {"value":"00000000","position":0x43,"offset":0x0,"size":0x4,"DOC":"uncore_33_PLLCount h "},\
    "uncore_38_PtA_l": {"value":"80000857","position":0x4c,"offset":0x0,"size":0x4,"DOC":"uncore_38_PtA l "},\
    "uncore_38_PtA_h": {"value":"00000000","position":0x4d,"offset":0x0,"size":0x4,"DOC":"uncore_38_PtA h "},\
    "uncore_39_PtB_l": {"value":"8000095A","position":0x4e,"offset":0x0,"size":0x4,"DOC":"uncore_39_PtB l "},\
    "uncore_39_PtB_h": {"value":"00000000","position":0x4f,"offset":0x0,"size":0x4,"DOC":"uncore_39_PtB h "},\
    "uncore_40_PtC_l": {"value":"80000A5D","position":0x50,"offset":0x0,"size":0x4,"DOC":"uncore_40_PtC l "},\
    "uncore_40_PtC_h": {"value":"00000000","position":0x51,"offset":0x0,"size":0x4,"DOC":"uncore_40_PtC h "},\
    "uncore_41_PtD_l": {"value":"80000B60","position":0x52,"offset":0x0,"size":0x4,"DOC":"uncore_41_PtD l "},\
    "uncore_41_PtD_h": {"value":"00000000","position":0x53,"offset":0x0,"size":0x4,"DOC":"uncore_41_PtD h "},\
    "uncore_42_PtE_l": {"value":"88000C63","position":0x54,"offset":0x0,"size":0x4,"DOC":"uncore_42_PtE l "},\
    "uncore_42_PtE_h": {"value":"00000000","position":0x55,"offset":0x0,"size":0x4,"DOC":"uncore_42_PtE h "},\
    "uncore_43_XCORE_CTRL_l": {"value":"00000000","position":0x56,"offset":0x0,"size":0x4,"DOC":"uncore_43_XCORE_CTRL l "},\
    "uncore_43_XCORE_CTRL_h": {"value":"00000000","position":0x57,"offset":0x0,"size":0x4,"DOC":"uncore_43_XCORE_CTRL h "},\
    "uncore_54_PIDCntl_l": {"value":"00000000","position":0x6c,"offset":0x0,"size":0x4,"DOC":"uncore_54_PIDCntl l "},\
    "uncore_54_PIDCntl_h": {"value":"00000000","position":0x6d,"offset":0x0,"size":0x4,"DOC":"uncore_54_PIDCntl h "},\
    "uncore_56_ForceOrderCntl_l": {"value":"80044FFF","position":0x70,"offset":0x0,"size":0x4,"DOC":"uncore_56_ForceOrderCntl l "},\
    "uncore_56_ForceOrderCntl_h": {"value":"00000000","position":0x71,"offset":0x0,"size":0x4,"DOC":"uncore_56_ForceOrderCntl h "},\
    "uncore_60_SpecStatus_l": {"value":"00000000","position":0x78,"offset":0x0,"size":0x4,"DOC":"uncore_60_SpecStatus l "},\
    "uncore_60_SpecStatus_h": {"value":"00000000","position":0x79,"offset":0x0,"size":0x4,"DOC":"uncore_60_SpecStatus h "},\
    "uncore_64_BUG_FIXES_l": {"value":"10000000","position":0x80,"offset":0x0,"size":0x4,"DOC":"uncore_64_BUG_FIXES l "},\
    "uncore_64_BUG_FIXES_h": {"value":"00000000","position":0x81,"offset":0x0,"size":0x4,"DOC":"uncore_64_BUG_FIXES h "},\
    "uncore_65_PCCR_l": {"value":"00000000","position":0x82,"offset":0x0,"size":0x4,"DOC":"uncore_65_PCCR l "},\
    "uncore_65_PCCR_h": {"value":"00000000","position":0x83,"offset":0x0,"size":0x4,"DOC":"uncore_65_PCCR h "},\
    "uncore_66_ICCR_l": {"value":"00000000","position":0x84,"offset":0x0,"size":0x4,"DOC":"uncore_66_ICCR l "},\
    "uncore_66_ICCR_h": {"value":"00000000","position":0x85,"offset":0x0,"size":0x4,"DOC":"uncore_66_ICCR h "},\
    "uncore_67_PGCR_l": {"value":"10004000","position":0x86,"offset":0x0,"size":0x4,"DOC":"uncore_67_PGCR l "},\
    "uncore_67_PGCR_h": {"value":"00000000","position":0x87,"offset":0x0,"size":0x4,"DOC":"uncore_67_PGCR h "},\
    "uncore_68_CGCR_l": {"value":"00000040","position":0x88,"offset":0x0,"size":0x4,"DOC":"uncore_68_CGCR l "},\
    "uncore_68_CGCR_h": {"value":"00000000","position":0x89,"offset":0x0,"size":0x4,"DOC":"uncore_68_CGCR h "},\
    "uncore_69_UC_MISC_ENABLE_l": {"value":"00153C89","position":0x8a,"offset":0x0,"size":0x4,"DOC":"uncore_69_UC_MISC_ENABLE l "},\
    "uncore_69_UC_MISC_ENABLE_h": {"value":"00000000","position":0x8b,"offset":0x0,"size":0x4,"DOC":"uncore_69_UC_MISC_ENABLE h "},\
    "uncore_70_PGCR2_l": {"value":"03F050C6","position":0x8c,"offset":0x0,"size":0x4,"DOC":"uncore_70_PGCR2 l "},\
    "uncore_70_PGCR2_h": {"value":"00000000","position":0x8d,"offset":0x0,"size":0x4,"DOC":"uncore_70_PGCR2 h "},\
    "uncore_84_TECR_l": {"value":"00000000","position":0xa8,"offset":0x0,"size":0x4,"DOC":"uncore_84_TECR l "},\
    "uncore_84_TECR_h": {"value":"00000000","position":0xa9,"offset":0x0,"size":0x4,"DOC":"uncore_84_TECR h "},\
    "uncore_85_MDCR_l": {"value":"00000000","position":0xaa,"offset":0x0,"size":0x4,"DOC":"uncore_85_MDCR l "},\
    "uncore_85_MDCR_h": {"value":"00000000","position":0xab,"offset":0x0,"size":0x4,"DOC":"uncore_85_MDCR h "},\
    "uncore_89_UC_CTR_BUSCLKS_H_l": {"value":"F56833CF","position":0xb2,"offset":0x0,"size":0x4,"DOC":"uncore_89_UC_CTR_BUSCLKS_H l "},\
    "uncore_89_UC_CTR_BUSCLKS_H_h": {"value":"00001479","position":0xb3,"offset":0x0,"size":0x4,"DOC":"uncore_89_UC_CTR_BUSCLKS_H h "},\
    "uncore_90_UC_CTR_CORECLKS_H_l": {"value":"C0713747","position":0xb4,"offset":0x0,"size":0x4,"DOC":"uncore_90_UC_CTR_CORECLKS_H l "},\
    "uncore_90_UC_CTR_CORECLKS_H_h": {"value":"00007ADB","position":0xb5,"offset":0x0,"size":0x4,"DOC":"uncore_90_UC_CTR_CORECLKS_H h "},\
    "uncore_91_UC_PERF_CTR0_H_l": {"value":"256CCC49","position":0xb6,"offset":0x0,"size":0x4,"DOC":"uncore_91_UC_PERF_CTR0_H l "},\
    "uncore_91_UC_PERF_CTR0_H_h": {"value":"00000077","position":0xb7,"offset":0x0,"size":0x4,"DOC":"uncore_91_UC_PERF_CTR0_H h "},\
    "uncore_92_UC_PERF_CTR1_H_l": {"value":"00000000","position":0xb8,"offset":0x0,"size":0x4,"DOC":"uncore_92_UC_PERF_CTR1_H l "},\
    "uncore_92_UC_PERF_CTR1_H_h": {"value":"00000000","position":0xb9,"offset":0x0,"size":0x4,"DOC":"uncore_92_UC_PERF_CTR1_H h "},\
    "L2_1_L2_STATUS_REG_IDX_H_l": {"value":"00000000","position":0xbc,"offset":0x0,"size":0x4,"DOC":"L2_1_L2_STATUS_REG_IDX_H l "},\
    "L2_1_L2_STATUS_REG_IDX_H_h": {"value":"00000000","position":0xbd,"offset":0x0,"size":0x4,"DOC":"L2_1_L2_STATUS_REG_IDX_H h "},\
    "L2_2_L2_CONFIG_REG_IDX_H_l": {"value":"60800002","position":0xbe,"offset":0x0,"size":0x4,"DOC":"L2_2_L2_CONFIG_REG_IDX_H l "},\
    "L2_2_L2_CONFIG_REG_IDX_H_h": {"value":"00000000","position":0xbf,"offset":0x0,"size":0x4,"DOC":"L2_2_L2_CONFIG_REG_IDX_H h "},\
    "L2_3_L2_SIZE_REG_IDX_H_l": {"value":"00000010","position":0xc0,"offset":0x0,"size":0x4,"DOC":"L2_3_L2_SIZE_REG_IDX_H l "},\
    "L2_3_L2_SIZE_REG_IDX_H_h": {"value":"00000040","position":0xc1,"offset":0x0,"size":0x4,"DOC":"L2_3_L2_SIZE_REG_IDX_H h "},\
    "L2_8_L2_CTRL00_REG_IDX_H_l": {"value":"00000000","position":0xca,"offset":0x0,"size":0x4,"DOC":"L2_8_L2_CTRL00_REG_IDX_H l "},\
    "L2_8_L2_CTRL00_REG_IDX_H_h": {"value":"28000000","position":0xcb,"offset":0x0,"size":0x4,"DOC":"L2_8_L2_CTRL00_REG_IDX_H h "},\
    "L2_9_L2_CTRL01_REG_IDX_H_l": {"value":"00000000","position":0xcc,"offset":0x0,"size":0x4,"DOC":"L2_9_L2_CTRL01_REG_IDX_H l "},\
    "L2_9_L2_CTRL01_REG_IDX_H_h": {"value":"00000010","position":0xcd,"offset":0x0,"size":0x4,"DOC":"L2_9_L2_CTRL01_REG_IDX_H h "},\
    "L2_10_L2_CTRL02_REG_IDX_H_l": {"value":"80008100","position":0xce,"offset":0x0,"size":0x4,"DOC":"L2_10_L2_CTRL02_REG_IDX_H l "},\
    "L2_10_L2_CTRL02_REG_IDX_H_h": {"value":"00100613","position":0xcf,"offset":0x0,"size":0x4,"DOC":"L2_10_L2_CTRL02_REG_IDX_H h "},\
    "L2_11_L2_CTRL03_REG_IDX_H_l": {"value":"000C4800","position":0xd0,"offset":0x0,"size":0x4,"DOC":"L2_11_L2_CTRL03_REG_IDX_H l "},\
    "L2_11_L2_CTRL03_REG_IDX_H_h": {"value":"00000000","position":0xd1,"offset":0x0,"size":0x4,"DOC":"L2_11_L2_CTRL03_REG_IDX_H h "},\
    "L2_12_L2_CTRL04_REG_IDX_H_l": {"value":"00000000","position":0xd2,"offset":0x0,"size":0x4,"DOC":"L2_12_L2_CTRL04_REG_IDX_H l "},\
    "L2_12_L2_CTRL04_REG_IDX_H_h": {"value":"00000000","position":0xd3,"offset":0x0,"size":0x4,"DOC":"L2_12_L2_CTRL04_REG_IDX_H h "},\
    "L2_13_L2_CTRL05_REG_IDX_H_l": {"value":"00000108","position":0xd4,"offset":0x0,"size":0x4,"DOC":"L2_13_L2_CTRL05_REG_IDX_H l "},\
    "L2_13_L2_CTRL05_REG_IDX_H_h": {"value":"20000001","position":0xd5,"offset":0x0,"size":0x4,"DOC":"L2_13_L2_CTRL05_REG_IDX_H h "},\
    "L2_14_L2_CTRL06_REG_IDX_H_l": {"value":"10502080","position":0xd6,"offset":0x0,"size":0x4,"DOC":"L2_14_L2_CTRL06_REG_IDX_H l "},\
    "L2_14_L2_CTRL06_REG_IDX_H_h": {"value":"28000008","position":0xd7,"offset":0x0,"size":0x4,"DOC":"L2_14_L2_CTRL06_REG_IDX_H h "},\
    "L2_15_L2_CTRL07_REG_IDX_H_l": {"value":"1042B204","position":0xd8,"offset":0x0,"size":0x4,"DOC":"L2_15_L2_CTRL07_REG_IDX_H l "},\
    "L2_15_L2_CTRL07_REG_IDX_H_h": {"value":"00000002","position":0xd9,"offset":0x0,"size":0x4,"DOC":"L2_15_L2_CTRL07_REG_IDX_H h "},\
    "L2_16_L2_CTRL08_REG_IDX_H_l": {"value":"08F00000","position":0xda,"offset":0x0,"size":0x4,"DOC":"L2_16_L2_CTRL08_REG_IDX_H l "},\
    "L2_16_L2_CTRL08_REG_IDX_H_h": {"value":"44000000","position":0xdb,"offset":0x0,"size":0x4,"DOC":"L2_16_L2_CTRL08_REG_IDX_H h "},\
    "L2_17_L2_CTRL09_REG_IDX_H_l": {"value":"08000444","position":0xdc,"offset":0x0,"size":0x4,"DOC":"L2_17_L2_CTRL09_REG_IDX_H l "},\
    "L2_17_L2_CTRL09_REG_IDX_H_h": {"value":"01000800","position":0xdd,"offset":0x0,"size":0x4,"DOC":"L2_17_L2_CTRL09_REG_IDX_H h "},\
    "L2_18_L2_CTRL10_REG_IDX_H_l": {"value":"E0000000","position":0xde,"offset":0x0,"size":0x4,"DOC":"L2_18_L2_CTRL10_REG_IDX_H l "},\
    "L2_18_L2_CTRL10_REG_IDX_H_h": {"value":"00001840","position":0xdf,"offset":0x0,"size":0x4,"DOC":"L2_18_L2_CTRL10_REG_IDX_H h "},\
    "L2_19_L2_CTRL11_REG_IDX_H_l": {"value":"000E0000","position":0xe0,"offset":0x0,"size":0x4,"DOC":"L2_19_L2_CTRL11_REG_IDX_H l "},\
    "L2_19_L2_CTRL11_REG_IDX_H_h": {"value":"80900000","position":0xe1,"offset":0x0,"size":0x4,"DOC":"L2_19_L2_CTRL11_REG_IDX_H h "},\
    "L2_20_L2_CTRL12_REG_IDX_H_l": {"value":"00040000","position":0xe2,"offset":0x0,"size":0x4,"DOC":"L2_20_L2_CTRL12_REG_IDX_H l "},\
    "L2_20_L2_CTRL12_REG_IDX_H_h": {"value":"009FE003","position":0xe3,"offset":0x0,"size":0x4,"DOC":"L2_20_L2_CTRL12_REG_IDX_H h "},\
    "L2_21_L2_CTRL13_REG_IDX_H_l": {"value":"22000002","position":0xe4,"offset":0x0,"size":0x4,"DOC":"L2_21_L2_CTRL13_REG_IDX_H l "},\
    "L2_21_L2_CTRL13_REG_IDX_H_h": {"value":"61088401","position":0xe5,"offset":0x0,"size":0x4,"DOC":"L2_21_L2_CTRL13_REG_IDX_H h "},\
    "L2_22_L2_CTRL14_REG_IDX_H_l": {"value":"00010004","position":0xe6,"offset":0x0,"size":0x4,"DOC":"L2_22_L2_CTRL14_REG_IDX_H l "},\
    "L2_22_L2_CTRL14_REG_IDX_H_h": {"value":"80EA0100","position":0xe7,"offset":0x0,"size":0x4,"DOC":"L2_22_L2_CTRL14_REG_IDX_H h "},\
    "L2_23_L2_CTRL15_REG_IDX_H_l": {"value":"03FA0700","position":0xe8,"offset":0x0,"size":0x4,"DOC":"L2_23_L2_CTRL15_REG_IDX_H l "},\
    "L2_23_L2_CTRL15_REG_IDX_H_h": {"value":"00000020","position":0xe9,"offset":0x0,"size":0x4,"DOC":"L2_23_L2_CTRL15_REG_IDX_H h "},\
    "L2_24_L2_CTRL16_REG_IDX_H_l": {"value":"00000000","position":0xea,"offset":0x0,"size":0x4,"DOC":"L2_24_L2_CTRL16_REG_IDX_H l "},\
    "L2_24_L2_CTRL16_REG_IDX_H_h": {"value":"00000000","position":0xeb,"offset":0x0,"size":0x4,"DOC":"L2_24_L2_CTRL16_REG_IDX_H h "},\
    "L2_25_L2_CTRL17_REG_IDX_H_l": {"value":"00000000","position":0xec,"offset":0x0,"size":0x4,"DOC":"L2_25_L2_CTRL17_REG_IDX_H l "},\
    "L2_25_L2_CTRL17_REG_IDX_H_h": {"value":"00000000","position":0xed,"offset":0x0,"size":0x4,"DOC":"L2_25_L2_CTRL17_REG_IDX_H h "},\
    "L2_26_L2_SNOOP_ADDR_REG_IDX_H_l": {"value":"00000000","position":0xee,"offset":0x0,"size":0x4,"DOC":"L2_26_L2_SNOOP_ADDR_REG_IDX_H l "},\
    "L2_26_L2_SNOOP_ADDR_REG_IDX_H_h": {"value":"00000000","position":0xef,"offset":0x0,"size":0x4,"DOC":"L2_26_L2_SNOOP_ADDR_REG_IDX_H h "},\
    "L2_27_L2_ERROR_REG_UC_IDX_H_l": {"value":"00000000","position":0xf0,"offset":0x0,"size":0x4,"DOC":"L2_27_L2_ERROR_REG_UC_IDX_H l "},\
    "L2_27_L2_ERROR_REG_UC_IDX_H_h": {"value":"00000000","position":0xf1,"offset":0x0,"size":0x4,"DOC":"L2_27_L2_ERROR_REG_UC_IDX_H h "},\
    "L2_28_L2_ERROR_REG_C0_IDX_H_l": {"value":"00000000","position":0xf2,"offset":0x0,"size":0x4,"DOC":"L2_28_L2_ERROR_REG_C0_IDX_H l "},\
    "L2_28_L2_ERROR_REG_C0_IDX_H_h": {"value":"00000040","position":0xf3,"offset":0x0,"size":0x4,"DOC":"L2_28_L2_ERROR_REG_C0_IDX_H h "},\
    "L2_29_L2_ERROR_REG_C1_IDX_H_l": {"value":"00000000","position":0xf4,"offset":0x0,"size":0x4,"DOC":"L2_29_L2_ERROR_REG_C1_IDX_H l "},\
    "L2_29_L2_ERROR_REG_C1_IDX_H_h": {"value":"00000000","position":0xf5,"offset":0x0,"size":0x4,"DOC":"L2_29_L2_ERROR_REG_C1_IDX_H h "},\
    "L2_30_L2_ERROR_REG_C2_IDX_H_l": {"value":"00000000","position":0xf6,"offset":0x0,"size":0x4,"DOC":"L2_30_L2_ERROR_REG_C2_IDX_H l "},\
    "L2_30_L2_ERROR_REG_C2_IDX_H_h": {"value":"00000000","position":0xf7,"offset":0x0,"size":0x4,"DOC":"L2_30_L2_ERROR_REG_C2_IDX_H h "},\
    "L2_31_L2_ERROR_REG_C3_IDX_H_l": {"value":"00000000","position":0xf8,"offset":0x0,"size":0x4,"DOC":"L2_31_L2_ERROR_REG_C3_IDX_H l "},\
    "L2_31_L2_ERROR_REG_C3_IDX_H_h": {"value":"00000000","position":0xf9,"offset":0x0,"size":0x4,"DOC":"L2_31_L2_ERROR_REG_C3_IDX_H h "},\
                 }
UC_CORE_REGS_PROLOG = {"offset":                      0xc,\
                       "prolog_size":                 0x20,\
                       "uncore_core_regs_data_size": {"value":"00000040","position":0x0,"offset":0x0,"size":0x4,"DOC":"uncore_core_regs data_size "},\
               "uncore_core_regs_type":      {"value":"00001000","position":0x1,"offset":0x0,"size":0x4,"DOC":"uncore_core_regs type "},\
               "uncore_core_BMR_l": {"value":"03000002","position":0x2,"offset":0x0,"size":0x4,"DOC":"uncore_core_BMR_l "},\
               "uncore_core_BMR_h":      {"value":"00000000","position":0x3,"offset":0x0,"size":0x4,"DOC":"uncore_core_BMR_h "},\
               "uncore_core_PERF_CTL_l": {"value":"00000C63","position":0x4,"offset":0x0,"size":0x4,"DOC":"uncore_core_PERF_CTL_l "},\
               "uncore_core_PERF_CTL_h":      {"value":"00000000","position":0x5,"offset":0x0,"size":0x4,"DOC":"uncore_core_PERF_CTL_h "},\
               "uncore_core_HCR_l": {"value":"00800000","position":0x6,"offset":0x0,"size":0x4,"DOC":"uncore_core_HCR_l "},\
               "uncore_core_HCR_h":      {"value":"00000000","position":0x7,"offset":0x0,"size":0x4,"DOC":"uncore_core_HCR_h "},\
                 }#uncore_core_regs_data_size value should be 00000018, but cnsim report 00000040
# UC_CORE_REGS_PROLOG data size from ic is 0x40???????
SUBHDR = [NANO_PEBS_SUBHDR, PEBS_JWAD2_SUBHDR, JWAD_EXCEPTION_SUBHDR, MPERF_SUBHDR]
PROLOG = [FXSAVE_PROLOG, PRAM_PROLOG, CORE_PROLOG, VMCS_STUFF_PROLOG, SMM_STATE_PROLOG, APIC_PROLOG, CTR_REGS_PROLOG, \
          UC_REGS_PROLOG, UC_CORE_REGS_PROLOG]
# prolog information PRAM prolag is 0x8 and PRAM data is 0x6C0, the same way for apic, uc_reg and un_core. But Core 0x528 include data and prolog. 
           #UC_REGS dump is not continuous. for example L2[3]-L2[7] is not dump, the size is (5*8). #So start, end is related to addr
           #FXSAVE, need to check
