# A part of the AegisBlade Python Client Library
# Copyright (C) 2019 Thornbury Organization, Bryan Thornbury
# This file may be used under the terms of the GNU Lesser General Public License, version 2.1.
# For more details see: https://www.gnu.org/licenses/lgpl-2.1.html

"""Package `aegisblade` provides the Python client library for [AegisBlade](/).

This is the reference documentation for the Python client library.

[Read the docs](/docs) for more detail.

[See more examples](https://www.github.com/aegisblade/examples) on Github.

Installation
=============

```pip install aegisblade```


Examples
==========

#### Hello World

```
from aegisblade import aegisblade

aegisblade.set_api_key("MY-API-KEY")

def hello_world():
    print("Hello World")
    return "Hello World"

job = aegisblade.run(lambda: do_work())

assert "Hello World" in job.get_return_value()
```

"""
from aegisblade.client import AegisBladeClient
from aegisblade.job_config import JobConfig
from aegisblade.capabilities import Capability

from aegisblade.__version__ import __version__

aegisblade = AegisBladeClient()
__version__ = __version__
