#-c COM11 -freq "867.00-869.00" -step 0.1 -chan "0-63" -bw "5,6,7,8" -sf "6,7,8,9,10,11,12" -t 10 -v -uc

#-c COM11 -freq "866.89" -chan "0-63" -bw "5,6,7,8" -sf "6,7,8,9,10,11,12" -t 10

import argparse
import serial #pip install pyserial
import time
from itertools import product
import sys


class ConsoleColors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[m"


class SmartFormatter(argparse.HelpFormatter):
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()
            # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)


def print_color(output, color, use_color):
    if use_color:
        print(f"{color}{output}")
    else:
        print(f"{output}")


def send_and_receive(ser, to_send, verbose, use_color):
    if verbose:
        print_color(f"{to_send}", f"{ConsoleColors.GREEN}", use_color)
    ser.write(bytearray(f"{to_send}\r\n", encoding="utf8"))
    time.sleep(0.01)
    while ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        if data and verbose:
            print_color(f"{data}", f"{ConsoleColors.BLUE}", use_color)


def main(com_port, frequencies, channels, bandwidths, spread_factors, coding_rates, preamble_lengths, sync_words,
         timeout, verbose, use_color):
    if verbose:
        print(f"COM port: {com_port}")
        print(f"Freq: {frequencies}")
        print(f"Channel: {channels}")
        print(f"Bandwidth: {bandwidths}")
        print(f"Spread factor: {spread_factors}")
        print(f"Coding rate: {coding_rates}")
        print(f"Preamble lengths: {preamble_lengths}")
        print(f"Sync words: {sync_words}")
        print(f"Timeout: {timeout}")
        print(f"Verbose: {verbose}")
        print(f"Use color: {use_color}")
    baud_rate = 9600
    try:
        with serial.Serial(com_port, baud_rate, timeout=1) as ser:
            print_color(f"Connected to {com_port} at {baud_rate} baud rate.", f"{ConsoleColors.GREEN}", use_color)
            time.sleep(0.5)
            while ser.in_waiting > 0:
                data = ser.readline().decode('utf-8').strip()
                if data and verbose:
                    print_color(f"{data}", f"{ConsoleColors.BLUE}", use_color)
            send_and_receive(ser, f"help", verbose,use_color)
            send_and_receive(ser, f"get_config", verbose, use_color)

            while True:
                for item in list(product(frequencies, channels, bandwidths, spread_factors, coding_rates,
                                         preamble_lengths, sync_words)):
                    (frequency, channel, bandwidth, spread_factor, coding_rate, preamble_length, sync_word) = item
                    state = ""
                    if frequency:
                        send_and_receive(ser, f"set_freq {frequency}", verbose, use_color)
                        state += f"freq {frequency}, "
                    if channel:
                        send_and_receive(ser, f"set_chann {channel}", verbose, use_color)
                        state += f"chan {channel}, "
                    if bandwidth:
                        send_and_receive(ser, f"set_bw {bandwidth}", verbose, use_color)
                        state += f"bw {bandwidth}, "
                    if spread_factor:
                        send_and_receive(ser, f"set_sf {spread_factor}", verbose, use_color)
                        state += f"sf {spread_factor}, "
                    if coding_rate:
                        send_and_receive(ser, f"set_cr {coding_rate}", verbose, use_color)
                        state += f"cr {coding_rate}, "
                    if preamble_length:
                        send_and_receive(ser, f"set_pl {preamble_length}", verbose, use_color)
                        state += f"pl {preamble_length}, "
                    if sync_word:
                        send_and_receive(ser, f"set_sw {sync_word}", verbose, use_color)
                        state += f"sw 0x{sync_word}"

                    print_color(f"{state}", f"{ConsoleColors.GREEN}", use_color)
                    # TODO REMOVE ME send_and_receive(ser, f"get_config", verbose, use_color)
                    # TODO REMOVE ME send_and_receive(ser, f"get_freq", verbose, use_color)


                    # TODO REMOVE ME input()

                    old_time = time.time()
                    while time.time() - old_time < timeout:
                        if ser.in_waiting > 0:
                            print_color("RECEIVED DATA!", f"{ConsoleColors.RED}", use_color)
                            data = ser.readline()
                            size = 16
                            index = 0

                            while index < len(data):
                                data_slice = data[index:(size + index)]
                                payload = format(" ".join(f"{i:02x}" for i in data_slice)).ljust(size * 3)
                                payload += "| "
                                payload += format(
                                    "".join((chr(i) if chr(i).isprintable() else ".") for i in data_slice))
                                print_color(f"{payload}", f"{ConsoleColors.BLUE}", use_color)
                                index += size
                    sys.stdout.flush()

    except serial.SerialException as e:
        print_color(f"Error: {e}", f"{ConsoleColors.RED}", use_color)
    except KeyboardInterrupt:
        print_color(f"Serial reading stopped", f"{ConsoleColors.RED}", use_color)


def parse_float_range(f, s, min_val, max_val, name):
    if f is None:
        return [None]

    if "," in f:
        return f.split(",")
    elif "-" in f:
        tokens = f.split("-")
        if len(tokens) != 2:
            raise ValueError(f"{name} {f} does not appear to be a valid range")
        try:
            start = float(tokens[0])
            end = float(tokens[1])
            step = float(s)

            if (start < min_val) or (end > max_val) or (step <= 0):
                raise ValueError(f"{name}={f}, step={s} does not appear to be valid, or within range of {min_val} "
                                 f"to {max_val}")

            result = [f"{start}"]
            while start <= end:
                start += step
                result.append(str(round(start, 2)))
            return result

        except Exception as e:
            raise ValueError(f"{name}={f}, step={s} does not appear to be valid")
    else:
        return [f]


def parse_int_range(n, min_val, max_val, name):
    if n is None:
        return [None]

    if "," in n:
        return n.split(",")
    elif "-" in n:
        tokens = n.split("-")
        if len(tokens) != 2:
            raise ValueError(f"{name}={n} does not appear to be a valid range")
        try:
            start = int(tokens[0])
            end = int(tokens[1])
            step = 1
            if (start < min_val) or (end > max_val) or (step <= 0):
                raise ValueError(f"{name}={n} does not appear to be valid, or within range of {min_val} "
                                 f"to {max_val}")
            result = [f"{start}"]
            while start < end:
                start += step
                result.append(f"{start}")
            return result

        except Exception as e:
            raise ValueError(f"{name}={n} does not appear to be valid")
    else:
        return [n]


def parse_hex_range(n, min_val, max_val, name):
    if n is None:
        return [None]

    if "," in n:
        return n.split(",")
    elif "-" in n:
        tokens = n.split("-")
        if len(tokens) != 2:
            raise ValueError(f"{name}={n} does not appear to be a valid range")
        try:
            start = int(tokens[0], 16)
            end = int(tokens[1], 16)
            step = 1
            if (start < min_val) or (end > max_val) or (step <= 0):
                raise ValueError(f"{name}={n} does not appear to be valid, or within range of {min_val} "
                                 f"to {max_val}")
            result = [f"{start:02X}"]
            while start < end:
                start += step
                result.append(f"{start:02X}")
            return result

        except Exception as e:
            raise ValueError(f"{name}={n} does not appear to be valid")
    else:
        return [n]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CatWan LoRa Scanner", formatter_class=SmartFormatter)
    parser.add_argument("-c",
                        metavar="COM port",
                        type=str,
                        nargs="?",
                        required="true",
                        help="COM port for CatWan device")
    parser.add_argument("-freq",
                        metavar="Frequencies",
                        type=str,
                        help="LoRa frequency (e.g. '868.1,868.2,868.3' or '867-869' (use -step for range interval))")
    parser.add_argument("-step",
                        metavar="Interval",
                        type=str,
                        default="0.1",
                        help="LoRa frequency interval for ranges. Defaults to 0.1")
    parser.add_argument("-chan",
                        metavar="Channel",
                        type=str,
                        help="Lora channel 0-63 (e.g. '0,1,2' or '0-63')")
    parser.add_argument("-bw",
                        metavar="Bandwidth",
                        type=str,
                        help="R|Bandwidth 0-8 (e.g. '0,2,4' or '0-8')\n"
                             "0 - 7.8 kHz\n"
                             "1 - 10.4 kHz\n"
                             "2 - 15.6 kHz\n"
                             "3 - 20.8 kHz\n"
                             "4 - 31.25 kHz\n"
                             "5 - 41.7 kHz\n"
                             "6 - 62.5 kHz\n"
                             "7 - 125 kHz\n"
                             "8 - 250 kHz")
    parser.add_argument("-sf",
                        metavar="Spread factor",
                        type=str,
                        help="Spread factor 6-12 (e.g. '6,7,8' or '6-12')")
    parser.add_argument("-cr",
                        metavar="Coding rate",
                        type=str,
                        help="R|Coding rate 5-8 (e.g. '5,6' or '5-8)\n"
                             "5 - 4/5 (1.25x overhead)\n"
                             "6 - 4/6 (1.5x overhead)\n"
                             "7 - 4/7 (1.75x overhead)\n"
                             "8 - 4/8 (2x overhead)")
    parser.add_argument("-pl",
                        metavar="Preamble length",
                        type=str,
                        help="Preamble length 6-65535 (e.g. '6,10,12' or '6-65535')")
    parser.add_argument("-sw",
                        metavar="Sync word",
                        type=str,
                        help="Sync word byte (e.g. '00,12,FF' or '0-FF')")
    parser.add_argument('-t',
                        metavar="Timeout",
                        default=10,
                        type=int,
                        help="Receive timeout in seconds. Defaults to 10s")
    parser.add_argument('-v',
                        action='store_true',
                        help="Verbose output. Defaults to off")
    parser.add_argument('-uc',
                        action='store_true',
                        help="Use color. Defaults to off")

    args = parser.parse_args()

    try:
        freq = parse_float_range(args.freq, args.step, 867.0, 869.0, "freq")
        chan = parse_int_range(args.chan, 0, 63, "chan")
        bw = parse_int_range(args.bw, 0, 8, "bw")
        sf = parse_int_range(args.sf, 6, 12, "sf")
        cr = parse_int_range(args.cr, 5, 8, "cr")
        pl = parse_int_range(args.pl, 6, 65536, "pl")
        sw = parse_hex_range(args.sw, 0x00, 0xFF, "sw")
        main(args.c,
             freq if True else [None],
             chan if True else [None],
             bw if True else [None],
             sf if True else [None],
             cr if True else [None],
             pl if True else [None],
             sw if True else [None],
             args.t,
             args.v,
             args.uc)
    except KeyboardInterrupt:
        print(ConsoleColors.RESET + "Aborting")
        print_color("Aborting", f"{ConsoleColors.RESET}", args.uc)
    print_color("", f"{ConsoleColors.RESET}", args.uc)
