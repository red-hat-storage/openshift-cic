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
import random

# regular expression to validate FQDN or IP based on RFCs
ocp_version = '3.9'

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

print (60 * '-')
print ("   CNS - Inventory File Creator")
print (60 * '-')
print "'\033[91m' \r\nThis tool is very highly version dependent. It is currently,"
print "configured to work with OpenShift 3.9 and CNS 3.9."
print "The output is NOT A COMPLETE Inventory File."
print "Created Inventory file options should be copied and pasted into" 
print "the larger openshift-ansible inventory file for your deployment.\r\n '\033[0m'"
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

        if avail_hosts >= 4:
                
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?:  ").split(" ")
                host_not_valid() 
                raw_devices = raw_input("What are the raw storage devices for these hosts (/dev/<device>) ?: ").split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version 
                print "  " 

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=registry.access.redhat.com/rhgs3/rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version
                print "  "

                print "# Container image to use for glusterblock-provisioner pod"
                print "openshift_storage_glusterfs_block_image=registry.access.redhat.com/rhgs3/rhgs-gluster-block-prov-rhel7"
                print "openshift_storage_glusterfs_block_version=v%s" % ocp_version
                print "  "
                print "# Container image to use for heketi pods"
                print "openshift_storage_glusterfs_heketi_image=registry.access.redhat.com/rhgs3/rhgs-volmanager-rhel7"
                print "openshift_storage_glusterfs_heketi_version=v%s" % ocp_version           
                print "    "
                print "[OSEv3:children]"
                print "glusterfs"
                print "   "

                print "# registry"
                print "openshift_hosted_registry_storage_kind=glusterfs"
                print "openshift_hosted_registry_storage_volume_size=%d" % registry_pvsize+"Gi"
                print "openshift_hosted_registry_selector=\"region=infra\"" 
                print "   "

                print "# CNS storage cluster"
                print "openshift_storage_glusterfs_namespace=app-storage"
                print "openshift_storage_glusterfs_storageclass=true"
                print "openshift_storage_glusterfs_storageclass_default=false"
                print "openshift_storage_glusterfs_block_deploy=false"
                print "   "

                print "[glusterfs]"
                for app_host in app_hosts:
                        print app_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(raw_devices) + "'"

        else :
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?:  ").split(" ")
                host_not_valid() 
                raw_devices = raw_input("What are the raw storage devices for these hosts (/dev/<device>) ?: ").split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version 
                print "  " 

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=registry.access.redhat.com/rhgs3/rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version
                print "  "

                print "# Container image to use for glusterblock-provisioner pod"
                print "openshift_storage_glusterfs_block_image=registry.access.redhat.com/rhgs3/rhgs-gluster-block-prov-rhel7"
                print "openshift_storage_glusterfs_block_version=v%s" % ocp_version
                print "  "
                print "# Container image to use for heketi pods"
                print "openshift_storage_glusterfs_heketi_image=registry.access.redhat.com/rhgs3/rhgs-volmanager-rhel7"
                print "openshift_storage_glusterfs_heketi_version=v%s" % ocp_version           
                print "    "

                print "    "
                print "[OSEv3:children]"
                print "glusterfs"
                print "   "

                print "# registry"
                print "openshift_hosted_registry_storage_kind=glusterfs"
                print "openshift_hosted_registry_storage_volume_size=%d" % registry_pvsize+"Gi"
                print "openshift_hosted_registry_selector=\"region=infra\"" 
                print "   "

                print "# CNS storage cluster"
                print "openshift_storage_glusterfs_namespace=app-storage"
                print "openshift_storage_glusterfs_storageclass=true"
                print "openshift_storage_glusterfs_storageclass_default=false"
                print "openshift_storage_glusterfs_block_deploy=false"
                print "   "
                print "[glusterfs]"
                for app_host in app_hosts:
                        print app_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(raw_devices) + "'"
                
elif choice == 2:
        print (60 * '-')
        print ("For this configuration 7 nodes are recommended")
        print ("With a minimum of 3 required ")
        print (60 * '-' )
        avail_hosts = int(raw_input("How many nodes are available ?:  "))

        if avail_hosts >= 6:
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").split(" ")
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_log = int(raw_input("How many replicas for logging ?: "))
                logging_pvsize = int(raw_input("What is the size for each logging persistent volume (GB) ?: "))
                log_hosts =  raw_input("What hosts will be used for CNS logging backend storage  (IP/FQDN) ?:  ").split(" ") 
                host_in_use()
                log_devices = raw_input("What are the raw storage devices for logging backend on these hosts (/dev/<device>) ?: ").split(" ")
                log_storage_size = int(raw_input("What is the size of each raw storage device (GB) ? : "))
                
                
                min_block_host_vol_size =  (logging_pvsize * replica_log) 
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version 
                print "  " 

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=registry.access.redhat.com/rhgs3/rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version
                print "  "

                print "# Container image to use for glusterblock-provisioner pod"
                print "openshift_storage_glusterfs_block_image=registry.access.redhat.com/rhgs3/rhgs-gluster-block-prov-rhel7"
                print "openshift_storage_glusterfs_block_version=v%s" % ocp_version
                print "  "
                print "# Container image to use for heketi pods"
                print "openshift_storage_glusterfs_heketi_image=registry.access.redhat.com/rhgs3/rhgs-volmanager-rhel7"
                print "openshift_storage_glusterfs_heketi_version=v%s" % ocp_version           
                print "    "

                print "   " 
                print "[OSEv3:children]"
                print "glusterfs"
                print "glusterfs_registry"
                print "  "

                print "# registry"
                print "openshift_hosted_registry_storage_kind=glusterfs"
                print "openshift_hosted_registry_storage_volume_size=%d" % registry_pvsize+"Gi"
                print "openshift_hosted_registry_selector=\"region=infra\"" 
                print "   "
        
                print "# logging"
                print "openshift_logging_install_logging=true"
                print "openshift_logging_es_pvc_dynamic=true "
                print "openshift_logging_es_pvc_size=%d" % logging_pvsize+"Gi"
                print "openshift_logging_es_cluster_size=%d" % replica_log
                print "openshift_logging_es_pvc_storage_class_name='glusterfs-registry-block'"
                print "openshift_logging_kibana_nodeselector={\"region\":\"infra\"}"
                print "openshift_logging_curator_nodeselector={\"region\":\"infra\"}"
                print "openshift_logging_es_nodeselector={\"region\":\"infra\"}"
                print "  "  
        
                print "# CNS storage cluster for applications"
                print "openshift_storage_glusterfs_namespace=app-storage"
                print "openshift_storage_glusterfs_storageclass=true"
                print "openshift_storage_glusterfs_storageclass_default=false"
                print "   "

                print "# CNS storage for OpenShift infrastructure"
                print "openshift_storage_glusterfs_registry_namespace=infra-storage"
                print "openshift_storage_glusterfs_registry_storageclass=false"
                print "openshift_storage_glusterfs_registry_block_deploy=true"
                print "openshift_storage_glusterfs_registry_block_host_vol_create=true"
                print "openshift_storage_glusterfs_registry_block_host_vol_size=%d" % block_host_size
                print "openshift_storage_glusterfs_registry_block_storageclass=true"
                print "openshift_storage_glusterfs_registry_block_storageclass_default=false"
                print "   "
                
                print "[glusterfs]"
                for app_host in app_hosts:
                        print app_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(raw_devices) + "'"
                print " "

                print "[glusterfs_registry]"
                for log_host in log_hosts:
                        print log_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(log_devices) + "'"
                print "  "
        else:
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").split(" ")
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_log = int(raw_input("How many replicas for logging ?: "))
                logging_pvsize = int(raw_input("What is the size for each logging persistent volume (GB) ?: "))

                min_block_host_vol_size =  (logging_pvsize * replica_log) 
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)


                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version 
                print "  " 

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=registry.access.redhat.com/rhgs3/rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version
                print "  "

                print "# Container image to use for glusterblock-provisioner pod"
                print "openshift_storage_glusterfs_block_image=registry.access.redhat.com/rhgs3/rhgs-gluster-block-prov-rhel7"
                print "openshift_storage_glusterfs_block_version=v%s" % ocp_version
                print "  "
                print "# Container image to use for heketi pods"
                print "openshift_storage_glusterfs_heketi_image=registry.access.redhat.com/rhgs3/rhgs-volmanager-rhel7"
                print "openshift_storage_glusterfs_heketi_version=v%s" % ocp_version           
                print "    "

                print "    "
                print "[OSEv3:children]"
                print "glusterfs"
                print "   "


                print "# registry"
                print "openshift_hosted_registry_storage_kind=glusterfs"
                print "openshift_hosted_registry_storage_volume_size=%d" % registry_pvsize+"Gi"
                print "openshift_hosted_registry_selector=\"region=infra\"" 
                print "   "
        
                print "# logging"
                print "openshift_logging_install_logging=true"
                print "openshift_logging_es_pvc_dynamic=true "
                print "openshift_logging_es_pvc_size=%d" % logging_pvsize+"Gi"
                print "openshift_logging_es_cluster_size=%d" % replica_log
                print "openshift_logging_es_pvc_storage_class_name='glusterfs-storage-block'"
                print "openshift_logging_kibana_nodeselector={\"region\":\"infra\"}"
                print "openshift_logging_curator_nodeselector={\"region\":\"infra\"}"
                print "openshift_logging_es_nodeselector={\"region\":\"infra\"}"
                print "  "  
        
                print "# CNS storage cluster for applications"
                print "openshift_storage_glusterfs_namespace=app-storage"
                print "openshift_storage_glusterfs_storageclass=true"
                print "openshift_storage_glusterfs_storageclass_default=false"
                print "openshift_storage_glusterfs_block_deploy=true"
                print "openshift_storage_glusterfs_block_host_vol_create=true"
                print "openshift_storage_glusterfs_block_host_vol_size=%d" % block_host_size
                print "openshift_storage_glusterfs_block_storageclass=true"
                print "openshift_storage_glusterfs_block_storageclass_default=false"
                print "   "
                          
                print "[glusterfs]"
                for app_host in app_hosts:
                        print app_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(raw_devices) + "'"


elif choice == 3:
        print (60 * '-')
        print ("For this configuration 7 nodes are recommended")
        print ("With a minimum of 3 required ")
        print (60 * '-' )
        avail_hosts = int(raw_input("How many nodes are available ?:  "))

        if avail_hosts >= 7:
                          
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").split(" ")
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_metrics = 1
                metrics_pvsize = int(raw_input("What is the size for each metrics persistent volume (GB) ?: "))
                met_hosts =  raw_input("What hosts will be used for CNS metrics backend storage  (IP/FQDN) ?:  ").split(" ") 
                met_in_use()
                met_devices = raw_input("What are the raw storage devices for metrics backend on these hosts (/dev/<device>) ?: ").split(" ")
                met_storage_size = int(raw_input("What is the size of each raw storage device (GB) ? : "))
                
                min_block_host_vol_size =  ( metrics_pvsize * replica_metrics) 
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version 
                print "  " 

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=registry.access.redhat.com/rhgs3/rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version
                print "  "

                print "# Container image to use for glusterblock-provisioner pod"
                print "openshift_storage_glusterfs_block_image=registry.access.redhat.com/rhgs3/rhgs-gluster-block-prov-rhel7"
                print "openshift_storage_glusterfs_block_version=v%s" % ocp_version
                print "  "
                print "# Container image to use for heketi pods"
                print "openshift_storage_glusterfs_heketi_image=registry.access.redhat.com/rhgs3/rhgs-volmanager-rhel7"
                print "openshift_storage_glusterfs_heketi_version=v%s" % ocp_version           
                print "    "
                print "  "        
                print "[OSEv3:children]"
                print "glusterfs"
                print "glusterfs_registry"
                print "   " 

                print "# registry"
                print "openshift_hosted_registry_storage_kind=glusterfs"
                print "openshift_hosted_registry_storage_volume_size=%d" % registry_pvsize+"Gi"
                print "openshift_hosted_registry_selector=\"region=infra\"" 
                print "   "
        
                print "# metrics"
                print "openshift_metrics_install_metrics=true "
                print "openshift_metrics_storage_kind=dynamic"
                print "openshift_metrics_storage_volume_size=%d" % metrics_pvsize+"Gi"
                print "openshift_metrics_cassanda_pvc_storage_class_name='glusterfs-registry-block'"
                print "openshift_metrics_hawkular_nodeselector={\"region\":\"infra\"}"
                print "openshift_metrics_cassandra_nodeselector={\"region\":\"infra\"}"
                print "openshift_metrics_heapster_nodeselector={\"region\":\"infra\"}"
                print "   "

                print "# CNS storage cluster"
                print "openshift_storage_glusterfs_namespace=app-storage"
                print "openshift_storage_glusterfs_storageclass=true"
                print "openshift_storage_glusterfs_storageclass_default=false"
                print "  "                

                print "# CNS storage for OpenShift infrastructure"
                print "openshift_storage_glusterfs_registry_namespace=infra-storage"
                print "openshift_storage_glusterfs_registry_storageclass=false"
                print "openshift_storage_glusterfs_registry_block_deploy=true"
                print "openshift_storage_glusterfs_registry_block_host_vol_create=true"
                print "openshift_storage_glusterfs_registry_block_host_vol_size=%d" % block_host_size
                print "openshift_storage_glusterfs_registry_block_storageclass=true"
                print "openshift_storage_glusterfs_registry_block_storageclass_default=false"
                print "   "
                
                print "[glusterfs]"
                for app_host in app_hosts:
                        print app_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(raw_devices) + "'"
                print "  "

                print "[glusterfs_registry]"
                for met_host in met_hosts:
                        print met_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(met_devices) + "'"
                print "  "

        else:
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").split(" ")
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_metrics = 1
                metrics_pvsize = int(raw_input("What is the size for each metrics persistent volume (GB) ?: "))
                
                
                min_block_host_vol_size =  ( metrics_pvsize * replica_metrics) 
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)
              
                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version 
                print "  " 

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=registry.access.redhat.com/rhgs3/rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version
                print "  "

                print "# Container image to use for glusterblock-provisioner pod"
                print "openshift_storage_glusterfs_block_image=registry.access.redhat.com/rhgs3/rhgs-gluster-block-prov-rhel7"
                print "openshift_storage_glusterfs_block_version=v%s" % ocp_version
                print "  "
                print "# Container image to use for heketi pods"
                print "openshift_storage_glusterfs_heketi_image=registry.access.redhat.com/rhgs3/rhgs-volmanager-rhel7"
                print "openshift_storage_glusterfs_heketi_version=v%s" % ocp_version           
                print "    "
            
                print "[OSEv3:children]"
                print "glusterfs"
                print "   " 

                print "# registry"
                print "openshift_hosted_registry_storage_kind=glusterfs"
                print "openshift_hosted_registry_storage_volume_size=%d" % registry_pvsize+"Gi"
                print "openshift_hosted_registry_selector=\"region=infra\"" 
                print "   "
        
                print "# metrics"
                print "openshift_metrics_install_metrics=true "
                print "openshift_metrics_storage_kind=dynamic"
                print "openshift_metrics_storage_volume_size=%d" % metrics_pvsize+"Gi"
                print "openshift_metrics_cassanda_pvc_storage_class_name='glusterfs-storage-block'"
                print "openshift_metrics_hawkular_nodeselector={\"region\":\"infra\"}"
                print "openshift_metrics_cassandra_nodeselector={\"region\":\"infra\"}"
                print "openshift_metrics_heapster_nodeselector={\"region\":\"infra\"}"
                print "   "

                print "# CNS storage cluster"
                print "openshift_storage_glusterfs_namespace=app-storage"
                print "openshift_storage_glusterfs_storageclass=true"
                print "openshift_storage_glusterfs_storageclass_default=false"
                print "openshift_storage_glusterfs_block_deploy=true"
                print "openshift_storage_glusterfs_block_host_vol_create=true"
                print "openshift_storage_glusterfs_block_host_vol_size=%d" % block_host_size
                print "openshift_storage_glusterfs_block_storageclass=true"
                print "openshift_storage_glusterfs_block_storageclass_default=false"
                print "   "
                          
                
                print "[glusterfs]"
                for app_host in app_hosts:
                        print app_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(raw_devices) + "'"
                print " "
                                       
         

elif choice == 4:
        print (60 * '-')
        print ("For this configuration 7 nodes are recommended")
        print ("With a minimum of 3 required ")
        print (60 * '-' )
        avail_hosts = int(raw_input("How many nodes are available ?:  "))

        if avail_hosts >= 6:
                
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").split(" ")
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_log = int(raw_input("How many replicas for logging ?: "))
                logging_pvsize = int(raw_input("What is the size for each logging persistent volume (GB) ?: "))
                replica_metrics = 1
                metrics_pvsize = int(raw_input("What is the size for each metrics persistent volume (GB) ?: "))
                met_log_hosts =  raw_input("What hosts will be used for CNS logging + metrics backend storage  (IP/FQDN) ?:  ").split(" ") 
                both_in_use()
                met_log_devices = raw_input("What are the raw storage devices for logging + metrics backend on these hosts (/dev/<device>) ?: ").split(" ")
                met_log_storage_size = int(raw_input("What is the size of each raw storage device (GB) ? : "))
                
                min_block_host_vol_size =  (logging_pvsize *  replica_log) + (replica_metrics * metrics_pvsize)
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version 
                print "  " 

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=registry.access.redhat.com/rhgs3/rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version
                print "  "

                print "# Container image to use for glusterblock-provisioner pod"
                print "openshift_storage_glusterfs_block_image=registry.access.redhat.com/rhgs3/rhgs-gluster-block-prov-rhel7"
                print "openshift_storage_glusterfs_block_version=v%s" % ocp_version
                print "  "
                print "# Container image to use for heketi pods"
                print "openshift_storage_glusterfs_heketi_image=registry.access.redhat.com/rhgs3/rhgs-volmanager-rhel7"
                print "openshift_storage_glusterfs_heketi_version=v%s" % ocp_version           
                print "    "
                print "  "        
                print "[OSEv3:children]"
                print "glusterfs"
                print "glusterfs_registry"
                print "   " 

                print "# registry"
                print "openshift_hosted_registry_storage_kind=glusterfs"
                print "openshift_hosted_registry_storage_volume_size=%d" % registry_pvsize+"Gi"
                print "openshift_hosted_registry_selector=\"region=infra\"" 
                print "   "

                print "# logging"
                print "openshift_logging_install_logging=true"
                print "openshift_logging_es_pvc_dynamic=true "
                print "openshift_logging_es_pvc_size=%d" % logging_pvsize+"Gi"
                print "openshift_logging_es_cluster_size=%d" % replica_log
                print "openshift_logging_es_pvc_storage_class_name='glusterfs-registry-block'"
                print "openshift_logging_kibana_nodeselector={\"region\":\"infra\"}"
                print "openshift_logging_curator_nodeselector={\"region\":\"infra\"}"
                print "openshift_logging_es_nodeselector={\"region\":\"infra\"}"
                print "  " 
        
                print "# metrics"
                print "openshift_metrics_install_metrics=true "
                print "openshift_metrics_storage_kind=dynamic"
                print "openshift_metrics_storage_volume_size=%d" % metrics_pvsize+"Gi"
                print "openshift_metrics_cassanda_pvc_storage_class_name='glusterfs-registry-block'"
                print "openshift_metrics_hawkular_nodeselector={\"region\":\"infra\"}"
                print "openshift_metrics_cassandra_nodeselector={\"region\":\"infra\"}"
                print "openshift_metrics_heapster_nodeselector={\"region\":\"infra\"}"
                print "   "

                print "# CNS storage cluster"
                print "openshift_storage_glusterfs_namespace=app-storage"
                print "openshift_storage_glusterfs_storageclass=true"
                print "openshift_storage_glusterfs_storageclass_default=false"
                print "  "                

                print "# CNS storage for OpenShift infrastructure"
                print "openshift_storage_glusterfs_registry_namespace=infra-storage"
                print "openshift_storage_glusterfs_registry_storageclass=false"
                print "openshift_storage_glusterfs_registry_block_deploy=true"
                print "openshift_storage_glusterfs_registry_block_host_vol_create=true"
                print "openshift_storage_glusterfs_registry_block_host_vol_size=%d" % block_host_size
                print "openshift_storage_glusterfs_registry_block_storageclass=true"
                print "openshift_storage_glusterfs_registry_block_storageclass_default=false"
                print "   "
                
                print "[glusterfs]"
                for app_host in app_hosts:
                        print app_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(raw_devices) + "'"
                print "  "

                print "[glusterfs_registry]"
                for met_log_host in met_log_hosts:
                        print  met_log_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(met_log_devices) + "'"
                print "   "
     
        else:
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").split(" ")
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
                registry_pvsize = int(raw_input("What is the size for the registry persistent volume (GB)?: "))
                replica_log = int(raw_input("How many replicas for logging ?: "))
                logging_pvsize = int(raw_input("What is the size for each logging persistent volume (GB) ?: "))
                replica_metrics = 1
                metrics_pvsize = int(raw_input("What is the size for each metrics persistent volume (GB) ?: "))
                
                
                min_block_host_vol_size =  (logging_pvsize *  replica_log) + (replica_metrics * metrics_pvsize)
                block_host_size = int ( min_block_host_vol_size + (30/100.0) * min_block_host_vol_size)
             
                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version 
                print "  " 

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=registry.access.redhat.com/rhgs3/rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version
                print "  "

                print "# Container image to use for glusterblock-provisioner pod"
                print "openshift_storage_glusterfs_block_image=registry.access.redhat.com/rhgs3/rhgs-gluster-block-prov-rhel7"
                print "openshift_storage_glusterfs_block_version=v%s" % ocp_version
                print "  "
                print "# Container image to use for heketi pods"
                print "openshift_storage_glusterfs_heketi_image=registry.access.redhat.com/rhgs3/rhgs-volmanager-rhel7"
                print "openshift_storage_glusterfs_heketi_version=v%s" % ocp_version           
                print "    "
                print "  "        
                print "[OSEv3:children]"
                print "glusterfs"
                print "   " 

                print "# registry"
                print "openshift_hosted_registry_storage_kind=glusterfs"
                print "openshift_hosted_registry_storage_volume_size=%d" % registry_pvsize+"Gi"
                print "openshift_hosted_registry_selector=\"region=infra\"" 
                print "   "

                print "# logging"
                print "openshift_logging_install_logging=true"
                print "openshift_logging_es_pvc_dynamic=true "
                print "openshift_logging_es_pvc_size=%d" % logging_pvsize+"Gi"
                print "openshift_logging_es_cluster_size=%d" % replica_log
                print "openshift_logging_es_pvc_storage_class_name='glusterfs-storage-block'"
                print "openshift_logging_kibana_nodeselector={\"region\":\"infra\"}"
                print "openshift_logging_curator_nodeselector={\"region\":\"infra\"}"
                print "openshift_logging_es_nodeselector={\"region\":\"infra\"}"
                print "  " 
        
                print "# metrics"
                print "openshift_metrics_install_metrics=true "
                print "openshift_metrics_storage_kind=dynamic"
                print "openshift_metrics_storage_volume_size=%d" % metrics_pvsize+"Gi"
                print "openshift_metrics_cassanda_pvc_storage_class_name='glusterfs-storage-block'"
                print "openshift_metrics_hawkular_nodeselector={\"region\":\"infra\"}"
                print "openshift_metrics_cassandra_nodeselector={\"region\":\"infra\"}"
                print "openshift_metrics_heapster_nodeselector={\"region\":\"infra\"}"
                print "   "

                print "# CNS storage cluster"
                print "openshift_storage_glusterfs_namespace=app-storage"
                print "openshift_storage_glusterfs_storageclass=true"
                print "openshift_storage_glusterfs_storageclass_default=false"
                print "openshift_storage_glusterfs_block_deploy=true"
                print "openshift_storage_glusterfs_block_host_vol_create=true"
                print "openshift_storage_glusterfs_block_host_vol_size=%d" % block_host_size
                print "openshift_storage_glusterfs_block_storageclass=true"
                print "openshift_storage_glusterfs_block_storageclass_default=false"
                print "   "
                          
                
                print "[glusterfs]"
                for app_host in app_hosts:
                        print app_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(raw_devices) + "'"
                print "   "
                
        
elif choice == 5: 
        print (60 * '-')
        print("For this configuration 4 nodes are recommended ")
        print( "With a minimum of 3 required.")  
        print (60 * '-')
        avail_hosts = int(raw_input("How many nodes are available ?:  "))
        if avail_hosts >= 4:
    
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?: ").split(" ")
                host_not_valid()
                raw_devices = raw_input("What are the raw storage devices these hosts(/dev/<device>) ?: ").split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device(s) ?: "))

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version 
                print "  " 

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=registry.access.redhat.com/rhgs3/rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version
                print "  "

                print "# Container image to use for glusterblock-provisioner pod"
                print "openshift_storage_glusterfs_block_image=registry.access.redhat.com/rhgs3/rhgs-gluster-block-prov-rhel7"
                print "openshift_storage_glusterfs_block_version=v%s" % ocp_version
                print "  "
                print "# Container image to use for heketi pods"
                print "openshift_storage_glusterfs_heketi_image=registry.access.redhat.com/rhgs3/rhgs-volmanager-rhel7"
                print "openshift_storage_glusterfs_heketi_version=v%s" % ocp_version           
                print "    "                
                print "  "
                print "[OSEv3:children]"
                print "glusterfs"
                print "  "

                print "# CNS storage cluster"
                print "openshift_storage_glusterfs_namespace=app-storage"
                print "openshift_storage_glusterfs_storageclass=true"
                print "openshift_storage_glusterfs_storageclass_default=false"
                print "openshift_storage_glusterfs_block_deploy=false"
                print "   "

                print "[glusterfs] "        
                for app_host in app_hosts:
                        print app_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(raw_devices) + "'"


        else:
                app_hosts =  raw_input("What hosts will be used for application storage (IP/FQDN) ?:  ").split(" ")
                host_not_valid() 
                raw_devices = raw_input("What are the raw storage devices for these hosts(/dev/<device>) ?: ").split(" ")
                raw_storage_size = int(raw_input("What is the size of each raw storage device (GB) ?: "))
 
                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version 
                print "  " 

                print "# Container image to use for glusterfs pods"
                print "openshift_storage_glusterfs_image=registry.access.redhat.com/rhgs3/rhgs-server-rhel7"
                print "openshift_storage_glusterfs_version=v%s" % ocp_version
                print "  "

                print "# Container image to use for glusterblock-provisioner pod"
                print "openshift_storage_glusterfs_block_image=registry.access.redhat.com/rhgs3/rhgs-gluster-block-prov-rhel7"
                print "openshift_storage_glusterfs_block_version=v%s" % ocp_version
                print "  "
                print "# Container image to use for heketi pods"
                print "openshift_storage_glusterfs_heketi_image=registry.access.redhat.com/rhgs3/rhgs-volmanager-rhel7"
                print "openshift_storage_glusterfs_heketi_version=v%s" % ocp_version           
                print "    " 
                print "  "
                print "[OSEv3:children]"
                print "glusterfs"
                print "  "

                print "# CNS storage cluster"
                print "openshift_storage_glusterfs_namespace=app-storage"
                print "openshift_storage_glusterfs_storageclass=true"
                print "openshift_storage_glusterfs_storageclass_default=false"
                print "openshift_storage_glusterfs_block_deploy=false"
                print "   "

                print  "[glusterfs]"
                for app_host in app_hosts:
                        print app_host + " glusterfs_zone="+ str(random.randint(1,3)) + " glusterfs_devices=" + "'" + json.dumps(raw_devices) + "'"

      
else:
        print ("Invalid number. Try again...")
