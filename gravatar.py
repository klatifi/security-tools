#!/usr/bin/env python
import sys
import hashlib
import requests

#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------
def get_gravatar(email):
    '''
    Generate an MD5 hash of the email address and query the Gravatar server
    for the profile associated with that hash. Return the associated data in
    JSON format.
    '''
    email_hash = hashlib.md5(email).hexdigest()
    resp = requests.get('http://en.gravatar.com/{0}.json'.format(email_hash))
    data = {}
    if resp.status_code == 200:
        try:
            print '[+] Found email address {0}.'.format(email) 
            data = resp.json()
        except ValueError:
            print '[-] Could not convert response to JSON.'
    elif resp.status_code == 404:
        pass
    else:
        print '[-] Received status {0}'.format(resp.status_code)

    return data


def get_profile(email):
    '''
    Parse the Gravatar JSON profile to extract specific data points if they
    exist. Return the list of parsed profile entries.
    '''
    prof = get_gravatar(email)
    
    entries = []
    if prof != {}:
        for e in prof['entry']:
            entry = {}
            entry['email'] = email
            entry['username'] = e.get('preferredUsername', '')
            entry['location'] = e.get('currentLocation', '')
            entry['name'] = get_name(e.get('name'))
            entry['accounts'] = get_accounts(e.get('accounts'))
            entries.append(entry)

    return entries


def get_name(name):
    '''
    Extract the formatted name from a name dictionary.
    '''
    if name is None:
        return ''
    elif name == []:
        return ''
    else:
        return name.get('formatted', '')


def get_accounts(data):
    '''
    Build a list of accounts by extracting specific data points if they exist.
    Return the list of accounts extracted.
    '''
    accounts = []
    if data is None:
        return accounts
    else:
        for a in data:
            account = {}
            account['username'] = a.get('username', '')
            account['url'] = a.get('url', '')
            accounts.append(account) 

    return accounts


def print_profile(profile):
    '''
    Print the profile in a readable format.
    '''
    for p in profile:
        print p['email']
        print '-' * len(p['email'])
        print 'Name: {}'.format(p['name'])
        print 'Username: {}'.format(p['username'])
        print 'Location: {}'.format(p['location'])
        print 'Accounts:'
        for account in p['accounts']:
            print '  Username: {}'.format(account['username'])
            print '  URL: {}'.format(account['url'])
        print



#-----------------------------------------------------------------------------
# Main Program
#-----------------------------------------------------------------------------

#
# Parse command line arguments using argparse
#
if len(sys.argv) != 2:
    print 'Usage: gravatar.py email_file'
    sys.exit(1)

email_file = sys.argv[1]

profiles = []
with open(sys.argv[1]) as emails:
    for email in emails:
        email = email.rstrip('\r\n')
        profile = get_profile(email)
        if profile != []:
            profiles.append(profile)

for profile in profiles:
    print_profile(profile)
