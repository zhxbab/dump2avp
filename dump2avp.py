#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
########################################################
# dump2avp is used for converting bochs dump files to avp
#
########################################################
import sys
from dump import Dump
import tracer
from logging import info,debug,error,warning,critical
dump = Dump(sys.argv[1:])
dump.Parse_dump()
#dump.print_arch_regs(tracer.major_dump_result) # for debug
#dump.print_tr7(tracer.major_dump_initial)
#dump.print_msrs(tracer.major_dump_initial)
#dump.print_fpu(tracer.major_dump_initial)
#dump.print_mmx_sse_avx(tracer.major_dump_initial)
#dump.print_apic(tracer.major_dump_initial)
dump.gen_avp()
