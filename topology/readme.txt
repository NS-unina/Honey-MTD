Ordine di configurazione:

Prerequisiti: 
openvswitch
vagrant
virtualbox
docker, docker compose


1. Eseguire lo script create_net.sh (da eseguire solo al primo setup)
2. Eseguire lo script setup.sh (controlla impostazioni interfaccia di rete per connessione ad internet delle macchine collegate all ovs) (da eseguire ad ogni accensione)
3. Nella cartella /vagrant/ubuntu eseguire "vagrant up" (solo primo setup)
5. Nella cartella /docker/docker-build eseguire "docker compose up"
6. Nella cartella /docker eseguire lo script setup_container.sh
7. Nella default dir eseguire lo script temp_restoring.sh


