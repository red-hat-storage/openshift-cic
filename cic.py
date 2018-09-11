#!/usr/bin/env python
#*******************************************************************************
#                                                                              *
#  Copyright (c) 2018 Red Hat, Inc. <http://www.redhat.com>                    *
#                                                                              *
#  This file is licensed to you under the GNU General Public License,          *
#  version 3 (GPLv3), as published by the Free Software Foundation             *
#------------------------------------------------------------------------------*
#                                                                              *
# cic.py: This tool is very highly version dependent.It is currently           *
#         configured to work with OpenShift 3.9 and CNS 3.9.The output is NOT  * 
#         A COMPLETE InventoryFile. Created Inventory file options should be   *
#         copied and pasted into the larger openshift-ansible inventory file   *
#         for your deployment.                                                 *
#                                                                              *     
# Usage:                $ ./cic.py                                             *
#                                                                              *
#*******************************************************************************


import argparse
from argparse import RawTextHelpFormatter
import pprint
import re
import json
import os
from jinja2 import Environment, FileSystemLoader




def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

def host_not_valid():
    for ahosts in app_hosts:
        if  is_valid_hostname(ahosts) == True:
            continue
        else:
            print "\033[91m %s \033[0m is not valid hostname" % ahosts
            exit()

            
def min_hosts():
        if len(app_hosts) < 3:
                print "\033[91m Require a minimum of 3 hosts \033[0m"
                exit() 


def host_in_use():
    for lhosts in log_hosts:
        if is_valid_hostname(lhosts) == True and lhosts not in app_hosts:
            continue
        elif is_valid_hostname(lhosts) == True and lhosts in app_hosts:
            print "Host: \033[91m %s \033[0m is already used for application hosting" % lhosts
            exit()    
        else:
            print "\033[91m %s \033[0m is not valid hostname" % lhosts
            exit()

def met_in_use():
    for hosts in met_hosts:
        if is_valid_hostname(hosts) == True and hosts not in app_hosts:
            continue
        elif is_valid_hostname(hosts) == True and hosts in app_hosts:
            print "Host: \033[91m %s \033[0m is already used for application hosting" % hosts
            exit()    
        else:
            print "\033[91m %s \033[0m is not valid hostname" % hosts
            exit()

def both_in_use():
    for hosts in met_log_hosts:
        if is_valid_hostname(hosts) == True and hosts not in app_hosts:
            continue
        elif is_valid_hostname(hosts) == True and hosts in app_hosts:
            print "Host: \033[91m %s \033[0m is already used for application hosting" % hosts
            exit()    
        else:
            print "\033[91m %s \033[0m is not valid hostname" % hosts
            exit()

def get_template_path():
        script_dir = os.path.dirname(os.path.realpath(__file__))
        template_path = os.path.join(script_dir, 'templates')
        return template_path 

def get_version(prompt):
    while True:
        ver = raw_input(prompt).strip()
        if ver not in ('3.9', '3.10'):
                print "The support versions are 3.9 and 3.10 only "
                exit()
        return ver

ver = get_version('What version of OpenShift Container Platform are you deploying (3.9 or 3.10)?: ')
print "%s" % ver


print (60 * '-')
print ("\033[91m   CIC - Inventory File Creator for CNS3.9 & OCS3.10 \033[0m")
print (60 * '-')


#ver = raw_input('What version of OpenShift Container Platform are you deploying (3.9 or 3.10)?: ').strip()
#print (' ')

print (60 * '-')
print "\033[91m \r\nThe output is NOT A COMPLETE Inventory File."
print "Created Inventory file options should be copied and pasted into" 
print "the larger openshift-ansible inventory file for your deployment.\r\n \033[0m"
print (60 * '-')
print ("1. Storage for Applications + Registry ")
print ("2. Storage for Applications + Logging")
print ("3. Storage for Applications + Metrics ")
print ("4. Storage for Applications + Registry + Logging + Metrics")
print ("5. Storage for Applications Only")
print (60 * '-')

is_valid=0
 
while not is_valid :
        try :
                choice = int ( raw_input('Enter your choice [1-5] : ') )
                is_valid = 1 
        except ValueError, e :
                print ("'%s' is not a valid integer." % e.args[0].split(": ")[1])

if choice == 1:
        print (60 * '-')
        print(" For this configuration 4 nodes are recommended ")
        print( " With a minimum of 3 required.")  
        print (60 * '-')
        avail_hosts = int(raw_input("How many nodes are available ?:  "))

        if avail_hosts >= 3:
                
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?:  ").strip().split(" ")
                min_hosts()
                host_not_valid() 
                raw_devices = raw_input("What are the raw storage devices for these hosts (/dev/<device>) ?: ").strip().split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))


                # Single cluster total storage calculation
                cluster_storage = len(raw_devices) * raw_storage_size * len(app_hosts)
                total_avail_store = cluster_storage / 3.0
      
                print "# Cluster 1"
                print "# Total Storage allocated (GB) = %d" % registry_pvsize
                print "# Total Storage available (GB) = %d" % total_avail_store 
                if registry_pvsize > raw_storage_size:
                        print "\033[91mWarning one or more persistent volumes are"
                        print "larger than the raw storage device size\033[0m"
                        exit()         
 
              
	        if ver in ['3.9', '3.10']:
                        template_file = os.path.join(get_template_path(), ''.join(ver.split('.')), 'appreg.j2')
                
                file_loader = FileSystemLoader(os.path.dirname(template_file))
		env = Environment(loader=file_loader)
		template = env.get_template(os.path.basename(template_file))
		output = template.render(ver=ver,app_hosts=app_hosts,raw_devices=json.dumps(raw_devices), raw_storage_size=raw_storage_size,registry_pvsize=registry_pvsize)
		#Print the output
		print(output)

             
elif choice == 2:
        print (60 * '-')
        print ("For this configuration 7 nodes are recommended")
        print ("With a minimum of 3 required ")
        print (60 * '-' )
        avail_hosts = int(raw_input("How many nodes are available ?:  "))

        if avail_hosts >= 6:

                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").strip().split(" ")
                min_hosts()
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").strip().split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_log = int(raw_input("How many replicas for logging ?: "))
                logging_pvsize = int(raw_input("What is the size for each logging persistent volume (GB) ?: "))
                log_hosts =  raw_input("What hosts will be used for CNS logging backend storage  (IP/FQDN) ?:  ").strip().split(" ") 
                host_in_use()
                log_devices = raw_input("What are the raw storage devices for logging backend on these hosts (/dev/<device>) ?: ").strip().split(" ")
                log_storage_size = int(raw_input("What is the size of each raw storage device (GB) ? : "))
                zone = [1,2,3]
                
                min_block_host_vol_size =  (logging_pvsize * replica_log) 
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)

                # Two cluster total storage calculation
                cluster_storage = len(raw_devices) * raw_storage_size * len(app_hosts)
                # App storage in Replica 3
                total_avail_store = cluster_storage / 3.0
                 # Reg store Replica-3 
                total_reg_store = (log_storage_size * len(log_devices) * len(log_hosts)) / 3.0  

                block_calc = registry_pvsize + block_host_size
                totalalloc = block_calc

                
                print "# Cluster 1"
                print "# Total Storage allocated (GB) = 0"
                print "# Total Storage available (GB) = %d" % total_avail_store
                print "     "
                print "# Cluster 2"
                print "# Total Storage allocated (GB) = %d" % totalalloc
                print "# Total Storage available (GB) = %d" % total_reg_store
                
                if  registry_pvsize > log_storage_size and totalalloc < total_reg_store :
                        print "\033[91mWarning one or more persistent volumes are"
                        print "larger than the raw storage device size\033[0m"
                        print "  "
                        exit()
                
                elif registry_pvsize < log_storage_size and totalalloc > total_reg_store :
                        print "\033[91mWarning your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit()
                    
                elif registry_pvsize > log_storage_size and totalalloc > total_reg_store :
                        print "\033[91mWarning one or more persistent volumes are"
                        print "larger than the raw storage device size"
                        print "  "
                        print "Warning your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit() 

	        if ver in ['3.9', '3.10']:
                        template_file = os.path.join(get_template_path(), ''.join(ver.split('.')), 'applog-multi.j2')
                
                file_loader = FileSystemLoader(os.path.dirname(template_file))
		env = Environment(loader=file_loader)
		template = env.get_template(os.path.basename(template_file))
		output = template.render(ver=ver,app_hosts=app_hosts,raw_devices=json.dumps(raw_devices), raw_storage_size=raw_storage_size, block_host_size=block_host_size,registry_pvsize=registry_pvsize,logging_pvsize=logging_pvsize,replica_log=replica_log,log_hosts=log_hosts,log_devices=log_devices, log_storage_size=log_storage_size )
		#Print the output
		print(output)
        else:
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").strip().split(" ")
                min_hosts()
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").strip().split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_log = int(raw_input("How many replicas for logging ?: "))
                logging_pvsize = int(raw_input("What is the size for each logging persistent volume (GB) ?: "))
                zone = [1,2,3]
                min_block_host_vol_size =  (logging_pvsize * replica_log) 
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)

                # Single cluster total storage calculation
                cluster_storage = len(raw_devices) * raw_storage_size * len(app_hosts)
                total_avail_store = cluster_storage / 3.0
                block_calc = registry_pvsize + block_host_size
                totalcalc = block_calc
      
                print "# Cluster 1"
                print "# Total Storage allocated (GB) = %d" % block_calc
                print "# Total Storage available (GB) = %d" % total_avail_store 

                if block_calc > total_avail_store and registry_pvsize < total_avail_store:
                        print "\033[91mWarning Your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit()

                elif block_calc < total_avail_store and registry_pvsize > total_avail_store:
                        print "\033[91m Warning one or more persistent volumes are"
                        print "larger than the raw storage device size\033[0m"
                        print "  "
                        exit()
                                
                elif block_calc > total_avail_store and registry_pvsize > total_avail_store:
                        print "\033[91mWarning one or more persistent volumes are"
                        print "larger than the raw storage device size"
                        print "  "
                        print "Warning your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit() 

	        if ver in ['3.9', '3.10']:
                        template_file = os.path.join(get_template_path(), ''.join(ver.split('.')), 'applog.j2')
                
                file_loader = FileSystemLoader(os.path.dirname(template_file))
		env = Environment(loader=file_loader)
		template = env.get_template(os.path.basename(template_file))
  
		output = template.render(ver=ver,app_hosts=app_hosts,raw_devices=json.dumps(raw_devices), raw_storage_size=raw_storage_size, block_host_size=block_host_size,registry_pvsize=registry_pvsize,logging_pvsize=logging_pvsize,replica_log=replica_log)
		#Print the output
		print(output)

elif choice == 3:
        print (60 * '-')
        print ("For this configuration 7 nodes are recommended")
        print ("With a minimum of 3 required ")
        print (60 * '-' )
        avail_hosts = int(raw_input("How many nodes are available ?:  "))

        if avail_hosts >= 6:
                          
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").strip().split(" ")
                min_hosts()
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").strip().split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_metrics = 1
                metrics_pvsize = int(raw_input("What is the size for each metrics persistent volume (GB) ?: "))
                met_hosts =  raw_input("What hosts will be used for CNS metrics backend storage  (IP/FQDN) ?:  ").strip().split(" ") 
                met_in_use()
                met_devices = raw_input("What are the raw storage devices for metrics backend on these hosts (/dev/<device>) ?: ").strip().split(" ")
                met_storage_size = int(raw_input("What is the size of each raw storage device (GB) ? : "))
                zone = [1,2,3]

                min_block_host_vol_size =  ( metrics_pvsize * replica_metrics) 
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)
                
                # Two cluster total storage calculation
                cluster_storage = len(raw_devices) * raw_storage_size * len(app_hosts)
                # App storage in Replica 3
                total_avail_store = cluster_storage / 3.0
                 # Reg store Replica-3 
                total_reg_store = (met_storage_size * len(met_devices) * len(met_hosts)) / 3.0  

                block_calc = registry_pvsize + block_host_size
                totalalloc = block_calc

                print "# Cluster 1"
                print "# Total Storage allocated (GB) = 0"
                print "# Total Storage available (GB) = %d" % total_avail_store
                print "   "
                print "# Cluster 2"
                print "# Total Storage allocated (GB) = %d" % totalalloc
                print "# Total Storage available (GB) = %d" % total_reg_store
                
                if  registry_pvsize > met_storage_size and totalalloc < total_reg_store :
                        print "\033[91mWarning one or more persistent volumes are"
                        print "larger than the raw storage device size\033[0m"
                        print "  "
                        exit()
                
                elif registry_pvsize < met_storage_size and totalalloc > total_reg_store :
                        print "\033[91mWarning your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit()
                    
                elif registry_pvsize > met_storage_size and totalalloc > total_reg_store :
                        print "\033[91mWarning one or more persistent volumes are"
                        print "larger than the raw storage device size"
                        print "  "
                        print "Warning your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit() 

	        if ver in ['3.9', '3.10']:
                        template_file = os.path.join(get_template_path(), ''.join(ver.split('.')), 'appmet-multi.j2')
                
                file_loader = FileSystemLoader(os.path.dirname(template_file))
		env = Environment(loader=file_loader)
		template = env.get_template(os.path.basename(template_file)) 
		output = template.render(ver=ver,app_hosts=app_hosts,raw_devices=json.dumps(raw_devices), raw_storage_size=raw_storage_size, block_host_size=block_host_size,registry_pvsize=registry_pvsize,metrics_pvsize=metrics_pvsize,met_hosts=met_hosts,met_devices=met_devices, met_storage_size=met_storage_size )
		#Print the output
		print(output)
#		with open("appmet-multi.txt", "wb") as fh:
#    			fh.write(output)		
               
                  

        else:
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").strip().split(" ")
                min_hosts()
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").strip().split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_metrics = 1
                metrics_pvsize = int(raw_input("What is the size for each metrics persistent volume (GB) ?: "))
                zone = [1,2,3]
                
                min_block_host_vol_size =  ( metrics_pvsize * replica_metrics) 
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)
                # Single cluster total storage calculation
                cluster_storage = len(raw_devices) * raw_storage_size * len(app_hosts)
                total_avail_store = cluster_storage / 3.0
                block_calc = registry_pvsize + block_host_size
                totalcalc = block_calc
      
                print "# Cluster 1"
                print "# Total Storage allocated (GB) = %d" % block_calc
                print "# Total Storage available (GB) = %d" % total_avail_store 

                if block_calc > total_avail_store and registry_pvsize < total_avail_store:
                        print "\033[91mWarning Your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit()

                elif block_calc < total_avail_store and registry_pvsize > total_avail_store:
                        print "\033[91m Warning one or more persistent volumes are"
                        print "larger than the raw storage device size\033[0m"
                        print "  "
                        exit()
                                
                elif block_calc > total_avail_store and registry_pvsize > total_avail_store:
                        print "\033[91mWarning one or more persistent volumes are"
                        print "larger than the raw storage device size"
                        print "  "
                        print "Warning your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit() 

	        if ver in ['3.9', '3.10']:
                        template_file = os.path.join(get_template_path(), ''.join(ver.split('.')), 'appmet.j2')
                
                file_loader = FileSystemLoader(os.path.dirname(template_file))
		env = Environment(loader=file_loader)
		template = env.get_template(os.path.basename(template_file))
		output = template.render(ver=ver,app_hosts=app_hosts,raw_devices=json.dumps(raw_devices), raw_storage_size=raw_storage_size, block_host_size=block_host_size,registry_pvsize=registry_pvsize, metrics_pvsize = metrics_pvsize)
		#Print the output
		print(output)

elif choice == 4:
        print (60 * '-')
        print ("For this configuration 7 nodes are recommended")
        print ("With a minimum of 3 required ")
        print (60 * '-' )
        avail_hosts = int(raw_input("How many nodes are available ?:  "))

        if avail_hosts >= 6:
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").strip().split(" ")
                min_hosts()
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").strip().split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_log = int(raw_input("How many replicas for logging ?: "))
                logging_pvsize = int(raw_input("What is the size for each logging persistent volume (GB) ?: "))
                replica_metrics = 1
                metrics_pvsize = int(raw_input("What is the size for each metrics persistent volume (GB) ?: "))
                met_log_hosts =  raw_input("What hosts will be used for CNS logging + metrics backend storage  (IP/FQDN) ?:  ").strip().split(" ") 
                both_in_use()
                met_log_devices = raw_input("What are the raw storage devices for logging + metrics backend on these hosts (/dev/<device>) ?: ").strip().split(" ")
                met_log_storage_size = int(raw_input("What is the size of each raw storage device (GB) ? : "))
                zone = [1,2,3]

                min_block_host_vol_size =  (logging_pvsize *  replica_log) + (replica_metrics * metrics_pvsize)
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)
                # Two cluster total storage calculation
                cluster_storage = len(raw_devices) * raw_storage_size * len(app_hosts)
                # App storage in Replica 3
                total_avail_store = cluster_storage / 3.0
                 # log metrics store Replica-3 
                total_reg_store = (met_log_storage_size * len(met_log_devices) * len(met_log_hosts)) / 3.0  

                block_calc = registry_pvsize + block_host_size
                totalalloc = block_calc

                
                print "# Cluster 1"
                print "# Total Storage allocated (GB) = 0"
                print "# Total Storage available (GB) = %d" % total_avail_store
                print "   "
                print "# Cluster 2"
                print "# Total Storage allocated (GB) = %d" % totalalloc
                print "# Total Storage available (GB) = %d" % total_reg_store

                if  registry_pvsize > met_log_storage_size and totalalloc < total_reg_store :
                        print "\033[91m Warning one or more persistent volumes are"
                        print "larger than the raw storage device size\033[0m"
                        print "  "
                        exit()
                
                elif registry_pvsize < met_log_storage_size and totalalloc > total_reg_store :
                        print "\033[91mWarning your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit()
                    
                elif registry_pvsize > met_log_storage_size and totalalloc > total_reg_store :
                        print "\033[91mWarning one or more persistent volumes are"
                        print "larger than the raw storage device size"
                        print "  "
                        print "Warning your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit() 

	        if ver in ['3.9', '3.10']:
                        template_file = os.path.join(get_template_path(), ''.join(ver.split('.')), 'applogmet-multi.j2')
                
                file_loader = FileSystemLoader(os.path.dirname(template_file))
		env = Environment(loader=file_loader)
		template = env.get_template(os.path.basename(template_file))
		output = template.render(ver=ver,app_hosts=app_hosts,raw_devices=json.dumps(raw_devices), raw_storage_size=raw_storage_size, block_host_size=block_host_size,registry_pvsize=registry_pvsize,logging_pvsize=logging_pvsize,replica_log=replica_log, met_log_hosts=met_log_hosts, met_log_devices=met_log_devices)
		#Print the output
		print(output)
        else:
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").strip().split(" ")
                min_hosts()
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").strip().split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_log = int(raw_input("How many replicas for logging ?: "))
                logging_pvsize = int(raw_input("What is the size for each logging persistent volume (GB) ?: "))
                replica_metrics = 1
                metrics_pvsize = int(raw_input("What is the size for each metrics persistent volume (GB) ?: "))
                zone = [1,2,3]
                
                min_block_host_vol_size =  (logging_pvsize *  replica_log) + (replica_metrics * metrics_pvsize)
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)


                # Single cluster total storage calculation
                cluster_storage = len(raw_devices) * raw_storage_size * len(app_hosts)
                total_avail_store = cluster_storage / 3.0
                block_calc = registry_pvsize + block_host_size
                totalcalc = block_calc
      
                print "# Cluster 1"
                print "# Total Storage allocated (GB) = %d" % block_calc
                print "# Total Storage available (GB) = %d" % total_avail_store 

                if block_calc > total_avail_store and registry_pvsize < total_avail_store:
                        print "\033[91mWarning Your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit()

                elif block_calc < total_avail_store and registry_pvsize > total_avail_store:
                        print "\033[91m Warning one or more persistent volumes are"
                        print "larger than the raw storage device size\033[0m"
                        print "  "
                        exit()
                                
                elif block_calc > total_avail_store and registry_pvsize > total_avail_store:
                        print "\033[91mWarning one or more persistent volumes are"
                        print "larger than the raw storage device size"
                        print "  "
                        print "Warning your Total Storage available is less "
                        print "than the Total Storage allocated\033[0m"
                        exit() 

		
	        if ver in ['3.9', '3.10']:
                        template_file = os.path.join(get_template_path(), ''.join(ver.split('.')), 'applogmet.j2')
                
                file_loader = FileSystemLoader(os.path.dirname(template_file))
		env = Environment(loader=file_loader)
		template = env.get_template(os.path.basename(template_file))

		output = template.render(ver=ver,app_hosts=app_hosts,raw_devices=json.dumps(raw_devices), raw_storage_size=raw_storage_size, block_host_size=block_host_size,registry_pvsize=registry_pvsize,logging_pvsize=logging_pvsize,replica_log=replica_log)
		#Print the output
		print(output)
        
elif choice == 5: 
        print (60 * '-')
        print("For this configuration 4 nodes are recommended ")
        print( "With a minimum of 3 required.")  
        print (60 * '-')
        avail_hosts = int(raw_input("How many nodes are available ?:  "))
        if avail_hosts >= 3:
    
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").strip().split(" ")
                min_hosts()
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices these hosts(/dev/<device>) ?: ").strip().split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device(s) ?: "))
 
 
                cluster_storage = len(raw_devices) * raw_storage_size * len(app_hosts)
                total_avail_store = cluster_storage / 3.0

                print "# Cluster 1"
                print "# Total Storage allocated (GB) = 0" 
                print "# Total Storage available (GB) = %d" % total_avail_store 
                
	        if ver in ['3.9', '3.10']:
                        template_file = os.path.join(get_template_path(), ''.join(ver.split('.')), 'app.j2')
                
                file_loader = FileSystemLoader(os.path.dirname(template_file))
		env = Environment(loader=file_loader)
		template = env.get_template(os.path.basename(template_file))

		output = template.render(ver=ver,app_hosts=app_hosts,raw_devices=json.dumps(raw_devices), raw_storage_size=raw_storage_size)
		#Print the output
		print(output)
    
else:
        print ("Invalid number. Try again...")

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="Directs the OCP Storage configuration to a file",metavar='PATH',default=None, )
args = parser.parse_args()
                
with open(args.output, 'w') as output_file:
        output_file.write("%s\n" % output)
