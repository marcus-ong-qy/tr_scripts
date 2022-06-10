from data_analysis import read_txt
from denoise import removeNoise

noise = read_txt(
    'arduino_readwrite/noise_samples/sample_17660_2'
)

sig = read_txt(
    'arduino_readwrite/440_samples/sample_17660_1'
)

rec = removeNoise(sig, noise, visual=True)  # TODO error
