# AMPS Python Client Kerberos Authentication

## Build

```bash
$ python setup.py build
```

## Dependencies

`amps_kerberos_authenticator` depends on the `kerberos` module for linux and
the `winkerberos` module for windows.

## Example

For Kerberos authentication using python there is a single module, `amps_kerberos_authenticator`, for authentication on both Linux and Windows.

```python
import AMPS
import amps_kerberos_authenticator

USERNAME = 'username'
HOSTNAME = 'hostname'
PORT = 10304

AMPS_SPN = 'AMPS/%s' % HOSTNAME
AMPS_URI = 'tcp://%s@%s:%d/amps/json' % (USERNAME, HOSTNAME, PORT)

def main():
    authenticator = amps_kerberos_authenticator.create(AMPS_SPN)
    client = AMPS.Client('KerberosExampleClient')
    client.connect(AMPS_URI)
    client.logon(5000, authenticator)

if __name__ == '__main__':
    main()
```

## See Also

[Kerberos Authentication Blog Article]()
[libamps_multi_authentication](http://devnull.crankuptheamps.com/documentation/html/5.3.0.0/user-guide/html/chapters/auxiliary_modules.html#authentication-with-the-amps-multimechanism-authentication-module) AMPS Server Module

