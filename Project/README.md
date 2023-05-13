# A Software Defined approach to Moving Target Defense in the Internet - M.Sc. Thesis

## Prequirements     
In order to execute the project on your machine
you need to install *Open vSwitch*, *Vagrant*, *Virtualbox*, *Docker* and *Docker Compose*.

The following steps allow project running on a Linux *(Ubuntu 20.04)* machine.

In **topology** folder: 
1. Execute the script *create_net.sh*.
2. Execute the script *setup.sh*.

Virtual Machines creation and configuration:
3. In **vagrant/ubuntu** folder run *vagrant up*.
3. VM username = *vagrant*. VM password = *vagrant*.
3. Enter in *ext_heralding* VM and execute the script *start.sh* in **root** directory.

Containers building and setup:
4. In **docker/docker-build** folder run *docker compose up*.
5. In **docker** folder execute the script *setup_container.sh*.
5. In each container go into the **/home** directory and execute the script *conf.sh*.

Start Ryu Controller
6. In *controller* Container, enter in **/home/rest_controller** directory and run the following command:
```  
ryu-manager rest_controller.py
```

Launch Elastalert
7. In *ELK* Virtual Machine, enter in **/elastalert** directory and run:
```  
python3 -m elastalert.elastalert --verbose
```

Now it is possible to proceed with **Attack Scenarios** demonstrations.

**PROJECT RESET**
1. In **/docker/docker-build** run *docker compose down*.
2. In **/vagrant/ubuntu** run *vagrant destroy*.
3. In **topology** execute the script *reset.sh*.