# -*- coding: utf-8 -*-

##############
# Script listens to serial port and writes contents into a file
##############
# requires pySerial to be installed

import serial
import time
import numpy as np

serial_port = 'COM3'
baud_rate = 115200  # In arduino, Serial.begin(baud_rate)
write_to_file_path = "output.txt"
output_file = open(write_to_file_path, "w+")

try:
    ser = serial.Serial(serial_port, baud_rate)

    data = np.empty(1000000, bytes)

    start = time.time()
    print('starts')

    c = 0

    while ser.isOpen():
        try:
            line = ser.readline()
            if line:
                data[c] = line
                c += 1

        except KeyboardInterrupt:
            break
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
        except ValueError:
            print('ValueError')

    end = time.time()
    print('ends')

    sample_counter = c

    sample_duration = (end - start)

    sample_rate = sample_counter / sample_duration

    print('Sample count:', sample_counter)
    print('Sample Duration (s):', sample_duration)
    print('Sample Rate (Hz):', sample_rate)

    with open('output.txt', 'w') as f:
        for line in data:
            if not line:
                break
            try:
                line = line.decode("utf-8")
                line = int(line)/1024
                print(line)
                f.write('{:.4f} '.format(line))
            except UnicodeDecodeError:
                print('UnicodeDecodeError')
            except ValueError:
                print('ValueError')

finally:
    ser.close()
