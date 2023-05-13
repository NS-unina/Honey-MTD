Setup Progetto (poi lo scriverò in inglese)

Prerequisiti: 
openvswitch
vagrant
virtualbox
docker, docker compose

ESECUZIONE
1. Eseguire lo script create_net.sh
2. Eseguire lo script setup.sh
3. Nella cartella /vagrant/ubuntu eseguire "vagrant up"
5. Nella cartella /docker/docker-build eseguire "docker compose up"
6. Nella cartella /docker eseguire lo script setup_container.sh
7. In tutti i container che si generano, eseguire lo script "conf.sh" nella directory /home
8. Non so per quale motivo heralding nella TI non si avvia, quindi entrare nella vm ext_heralding e eseguire lo script "./start" (sta nella home)
9. Entrare nella vm elk, e nella folder elastalert eseguire il seguente comando per caricare le regole:
   "python3 -m elastalert.elastalert --verbose"
10. Entrare nel container controller, andare in "/home/rest_controller" ed eseguire il comando: "ryu-manager rest_controller.py" per avviarlo.
11. A questo punto la rete è pronta per poter eseguire le varie demo.


RESET
1. In /docker/docker-build eseguire "docker compose down"
2. In /vagrant/ubuntu eseguire "vagrant destroy"
3. Nella cartella principale eseguire lo script "reset.sh"


