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

```javascript
const {aegisblade} = require('aegisblade');
const os = require("os");

/**
 * In this example the `helloWorld()` function will be run on a
 * server using AegisBlade. 
 */
async function helloWorld() {
    console.log(`The server's hostname is ${os.hostname()}`);

    return `Hello World from ${os.hostname()}`;
}

// Any target function to be run on AegisBlade must be exported.
module.exports = {helloWorld};

/**
 * The `main()` function will run on your local machine
 * and start the job running the `helloWorld()` function
 * on a server using AegisBlade.
 */
async function main() {
    let job = await aegisblade.run(helloWorld);
    
    console.log(`Job Id: ${job.id}`);
    console.log("Waiting for the job to finish running...");

    let jobReturnValue = await job.getReturnValue();
    let jobLogs = await job.getLogs();

    console.log(`Job Return Value: ${jobReturnValue}`);
    console.log(`Job Logs: ${jobLogs}`);
}

//  Using the `require.main === module` idiom to only run main when this script
//    is called directly is especially important when using AegisBlade to prevent
//    infinite loops of jobs creating jobs.
if (require.main === module) {
    (async () => {
        try {
            await main();
        } catch (err) {
            console.error(err);
        }
    })();
}
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

