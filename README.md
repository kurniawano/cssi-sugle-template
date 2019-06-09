# Sugle Network Exercise

## Requirement
To run the whole program, you will need to install [Pyro4](https://pyro4.readthedocs.io/en/stable/) library. To do so, you can use pip. On the terminal type:

```
$ pip install Pyro4
```

See [Pyro4 Installation](https://pyro4.readthedocs.io/en/stable/install.html) for more detail.

## How to Run

### Preparation

- Download the source code from the Github:

```
$ git clone https://github.com/kurniawano/cssi-sugle-working.git
```

- You also need to complete `suglework.py` by writing the code for the methods in the class `SugleAccount`.

### Running on One Computer

After downloading the source code, follow the steps below:

- Open a **new terminal**, and go to the folder you download the source code. For example,

```
$ cd ~/Documents/cssi-python-class-template
```
- And go to the folder you download the source code. You need to set the environment so that the Pyro accepts `pickle` for its object serialization. To do so run the script `setenvserver.sh`. You only need to run this once.

```
$ chmod 755 setenvserver.sh
$ source ./setenvserver.sh
```

- In this terminal, run Pyro4 nameserver.

```
$ chmod 755 runnameserver.sh
$ ./runnameserver.sh &
```


- In the same terminal, run the python file `suglserver.py`. This runs the server with the class `SugleNetwork` registered as a PyroObject.

```
$ python sugleserver.py
```

- Open **another terminal**, and go to the folder you download the source code. You need to set the environment so that Pyro uses `pickle` to send the object. To do so, run the script `setenvclient.sh`. You only need to run this once.

```
$ chmod 755 setenvclient.sh
$ source ./setenvclient.sh
```

- In the same terminal, run the python file `sugleclient.py`. This runs the client program that will connect to `SugleNetwork`. This files requires that you have a working `suglework.py` containing `SugleAccount` class definition.

```
$ python sugleclient.py
```

### Running on a Network

- First, you need to find your ip address. You can find it from a terminal using:

```
$ ifconfig
```

- Edit the file, `runnameserver.sh` and change `localhost` to your ip address. For example, if your ip address is `192.168.1.96`. Then your `runnameserver.sh` should look like below:

```
#!/bin/bash
HOST=192.168.1.96
pyro4-ns -n $HOST
```

- Edit the file, `sugleserver.py`, and scroll down to the second last line until you see the variables `network_name` and `ipaddress`.

```
network_name = 'oka'
ipaddress = 'localhost'
run_pyro_daemon(network_name, ipaddress)
```

Change the network name and ip address. For example,

```
network_name = 'foo'
ipaddress = '192.168.1.96'
run_pyro_daemon(network_name, ipaddress)
```

- Edit the file, `sugleclient.py` and modify the network name:

```
# You can change the network name to create a separate network
network_name = 'oka'
```

to

```
# You can change the network name to create a separate network
network_name = 'foo'
```

- The rest of the steps are the same as above. One of the computer must run `runnameserver.sh` and the python file `sugleserver.py`. 
