# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html


class Capability(object):
    """Enum-like class of capabilities available to be
    requested as part of an application.
    
    Capabilities are used to request functionality that cannot 
    be defined through the native package manager (pip in python's case).

    Attributes:
        xvfb: Requests that the application be run with xvfb-run.

        chrome: Requests that the application have the `google-chrome` and `chromedriver` 
            binaries available on the PATH. Also implies `Capability.xvfb`.

        firefox: Requests that the application have the `firefox` and `geckodriver` 
            binaries available on the PATH. Also implies `Capability.xvfb`.
    """

    xvfb = "xvfb"
    """Requests that the application be run with `xvfb-run`."""


    chrome = "browser-chrome"
    """Requests that the application have the `google-chrome` and `chromedriver` 
        binaries available on the PATH. Also implies `Capability.xvfb`"""

    firefox = "browser-firefox"
    """Requests that the application have the `firefox` and `geckodriver` 
            binaries available on the PATH. Also implies `Capability.xvfb`."""