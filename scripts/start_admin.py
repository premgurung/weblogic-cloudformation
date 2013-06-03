#!/usr/bin/python
import urllib2
import os, sys

###########################################

loadProperties('/tmp/weblogic-cloudformation-master/scripts/settings')
public_dns = urllib2.urlopen('http://169.254.169.254/latest/meta-data/public-hostname').read()
instance_id = urllib2.urlopen('http://169.254.169.254/latest/meta-data/instance-id').read()

machine_data = {'name':'linux.%s' % instance_id, 'address': public_dns, 'machine_type':'UnixMachine'}
servers_data = [
    { 'name': 'AdminServer', 'port': 7001, 'port_ssl': 7002, 'address': public_dns, 'is_admin':True},
    { 'name': 'MS_%s' % instance_id, 'port': 7003, 'port_ssl': 7502, 'address': public_dns, 'is_admin':False}
]
domain_type = 'dev'
is_new_domain = False
###########################################

def start_domain(name, status_type):
    # Start Up
    if is_new_domain:
        print('Setting StartUp Options')
        setOption('CreateStartMenu', 'false')
        setOption('DomainName',name)
        setOption('ServerStartMode', status_type)
        setOption('JavaHome','/opt/jrockit-jdk1.6.0_45-R28.2.7-4.1.0')
        setOption('OverwriteDomain', 'true')

        # Create Domain to File System
        print('Writing Domain To File System')
        writeDomain('/opt/Oracle/Middleware/user_projects/domains/%s' % name)
        closeTemplate()

        # Read the Created Domain
        print('Reading the Domain from In Offline Mode')
        readDomain('/opt/Oracle/Middleware/user_projects/domains/%s' % name)

def create_password(pwd):
    try: 
        cd('/')
        cd('Security/base_domain/User/weblogic')
        print 'Creating Password for weblogic user: %s' % pwd
        cmo.setPassword(pwd)
    except:
        print 'PASSWORD ALREADY SET'

def create_machine(parameter):
    
    try: 
        cd('/Machines/%s' % parameter['name'])
        print '===> MACHINE %s ALREADY EXISTS' % parameter['name']
    except:
        print 'CREATING MACHINE: %s' % parameter['name']
        create(parameter['name'],parameter['machine_type'])

    try: 
        cd('/Machines/%s/NodeManager' % parameter['name'])
        print '===> NODE MANAGER FOR %s ALREADY EXISTS' % parameter['name']
    except:
        print 'CREATING NODE MANAGER FOR MACHINE: %s' % parameter['name']
        cd('/Machines/%s' % parameter['name'])
        create(parameter['name'], 'NodeManager')

    cd('/Machines/%s/NodeManager/%s' % (parameter['name'], parameter['name']))
    set('ListenAddress',parameter['address'])

def create_server(parameter, machine):
    try: 
        cd('/Servers/%s' % parameter['name'])
        print '===> SERVER %s ALREADY EXISTS' % parameter['name']
    except:
        print 'CREATING SERVER: %s' % parameter['name']
        if not parameter['is_admin']:
            create(parameter['name'], 'Server')
        cd('/Servers/%s' % parameter['name'])

    
    set('ListenPort', int(parameter['port']))
    set('ListenAddress', parameter['address'])

    try: 
        cd('/Servers/%s/SSL/%s' % (parameter['name'],parameter['name']))
        print '===> SSL SERVER %s ALREADY EXISTS' % parameter['name']
    except:
        print 'CREATING SSL SERVER: %s' % parameter['name']
        create(parameter['name'],'SSL')

    cd('/Servers/%s/SSL/%s' % (parameter['name'],parameter['name']))
    set('Enabled', 'True')
    set('ListenPort', int(parameter['port_ssl']))

    if parameter['is_admin'] and is_new_domain:
        create_password(admin_pwd)
    #else:
    #    assign('Server', parameter['name'],'Machine', machine['name'])

def create_cluster(name, managed_servers):
    try: 
        cd('/Clusters/%s/' % name)
        print '===> CLUSTER %s ALREADY EXISTS' % parameter['name']
    except:
        print 'CREATING CLUSTER: %s' % name
        cd('/')
        create(name, 'Cluster')

    cd('Cluster/%s' % name)
    #set('ClusterAddress', address)
    set('WeblogicPluginEnabled', True)

def assign_all(servers,machine,cluster):
    # assign server to machine
    txt = ''
    cd('/Machines/%s' % machine['name'])
    for info in servers:
        print 'ASSIGN %s TO %s' % (info['name'],machine['name'])
        assign('Server', info['name'],'Machine', machine['name'])
        if info['name'] != 'AdminServer':
            txt += "%s," % info['name']

    # assign server to cluster
    cd('/Cluster/%s' % cluster)   
    print 'ASSIGN %s TO %s' % (txt[0:-1],cluster)
    assign('Server', txt[0:-1],'Cluster',cluster)
        

###########################################

# This is an Offline  WLST script to create a WLS 10.3.1 (Oracle Weblogic Server 11gR1) Domain
#
# Domain consists of:
# 1. Admin Server
# 2. Two Managed Servers
# 3. A Cluster with Two Managed Server

# Read a domain template
try: 
    print 'CHECKING DOMAIN %s' % domain_name
    readDomain('/opt/Oracle/Middleware/user_projects/domains/%s' % domain_name)
except:
    print('READING TEMPLATE - /opt/Oracle/Middleware/wlserver_10.3/common/templates/domains/wls.jar')
    readTemplate('/opt/Oracle/Middleware/wlserver_10.3/common/templates/domains/wls.jar')
    is_new_domain = True

# Creating Machine
create_machine(machine_data)

# Admin Server
create_server(servers_data[0], machine_data)

# Start Up
start_domain(domain_name, domain_type)

# Creating Managed Servers
for info in servers_data:
    if info['name'] != 'AdminServer':
        create_server(info, machine_data)

# Create and configure a cluster and assign the Managed Servers to that cluster.
create_cluster(cluster_name, servers_data)

assign_all(servers_data,machine_data,cluster_name)

# updating the changes
print('Finalizing the changes')
updateDomain()
closeDomain()

# Exiting
print('Exiting...')
exit()
