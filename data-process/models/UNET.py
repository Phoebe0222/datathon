import os
import numpy as np

import matplotlib as mpl
mpl.rcParams['axes.grid'] = False
mpl.rcParams['figure.figsize'] = (12,12)

from sklearn.model_selection import train_test_split
import matplotlib.image as mpimg
import functools

import tensorflow as tf
import tensorflow.contrib as tfcontrib
from tensorflow.python.keras import layers
from tensorflow.python.keras import losses
from tensorflow.python.keras import models
from tensorflow.python.keras import backend as K

from Util import ImageGen
from Util import UNETLibrary

img_shape = (512, 512, 3)
batch_size = 3
epochs = 5

###################### getting filenames ######################
f = open("./ModelTrainingData/TileIds.txt")
x_train_filenames = []
y_train_filenames = []
DATE = '2019-08-09' # only training with one date 
# each mask has 3 inputs, namely tci, ndvi and fci
for id in f:
    id = str(id).replace("\n","")
    x_train_filenames.append(os.path.join('./ModelTrainingData/input', 
                                          "tci-{}-{}.png".format(id,DATE)))
    y_train_filenames.append(os.path.join('./ModelTrainingData/label', 
                                          "mask-{}.png".format(id)))
    x_train_filenames.append(os.path.join('./ModelTrainingData/input', 
                                          "ndvi-{}-{}.png".format(id,DATE)))
    y_train_filenames.append(os.path.join('./ModelTrainingData/label', 
                                          "mask-{}.png".format(id)))
    x_train_filenames.append(os.path.join('./ModelTrainingData/input', 
                                          "fci-mode1-{}-{}.png".format(id,DATE)))
    y_train_filenames.append(os.path.join('./ModelTrainingData/label', 
                                          "mask-{}.png".format(id)))

####################### splitting into train/val set ######################
x_train_filenames, x_val_filenames, y_train_filenames, y_val_filenames = \
                    train_test_split(x_train_filenames, y_train_filenames, 
                                     test_size=0.2, random_state=42)

num_train_examples = len(x_train_filenames)
num_val_examples = len(y_val_filenames)
print("There are {} training inputs.".format(num_train_examples))
print("There are {} validation labels.".format(num_val_examples))
print(x_train_filenames[:4])
print(y_train_filenames[:4])    



############# apply augmentation to training set but not validation set ##########
tr_cfg = {
    'resize': [img_shape[0], img_shape[1]],
    'scale': 1 / 255.,
    'hue_delta': 0.1,
    'horizontal_flip': True,
    'width_shift_range': 0,
    'height_shift_range': 0
} # passing augment parameters
tr_preprocessing_fn = functools.partial(UNETLibrary._augment, **tr_cfg)  

val_cfg = {
    'resize': [img_shape[0], img_shape[1]],
    'scale': 1 / 255.,
}
val_preprocessing_fn = functools.partial(UNETLibrary._augment, **val_cfg)



##################### creating dataset using augmentation ####################
train_ds = UNETLibrary.get_baseline_dataset(x_train_filenames,
                                y_train_filenames,
                                preproc_fn=tr_preprocessing_fn,
                                batch_size=batch_size)
val_ds = UNETLibrary.get_baseline_dataset(x_val_filenames,
                              y_val_filenames, 
                              preproc_fn=val_preprocessing_fn,
                              batch_size=batch_size)




########################### UNET model ###########################
inputs = layers.Input(shape=img_shape)
# 256

encoder0_pool, encoder0 = UNETLibrary.encoder_block(inputs, 32)
# 128

encoder1_pool, encoder1 = UNETLibrary.encoder_block(encoder0_pool, 64)
# 64

encoder2_pool, encoder2 = UNETLibrary.encoder_block(encoder1_pool, 128)
# 32

encoder3_pool, encoder3 = UNETLibrary.encoder_block(encoder2_pool, 256)
# 16

encoder4_pool, encoder4 = UNETLibrary.encoder_block(encoder3_pool, 512)
# 8

center = UNETLibrary.conv_block(encoder4_pool, 1024)
# center

decoder4 = UNETLibrary.decoder_block(center, encoder4, 512)
# 16

decoder3 = UNETLibrary.decoder_block(decoder4, encoder3, 256)
# 32

decoder2 = UNETLibrary.decoder_block(decoder3, encoder2, 128)
# 64

decoder1 = UNETLibrary.decoder_block(decoder2, encoder1, 64)
# 128

decoder0 = UNETLibrary.decoder_block(decoder1, encoder0, 32)
# 256

outputs = layers.Conv2D(1, (1, 1), activation='sigmoid')(decoder0)

model = models.Model(inputs=[inputs], outputs=[outputs])

model.compile(optimizer='adam', loss=UNETLibrary.bce_dice_loss, metrics=[UNETLibrary.dice_loss])

save_model_path = './savedModels/UNET.hdf5'
cp = tf.keras.callbacks.ModelCheckpoint(filepath=save_model_path, 
                                        monitor='val_dice_loss', 
                                        save_best_only=True, verbose=1)

# training the model
history = model.fit(train_ds, 
                   steps_per_epoch=int(np.ceil(num_train_examples / float(batch_size))),
                   epochs=epochs,
                   validation_data=val_ds,
                   validation_steps=int(np.ceil(num_val_examples / float(batch_size))),
                   callbacks=[cp])

