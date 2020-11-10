# Installation
Note: these instructions only tested on my machine (2013 Macbook Air)

## Installing Raspbian
- Download and unzip the most recent Raspberry Pi OS from [here](https://www.raspberrypi.org/downloads/raspberry-pi-os/)
- Using [balenaEtcher](https://www.balena.io/etcher/), flash the OS onto an micro SD card
  - Currently using SanDisk Ultra 16GB

### Enable SSH (and connect to internet)
[Source](https://desertbot.io/blog/headless-raspberry-pi-3-bplus-ssh-wifi-setup)
- Plug SD card back into computer
- Navigate to the `boot` folder
  - `cd /Volumes/boot`
- Create a blank `ssh` file
  - `touch ssh`
- Create a `wpa_supplicant.conf` file
  - `touch wpa_supplicant.conf`
- Edit this file with the following (with your own network credentials):
```
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="NETWORK-NAME"
    psk="NETWORK-PASSWORD"
}
```
- Eject the SD card and place into Pi - power it up
- Pi will automatically try to connect to internet with your network credentials
- Check your network for any new clients - Save the IP address of the Pi once found
- `ssh pi@[ip address]` to ssh in from your computer (on the same network)

### Change your password
- By default, your username is `pi` and password is `raspberry`.
- After connecting through SSH, use `passwd` to change your password

### Installing Plex
[Source](https://pimylifeup.com/raspberry-pi-plex-server/)
- Run these two commands
```
sudo apt-get update
sudo apt-get upgrade
```
- Install `apt-transport-https` package
  - `sudo apt-get install apt-transport-https`
- Add Plex repos to `apt`
```
curl https://downloads.plex.tv/plex-keys/PlexSign.key | sudo apt-key add -
echo deb https://downloads.plex.tv/repo/deb public main | sudo tee /etc/apt/sources.list.d/plexmediaserver.list
sudo apt-get update
```
- Install Plex
  - `sudo apt install plexmediaserver`
-

### Manually mount external hard drive
[Source](https://pimylifeup.com/raspberry-pi-mount-usb-drive/)
