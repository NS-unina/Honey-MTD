Ordine di configurazione:

Prerequisiti: 
openvswitch
vagrant
virtualbox
docker, docker compose

PER IL SETUP DELLA TOPOLOGIA

1. Eseguire lo script create_net.sh (SOLO AL PRIMO SETUP)
2. Eseguire lo script setup.sh (controlla impostazioni interfaccia di rete per connessione ad internet delle macchine collegate all ovs) (SEMPRE)
3. Nella cartella /vagrant/ubuntu eseguire "vagrant up" (SOLO AL PRIMO SETUP)
5. Nella cartella /docker/docker-build eseguire "docker compose up" (SEMPRE)
6. Nella cartella /docker eseguire lo script setup_container.sh (SEMPRE)
7. Nella default dir eseguire lo script temp_restoring.sh (SEMPRE, SOLO DOPO AVER CONFIGURATO TUTTE LE MACCHINE)

8. Nel container controller scaricare il codice del controller (rest_controller in SkyTrap-MTD) e aggiornare il file topology.py in funzione dei parametri caratterizzanti la
topologia appena settata. Rispetto al codice dovrebbero cambiare i mac address delle vm e i dpid degli ovs.

NON ESEGUIRE reset.sh A MENO CHE NON SI VOGLIA PULIRE COMPLETAMENTE IL DISPOSITIVO
QUESTA COSA NON CONVIENE IN QUANTO ALLA CREAZIONE DI DUE NUOVI OVS, CAMBIA IL LORO
dpid CHE DEVE ESSERE SETTATO MANUALMENTE NEL CONTROLLER.
