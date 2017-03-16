#!/usr/bin/python
from ambariclient.client import Ambari
client = Ambari('sbathe-node-1.openstacklocal', port=8080, username='admin', password='admin')

aclusters = []
services = []
components = []
cnames = []
host_group_template = open('/home/sbathe/group-template.conf').read()

def create_group_conf(component, outfile):
  conf = host_group_template.replace('COMPONENT',component)
  ofdata = open(outfile).read()
  if ofdata.find(component) < 0:
    ofdata = ofdata + conf
  open(outfile,'w').write(ofdata)

for c in client.clusters:
#    aclusters.append(c)
#    cnames.append(c.cluster_name)
    cluster_host_group_file = '/home/sbathe/clusters.conf'
    create_group_conf(c.cluster_name, cluster_host_group_file)
    service_list = c.services.to_dict()
    for s in service_list:
      create_group_conf(s['service_name'], cluster_host_group_file)
    for s in client.clusters(c.cluster_name).services:
        for cp in client.clusters(c.cluster_name).services(s.service_name).components:
          create_group_conf(cp.component_name,cluster_host_group_file)

"""
for c in client.clusters:
    for s in client.clusters(c.cluster_name).services:
        for cp in client.clusters(c.cluster_name).services(s.service_name).components:
            print cp.component_name
"""
