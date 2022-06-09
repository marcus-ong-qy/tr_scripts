# -*- coding: utf-8 -*-

##############
# Script listens to serial port and writes contents into a file
##############
# requires pySerial to be installed

import serial
import time

serial_port = 'COM3'
baud_rate = 2000000  # In arduino, Serial.begin(baud_rate)
write_to_bin_path = "output_bin.txt"


def main():
    sample_counter = 0

    try:
        ser = serial.Serial(serial_port, baud_rate)

        with open(write_to_bin_path, 'wb') as f:
            start = time.time()
            while True:
                # if ser.isOpen():
                try:
                    line = ser.readline().strip()
                    if line:
                        # print(line)

                        # # ser.readline returns a binary, convert to string
                        # line = line.decode("utf-8")
                        # print(line)

                        # dat = float(line)/1024
                        # # print(dat)

                        f.write(line)
                        # # f.write('{:.4f} '.format(dat))
                        # print('{:.4f} '.format(dat))
                        sample_counter += 1

                except KeyboardInterrupt:
                    print('\nKeyboardInterrupt\n')
                    break
                except UnicodeDecodeError:
                    print('UnicodeDecodeError')

        end = time.time()

        sample_duration = (end - start)

        sample_rate = sample_counter / sample_duration

        print('Sample count:', sample_counter)
        print('Sample Duration (s):', sample_duration)
        print('Sample Rate (Hz):', sample_rate)

    finally:
        ser.close()


if __name__ == '__main__':
    main()