# CatWanSniff
LoRa packet sniffer for the Electronic Cats CatWan device in Python (Currently not working)

![Screenshot](https://github.com/James-P-D/CatWanSniff/blob/main/screenshot.png)

## Introduction

I purchased a [CatWAN USB Stick](https://electroniccats.com/store/catwan-usb-stick/) from @ElectronicCats in the hope that it might be possible to make a general-purpose LoRa scanner and be able to specify a frequency range and other paramaters, and then have the device sweep for any LoRa packets. I've tried leaving the device on and sweeping around the 868MHz range, with varying values for the other parameters in the hope that I might be able to sniff some traffic from the various LoRa devices I can see on my SDR. Sadly, so far no luck.

If anyone can see what the issue is, I'd be interested to hear.

## Requirements

```
pip install argparse
pip install pyserial
```

## Usage

The project requires `argparse` and `pyserial` so you'll need to run:

```
pip install argparse
pip install pyserial
```

If you run the script without arguments you will see the following:

```
C:\python.exe CatWanSniff.py
usage: CatWanSniff.py [-h] -c [COM port] [-freq Frequencies] [-step Interval] [-chan Channel] [-bw Bandwidth]
                      [-sf Spread factor] [-cr Coding rate] [-pl Preamble length] [-sw Sync word] [-t Timeout] [-v]
                      [-uc]
CatWanSniff.py: error: the following arguments are required: -c
```

Use the `-h` for full details:

```
usage: CatWanSniff.py [-h] -c [COM port] [-freq Frequencies] [-step Interval] [-chan Channel] [-bw Bandwidth]
                      [-sf Spread factor] [-cr Coding rate] [-pl Preamble length] [-sw Sync word] [-t Timeout] [-v]
                      [-uc]

CatWan LoRa Scanner

options:
  -h, --help           show this help message and exit
  -c [COM port]        COM port for CatWan device
  -freq Frequencies    LoRa frequency (e.g. '868.1,868.2,868.3' or '867-869' (use -step for range interval))
  -step Interval       LoRa frequency interval for ranges. Defaults to 0.1
  -chan Channel        Lora channel 0-63 (e.g. '0,1,2' or '0-63')
  -bw Bandwidth        Bandwidth 0-8 (e.g. '0,2,4' or '0-8')
                       0 - 7.8 kHz
                       1 - 10.4 kHz
                       2 - 15.6 kHz
                       3 - 20.8 kHz
                       4 - 31.25 kHz
                       5 - 41.7 kHz
                       6 - 62.5 kHz
                       7 - 125 kHz
                       8 - 250 kHz
  -sf Spread factor    Spread factor 6-12 (e.g. '6,7,8' or '6-12')
  -cr Coding rate      Coding rate 5-8 (e.g. '5,6' or '5-8)
                       5 - 4/5 (1.25x overhead)
                       6 - 4/6 (1.5x overhead)
                       7 - 4/7 (1.75x overhead)
                       8 - 4/8 (2x overhead)
  -pl Preamble length  Preamble length 6-65535 (e.g. '6,10,12' or '6-65535')
  -sw Sync word        Sync word byte (e.g. '00,12,FF' or '0-FF')
  -t Timeout           Receive timeout in seconds. Defaults to 10s
  -v                   Verbose output. Defaults to off
  -uc                  Use color. Defaults to off
```