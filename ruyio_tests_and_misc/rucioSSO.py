#!/usr/bin/env python

# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Cheng-Hsi Chao, <cheng-hsi.chaos@cern.ch>, 2014
"""
LDAP Integration Script
"""
import ConfigParser
import getpass
import ldap 
import ldapurl
import os
from rucio.client import Client

def initiateLDAP():
    """
    contact the LDAP server
    """
    ldap_schemes = ['ldap://', 'ldaps://'] 
    ldapmodule_trace_level = 1
    ldap.set_option(ldap.OPT_DEBUG_LEVEL,0)
    ldap.set_option(ldap.OPT_X_TLS_CACERTDIR, config.get('ldap', 'cacertdir'))
    ldap.set_option(ldap.OPT_X_TLS_CERTFILE, config.get('ldap', 'certfile'))
    ldap.set_option(ldap.OPT_X_TLS_KEYFILE, config.get('ldap', 'keyfile'))
    ldap.set_option(ldap.OPT_X_TLS_DEMAND, True)
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_DEMAND) #TRY, NEVER, DEMAND
    ldap.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
    for scheme in ldap_schemes:
        print scheme
        ldap_url = scheme + server_url
        l = ldap.initialize(ldap_url)
        try:
            l.start_tls_s()
        except ldap.OPERATIONS_ERROR as e:
            e_msg = e[0]['info']
            if e_msg == 'TLS already started':
                pass
            else:
                raise
        except ldap.SERVER_DOWN:
             if scheme is not ldap_schemes[-1]:
                 continue
             else:
                 raise
        if login_dn != 'DEFAULT': #use anonymous bind if login_dn is DEFAULT
            l.bind(login_dn, password, ldap.AUTH_SIMPLE)
        else:
            try: 
                l.whoami_s()
            except ldap.UNWILLING_TO_PERFORM:
                print 'Anonymous binding is disabled by server'
                raise SystemExit
        return l
        break

def addIdentity(ldapObject):
    """
    add LDAP entry as Rucio Identity
    """
    results = ldapObject.search_s(baseDN, searchScope, searchFilter, retrieveAttributes)
    c = Client()
    for i in results:
        try:
            if 'account' in retrieveAttributes:
                account = i[1]['account'][0]
            else:
                account = i[1]['uid'][0]
            if 'auth_type' in retrieveAttributes:
                authtype = i[1]['auth_type'][0]
            else: 
                authtype = 'x509' #default authtype set as X509
            identity = i[1]['gecos'][0]
            email = i[1]['mail'][0]
            #c.add_identity(account, identity, authtype, email)
            print 'Added new identity to account: %s-%s' % (identity, account)
            #break
        except KeyError as e:
            print 'Attribute', e, 'for account', account, 'is missing' 
            continue
        except:
            #print 'duplicate identity' 
            raise

config = ConfigParser.ConfigParser()
configfiles = list()

if 'RUCIO_HOME' in os.environ:
    configfiles.append('%s/etc/ldap.cfg' % os.environ['RUCIO_HOME'])
configfiles.append('/opt/rucio/etc/ldap.cfg')

if 'VIRTUAL_ENV' in os.environ:
    configfiles.append('%s/etc/ldap.cfg' % os.environ['VIRTUAL_ENV'])
has_config = False
for configfile in configfiles:
    has_config = config.read(configfile) == [configfile]
    if has_config:
        break
 
server_url = config.get('ldap', 'ldap_host')
baseDN = config.get('ldap', 'baseDN')
searchScope = ldapurl.LDAP_SCOPE_SUBTREE
retrieveAttributes = ['uid', 'gecos', 'mail']
if config.get('attributes', 'accounts') != 'uid':
    retrieveAttributes.append('account')
if config.get('attributes', 'auth_type') != 'DEFAULT':    
    retrieveAttributes.append('auth_type')
print retrieveAttributes
searchFilter = config.get('ldap', 'searchFilter')
login_dn = config.get('ldap', 'login_dn')
if login_dn is 'DEFAULT':
    login_dn = None
print 'login_dn', login_dn
password = config.get('ldap', 'password')
if not password and login_dn is not 'DEFAULT': #prompt for password if using DN bind
    password = str(getpass.getpass("Please input LDAP LoginDN's password: "))

if __name__ == '__main__':
    addIdentity(initiateLDAP()) 
