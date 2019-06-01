#!/bin/bash
aws ec2 run-instances --image-id ami-0cb72367e98845d43 --count 1 --instance-type t2.micro \
--region us-west-2 --subnet-id subnet-4dade534 --security-group-ids sg-0ae4e07a \
--key-name aws-eb --user-data file://dockinst.txt
