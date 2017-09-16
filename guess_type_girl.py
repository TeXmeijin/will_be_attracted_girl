from PIL import Image
import numpy as np
import glob, os, sys

import init_model

ROOT_DIR = ''
img_dir = './' + ROOT_DIR + 'static/img_famous_people'
test_files = glob.glob(img_dir + '/*.jpg')

def exec(img_size, npy_file_name):
    test_converterd_data = []
    for test_file in test_files:
        img = Image.open(test_file).convert("RGB").resize((img_size, img_size))
        converted_data = np.asarray(img)
        test_converterd_data.append(converted_data)

    test_converterd_data = np.array(test_converterd_data)

    model = init_model.exec(img_size, img_size, 3, 5)

    hdf5_file = './' + ROOT_DIR + 'learned_model/' + npy_file_name + '.hdf5'
    if not os.path.exists(hdf5_file):
        print('hdf5 file' + hdf5_file + ' is not exist')
        return ''

    model.load_weights(hdf5_file)
    result_set = model.predict(test_converterd_data)

    print(result_set)
    print(test_files[result_set.argmax(axis = 0)[0]])

    scores = []
    for r in result_set:
        score = 10000 * r[0] + 1000 * r[1] + 100 * r[2] + 10 * r[3] + r[4]
        scores.append(score)
    return test_files[np.asarray(scores).argmax()]
