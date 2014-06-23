#!/usr/bin/env python

import subprocess
import ldap 

#subprocess.call("voms-proxy-init", shell=True)
baseDN = "dc=UI01,dc=grid,dc=sinica,dc=edu,dc=tw"
searchScope = ldap.SCOPE_SUBTREE
## retrieve all attributes - again adjust to your needs - see documentation for more options
#retrieveAttributes = ['uid','gecos'] 
retrieveAttributes = []
#searchFilter = "uid=cckuo,ou=TAIWAN,dc=UI01,dc=grid,dc=sinica,dc=edu,dc=tw"
searchFilter = "uid=cckuo"

l = ldap.initialize("ldap://vt-095.grid.sinica.edu.tw")
#username = "cn=admin,dc=UI01,dc=grid,dc=sinica,dc=edu,dc=tw"
username = "cn=rucio-server,ou=service,dc=UI01,dc=grid,dc=sinica,dc=edu,dc=tw"
#password  = ";0psSso@tw"
password  = "~!QAZ2wsx3edc"
#password = ""
l.simple_bind_s(username,password)
    
	#mod_attrs = [( ldap.MOD_ADD, 'memberUid', 'GG123456' )]
        #l.modify_s('cn=twgrid,ou=group,ou=login,dc=UI01,dc=grid,dc=sinica,dc=edu,dc=tw', mod_attrs)
    
ldap_result_id = l.search_s(baseDN, searchScope, searchFilter, retrieveAttributes)
result_set = []
result_uid = []
print ldap_result_id
#print l.whoami_s()
