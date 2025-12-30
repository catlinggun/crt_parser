import sys
import argparse
import csv
import socket
import requests
import re


def grab_data(domain, res):
    filename = 'crtsh_%s' % domain[0].replace('.', '_')
    # generate the web request and grab the data
    print('[-] Requesting data for %s...' % domain[0])
    request = 'https://crt.sh/?q=%s' % (domain[0])
    raw_data = requests.get(request)
    # use regex to grab all hostnames from the HTML
    regex = re.compile('(?<=>)[a-zA-Z0-9\-\.]+?\.%s(?=<)' % (domain[0]))
    all_domains_dirty = regex.findall(str(raw_data.content))
    # create a set datatype that removes all duplicates
    all_domains = set(all_domains_dirty)
    if len(all_domains) != 0:
        if len(all_domains) != 1:
            domain.append('domains')
        else:
            domain.append('domain')
    else:
        print('[\033[91m!\033[0m] No domains found. Exiting...')
        sys.exit()
    print('    [\033[92m*\033[0m] %d unique %s found!' % (len(all_domains), domain[1]))
    if res:
        resolve_domains(filename, domain, all_domains)
    else:
        filename = filename + '.txt'
        print('[-] Not resolving (-r not specified), writing all unique domains to file...')
        f = open(filename, 'w')
        for domain_name in all_domains:
            f.write(domain_name + '\n')
        f.close()
        print('    [\033[92m*\033[0m] Done! %d %s written to [\033[92m%s\033[0m].\n' % (len(all_domains), domain[1],
                                                                                        filename))


def resolve_domains(filename, domain, all_domains):
    filename = filename + '.csv'
    print('[-] Resolving %s...' % (domain[1]))
    # set up the dict that the final data will be stored in
    domain_ip = {}
    # attempt to resolve each domain and skip writing to dict if it fails
    for host in all_domains:
        try:
            ip = socket.gethostbyname(host)
            if ip != '':
                domain_ip[host] = ip
            else:
                continue
        except:
            continue
    # write the dict to a .csv file
    print('    [\033[92m*\033[0m] %d %s successfully resolved!' % (len(domain_ip), domain[1]))
    print('[-] Writing to %s.csv...' % domain[0])
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Domain', 'IP'])
        for key, value in domain_ip.items():
            if value != '':
                writer.writerow([key, value])
            else:
                continue
    print('    [\033[92m*\033[0m] Done! %d %s written to [\033[92m%s\033[0m].\n' % (len(domain_ip),
                                                                                    domain[1],
                                                                                    filename))


def main():
    print("""
             __                                 
  __________/ /_      ____  ____ ______________ 
 / ___/ ___/ __/     / __ \/ __ `/ ___/ ___/ _ \\
/ /__/ /  / /_      / /_/ / /_/ / /  (__  )  __/
\___/_/   \__/_____/ .___/\__,_/_/  /____/\___/ 
            /_____/_/                           
    """)
    arguments = argparse.ArgumentParser(prog='crt_parse',
                                        description='Grabs all subdomains from crt.sh, (optionally) checks if they '
                                                    'resolve, then packages everything nice and neat into a file for '
                                                    'later use.')
    arguments._action_groups.pop()
    required = arguments.add_argument_group('required arguments')
    optional = arguments.add_argument_group('optional arguments')
    optional.add_argument('-r', '--resolve',
                          action='store_true',
                          help="Will automatically resolve domains and write only resolvable hosts to .csv")
    required.add_argument('-d', '--domain',
                          type=str,
                          nargs=1,
                          help="Client Domain Name",
                          metavar='',
                          default='[DOMAIN]',
                          required=True)
    args = arguments.parse_args()
    grab_data(args.domain, args.resolve)


if __name__ == '__main__':
    main()
