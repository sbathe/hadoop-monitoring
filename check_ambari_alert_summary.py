#!/usr/bin/python
import sys
from ambariclient.client import Ambari
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", action="store_true", default=False, dest='verbose', help="increase output verbosity")
parser.add_argument("-H", action="store", dest='host', help="Ambari host to contact")
parser.add_argument("-P", action="store", dest='port', help="increase output verbosity")
parser.add_argument("-u", action="store", dest='user_name', help="increase output verbosity")
parser.add_argument("-p", action="store", dest='password', help="increase output verbosity")
args = parser.parse_args()

client = Ambari(args.host, port=args.port, username=args.user_name, password=args.password)
states = {'OK': 0, 'WARNING':1, 'CRITICAL':2, 'UNKNOWN':3 }

for c in client.clusters:
  alerts = c.alerts().to_dict() 
  OK = []
  WARNING = [] 
  UNKNOWN = []
  CRITICAL = []
  MAINTENANCE = []
  for a in alerts:
    if a['state'] == 'OK':
      OK.append((a['cluster_name'], a['service_name'], a['component_name'], a['definition_name'], a['text']))
    elif a['state'] == 'UNKNOWN':
      UNKNOWN.append((a['cluster_name'], a['service_name'], a['component_name'],a['definition_name'], a['text']))
    elif a['state'] == 'WARNING':
      WARNING.append((a['cluster_name'], a['service_name'], a['component_name'],a['definition_name'], a['text']))
    elif a['state'] == 'CRITICAL':
      CRITICAL.append((a['cluster_name'], a['service_name'], a['component_name'],a['definition_name'], a['text']))
    elif a['state'] == 'MAINTENANCE':
      MAINTENANCE.append((a['cluster_name'], a['service_name'], a['component_name'],a['definition_name'], a['text']))
#WARNING: Ambari alerts: CRITICAL=0, WARNING=1, UNKNOWN=1, OK=95, MAINTENANCE=4 | 'CRITICAL'=0 'WARNING'=1 'UNKNOWN'=1 'OK'=95 'MAINTENANCE'=4
if len(CRITICAL) > 0:
  state = 'CRITICAL'
elif len(WARNING) > 0:
  state = 'WARNING'
elif len(UNKNOWN) > 0:
  state = 'UNKNOWN'
else:
  state = 'OK'

alert_summary = "{0}: Ambari alerts: OK={1}, WARNING={2}, CRITICAL={3}, UNKNOWN={4}, MAINTENANCE={5} | 'OK'={1} ''WARNING'={2} 'CRITICAL'={3} 'UNKNOWN'={4} 'MAINTENANCE'={5}".format(state, len(OK), len(WARNING), len(CRITICAL), len(UNKNOWN), len(MAINTENANCE))

verbose_summary = alert_summary + "\n Services in state"

if args.verbose:
  if state == 'OK':
    print "{0} {1}: {2}".format(verbose_summary,state, OK) 
  if state == 'CRITICAL':
    print "{0} {1}: {2}".format(verbose_summary,state,CRITICAL) 
  if state == 'WARNING':
    print "{0} {1}: {2}".format(verbose_summary,state, WARNING) 
  if state == 'UNKNOWN':
    print "{0} {1}: {2}".format(verbose_summary,state,UNKNOWN) 
else:
  print alert_summary
sys.exit(states[state])



