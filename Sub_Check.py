from concurrent.futures import ThreadPoolExecutor
import requests
import logging
import argparse
import re
import time

# Function to validate subdomain format
def is_valid_subdomain(sub):
    # Regular expression to check for valid subdomain format
    return re.match(r"^[a-zA-Z0-9-]{1,63}$", sub) is not None

# Function to check subdomains
def check_subdomain(sub, domain, verbose=False, vhost=False, target_ip=None, current=None, total=None):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive'
    }
    
    if not is_valid_subdomain(sub):
        return None

    if vhost:
        # VHost brute-forcing mode: use the subdomain as the Host header and request the main IP
        headers['Host'] = f"{sub}.{domain}"
        url = f"http://{target_ip}"  # Send the request to the IP
        domain_display = f"{sub}.{domain}"  # Display the full domain being tested
        protocol_list = ['http']  # Typically VHost brute-forcing happens over HTTP
    else:
        # Standard subdomain checking
        protocol_list = ['http', 'https']
        url = None
        domain_display = f"{sub}.{domain}"  

    for protocol in protocol_list:
        if not vhost:
            # If not in vhost mode, construct the URL normally
            url = f"{protocol}://{sub}.{domain}"
        
        try:
            # Send a GET request to check if the subdomain or vhost is live
            response = requests.get(url, headers=headers, timeout=10)
            status_code = response.status_code
        except requests.ConnectionError:
            return None
        else:
            if verbose and current is not None and total is not None:
                
                print(f"[{current}/{total}] Valid: {domain_display} -> {status_code}")
            return url

# Main function to read the wordlist and check subdomains or vhosts
def main(domain, wordlist_file, output_file=None, verbose=False, vhost=False, target_ip=None):
    
    with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as file:
        sub_list = file.read().splitlines()

    total_subs = len(sub_list)  

    
    if verbose:
        logging.basicConfig(level=logging.INFO)

    valid_domains = [] 

    # Use ThreadPoolExecutor to check subdomains concurrently
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for i, sub in enumerate(sub_list, start=1):  # Enumerate to get progress count
            futures.append(executor.submit(check_subdomain, sub, domain, verbose, vhost, target_ip, i, total_subs))
        
        for future in futures:
            result = future.result()
            if result:
                print(f"Valid domain: {result}")
                valid_domains.append(result)
            time.sleep(0.1)  # Avoid overwhelming the server    

    # Write valid domains to the output file if specified
    if output_file:
        with open(output_file, 'w') as file:
            for domain in valid_domains:
                file.write(domain + '\n')

# Argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain Checker with VHost brute-forcing option")
    parser.add_argument('-d', '--domain', required=True, help='Domain to check subdomains for (used in Host header)')
    parser.add_argument('-w', '--wordlist', required=True, help='Wordlist file containing subdomains')
    parser.add_argument('-o', '--output', help='File to save valid domains')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--vhost', action='store_true', help='Enable VHost brute-forcing (use Host header)')
    parser.add_argument('--ip', help='Target IP address for VHost brute-forcing')

    args = parser.parse_args()

    if args.vhost and not args.ip:
        parser.error("--vhost requires --ip to specify the target IP address.")

    
    main(args.domain, args.wordlist, args.output, args.verbose, args.vhost, args.ip)
