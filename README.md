<!-- PROJECT LOGO -->

<p align="center">
  <a href="https://www.aegisblade.com">
    <img src="https://www.aegisblade.com/images/BigCloud.png" alt="Logo" width="80">
  </a>

  <h3 align="center">AegisBlade Python Client</h3>

  <p align="center">
    <img src="https://img.shields.io/pypi/v/aegisblade" alt="pypi version" />
    <img src="https://img.shields.io/pypi/pyversions/aegisblade" alt="supported python versions" />
    <img src="https://img.shields.io/github/license/aegisblade/aegis-python" alt="license">
  </p>

  <p align="center">
    Deploy & run your code in a single function call.
    <br />
    <a href="https://www.aegisblade.com/docs"><strong>Read the docs »</strong></a>
    <br />
    <br />
    <a href="https://www.github.com/aegisblade/examples">Examples</a>
    ·
    <a href="https://www.aegisblade.com/account/register">Sign Up for an API Key</a>
    ·
    <a href="https://github.com/aegisblade/aegis-nodejs/issues">Report Bug</a>
  </p>
</p>

## Installation

We recommend using [virtualenv](https://virtualenv.pypa.io/en/latest/) to create an isolated environment for your python application.

Install the python package as a dependency of your application.

```bash
$ pip install aegisblade
```

Or for `python3`:

```bash
pip3 install aegisblade
```

## Hello World Example

```python
import socket

from aegisblade import aegisblade


def helloworld():
    """
    In this example we will deploy & run this function
        inside of AegisBlade.
    """
    hostname = socket.gethostname()

    print("The server's hostname is {0}".format(hostname))

    return "Hello World from {0}".format(hostname)


def main():
    """
    The main() function will run on your local machine
    and start two jobs on AegisBlade with the above functions.
    """

    # Calling aegisblade.run() will start the job on a server managed by AegisBlade.
    # AegisBlade will handle provisioning hosts, deploying your code, and running it.
    job = aegisblade.run(lambda: helloworld())
    
    # Return values are serialized and can be fetched when the job is finished.
    #
    # Calling .get_return_value() will wait for the job to finish, 
    #   then get the return value.
    print("Waiting for job to finish...")
    job_return_value = job.get_return_value()

    print("RETURN VALUE")
    print(job_return_value)

    assert "Hello World" in job_return_value

    # Logs are stored and can also be fetched after the job is finished.
    job_logs = job.get_logs()

    print("LOGS:")
    print(job_logs)

    assert "hostname" in job_logs


# Using the __name__ == "__main__" idiom to only run main when this script
#   is called directly is especially important when using AegisBlade.
#
# This script may be imported by the AegisBlade runtime, and without the 
#   protective check of __name__, main() would be called inside the job 
#   potentially causing an infinite loop of jobs starting more jobs.
if __name__ == "__main__":
    main()

```

## Note on Python 2

The official python organization will no longer support Python 2 following January 2020.

Due to it's popular usage though, we will likely continue to support a Python 2.7 client for the forseeable future.

## Reference

[Python Client Reference Docs](https://www.aegisblade.com/docs/reference/python)

<!-- CONTACT -->
## Contact

AegisBlade - [@aegisbladehq](https://twitter.com/aegisbladehq) - welovedevs@aegisblade.com

Project Link: [https://github.com/aegisblade/aegis-nodejs](https://github.com/aegisblade/aegis-nodejs)


