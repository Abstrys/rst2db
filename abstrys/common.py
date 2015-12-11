#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ################
# script_common.py
# ################
#
# Common bits of command-line scripts.
#
# by Eron Hennessey
#

def printerr(error_text):
    """Prints an error message to stderr"""
    sys.stderr.write("ERROR -- %s\n" % error_text)


