#!/usr/bin/env python
############################################################################
##
## Copyright (c) 2012-2018 60East Technologies Inc., All Rights Reserved.
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

import os
import sys
import platform
import AMPS
import amps_kerberos_authenticator
from nose.tools import *

OS = platform.system()

required_env_vars = {
    'AMPS_HOST': None,
    'AMPS_PORT': None
}

if 'Linux' in OS:
    required_env_vars['KRB5_CLIENT_KTNAME'] = '/home/ubuntu/.krb/60east-linux.keytab'
    required_env_vars['KRB5_CONFIG'] = None

for env_var, default_value in required_env_vars.items():
    if env_var not in os.environ:
        if default_value:
            print('%s was not set. Setting it to %s.' % (env_var, default_value))
            os.environ[env_var] = default_value
        else:
            raise RuntimeError('The %s env var must be set' % env_var)

HOST = os.environ.get('AMPS_HOST')
if not HOST:
    raise RuntimeError('AMPS_HOST env var must be set')

PORT = os.environ.get('AMPS_PORT')
if not PORT:
    raise RuntimeError('AMPS_PORT env var must be set')

URI = 'tcp://60east@%s:%s/amps/json' % (HOST, PORT)
SPN = 'AMPS/%s' % HOST

def test_obtain_token():
    authenticator = amps_kerberos_authenticator.create(SPN)
    token = authenticator.authenticate(None, None)
    assert token
    assert token.startswith('YII')

def test_publish():
    authenticator = amps_kerberos_authenticator.create(SPN)
    client = AMPS.Client('KerberosTestPublisher')
    client.connect(URI);
    client.logon(10000, authenticator);
    client.publish('/topic', "{'foo': 'bar'}");

def test_undefined_spn():
    error_thrown = False
    authenticator = amps_kerberos_authenticator.create('AMPS/foo.com')
    try:
        authenticator.authenticate(None, None)
    except Exception:
        error_thrown = True
    assert error_thrown

def test_validate_spn():
    spns = [
        'AMPS/localhost',
        'AMPS/localhost:1234',
        'AMPS/localhost.localdomain',
        'AMPS/localhost.localdomain:1234',
        'AMPS/ac-1234.localhost.com',
        'AMPS/ac-1234.localhost.com:1234',
    ]
    spns_with_realm = [
        'AMPS/localhost@SOMEREALM',
        'AMPS/localhost@SOMEREALM.COM',
        'AMPS/localhost@SOME.REALM.COM',
        'AMPS/localhost:1234@SOMEREALM',
        'AMPS/localhost:1234@SOMEREALM.COM',
        'AMPS/localhost:1234@SOME.REALM.COM',
        'AMPS/localhost.localdomain@SOMEREALM',
        'AMPS/localhost.localdomain@SOMEREALM.COM',
        'AMPS/localhost.localdomain@SOME.REALM.COM',
        'AMPS/localhost.localdomain:1234@SOMEREALM',
        'AMPS/localhost.localdomain:1234@SOMEREALM.COM',
        'AMPS/localhost.localdomain:1234@SOME.REALM.COM',
    ]

    invalid_spns = [
        'FOO',
        'localhost.localdomain',
        'AMPS@localhost',
        'AMPS@localhost.localdomain',
        'AMPS@localhost.localdomain',
        'AMPS@localhost.localdomain/FOO',
    ]

    if 'Windows' in OS:
        spns.extend(spns_with_realm)

    if 'Linux' in OS:
        invalid_spns.extend(spns_with_realm)

    for spn in spns:
        amps_kerberos_authenticator.validate_spn(spn)

    for spn in invalid_spns:
        error_thrown = False
        try:
            amps_kerberos_authenticator.validate_spn(spn)
        except AMPS.AuthenticationException:
            error_thrown = True
        assert error_thrown

