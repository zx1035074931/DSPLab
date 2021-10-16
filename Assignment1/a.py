#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
plot wave graphic
plottingWaveform.py
"""
import wave
import pylab as pl
import numpy as np
# open 'wav'  xyuuu
file = wave.open(r"original2.wav", "rb")

# get wav information
# (nchannels, sampwidth,framerate, nframes, comptype, compname)
params = file.getparams()
nchannels,sampwidth,framerate,nframes = params[:4]
print(params)

# 读取波形数据
str_data = file.readframes(nframes) # readframes--return n frames with byte type

# close file
file.close()

''' turn wave data into array
frombuffer -- turns string into ASCII, 
dtype is the data type, controlling how many bits form an ASCII value
len(wave_data) = 96000, half wave_data's size by extracting by odd-even
'''
wave_data = np.frombuffer(str_data, dtype=np.short) # wave_data is an array stores ASCII
wave_data.shape = (-1, 2) # wave_data.shape = (m,n) means reshaping array into 'm'rows*'n'collums.
wave_data = wave_data.T  # matrix transpose

time = np.arange(0, nframes) * (1.0 / framerate) # time array is needed for plotting
print ("wave_data:", len(wave_data[0][0:len(time)]))

# plot the graphic
""" subplot(mnp) / (m,n,p)
plot several graphics into one image
'm' means m rows, 'n' means n collums,
'p' means this graphic's position, counts from left to right and top to bottom  
"""
pl.subplot(2, 1, 1)
pl.plot(time, wave_data[0][0:len(time)])
pl.subplot(2, 1, 2)
pl.plot(time, wave_data[1][0:len(time)], c="g")
pl.xlabel("time (seconds)")
pl.show()

