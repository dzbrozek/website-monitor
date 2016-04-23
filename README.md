Simple program that monitors web sites and reports their availability. This tool is intended as a monitoring tool for web site administrators for detecting problems on their sites.

**Features**:

1. Reads a list of web pages (HTTP URLs) and corresponding page content requirements from a configuration file.
2. Periodically makes an HTTP GET request to each page. The interval can be configured using CRON-like syntax.
3. Verifies that the response received from the server matches the conditions. Supported conditions:
    1. **status** -  checks if the server returns appropriate HTTP response status code
    2. **content** -  checks if the response content includes appropriate content
    3. **regex** -  checks if the  response content matches appropriate regex
4. Measures the time it took for the web server to complete the request.
5. Writes a log file that shows the progress of the program.
6. Displays recent results in the Web browser (http://127.0.0.1:1080)

**Requirements**

See requirements.txt for the required Python packages.

**Configuration**

You need to pass a configuration file as a parameter to the program. Please see example_config.yaml.