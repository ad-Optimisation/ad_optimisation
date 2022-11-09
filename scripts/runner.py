# region: reference


"""
cp -r 'adunit-j&j-listerine-tonicadunit-instagram-bio-mob'
    'adunit-ihop-window4-scary-face-mpu' 'adunit-ihop-window4-scary-face-mob'
    'adunit-ihop-window4-reeses-mpu' 'adunit-ihop-window4-reeses-mob'
    'adunit-ihop-ihoppy-hour-save-dollar-5-mpu'
    'adunit-ihop-ihoppy-hour-save-dollar-5-mob'
    'adunit-ihop-ihoppy-hour-no-offer-mpu'
    'adunit-ihop-ihoppy-hour-no-offer-mob' ~/ad_optimization/data/


cp -r  "db69df88f5a7b1540d4ff829bffb97f9" ~/ad_optimization/data/
"""

# # to measure exec time

# # normal function to run on cpu
# def func(a):
#     for i in range(10000000):
#         a[i] += 1


# # function optimized to run on gpu
# @jit(target_backend='cuda')
# def func2(a):
#     for i in range(10000000):
#         a[i] += 1


# if __name__ == "__main__":
#     n = 10000000
#     a = np.ones(n, dtype=np.float64)

#     start = timer()
#     func(a)
#     print("without GPU:", timer()-start)

#     start = timer()
#     func2(a)
#     print("with GPU:", timer()-start)


# for subdir, dirs, files in os.walk(APP_FOLDER):
#     for file in files:
#         print(os.path.join(subdir, file))

# max_loop = 1
# loop = 0
# for subdir, dirs, files in os.walk(APP_FOLDER):
#     loop += 1
#     if loop > max_loop:
#         break  # In order just to complete only one walkthrough
#     for dir in dirs:
#         dir_path = os.path.join(subdir, dir)
#         color_dict = {}
#         for _, d, contents in os.walk(dir_path):
#             print(len(contents))
#             # p.append(contents)
#             print(contents)
#             for content in contents:
#                 # put your code here
#                 print(content)


# endregion


import os
import cv2
import sys
import datetime
import pandas as pd
import defaults as defs
import dataCleaner as dc
from typing import List, Tuple
from matplotlib import pyplot as plt
from deepface import DeepFace
import matplotlib.pyplot as plt


cleaner = dc.dataCleaner("development environment's runner script")

sys.path.append('../observations/')
sys.path.append('../data/')
APP_FOLDER = defs.root_challenge_path + defs.root_assets_path


def extract_objects(col: str):
    """
    A function that extracts the objects from a given image
    """

# print(f'started at: {datetime.datetime.now()}')
# perf_df = pd.read_csv('data/performance_data.csv')
# df = pd.DataFrame()
# # for i in range(100):
# for i in range(len(perf_df)):
#     c_df = locate_image_on_image(perf_df['game_id'][i],
#                                  'engagement',
#                                  '_preview.png', prefix='eng_')
#     df = pd.concat([df, c_df])
#     print(f'Extraction status: {round((i/len(perf_df) * 100), 1)}%')

# # save engagement position composition
# df.to_csv('observations/engagement_position.csv', index=False)
# print(f'ended at: {datetime.datetime.now()}')
