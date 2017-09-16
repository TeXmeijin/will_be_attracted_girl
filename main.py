#!/usr/bin/env python
import glob, sys, os
import numpy as np
import string
import random

import build_npy
import build_learned_model
import guess_type_girl

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

CATEGORIES = ["love","like","normal","unlike","hate"]
IMG_SIZE = 128
ALPHABET_A_CODE = 65

ALLOW_REUSE_DISTANCE = 1

ROOT_DIR = ''
USER_INPUTED_DIR = './' + ROOT_DIR + 'img_user_inputed'

def get_user_input_list():
    user_input = []
    user_love = []
    user_like = []
    user_normal = []
    user_unlike = []
    user_hate = []

    for idx in range(10, 35):
        idx = str(idx)
# 3, 1, 2, 4, 0
        user_love.append('3' + idx)
        user_like.append('1' + idx)
        user_normal.append('2' + idx)
        user_unlike.append('4' + idx)
        user_hate.append(idx)

    user_input.append(user_love)
    user_input.append(user_like)
    user_input.append(user_normal)
    user_input.append(user_unlike)
    user_input.append(user_hate)

    return user_input

# とにかくランダムな文字列を10個生成している
def create_rand_npy_name():
    n = 10
# ユーティリティ関数にすると便利かも?
    random_str = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])
    return random_str

def save_user_input_img_data(file_name, user_input):
    np.save(USER_INPUTED_DIR + '/' + file_name, user_input)

def convert_score_array(score_array):
    ret = [i for i in range(0, 499)]
    print(score_array)
    for idx, numbers_each_level in enumerate(score_array):
        for number in numbers_each_level:
            ret[int(number)] = idx
    return np.asarray(ret)

# 存在するnpyの中で最も近い距離になるベクトルの距離とそのファイル名を返す
def get_most_nearest_npy_distance_filename(user_input):
    user_input_np = np.asarray(user_input)
# target_npy_filesにnpy形式のファイルの一覧が入る
# このファイルには今までユーザーが入力した、もしくは事前準備した入力パターンが入っている
    target_npy_files = glob.glob(USER_INPUTED_DIR + '/*.npy')
# min_distanceにめっちゃでかい数値を入れる
    min_distance = sys.maxsize
    min_file_name = ''
# 最初実行した時は、target_npy_filesが一個もないので以下の処理は走らない
    for target_npy_file in target_npy_files:
        npy_file_name = target_npy_file.split('/')[2]
        file_name = npy_file_name.split('.')[0]
        # if not os.path.exists('./' + ROOT_DIR + 'learned_model/' + file_name + '.hdf5'):
        #     continue
        decoded_target_input = np.load(target_npy_file)
        if decoded_target_input is None:
            return (sys.maxsize, '')
        # this_distance = np.linalg.norm(user_input_np.astype(int) - decoded_target_input.astype(int))
        print(str(np.linalg.norm(convert_score_array(decoded_target_input))))
        this_distance = np.linalg.norm(convert_score_array(user_input_np) - convert_score_array(decoded_target_input))
        print(file_name + ': this_distance: ' + str(this_distance))
        if this_distance < min_distance:
            min_distance = this_distance
            min_file_name = file_name

    return (min_distance, min_file_name)

def exec(user_input):
# ユーザーの入力が空っぽの場合は、適当なデータを用意する
    if user_input is None:
        print('www')
        user_input = get_user_input_list()
# ランダムなファイル名を生成している 
    rand_file_name = create_rand_npy_name()
# 既存の学習モデルの中で一番入力のパターンが近いものを探している
    min_distance, min_file_name = get_most_nearest_npy_distance_filename(user_input)
    print(str(np.linalg.norm(convert_score_array(user_input))))
    print('min_distance: ' + str(min_distance))
    # min_distanceが0以上の場合、少なくとも未知のパターンなので保存する
    if min_distance < ALLOW_REUSE_DISTANCE:
        return guess_type_girl.exec(IMG_SIZE, min_file_name)
# min_distanceがallow_reuse_distance以上の場合、こちらの処理が走る
    else:
        if min_distance > 0:
# 今回ユーザーが入力した50次元のベクトルをファイルに保存しておく
            save_user_input_img_data(rand_file_name, user_input)
# 画像を配列に置換したもの（入力データ）と、回答（教師データ）をまとめて配列に入れてファイルに保存
        build_npy.exec(user_input, CATEGORIES, IMG_SIZE, rand_file_name)
        build_learned_model.exec(IMG_SIZE, rand_file_name)
        return guess_type_girl.exec(IMG_SIZE, rand_file_name)

# exec()
