#!/usr/bin/python
import urllib2
import os, sys

###########################################

loadProperties('/tmp/weblogic-cloudformation-master/scripts/settings')
public_dns = urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-hostname').read()
instance_id = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read()

machine_data = {'name':'linux.%s' % instance_id, 'address': public_dns, 'machine_type':'UnixMachine'}
servers_data = {'name': 'MS_%s' % instance_id, 'port': 7003, 'port_ssl': 7502, 'address': public_dns}

###########################################

connect('weblogic', admin_pwd, '%s:7001' % admin_ip)
edit()
startEdit()

print 'CREATING MACHINE: %s' % machine_data['name']
ref = getMBean('/Machines/%s' % machine_data['name'])
if ref != None:
    print 'MACHINE %s ALREADY EXISTS' % machine_data['name']
else:
    cd('/')
    create(machine_data['name'], machine_data['machine_type'])
    #cmo.createUnixMachine(machine_data['name'])
    #machine = cmo.createUnixMachine(machine_data['name'])
    #machine.getNodeManager().setNMType('ssl')

ref = getMBean('/Machines/%s/NodeManager' % machine_data['name'])
if ref != None:
    print 'NODE MANAGER %s ALREADY EXISTS' % machine_data['name']
else:
    cd('/Machines/%s' % machine_data['name'])
    create(machine_data['name'], 'NodeManager')

cd('/Machines/%s/NodeManager/%s' % (machine_data['name'],machine_data['name']))
cmo.setListenAddress(machine_data['address'])
#machine.getNodeManager().setListenAddress(machine_data['address'])

print 'CREATING SERVER: %s' % servers_data['name']
ref = getMBean('/Servers/%s' % servers_data['name'])
if ref != None:
    print 'SERVER %s ALREADY EXISTS' % servers_data['name']
else:
    cd('/')
    server = cmo.createServer(servers_data['name'])

cd('/')
cd('/Servers/%s' % servers_data['name'])
cmo.setListenPort(servers_data['port'])
cmo.setListenAddress(servers_data['address'])

print ' ADD MANAGED SERVERS TO MACHINE'
cmo.setMachine(getMBean('/Machines/%s' % machine_data['name'] ))
print ' ADD MANAGED SERVERS TO CLUSTER'
cmo.setCluster(getMBean('/Clusters/%s' % cluster_name))

ref = getMBean('/Servers/%s/SSL/%s' % (servers_data['name'],servers_data['name']))
if ref != None:
    print 'SSL SERVER %s ALREADY EXISTS' % servers_data['name']
else:
    create(servers_data['name'],'SSL')

cd('/Servers/%s/SSL/%s' % (servers_data['name'],servers_data['name']))
cmo.setEnabled(true)
cmo.setListenPort(servers_data['port_ssl'])

save()
activate(block="true")
nmEnroll ('/opt/Oracle/Middleware/user_projects/domains/%s' % domain_name,'/opt/Oracle/Middleware/wlserver_10.3/common/nodemanager')
start(servers_data['name'],'Server',block='false')
disconnect()
exit()
