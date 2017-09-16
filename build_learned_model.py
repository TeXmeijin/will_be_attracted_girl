import numpy as np

import init_model

ROOT_DIR = ''

def exec(img_size, npy_file_name):
# データをロード --- (※1)
    X_train, X_test, y_train, y_test = np.load("./" + ROOT_DIR + "img_built_data/" + npy_file_name + '.npy')
# データを正規化する
    X_train = X_train.astype("float") / 256
    X_test  = X_test.astype("float")  / 256

    model = init_model.exec(img_size, img_size, 3, 5)

# モデルを訓練する --- (※4)
    hdf5_dir = './' + ROOT_DIR + 'learned_model/'
    hdf5_file = npy_file_name + '.hdf5'
    model.fit(X_train, y_train, batch_size=img_size / 2, nb_epoch=50)
    model.save_weights(hdf5_dir + hdf5_file)
