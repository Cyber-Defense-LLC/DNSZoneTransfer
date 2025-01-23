#!/usr/bin/env python3

# Dependencies:
# python3-dnspython

# Used Modules:
import dns.zone as dz
import dns.query as dq
import dns.resolver as dr
import argparse

# Initialize Resolver-Class from dns.resolver as "NS"
NS = dr.Resolver()

# Target domain
Domain = 'example.com'  # Replace with a valid domain

# Set the nameservers that will be used
NS.nameservers = ['8.8.8.8', '8.8.4.4']  # Replace with valid nameservers

# List of found subdomains
Subdomains = []

# Define the AXFR Function
def AXFR(domain, nameserver):
    global Subdomains  # Use global Subdomains list
    
    # Try zone transfer for given domain and nameserver
    try:
        # Perform the zone transfer
        axfr = dz.from_xfr(dq.xfr(nameserver, domain))

        # If zone transfer was successful
        if axfr:
            print(f'[*] Successful Zone Transfer from {nameserver}')

            # Add found subdomains to global 'Subdomains' list
            for record in axfr.nodes.keys():
                subdomain = f'{record}.{domain}'
                Subdomains.append(subdomain)
                print(f'Found subdomain: {subdomain}')

    # If zone transfer fails
    except Exception as error:
        print(f'[!] Error: {error}')

# Example usage
if __name__ == "__main__":
    for nameserver in NS.nameservers:
        AXFR(Domain, nameserver)
    print("\nDiscovered Subdomains:")
    for subdomain in Subdomains:
        print(subdomain)