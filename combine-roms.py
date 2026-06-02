#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) != 4:
        print("syntax: combine-roms [input1] [input2] [output]")
        sys.exit(1)

    input1_path, input2_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]

    try:
        fin1 = open(input1_path, "rb")
    except FileNotFoundError:
        print("[input1] missing!")
        sys.exit(1)

    try:
        fin2 = open(input2_path, "rb")
    except FileNotFoundError:
        fin1.close()
        print("[input2] missing!")
        sys.exit(1)

    try:
        fout = open(output_path, "wb")
    except OSError:
        fin1.close()
        fin2.close()
        print("[output] error.")
        sys.exit(1)

    print("creating [output] file.")

    data1 = fin1.read()
    bufsize = len(data1)
    data2 = fin2.read()

    print(f"combining {bufsize} x2 bytes.")

    # Interleave bytes from both files: byte from file1, byte from file2, repeat
    buf = bytearray(bufsize * 2)
    for i in range(bufsize):
        buf[i * 2]     = data1[i]
        buf[i * 2 + 1] = data2[i]

    fout.write(buf)

    fout.close()
    fin2.close()
    fin1.close()

if __name__ == "__main__":
    main()
