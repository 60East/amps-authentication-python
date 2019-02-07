#!/usr/bin/env python
############################################################################
##
## Copyright (c) 2012-2019 60East Technologies Inc., All Rights Reserved.
##
## This computer software is owned by 60East Technologies Inc. and is
## protected by U.S. copyright laws and other laws and by international
## treaties.  This computer software is furnished by 60East Technologies
## Inc. pursuant to a written license agreement and may be used, copied,
## transmitted, and stored only in accordance with the terms of such
## license agreement and with the inclusion of the above copyright notice.
## This computer software or any other copies thereof may not be provided
## or otherwise made available to any other person.
##
## U.S. Government Restricted Rights.  This computer software: (a) was
## developed at private expense and is in all respects the proprietary
## information of 60East Technologies Inc.; (b) was not developed with
## government funds; (c) is a trade secret of 60East Technologies Inc.
## for all purposes of the Freedom of Information Act; and (d) is a
## commercial item and thus, pursuant to Section 12.212 of the Federal
## Acquisition Regulations (FAR) and DFAR Supplement Section 227.7202,
## Government's use, duplication or disclosure of the computer software
## is subject to the restrictions set forth by 60East Technologies Inc..
##
############################################################################

import os, glob, sys

if "bdist_egg" in sys.argv:
  from setuptools import setup
else:
  from distutils.core import setup

#TODO: How should the version be set?

setup(name='amps-kerberos-authenticator',
      description='AMPS Kerberos Authenticator',
      version='1.0.0',
      py_modules=['amps_kerberos_authenticator'],
      maintainer='60East Technologies, Incorporated',
      maintainer_email='support@crankuptheamps.com',
      url='http://crankuptheamps.com')


