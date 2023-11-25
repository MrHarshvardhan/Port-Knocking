# Port-Knocking
# Advanced Port Knocking Client

Simple port-knocking client written in Python 3.

## Description

This script performs port knocking on all TCP and UDP ports (1 to 65535) for multiple IP addresses. It uses a specified timeout and delay between knocks. Results are stored in text files in the same directory.

## Usage

```bash
./port-knocking.py -t <timeout> -d <delay> -v <host1> <host2> ...

-t, --timeout: Timeout in milliseconds (default is 200 ms).
-d, --delay: Delay in milliseconds between knocks (default is 200 ms).
-v, --verbose: Be verbose (optional).
<host1> <host2> ...: Hostnames or IP addresses to knock on (supports IPv6).

**Example**
./port-knocking.py -t 300 -d 100 -v 127.0.0.1 127.0.0.2 127.0.0.3

This command performs port knocking on all TCP and UDP ports for the specified hosts with a timeout of 300 ms and a delay of 100 ms between knocks.

## Result
The results will be stored in text files named knock_results_<host>.txt in the same directory.
