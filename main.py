#!/usr/bin/env python3

from onvif import ONVIFCamera


if __name__ == '__main__':
    mycam = ONVIFCamera('192.168.1.64', 80, 'admin', 'admin')
    print(mycam)


