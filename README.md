# openshift-cic

# Installation

Across Distributions
--------------------
- Install [pip](https://pip.pypa.io/en/stable/installing/)
	 (Eg. in OSX brew install pip or easy_install pip )
- cd openshift-cic
- pip install -r requirements.txt
- sudo python setup.py install

For RHEL7.5 , Centos or Fedora
------------------------------
- yum install python-jinja2
- sudo python setup.py install
- cic -o <outputfile>

There is also a RPM SPEC file provided, if you like to build an RPM before you install.   

# CNS Inventory file Creator (CIC)

Script which the user runs and then answers a list of questions to create set of inventory_file options to be incorporated into their larger inventory_file for running openshift-ansible playbooks. The goal is to reduce the complexity and error prone nature of needing to know the correct inventory_file options for a particular OCP version. CIC will generate inventory file options for OCP 3.9, OCP 3.10 and OCP 3.11.

Embedded in the answers will be calculations or ‘pre-flight checks’. An example is the minimum size for the block_host_vol_size (GB). The minimum size is equal to all of the blockvolume PVs added up for metrics and logging + 30% overhead which is a good practice for file system overhead. Also, there is a calculation done for the Total available storage compared to the Total allocated storage as well as a check to make sure the size of any Persistent Volume (PV) does not exceed the size of the raw storage devices. Both of these conditions, if violated, will print out a Warning message and the user will need to try again.
```
$ ./cic.py
What version of OpenShift Container Platform are you deploying (3.9, 3.10 or 3.11)?: 3.9
------------------------------------------------------------
   CNS - Inventory File Creator
------------------------------------------------------------
'' 
The output is NOT A COMPLETE Inventory File.
Created Inventory file options should be copied and pasted into
the larger openshift-ansible inventory file for your deployment.
 ''
1. Storage for Applications + Registry 
2. Storage for Applications + Logging
3. Storage for Applications + Metrics 
4. Storage for Applications + Registry + Logging + Metrics
5. Storage for Applications Only
------------------------------------------------------------
Enter your choice [1-5] : 4
------------------------------------------------------------
For this configuration 7 nodes are recommended
With a minimum of 3 required 
------------------------------------------------------------
How many nodes are available ?:  6

What hosts will be used for application storage (IP/FQDN) ?: ip-172-16-17-219.us-west-2.compute.internal ip-172-16-47-113.us-west-2.compute.internal ip-172-16-61-81.us-west-2.compute.internal

What are the raw storage devices for these hosts(/dev/<device>) ?: /dev/xvdf /dev/xvdg

What is the size of each raw storage device (GB) ?: 100

What is the size for the registry persistent volume (GB)?: 10

How many replicas for logging ?: 3

What is the size for each logging persistent volume (GB) ?: 40

What is the size for each metrics persistent volume (GB) ?: 20

What hosts will be used for CNS logging + metrics backend storage  (IP/FQDN) ?:  ip-172-16-17-115.us-west-2.compute.internal ip-172-16-17-68.us-west-2.compute.internal ip-172-16-28-160.us-west-2.compute.internal

What are the raw storage devices for logging + metrics backend on these hosts (/dev/<device>) ?: /dev/xvdf /dev/xvdg

What is the size of each raw storage device (GB) ? : 100

# Cluster 1
# Total Storage allocated (GB) = 0
# Total Storage available (GB) = 200
   
# Cluster 2
# Total Storage allocated (GB) = 192
# Total Storage available (GB) = 200

[OSEv3:children]
glusterfs
glusterfs_registry
   
[OSEv3:vars]
# registry
openshift_hosted_registry_storage_kind=glusterfs
openshift_hosted_registry_storage_volume_size=10Gi
openshift_hosted_registry_selector="region=infra"
   
# logging
openshift_logging_install_logging=true
openshift_logging_es_pvc_dynamic=true 
openshift_logging_es_pvc_size=40Gi
openshift_logging_es_cluster_size=3
openshift_logging_es_pvc_storage_class_name='glusterfs-registry-block'
openshift_logging_kibana_nodeselector={"region":"infra"}
openshift_logging_curator_nodeselector={"region":"infra"}
openshift_logging_es_nodeselector={"region":"infra"}
  
# metrics
openshift_metrics_install_metrics=true 
openshift_metrics_storage_kind=dynamic
openshift_metrics_storage_volume_size=20Gi
openshift_metrics_cassanda_pvc_storage_class_name='glusterfs-registry-block'
openshift_metrics_hawkular_nodeselector={"region":"infra"}
openshift_metrics_cassandra_nodeselector={"region":"infra"}
openshift_metrics_heapster_nodeselector={"region":"infra"}
   
# Container image to use for glusterfs pods
openshift_storage_glusterfs_image=registry.access.redhat.com/rhgs3/rhgs-server-rhel7
openshift_storage_glusterfs_version=v3.9
  
# Container image to use for glusterblock-provisioner pod
openshift_storage_glusterfs_block_image=registry.access.redhat.com/rhgs3/rhgs-gluster-block-prov-rhel7
openshift_storage_glusterfs_block_version=v3.9
  
# Container image to use for heketi pods
openshift_storage_glusterfs_heketi_image=registry.access.redhat.com/rhgs3/rhgs-volmanager-rhel7
openshift_storage_glusterfs_heketi_version=v3.9
    
# CNS storage cluster
openshift_storage_glusterfs_namespace=app-storage
openshift_storage_glusterfs_storageclass=true
openshift_storage_glusterfs_storageclass_default=false
  
# CNS storage for OpenShift infrastructure
openshift_storage_glusterfs_registry_namespace=infra-storage
openshift_storage_glusterfs_registry_storageclass=false
openshift_storage_glusterfs_registry_block_deploy=true
openshift_storage_glusterfs_registry_block_host_vol_create=true
openshift_storage_glusterfs_registry_block_host_vol_size=182
openshift_storage_glusterfs_registry_block_storageclass=true
openshift_storage_glusterfs_registry_block_storageclass_default=false
   
[glusterfs]
ip-172-16-17-219.us-west-2.compute.internal glusterfs_zone=1 glusterfs_devices='["/dev/xvdf", "/dev/xvdg"]'
ip-172-16-47-113.us-west-2.compute.internal glusterfs_zone=2 glusterfs_devices='["/dev/xvdf", "/dev/xvdg"]'
ip-172-16-61-81.us-west-2.compute.internal glusterfs_zone=3 glusterfs_devices='["/dev/xvdf", "/dev/xvdg"]'
  
[glusterfs_registry]
ip-172-16-17-115.us-west-2.compute.internal glusterfs_zone=1 glusterfs_devices='["/dev/xvdf", "/dev/xvdg"]'
ip-172-16-17-68.us-west-2.compute.internal glusterfs_zone=2 glusterfs_devices='["/dev/xvdf", "/dev/xvdg"]'
ip-172-16-28-160.us-west-2.compute.internal glusterfs_zone=3 glusterfs_devices='["/dev/xvdf", "/dev/xvdg"]'

```   
