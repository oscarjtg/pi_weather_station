<!-- connecting_to_network.md -->
# Connecting raspberry pi to network

## Step 1: mobile hotspot

Set up a mobile hotspot using your laptop or phone. 
Give your hotspot name `pi_wifi` and password `raspberry`.

## Step 2: setup pi

When you first boot up a raspberry pi with pre-installed OS 
on a micro SD card,
the operating system puts you through a setup process.

To be consistent with previous years, choose:

```
username: pi
password: raspberry
```

When asked to connect to a wifi network, connect to your mobile hotspot.

## Step 3: change hostname

This is required so that we can have multiple pis on the same local network.

See `change_hostname.md`, or below:

```
sudo hostname new-hostname
hostnamectl set-hostname new-hostname
sudo nano /etc/hostname
sudo nano /etc/hosts
sudo systemctl reboot
```

Turn your mobile hotspot off and on again.


## Step 4: enable SSH

Plug raspberry pi into a monitor and enable SSH.

To do this, type the following into a terminal [1]

```
sudo raspi-config 
```

and navigate through the pop-up menu as follows

```
>>> Interface Options
>>> SSH
>>> YES
```

## Step 5: ssh from your computer

Check the pi can be identified on the network:

```
ping new-hostname.local
```

ssh into the pi:

```
ssh pi@new-hostname.local
```

followed by typing in the password `raspberry`.

If you chose a username other than pi 
(for consistency with the existing pis, this is not recommended)
replace `pi` with the `username` in the commands above.

## Step 6: copy files

Make directories

```
mkdir pi_weather_station
cd pi_weather_station
mkdir data
```

Exit the ssh by typing 

```
exit
```

then copy `weatherstations.py` into the `pi_weather_station` directory using the `scp` command

```
scp ./weatherstation.py pi@new-hostname.local:/home/pi/pi_weather_station/weatherstation.py
```

and enter the password `raspberry` when prompted.

In `weatherstation.py`, change `codename` to whatever the hostname is.


## References

[1] https://raspberrypi.stackexchange.com/questions/54573/connect-to-host-port-22-connection-refused

[2] https://raspberrypi.stackexchange.com/questions/83324/enabling-and-connecting-to-a-raspberry-pi

[3] https://raspberrypi.stackexchange.com/questions/73482/first-setup-of-raspberry-pi-zero-w?rq=1


