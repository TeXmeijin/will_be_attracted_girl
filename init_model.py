from keras.layers import Convolution2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.models import Sequential

def exec(img_w, img_h, dimension, layer_count):
    # モデルを構築 --- (※2)
    model = Sequential()
    model.add(Convolution2D(int(img_w / 2), dimension, dimension, 
        border_mode='same',
        input_shape=(img_w, img_h, dimension)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Convolution2D(img_w, dimension, dimension, border_mode='same'))
    model.add(Activation('relu'))
    model.add(Convolution2D(img_w, dimension, dimension))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten()) # --- (※dimension) 
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(layer_count))
    model.add(Activation('softmax'))

    model.compile(loss='binary_crossentropy',
        optimizer='rmsprop',
        metrics=['accuracy'])

    return model
