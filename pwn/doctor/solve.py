# Author: k4rt0fl3r
from pwn import *
import sys

elf = context.binary = ELF("src/baby_bof")

def run():
    if "--remote" in sys.argv:
        host_pos = sys.argv.index("--host") if "--host" in sys.argv else None
        port_pos = sys.argv.index("--port") if "--port" in sys.argv else None
        if not host_pos or not port_pos:
            print("Please provide --host and --port when specifying --remote!")
            exit(1)
        return remote(sys.argv[host_pos + 1], int(sys.argv[port_pos + 1]))

    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs) #
    elif args.R:
        return remote(args.HOST, args.PORT)
    else:
        return process(elf.path)

p = run()
p.send(b"AAAAAA\n")
p.interactive()
