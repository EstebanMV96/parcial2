#Install Jenkins

## On the CI server machine

Install a virtualbox machine with CentOS 6.7

Enable network interfaces at boot (nat, bridge)

Update server date 

```sh
yum install ntp ntpdate ntp-doc
chkconfig ntpd on
ntpdate pool.ntp.org
/etc/init.d/ntpd start
```

***(Optional)*** You can configure additional parameters for ntd in the configuration file

```sh
vi /etc/ntp.conf
```

Install the needed dependencies

```sh
yum install java-1.7.0-openjdk
yum install wget -y
yum install git -y
sudo wget -O /etc/yum.repos.d/jenkins.repo http://pkg.jenkins-ci.org/redhat/jenkins.repo
sudo rpm --import https://jenkins-ci.org/redhat/jenkins-ci.org.key
sudo yum install jenkins
```

Enable jenkins at boot, start service, and open 8080 port

```sh
chkconfig jenkins on
service jenkins start
iptables -I INPUT 5 -p tcp -m state --state NEW -m tcp --dport 8080 -j ACCEPT
service iptables save
```

***(Optional)*** You can open a port editting the iptables configuration file. Save file changes with **esc, :x**

```sh
vi /etc/sysconfig/iptables
-A INPUT -m state --state NEW -m tcp -p tcp --dport 8080 -j ACCEPT
service iptables restart
```

Install Python package manager and virtualenv package

```sh
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip install virtualenv
```

Give user jenkins temporary permissions to use a console while preparing the virtualenvironment for the project. Save file changes with **esc, :x**

```sh
vi /etc/passwd
change for user jenkins /bin/false with /bin/bash
```

Create a virtual environment for the project

```sh
su jenkins
mkdir /var/lib/jenkins/.virtualenvs
cd /var/lib/jenkins/.virtualenvs
virtualenv testproject
. testproject/bin/activate
```

***(Optional)*** You can specify the Python version for using in the environment
```sh
virtualenv -p /usr/bin/python3.0 <path/to/new/virtualenv/>
```

Install requirements for the project in the virtualenv

```sh
pip install xmlrunner
pip install unittest2
pip install pytest
pip install pytest-cov
pip install flask
```

Export dependencies for the project. You must have your virtual environment activated. In a project, you must provide the requeriments file to your developing team

```sh
pip freeze > requirements.txt
```

## Configure Jenkins through website

Get the ip address of the server and open it in a browser

http://192.168.56.101:8080

If jenkins stuck on the loading screen, go into the server console and restart jenkins service. Follow
the wizard configurations. Select the suggested plugins option, also install github plugin, cobertura plugin, html publisher plugin. You can install more plugins later (manage jenkins -> manage plugins)

Create a free-style project with the name **testproject**. Use the configurations as show in the graphics below

![][1]

If the installation was correct, you can see jenkins reports

![][2]

![][3]

If you also want to show coberture tests use the following configuration

![][4]

## On the Developer machine

If you wish to make changes to the project, you have to fork the repository and configure the jenkins project according to
your specifications. Also if you want to configure a developer environment follow the intructions above.

Install the needed dependencies

```sh
yum install git -y
```

Install Python package manager and virtualenv package

```sh
wget https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip install virtualenv
```

Create a user and a folder for your projects

```sh
adduser developer
passwd developer
su developer
mkdir ~/projects
mkdir ~/virtualenvs
```

Create the environment for the project, activate it and install requeriments

```sh
cd ~/virtualenvs
virtualenv testproject
. testproject/bin/activate
```

Get the requirements file from your devops engineer, and install dependencies on the testproject virtual environment

```sh
pip install -r requirements
```

Clone files from the test repository (In this case I am using my own repository)

```sh
cd ~/projects
git clone https://github.com/d4n13lbc/testproject.git
cd ~/projects/testproject
```

Run test from the terminal with pytest
```sh
py.test
```

Run coberture test from the terminal

```sh
py.test --cov-report term --cov=../testproject
```

There is a file in the sources called run_tests.sh. Check permissions for this file.

```sh
$ git ls-files --stage
$ git ls-tree HEAD
```

It is important that this file has execution permissions due to when this file is clone by jenkins, it needs 
to be execute in the CI server. If you find that run_tests.sh does not have execution permissions you can set the appropiated permissions using the following command

```sh
$ git update-index --chmod=+x run_tests.sh
```
## Links and References
https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+on+Red+Hat+distributions#InstallingJenkinsonRedHatdistributions-ImportantNoteonCentOSJava <br/>
https://www.youtube.com/watch?v=iGtM_OP01FU <br/>
https://github.com/rgeoghegan/pystache <br/>
https://pypi.python.org/pypi/pytest-cov <br/>
http://stackoverflow.com/questions/23146253/test-redirection-in-flask-with-python-unittest

[1]: images/jenkins_configuration_icesi.png
[2]: images/jenkins_ok.png
[3]: images/jenkins_console.png
[4]: images/jenkins_configuration_coverage_icesi.png

<!---
#Respuestas
set -e = termina inmediatamente si algun comando produce un error
python -m = permite ejecutar un modulo como script
instalar violations plugin
-->