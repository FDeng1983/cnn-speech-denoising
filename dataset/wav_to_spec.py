#!/usr/bin/env python
"""
Usage:

Compute and display a spectrogram.
Give WAV file as input
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.io.wavfile
import numpy as np
import sys
import os

directory = sys.argv[1]

for fname in [f for f in os.listdir(directory) if f.endswith('.wav')]:

  print 'working on', fname

  wavfile = os.path.join(directory, fname)

  sr,x = scipy.io.wavfile.read(wavfile)

  ## Parameters: 10ms step, 30ms window
  nstep = int(sr * 0.01)
  nwin  = int(sr * 0.03)
  nfft = nwin

  window = np.hamming(nwin)

  ## will take windows x[n1:n2].  generate
  ## and loop over n2 such that all frames
  ## fit within the waveform
  nn = range(nwin, len(x), nstep)

  X = np.zeros( (len(nn), nfft/2) )

  for i,n in enumerate(nn):
      xseg = x[n-nwin:n]
      z = np.fft.fft(window * xseg, nfft)
      X[i,:] = np.log(np.abs(z[:nfft/2]))

  matfile = wavfile + '.mat'
  np.save(matfile, X)

  figfile = wavfile + '.png'
  plt.imshow(X.T, interpolation='nearest',
      origin='lower',
      aspect='auto')

  plt.savefig(figfile)
  plt.close('all')

plt.show()
