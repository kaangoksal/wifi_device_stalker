
**Wifi Stalker**

This project aims to raise awareness about how easily we can be traced in physical world. This is possible
thanks to wifi communications and our addiction to being connected. All of us have mobile phones, laptops, 
cars that are connected to wifi.  Even though our communication seems to be secure, our devices can be identified by 
the bystanders in vicinity. If your MAC address is captured by someone who is interested in you, she can walk around and 
sniff wifi packets looking for your MAC address, if she finds a packet, she would know that you are nearby without even
seeing you. This method can be used in so many different ways, and as I know it is used for advertisement purposes at the moment.
This project only aims to sniff wifi, in the future I will also implement a GSM version, I believe
GSM will have more range and will be more reliable since we never tend to put our mobile phones in airplane mode. After 
some research, I discovered that it is not simple to do this with GSM due to the fact that packets are encrypted in a way
that 3rd parties cant read number data without acting as a fake cell tower which is illegal for citizens to do so. Damn..


At the moment the project is in draft stage, I implemented a basic way of sniffing wifi packets with an of the shelf
wifi dongle, it filters the clients and access points and prints them to the console. In near future I will implement
SQLite Database to keep track of the access points and the clients that I see, I will also add an option to label certain
clients as people of interest. I will receive notifications if a person of interest is in vicinity. I'm planning to run
this on a raspberry pi zero all day. I would love to have this on android, however compiling aircrack drivers for different
chipsets of Android is a nightmare that I would not like to do for free. Therefore I'm planning to use bluetooth to
communicate with the android device through that. The android device will be used for UI and the 
raspberry pi will be the sensor suite. 

This project is still in progress... 

This is probably how will it look like:

![Alt text](https://github.com/kaangoksal/wifi_device_stalker/blob/master/media/Dashboard.png)


Live view page

![Alt text](https://github.com/kaangoksal/wifi_device_stalker/blob/master/media/Live%20View.png)

**Up Coming Features**

- SQLite Database
- Signal Strength
- Android Application
- 5GHZ compability (find a usb dongle that supports monitor mode)
- Some kind of ui


**Requirements**  

`sudo apt-get install python3-pip, git, tcpdump python3-crypto ipython3`


Scappy Installation  
`cd /tmp`  
`git clone https://github.com/phaethon/scapy`  
`cd scapy`  
`sudo python3 setup.py install`  

Sources: 
https://github.com/DanMcInerney/wifijammer/blob/master/wifijammer.py
