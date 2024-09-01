# CatWanSniff
LoRa packet sniffer for the Electronic Cats CatWan device in Python

## Introduction

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
                      [-sf Spread factor] [-cr Coding rate] [-t Timeout] [-v] [-uc]
CatWanSniff.py: error: the following arguments are required: -c
```

Use the `-h` for full details:

```
C:\python.exe CatWanSniff.py -h
usage: CatWanSniff.py [-h] -c [COM port] [-freq Frequencies] [-step Interval] [-chan Channel] [-bw Bandwidth]
                      [-sf Spread factor] [-cr Coding rate] [-t Timeout] [-v] [-uc]

CatWan LoRa Scanner

options:
  -h, --help         show this help message and exit
  -c [COM port]      COM port for CatWan device
  -freq Frequencies  LoRa frequency ('868.1,868.2,868.3' or '867-869' (use -step for range interval))
  -step Interval     LoRa frequency interval for ranges. Defaults to 0.1
  -chan Channel      LoRa channel (0-63) ('0,1,2' or '0-63')
  -bw Bandwidth      0 - 7.8 kHz
                     1 - 10.4 kHz
                     2 - 15.6 kHz
                     3 - 20.8 kHz
                     4 - 31.25 kHz
                     5 - 41.7 kHz
                     6 - 62.5 kHz
                     7 - 125 kHz
                     8 - 250 kHz
  -sf Spread factor  6-12
  -cr Coding rate    5 - 4/5 (1.25x overhead)
                     6 - 4/6 (1.5x overhead)
                     7 - 4/7 (1.75x overhead)
                     8 - 4/8 (2x overhead)
  -t Timeout         Receive timeout in seconds. Defaults to 10s
  -v                 Verbose output. Defaults to off
  -uc                Use color. Defaults to off
```