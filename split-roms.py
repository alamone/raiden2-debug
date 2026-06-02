#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) != 4:
        print("syntax: split-roms [input] [output1] [output2]")
        sys.exit(1)

    input_path, output1_path, output2_path = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        fin = open(input_path, "rb")
    except FileNotFoundError:
        print("[input] missing!")
        sys.exit(1)

    try:
        fout1 = open(output1_path, "wb")
        fout2 = open(output2_path, "wb")
    except OSError:
        fin.close()
        print("[output] error.")
        sys.exit(1)

    print("creating [output] files.")

    buf = fin.read()
    bufsize = len(buf)

    print(f"splitting {bufsize} bytes.")

    # De-interleave: even-indexed bytes go to output1, odd-indexed to output2
    fout1.write(buf[0::2])
    fout2.write(buf[1::2])

    fin.close()
    fout1.close()
    fout2.close()

if __name__ == "__main__":
    main()
