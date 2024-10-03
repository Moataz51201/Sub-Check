# Subdomain and VHost Brute-Forcing Script

This Python script is designed to discover subdomains and perform VHost brute-forcing. It uses concurrent threading for faster execution and can handle both subdomain checking and VHost brute-forcing with the use of custom HTTP headers.

## Features:
- Check subdomains against a given domain using HTTP/HTTPS.
- Perform VHost brute-forcing by sending requests with custom `Host` headers.
- Multi-threading for concurrent subdomain checks.
- Optionally output valid domains to a file.
- Verbose mode to display detailed progress logs.

## Usage:
Example Commands:
Basic Subdomain Checking:
python subdomain_checker.py -d example.com -w subdomains.txt

python subdomain_checker.py -d example.com -w subdomains.txt --vhost --ip 192.168.1.1

python subdomain_checker.py -d example.com -w subdomains.txt -o valid_domains.txt

## Arguments:
-d, --domain: Domain to check subdomains for (used in Host header).
-w, --wordlist: Wordlist file containing subdomains.
-o, --output: File to save valid domains (optional).
-v, --verbose: Enable verbose logging.
--vhost: Enable VHost brute-forcing (uses Host header).
--ip: Target IP address for VHost brute-forcing (required with --vhost).

## Disclaimer:
This script is intended for educational and ethical purposes only. Do not use it to check or brute-force domains you do not own or have explicit permission to test. Misuse of this tool may be illegal.

