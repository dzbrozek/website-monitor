### Website monitor ###

Simple program that monitors web sites and reports their availability. 
This tool is intended as a monitoring tool for web site administrators for detecting problems 
on their sites.

**Features**:

1. Reads a list of web pages (HTTP URLs) and corresponding page content requirements from a configuration file.
2. Periodically makes an HTTP GET request to each page. The interval can be configured using CRON-like syntax.
3. Verifies that the response received from the server matches the conditions. Supported conditions:
    1. **status** -  checks if the server returns appropriate HTTP response status code
    2. **content** -  checks if the response content includes appropriate content
    3. **regex** -  checks if the  response content matches appropriate regex
4. Measures the time it took for the web server to complete the request.
5. Writes a log file that shows the progress of the program.
6. Displays recent results in the Web browser (http://127.0.0.1:8000)

**Installation**

The app is using Python 3.6 and Pipenv. 
If you don't have one of them please install them first.
After that move to your project's directory and call the following command:

```
pipenv install
```

**Configuration**

You need to pass a configuration file as a parameter to the program. 
Please see `example_config.yaml` to learn more.


**Running app**

To start the app run the `monitor.py` script

_Example:_

```
pipenv run python monitor/monitor.py --config my_config.yaml
```

To see the recent results open http://127.0.0.1:8000 in your browser.


**Running tests**

To run the tests use the following command:

```
pipenv run pytest
```