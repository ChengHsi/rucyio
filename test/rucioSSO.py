#!/usr/bin/env python

# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Cheng-Hsi Chao, <cheng-hsi.chaos@cern.ch>, 2014

import ConfigParser
import ldap 
import ldapurl
import os
from rucio.client import Client
if __name__ == '__main__':
    
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
    server = config.get('ldap', 'server')
    baseDN = config.get('ldap', 'baseDN')
    searchScope = ldapurl.LDAP_SCOPE_SUBTREE
    if config.get('attributes', 'accounts') is 'uid':
        retrieveAttributes = ['uid', 'gecos', 'mail'] 
    else:
        retrieveAttributes = ['uid', 'gecos', 'mail', 'accounts']
    searchFilter = config.get('ldap', 'searchFilter')
    ldap_url = 'ldap://' + server
    
    ldapmodule_trace_level = 1
    ldap.set_option(ldap.OPT_DEBUG_LEVEL,2)
    ldap.set_option(ldap.OPT_X_TLS_CACERTDIR, config.get('ldap', 'CACERTDIR'))
    ldap.set_option(ldap.OPT_X_TLS_CERTFILE, config.get('ldap', 'CERTFILE'))
    ldap.set_option(ldap.OPT_X_TLS_KEYFILE, config.get('ldap', 'KEYFILE'))
    ldap.set_option(ldap.OPT_X_TLS_DEMAND, True)
    #ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
    #create new TLS context and store TLS options into the new TLS context
    ldap.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
    l = ldap.initialize(ldap_url)
    l.start_tls_s()
    username = config.get('ldap', 'username')
    #password = config.get('ldap', 'password')
    password = str(raw_input("Please input LDAP password: "))
    #l.sasl_interactive_bind_s(username, password)
    l.simple_bind_s(username,password)
    #mod_attrs = [( ldap.MOD_ADD, 'memberUid', 'GG123456' )]
    #l.modify_s('cn=twgrid,ou=group,ou=login,dc=UI01,dc=grid,dc=sinica,dc=edu,dc=tw', mod_attrs)

    ldap_result_id = l.search_s(baseDN, searchScope, searchFilter, retrieveAttributes)
    c = Client()
    for i in ldap_result_id:
        try:
            account=i[1]['uid'][0]
            identity=i[1]['gecos'][0]
            #c.add_identity(account, identity, authtype='x509', email=i[1]['mail'][0])
            print 'Added new identity to account: %s-%s' % (identity, account)
            break
        except KeyError as e:
            print 'key', e, 'for account', account, 'is missing' 
            continue
        except:
            #print 'duplicate identity' 
            raise
