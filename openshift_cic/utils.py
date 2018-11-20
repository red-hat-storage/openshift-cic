# It contains common functions in order to do validation

import re
import os

from jinja2 import Environment, FileSystemLoader


def check_input(no_of_hosts):
    hosts_found = re.split(r"[,\s?]", no_of_hosts)
    hosts = [host for host in hosts_found if host]
    return hosts


def is_valid_hostname(hostname):
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[
            :-1
        ]  # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))


def host_not_valid(app_hosts):
    for ahosts in app_hosts:
        if is_valid_hostname(ahosts) == True:
            continue
        else:
            print "\033[91m %s \033[0m is not valid hostname" % ahosts
            exit()


def min_hosts(app_hosts):
    if len(app_hosts) < 3:
        print "\033[91m Require a minimum of 3 hosts \033[0m"
        exit()


def host_in_use(log_hosts,app_hosts):
    for lhosts in log_hosts:
        if is_valid_hostname(lhosts) == True and lhosts not in app_hosts:
            continue
        elif is_valid_hostname(lhosts) == True and lhosts in app_hosts:
            print "Host: \033[91m %s \033[0m is already used for application hosting" % lhosts
            exit()
        else:
            print "\033[91m %s \033[0m is not valid hostname" % lhosts
            exit()


def met_in_use(met_hosts,app_hosts):
    for hosts in met_hosts:
        if is_valid_hostname(hosts) == True and hosts not in app_hosts:
            continue
        elif is_valid_hostname(hosts) == True and hosts in app_hosts:
            print "Host: \033[91m %s \033[0m is already used for application hosting" % hosts
            exit()
        else:
            print "\033[91m %s \033[0m is not valid hostname" % hosts
            exit()


def both_in_use(met_log_hosts,app_hosts):
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
    template_path = os.path.join(script_dir, "templates")
    return template_path


def get_template_input(ver, jinjafile):
    if ver in ["3.9", "3.10", "3.11"]:
        template_file = os.path.join(
            get_template_path(), "".join(ver.split(".")), jinjafile
        )
    file_loader = FileSystemLoader(os.path.dirname(template_file))
    env = Environment(loader=file_loader)
    return env.get_template(os.path.basename(template_file))

def get_version(prompt):
    while True:
        ver = raw_input(prompt).strip()
        if ver not in ('3.9', '3.10', '3.11'):
                print "The supported versions are 3.9, 3.10 and 3.11 only "
                exit()
        return ver
