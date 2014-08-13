#!/usr/bin/env python

import smtpd
import smtplib
import asyncore
import dns.resolver

port = 2525
debug = False

def get_mx_record(domain):
    records = dns.resolver.query(domain, 'MX')
    return str(records[0].exchange)


class CustomSMTPServer(smtpd.SMTPServer):
    
    def process_message(self, peer, mailfrom, rcpttos, data):
        for rcptto in rcpttos:
            print '[*] Sending message to {0}.'.format(rcptto)

            domain = rcptto.split('@')[1]
            mx = get_mx_record(domain)
            
            try:
                server = smtplib.SMTP(mx, 25)
                if debug:
                    server.set_debuglevel(True)
                server.sendmail(mailfrom, rcptto, data)

            except smtplib.SMTPDataError as e:
                print '[-] {0}'.format(str(e[1]))

            except smtplib.SMTPServerDisconnected as e:
                print '[-] {0}'.format(str(e))

            except smtplib.SMTPConnectError as e:
                print '[-] {0}'.format(str(e[1]))


server = CustomSMTPServer(('127.0.0.1', port), None)
print '[+] Server listening on port {0}'.format(port)
asyncore.loop()
