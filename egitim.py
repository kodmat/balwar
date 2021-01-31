import tensorflow as tf
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras import Sequential
import numpy as np

my_dat_input = np.load('kayit_giris.npy').reshape(-1,3) / 600.0
my_dat_output = np.load('kayit_cikis.npy').reshape(-1,)


output = [0 if i == -15 else 1 for i in my_dat_output]

model = Sequential()
model.add(Dense(64, input_shape=(3,), activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam',
              loss=tf.keras.losses.binary_crossentropy,
              metrics=['accuracy'])

model.fit(my_dat_input, output, epochs=50, batch_size=20, validation_split=0.1)

model.save('ballwar.h5')