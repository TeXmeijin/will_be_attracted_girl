from sklearn import cross_validation
from PIL import Image
from PIL import ImageOps
import os, glob
import numpy as np

ROOT_DIR = ''

img_sample_dir = "./" + ROOT_DIR + "static/img_sample_models"
# categories = ["love","like","normal","unlike","hate"]

def convert_gray_scale_array(gray_array):
    ret = []
    for g in gray_array:
        ret_pixel = [g, g, g,]
        ret.append(ret_pixel)

    # print(ret)
    return ret

def exec(user_input, categories, img_size, npy_file_name):
    nb_classes = len(categories)

    # 画像データを読み込み --- (※3)
    X = []
    Y = []
    for idx, cat in enumerate(categories):
        # ラベルを指定 --- (※4)
        label = [0 for i in range(nb_classes)]
        label[idx] = 1
        # 画像 --- (※5)
        for i, f in enumerate(user_input[idx]):
            f = img_sample_dir + '/' + f + '.jpg'
            if not os.path.exists(f):
                print(f + 'is not exist')
                continue
            open_img = Image.open(f) # --- (※6)
            img = open_img.convert("RGB")
            img = img.resize((img_size, img_size))
            data = np.asarray(img)
            X.append(data)
            Y.append(label)
            X.append(np.asarray(img.transpose(Image.FLIP_LEFT_RIGHT)))
            Y.append(label)
            X.append(np.asarray(img.transpose(Image.FLIP_TOP_BOTTOM)))
            Y.append(label)
            X.append(np.asarray(img.transpose(Image.ROTATE_90)))
            Y.append(label)

            # gray_img = open_img.convert("L")
            # gray_img = convert_gray_scale_array(np.asarray(gray_img))
            # gray_data = np.asarray(gray_img)
            # X.append(gray_data)
            # Y.append(label)
    X = np.array(X)
    Y = np.array(Y)

# 学習データとテストデータを分ける --- (※7)
    X_train, X_test, y_train, y_test = \
        cross_validation.train_test_split(X, Y, test_size=0.0)
    xy = (X_train, X_test, y_train, y_test)
    np.save("./" + ROOT_DIR + "img_built_data/" + npy_file_name + '.npy', xy)

    print("ok,", len(Y))
