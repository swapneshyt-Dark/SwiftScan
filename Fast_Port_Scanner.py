#!/usr/bin/env python3
import pyfiglet
import socket
import threading
import concurrent.futures
import datetime
import argparse
import time
import math
from colorama import init as colorama_init, Fore, Back, Style

# Initialize colorama (makes colors work on Windows)
colorama_init(autoreset=True)

# ---------- Argparse & port parsing (same as before) ----------
parser = argparse.ArgumentParser(
    prog='fast.py',
    usage='%(prog)s [Target] [Port]',
    epilog="Example: fast.py google.com 1-10000   fast.py github.com all"
)
parser.add_argument("target", help="[target ip or hostname]")
parser.add_argument(
    "port",
    help="[port] (examples: 80, 1-1000, all). Default = 1-1000",
    nargs='?',
    default="1-1000"
)
args = parser.parse_args()

ip = args.target
nport = args.port

if isinstance(nport, str) and nport.lower() == "all":
    start, end = 1, 65535
elif isinstance(nport, str) and "-" in nport:
    s, e = nport.split("-", 1)
    start, end = int(s), int(e)
else:
    start = int(nport)
    end = int(nport)

start = max(1, start)
end = min(65535, end)
if end < start:
    start, end = end, start

# ---------- Banner with color ----------
ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print("-" * 70)
print(Fore.YELLOW + "github.com/swapneshyt-Dark" + Style.RESET_ALL)
# You can combine Fore + Back + Style
print(Fore.CYAN + ascii_banner + Style.RESET_ALL)

def date_time():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

print_lock = threading.Lock()

try:
    targetip = socket.gethostbyname(ip)
except socket.gaierror as e:
    print(Fore.RED + f"Error resolving host '{ip}': {e}" + Style.RESET_ALL)
    raise SystemExit(1)

print("-" * 70)
print(f"Scanning Target - {Fore.YELLOW}{ip}{Style.RESET_ALL} ({targetip})")
print("Scan started - [{}]".format(date_time()))
print("-" * 70)
print("\n      Ip\t\tPort\t\tState")
print("-" * 55)

# ---------- Scanner function ----------
def scan(ip_addr, port, timeout=1.0):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        result = s.connect_ex((ip_addr, port))
        return port, (result == 0)
    except Exception:
        return port, False
    finally:
        try:
            s.close()
        except Exception:
            pass

# ---------- Helpers for colored progress ----------
def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)}s"
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}m{s:02d}s"

def colored_bar(scanned, total, start_time):
    elapsed = time.time() - start_time
    pct = (scanned / total) * 100 if total else 100
    eta = "-"
    if scanned > 0 and scanned < total:
        rate = scanned / elapsed
        remaining = total - scanned
        eta_seconds = (remaining / rate) if rate > 0 else None
        if eta_seconds is not None:
            eta = format_time(eta_seconds)

    bar_width = 30
    filled = int(math.floor(bar_width * scanned / total)) if total else bar_width
    bar = "[" + "#" * filled + "-" * (bar_width - filled) + "]"

    # Color logic: progress in cyan, percent in yellow
    return (f"\r{Fore.CYAN}{bar}{Style.RESET_ALL} "
            f"{scanned}/{total} ({Fore.YELLOW}{pct:5.1f}%{Style.RESET_ALL}) "
            f"Elapsed: {format_time(elapsed)} ETA: {eta}")

# ---------- Run threaded scan with progress ----------
ports = list(range(start, end + 1))
total_ports = len(ports)
max_workers = min(1000, total_ports, 200)

start_time = time.time()
scanned = 0

with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    futures = {executor.submit(scan, targetip, p): p for p in ports}

    # initial progress line
    print(colored_bar(scanned, total_ports, start_time), end="", flush=True)

    for fut in concurrent.futures.as_completed(futures):
        port = futures[fut]
        try:
            p, is_open = fut.result()
        except Exception:
            p, is_open = port, False

        scanned += 1

        if is_open:
            # Print a dedicated colored line for open ports, then redraw progress
            with print_lock:
                print()  # move to next line so the open port isn't mixed with the bar
                print(f"{targetip}\t\t{Fore.GREEN}{p}{Style.RESET_ALL}\t\t{Fore.GREEN}Open{Style.RESET_ALL}")

        # redraw the colored progress bar
        print(colored_bar(scanned, total_ports, start_time), end="", flush=True)

# finish
print()  # newline after progress bar
print("\nScan finished - [{}]".format(date_time()))
print("-" * 70)
