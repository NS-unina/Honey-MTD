# SkyTrap-MTD

## Prequirements     
You need to install *python 3.9* in order to use mininet. 
If you have ubuntu 22.04, the official version is 3.10.  
You can install an alternative python version by using the following guide: 
https://towardsdatascience.com/installing-multiple-alternative-versions-of-python-on-ubuntu-20-04-237be5177474

1. Install mininet: 
``` 
pip install mininet  
sudo apt-get install mininet
``` 

2. Install ryu  
```  
pip install ryu 
```    

Run the ryu controller:  
```  
ryu-manager <controller.py> 
```   

Run the mininet environment that uses ryu
```  
python <mininet_env>
``` 
## Troubleshooting   
If you have the following error: 
```  
cannot import name 'ALREADY_HANDLED' from 'eventlet.wsgi'  
```   
You should downgrade the `eventlet` version:
```  
pip install eventlet==0.30.2
``` 