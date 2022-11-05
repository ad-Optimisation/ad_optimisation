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


cleaner = dc.dataCleaner("development environment's runner script")

sys.path.append('../observations/')
sys.path.append('../data/')
APP_FOLDER = defs.root_challenge_path + defs.root_assets_path


def extract_objects(col: str):
    """
    A function that extracts the objects from a given image
    """


def locate_image_on_image(directory: str, locate_image: str, on_image: str,
                          prefix: str = '', visualize: bool = False,
                          color: Tuple[int, int, int] = (0, 0, 255)):

    last_df = pd.DataFrame(columns=['Assets', 'located_image', 'base_image',
                                    'top_left_X', 'top_left_Y',
                                    'bottom_right_X', 'top_right_Y', 'height',
                                    'width', 'total_image_height',
                                    'total_image_width'])

    locate_image_ = ''
    match_count = 0
    match_count_list = []
    try:
        for filename in os.listdir(f'{APP_FOLDER}{directory}'):
            print(f'current file name: {filename}')
            if locate_image in filename:
                locate_image_ = filename
                print(f'found match: {locate_image_}')
                match_count += 1
                match_count_list.append(match_count)
        print(f'total matches found: {match_count}')
        print(f'total matches list: {match_count_list}\n')
    except Exception as e:
        print(e)

    try:
        image = cv2.imread(f'{APP_FOLDER}{directory}/{on_image}')
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        template = cv2.imread(f'{APP_FOLDER}{directory}/{locate_image_}', 0)

        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        # get the locate image size
        height, width = template.shape[:2]
        # get the total image size
        image_height, image_width = image.shape[:2]

        top_left = max_loc
        bottom_right = (top_left[0] + width, top_left[1] + height)

        if visualize:
            cv2.rectangle(image, top_left, bottom_right, color, 1)
            plt.figure(figsize=(10, 10))
            plt.axis('off')
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            plt.imshow(image)

        # create dataframe, add position data and return
        last_df.loc[0] = [directory, locate_image_, on_image, top_left[0],
                          top_left[1], bottom_right[0], bottom_right[1],
                          height, width, image_height, image_width]
        return last_df

    except cv2.error as err:
        last_df.loc[0] = [directory, locate_image, on_image, 'NA', 'NA', 'NA',
                          'NA', 'NA', 'NA', 'NA', 'NA']
        print(err)
        return last_df


print(f'started at: {datetime.datetime.now()}')
perf_df = pd.read_csv('data/performance_data.csv')
df = pd.DataFrame()
# for i in range(100):
for i in range(len(perf_df)):
    c_df = locate_image_on_image(perf_df['game_id'][i],
                                 'engagement',
                                 '_preview.png', prefix='eng_')
    df = pd.concat([df, c_df])
    print(f'Extraction status: {round((i/len(perf_df) * 100), 1)}%')

# save engagement position composition
df.to_csv('observations/engagement_position.csv', index=False)
print(f'ended at: {datetime.datetime.now()}')

# df1 = locate_image_on_image('4c3bb41d4f40f39842b7b8d3f536366a',
#                             'engagement_instruction.png',
#                             '_preview.png', prefix='eng_', visualize=True)

# df2 = locate_image_on_image('fef95c5e1ee5bc235b56d7c508d3bcd0',
#                             'engagement_instruction.png',
#                             '_preview.png', prefix='eng_', visualize=True)
