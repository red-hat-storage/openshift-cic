#!/usr/bin/env python
import os
import shlex
import subprocess

ocpversion = raw_input('What version of OpenShift Container Platform are you deploying (3.9 or 3.10)?: ')

if ocpversion == '3.9':
    execfile('cns.py')
elif ocpversion == '3.10':
    execfile('ocp.py')
else:
    print "Enter a valid supported version of OCP"

