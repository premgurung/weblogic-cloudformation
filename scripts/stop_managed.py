#!/usr/bin/python
import urllib2
import os, sys

###########################################

loadProperties('/tmp/weblogic-cloudformation-master/scripts/settings')
r = urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-hostname')
public_dns = r.read()
r = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id')
instance_id = r.read()

machine_data = {'name':'linux.%s' % instance_id, 'address': public_dns, 'machine_type':'UnixMachine'}
servers_data = {'name': 'MS_%s' % instance_id, 'port': 7003, 'port_ssl': 7502, 'address': public_dns}

###########################################

connect('weblogic', admin_pwd, '%s:7001' % admin_ip)
edit()
startEdit()

print 'DELETING MACHINE: %s' % machine_data['name']
cd('/')
editService.getConfigurationManager().removeReferencesToBean(getMBean('/Machines/%s' % machine_data['name']))
cd('/')
cmo.destroyMachine(getMBean('/Machines/%s' % machine_data['name']))

print 'DELETING SERVER: %s' % servers_data['name']
cd('/')
if servers_data['name'] != 'AdminServer':
    cd('/Servers/%s' % servers_data['name'])
    cmo.setCluster(None)
    cmo.setMachine(None)
    editService.getConfigurationManager().removeReferencesToBean(getMBean('/Servers/%s' % servers_data['name']))
    cd('/')
    cmo.destroyServer(getMBean('/Servers/%s' % servers_data['name']))

save()
activate(block="true")
disconnect()
exit()
