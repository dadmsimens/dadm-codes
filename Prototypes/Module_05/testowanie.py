from unmlbackup1440 import unlm
import scipy.io
import numpy as np
import matplotlib.pyplot as plt
import time
from multiprocessing import Pool
import cProfile
#python -m cProfile -o stats testowanie.py
#cprofilev -f stats /if in directory

#multiprocessing

# dane nowe od Kacpra 9.01
mat = scipy.io.loadmat('imnoi.mat')
scan = mat['In']
map = scipy.io.loadmat('mapa.mat')
noise_map = map['MapaR2']


# stare dane
#mat = scipy.io.loadmat('nima.mat')
#scan = mat['nimage']
#noise = scipy.io.loadmat('map_noise.mat')
#noise_map = noise['MapaR_nimage']

start = time.time()

filtered = unlm(scan, 5, 2, noise_map)

end = time.time()
print(end - start)


fig = plt.figure()
plt.suptitle('moje wyniki')

plt.subplot(2, 2, 1)
plt.imshow(np.squeeze(scan), cmap='gray')
plt.axis('off')
plt.title('zaszumiony obraz')

plt.subplot(2, 2, 2)
plt.imshow(np.squeeze(noise_map), cmap='gray')
plt.axis('off')
plt.title('mapa szumu')

plt.subplot(2, 2, 3)
plt.imshow(np.squeeze(filtered), cmap='gray')
plt.axis('off')
plt.title('filtracja UNLM')

plt.subplot(2, 2, 4)
plt.imshow(np.squeeze(filtered-scan), cmap='gray')
plt.axis('off')
plt.title('reszty')

plt.show()
