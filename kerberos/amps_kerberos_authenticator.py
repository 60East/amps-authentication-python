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

import re
import platform
import AMPS
OS = platform.system()

if 'Linux' in OS:
    import kerberos
elif 'Windows' in OS:
    import winkerberos as kerberos
else:
    raise RuntimeError('%s is not a supported platform' % OS)

def validate_spn(spn):
    hostPattern = '(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\\-]*[a-zA-Z0-9])\\.)*([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\\-]*[a-zA-Z0-9])'
    spnPattern = '^(\\w+/)(%s)(:\\d+)?' % hostPattern

    if 'Linux' in OS:
        spnFormat = '<service>/<host>[:<port>]'
        spnPattern = '%s$' % spnPattern
    elif 'Windows' in OS:
        realmPattern = "@[\\w\\d]+([\\.\\w\\d]*)?";
        spnPattern = '%s(%s)?$' % (spnPattern, realmPattern)
        spnFormat = '<service>/<host>[:<port>][@REALM]'

    spnRE = re.compile(spnPattern)
    if not spnRE.match(spn):
        raise AMPS.AuthenticationException('The specified SPN %s does not match the format %s' % (spn, spnFormat))

class AMPSKerberosAuthenticator(object):
    def __init__(self, spn):
        validate_spn(spn)
        self.spn = spn.replace('/', '@')
        self.ctx = None
        self.init()

    def init(self):
        print('init')
        (result, self.ctx) = kerberos.authGSSClientInit(self.spn)
        if result != 1:
            raise AMPS.AuthenticationException('Failed to initialize the security context')

    def authenticate(self, username, token):
        print('authenticate')
        if not self.ctx:
            self.init()
        token = token or ''
        result = kerberos.authGSSClientStep(self.ctx, token)
        response = kerberos.authGSSClientResponse(self.ctx)
        if result == 1:
            self.dispose()
        return response if result >= 0 else None

    def completed(self, username, token, reason):
        print('completed')
        if reason == AMPS.Reason.AuthDisabled:
            self.dispose()
            return
        self.authenticate(username, token)

    def retry(self, username, token):
        self.authenticate(username, None)

    def dispose(self):
        print('dispose')
        self.ctx = None

def create(spn):
    return AMPSKerberosAuthenticator(spn)

