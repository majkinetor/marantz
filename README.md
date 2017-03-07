# Marantz reciever web controler

Very simple marantz receiver web controler. Should support any marantz model that follows any variation of the telnet interface in the PROTOCOL pdf.

## Install

Requires:
- python3
- flask: `pip install flask`

## Configuration

Edit the marantz shell script and set the IP address of the receiver. Then run it, it will self host python flask application with simple interface that can be customized quickly.

## Usage

Index page shows current receiver status along with few options you can set there. Send any supported reciever telnet command via `/command` url, for example, this will change source to DVD:

```
http://localhost:5000/command?cmd=SI&arg=DVD
```
