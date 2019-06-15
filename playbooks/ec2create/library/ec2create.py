#!/usr/bin/python

DOCUMENTATION = '''
---
module: ec2create
short_description: Create an EC2 instance on AWS and install Docker on it.
'''

EXAMPLES = '''
- name: Create an EC2 instance on AWS and install Docker on it. 
  ec2-create:
    register: result

- name: Display debug info
  debug: var=result
'''

#def Apt_or_Yum():
#    import os
#    import platform

#    print('checking distribution')
#    dist = platform.linux_distribution()[0].lower()
#    if (dist == 'ubuntu') or (dist == 'debian'):
#        result = 'apt'
#    else:
#        result = 'yum'
#    return result

#def InstallAp2Apt():
#    import subprocess
#    import apt
#    import sys
#
#    # Install Apache2
#    pkg_name = "apache2"
#
#    cache = apt.cache.Cache()
#    cache.update
#
#    pkg = cache[pkg_name]
#    if pkg.is_installed:
#       return 2 
#    else:
#        pkg.mark_install()
#
#        try:
#            cache.commit()
#            return 0
#        except Exception, arg:
#            return 1 

#def InstallAp2Yum():
#    import yum
 
#    yb=yum.YumBase()
#    yb.setCacheDir()
#    yb.conf.assumeyes = True
#    inst = yb.rpmdb.returnPackages()
#    installed=[x.name for x in inst]
#    packages=['httpd']
#    for package in packages:
#        if package in installed:
#            # Already installed
#            return 2
#        else:
#            # Install Apache2/HTTPD
#            kwarg = {
#                    'name':package
#            }
#            yb.install(**kwarg)
#            yb.resolveDeps()
#            yb.buildTransaction()
#            yb.processTransaction()
#            return 3

def RunModule():

    module = AnsibleModule(argument_spec={})
    #response = {"apache2": "installed"}

#    if Apt_or_Yum() == 'apt':
#        status = InstallAp2Apt()
#    else:
#        status = InstallAp2Yum()

    if status == 0:
        module.exit_json(changed=True, meta={"apache2": "installed via apt"})
    elif status == 2:
        module.exit_json(changed=False, meta={"apache2": "already installed"})
    elif status == 3:
        module.exit_json(changed=True, meta={"apache2": "installed via yum"})
    else:
        module.fail_json(changed=False, meta="Error occured while installing Apache2")


from ansible.module_utils.basic import *

if __name__ == '__main__':
    RunModule()

