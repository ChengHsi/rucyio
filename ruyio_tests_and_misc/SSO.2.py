#!/usr/bin/env python

import subprocess
import ldap 
import ldapurl

#subprocess.call("voms-proxy-init", shell=True)
server = "vt-095.grid.sinica.edu.tw"
baseDN = "dc=UI01,dc=grid,dc=sinica,dc=edu,dc=tw"
searchScope = ldapurl.LDAP_SCOPE_SUBTREE
#print searchScope
#searchScope = 
## retrieve all attributes - again adjust to your needs - see documentation for more options
retrieveAttributes = ['uid', 'gecos', 'mail'] 
#retrieveAttributes = 
#searchFilter = "uid=cckuo,ou=TAIWAN,dc=UI01,dc=grid,dc=sinica,dc=edu,dc=tw"
#searchFilter = "uid=chenghsi"
searchFilter = "(objectClass=OpenLDAPperson)"
ldap_url = "ldap://" + server

l = ldap.initialize(ldap_url)
#username = "cn=admin,dc=UI01,dc=grid,dc=sinica,dc=edu,dc=tw"
username = "cn=rucio-server,ou=service,dc=UI01,dc=grid,dc=sinica,dc=edu,dc=tw"
#password  = ";0psSso@tw"
password  = "~!QAZ2wsx3edc"
#password = ""
l.simple_bind_s(username,password)
    
	#mod_attrs = [( ldap.MOD_ADD, 'memberUid', 'GG123456' )]
        #l.modify_s('cn=twgrid,ou=group,ou=login,dc=UI01,dc=grid,dc=sinica,dc=edu,dc=tw', mod_attrs)

#ldap_attributes = l.search_s(baseDN, searchScope, searchFilter)
#for x in ldap_attributes[0][1]:
#    print x
ldap_result_id = l.search_s(baseDN, searchScope, searchFilter, retrieveAttributes), "\n"
result_set = []
result_uid = []
print ldap_result_id
#print l.whoami_s()
