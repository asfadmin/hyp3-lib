#!/usr/bin/env python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
###############################################################################
# execute.py
#
# Project:  APD 
# Purpose:  Execute a commnand 
#  
# Author:   Tom Logan
#
# Issues/Caveats:
#
###############################################################################
# Copyright (c) 2017, Alaska Satellite Facility
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Library General Public
# License as published by the Free Software Foundation; either
# version 2 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Library General Public License for more details.
# 
# You should have received a copy of the GNU Library General Public
# License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
###############################################################################
import os
import subprocess
import logging

def execute(cmd, expected=None, logfile=None, uselogging=False):

    if uselogging:
        logging.info('Running command: ' + cmd)
    else:
        print('Running command: ' + cmd)
    rcmd = cmd + ' 2>&1'

    pipe = subprocess.Popen(rcmd, shell=True, stdout=subprocess.PIPE)
    output = pipe.communicate()[0]
    return_val = pipe.returncode
    if uselogging:
        logging.info('subprocess return value was ' + str(return_val))
    else:
        print('subprocess return value was ' + str(return_val))
    
    for line in output.split('\n'):
        if len(line.rstrip()) > 0:
            if uselogging:
                logging.info('Proc: ' + line)
            else:
                print('Proc: ' + line)
            if logfile is not None:
                logfile.write("%s\n" % line)
                
    if uselogging:
        logging.info('Finished: ' + cmd)
    else:
        print('Finished: ' + cmd)

    if return_val != 0:
        if uselogging:
            logging.error('Nonzero return value!')
        else:
            print('Nonzero return value!')
        tool = cmd.split(' ')[0]
        last = 'Nonzero return value: ' + str(return_val)
        next_line = False
        for line in output.split('\n'):
            last = line
            if next_line:
                raise Exception(tool + ': ' + line)
            elif '** Error: *****' in line: # MapReady style error
                next_line = True
            elif 'Error per GCP' in line: # MapReady message that is NOT an error
                pass
            elif 'Setting maximum error to be' in line: # RTC message that is NOT an error
                pass
            elif 'Root mean squared error' in line: # RTC message that is NOT an error
                pass
            elif 'ERROR' in line.upper():
                raise Exception(tool + ': ' + line)
        # No error line found, die with last line
        raise Exception(tool + ': ' + last)

    if expected is not None:
        if uselogging:
            logging.info('Checking for expected output: ' + expected)
        else:
            print('Checking for expected output: ' + expected)
        if os.path.isfile(expected):
            if uselogging:
                logging.info('Found: ' + expected)
            else:
                print('Found: ' + expected)
        else:
            if uselogging:
                logging.info('Expected output file not found: ' + expected)
            else:
                print('Expected output file not found: ' + expected)
            raise Exception("Expected output file not found: " + expected)

    return output
 
