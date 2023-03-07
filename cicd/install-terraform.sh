#!/bin/bash

# fail on any error
set -eu

#from terraform
yum install -y yum-utils shadow-utils
yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
yum -y install terraform

#confirm installation, will fail if terraform fails to install 
terraform --version