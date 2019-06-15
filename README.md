This is my msningest project. I am modifying the tutorial located here:

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

I am making modifications for it to take user data and input it into a database or json file that will eventually populate an MRSS feed.

The current project contains files to allow the project to run locally as a FLASK application, it can be run as a Docker container, and it can be configured to run on AWS Elastic Beanstalk.

Current goes is to automate the process of creating an AWS EC2 instance and configuring the Docker container to run on it via Ansible Playbook.
