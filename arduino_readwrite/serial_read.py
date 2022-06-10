# -*- coding: utf-8 -*-

##############
# Script listens to serial port and writes contents into a file
##############
# requires pySerial to be installed

'''
Arduino => serial_read.py => bin2text.py => Audacity or data_analysis.py
'''

import serial
import time

serial_port = 'COM3'
baud_rate = 2000000  # In arduino, Serial.begin(baud_rate)

# use bin2text.py to convert to readable text format
WRITE_TO_BIN_PATH = "serial_read_bin.txt"
# empirically derived from running an experiment with _sample()
SAMPLE_RATE = 17660


def _buffer(buffer_count, serial):
    n = 0

    print(f'Buffering {buffer_count} readings...')

# give buffer cos initial reading frequencies are somewhat unreliable
    while n < buffer_count:
        try:
            line = serial.readline()
            if line:
                n += 1
        except UnicodeDecodeError:
            print('UnicodeDecodeError')


def _sample():
    '''
        Empirically determine the sample rate
    '''
    print('Sampling Sampling Rate')
    sample_counter = 0

    try:
        ser = serial.Serial(serial_port, baud_rate)

        with open(WRITE_TO_BIN_PATH, 'wb') as f:
            BUFFER_COUNT = 20000
        # give buffer cos initial reading frequencies are somewhat unreliable
            _buffer(BUFFER_COUNT, ser)

            print('Recording Start!')

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

        sample_rate = sample_counter / (sample_duration)

        print('Sample count:', sample_counter)
        print('Sample Duration (s):', '{:.3f}'.format(sample_duration))
        print('Sample Rate (Hz):', int(sample_rate + 1))

    finally:
        ser.close()


def serial_read():
    '''
        Reads serial output from Arduino and writes data to binary file
        You can run bin2text.py to convert the binary data to Audacity
        Sample Data Import text file format
    '''

    try:
        ser = serial.Serial(serial_port, baud_rate)

        with open(WRITE_TO_BIN_PATH, 'wb') as f:
            BUFFER_COUNT = 20000
        # give buffer cos initial reading frequencies are somewhat unreliable
            _buffer(BUFFER_COUNT, ser)

            print('Recording Start!')

            start = time.time()

            while True:
                try:
                    line = ser.readline().strip()
                    if line:
                        f.write(line)

                except KeyboardInterrupt:
                    print('\nKeyboardInterrupt\n')
                    break
                except UnicodeDecodeError:
                    print('UnicodeDecodeError')

            end = time.time()

        sample_duration = (end - start)

        print('Sample Duration (s):', '{:.3f}'.format(sample_duration))
        print('Indicated Sample Rate (Hz):', SAMPLE_RATE)

    finally:
        ser.close()


if __name__ == '__main__':
    serial_read()
