#!/usr/bin/python
from ambariclient.client import Ambari
from jinja2 import Template
import argparse, json
import socket
parser = argparse.ArgumentParser()
parser.add_argument("-v", action="store_true", default=False, dest='verbose', help="increase output verbosity")
parser.add_argument("-H", action="store", dest='host', help="Ambari host to contact", required=True)
parser.add_argument("-P", action="store", dest='port', help="increase output verbosity",required=True)
parser.add_argument("-u", action="store", dest='user_name', help="Ambari username ",required=True)
parser.add_argument("-p", action="store", dest='password', help="Ambari user password",required=True )
args = parser.parse_args()

client = Ambari(args.host, port=args.port, username=args.user_name,
                password=args.password)

aclusters = []
services = []
components = []
cnames = []

host_template = open('ambari-host-template.conf.j2').read() # "NAME", "ADDRESS",
#                           USER, PASSWORD, PORT, SERVICES, CLUSTER
service_template = open('ambari-service-template.conf').read() # "SERVICE"

def create_group_conf(component, outfile):
  conf = host_group_template.replace('COMPONENT',component)
  ofdata = open(outfile).read()
  if ofdata.find(component) < 0:
    ofdata = ofdata + conf
  open(outfile,'w').write(ofdata)

def create_service_command(service, outfile):
    conf = service_template.replace('SERVICE',service.lower())
    try:
      ofdata = open(outfile).read()
    except:
        ofdata = ''
    if ofdata.find(service) < 0:
      ofdata = ofdata + conf
    open(outfile,'w+').write(ofdata)

"""
A host needs: "NAME", "ADDRESS", USER, PASSWORD, PORT, SERVICES, CLUSTER
We will pass on all those as list:
[ hostname, user, password, port, [list of services], cluster ]
"""
def create_host_template(array):
    hostname, address, user, password, port, services, cluster = array
    address = socket.gethostbyname_ex(hostname)[2][0]
    t = Template(host_template)
    outtext = t.render(hostname=hostname,address=address, user=user,password=password,port=port,services=str(json.dumps(services)),cluster=cluster)
    outfile = hostname + '.conf'
    open(outfile,'w').write(outtext)

address = socket.gethostbyname_ex(args.host)[2][0]
for c in client.clusters:
#    aclusters.append(c)
#    cnames.append(c.cluster_name)
    cluster = c.cluster_name
    cluster_host_group_file = 'clusters.conf'
    service_checkcommand_file = 'ambari-services.conf'
    service_list = c.services.to_dict()
    services_list = []
    for s in service_list:
      services_list.append(str(s['service_name']) )

    create_host_template([args.host, address, args.user_name, args.password,
                         args.port, services_list, cluster ])
    for s in service_list:
      #create_group_conf(s['service_name'], cluster_host_group_file)
      create_service_command(s['service_name'],service_checkcommand_file)
    #for s in client.clusters(c.cluster_name).services:
    #    for cp in client.clusters(c.cluster_name).services(s.service_name).components:
    #      create_group_conf(cp.component_name,cluster_host_group_file)

"""
for c in client.clusters:
    for s in client.clusters(c.cluster_name).services:
        for cp in client.clusters(c.cluster_name).services(s.service_name).components:
            print cp.component_name
"""
