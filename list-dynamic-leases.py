#!/usr/bin/env python3

"""Total Perspective Vortex - List Dynamic Leases

A utility script to list dynamic DHCP leases so that you find dynamic hosts and
migrate them to static IPs.

Copyright (C) 2018 Joey Parrish <joey.parrish@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import datetime
import re
import sys


def parse_dhcp_time(dhcp_time):
  return datetime.datetime.strptime(dhcp_time, '%Y/%m/%d %H:%M:%S')


def parse_leases(lease_file_path, delta=datetime.timedelta(minutes=0)):
  leases = {}
  now = datetime.datetime.utcnow()

  with open(lease_file_path, 'rb') as f:
    new_lease = None

    for line in f:
      line = line.decode('utf-8')

      if re.search('^\s*(?:#.*)?$', line):
        continue

      words = re.split('\s+', line.strip().strip(';'))
      if not new_lease:
        if words[0] == 'lease':
          new_lease = { 'ip': words[1], 'name': None }
      else:
        if words[0] == 'starts':
          new_lease['starts'] = parse_dhcp_time(' '.join(words[2:]))
        elif words[0] == 'ends':
          new_lease['ends'] = parse_dhcp_time(' '.join(words[2:]))
        elif words[0] == 'hardware':
          new_lease['mac'] = words[2]
        elif words[0] == 'client-hostname':
          new_lease['name'] = words[1].strip('"')
        elif new_lease['name'] is None and words[0] == 'set' and words[1] == 'vendor-class-identifier' and words[2] == '=':
          new_lease['name'] = ' '.join(words[3:]).strip('"')
        elif words[0] == '}':
          if new_lease['ends'] < now - delta:
            new_lease = None
            continue

          ip = new_lease['ip']
          old_lease = leases.get(ip, None)
          if old_lease and old_lease['starts'] > new_lease['starts']:
            new_lease = None
            continue

          leases[ip] = new_lease
          new_lease = None

  return leases


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--expired', type=float, default=60,
      help='In addition to current leases, show leases that expired within the given number of minutes in the past.')

  args = parser.parse_args()

  leases = parse_leases('/var/lib/dhcp/dhcpd.leases', delta=datetime.timedelta(minutes=args.expired))

  for lease in leases.values():
    if lease.get('mac'):
      print(lease['ip'], '\t', lease['mac'], '\t', 'until', lease['ends'], '\t', lease['name'])


if __name__ == '__main__':
  main()
