from scipy.io import wavfile
import swipe
import numpy as np

import matplotlib.pyplot as plt

group = "HC"

if group == "HC":
    sample_rate, data = wavfile.read("HC/prodlouzena_fonace/HC849a2.wav")

elif group == "PN":
    sample_rate, data = wavfile.read("PN/prodlouzena_fonace/PN645a1.wav")

elif group == "MSA":
    sample_rate, data = wavfile.read("MSA/prodlouzena_fonace/MSA10a.wav")

elif group == "RBD":
    sample_rate, data = wavfile.read("RBD/prodlouzena_fonace/RBD148i1.wav")


print("Sample rate:", sample_rate)
print("Data shape:", data.shape)

pitches, t, strength = swipe.swipe(data, sample_rate)

print("SWIPE FINISHED")
print(pitches.size)
print(t.size)
print(strength.size)

avg_f0 = np.mean(pitches)

print(f"Average f0: {avg_f0}")

plt.figure(figsize=(12, 4))
plt.plot(t, pitches)
plt.xlim(t[80], t[-50])
plt.ylim(0.95*np.min(pitches[80:-50]), 1.05*np.max(pitches[80:-50]))
plt.show()