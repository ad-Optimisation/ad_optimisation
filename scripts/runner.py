# region: reference


"""
cp -r 'adunit-j&j-listerine-tonicadunit-instagram-bio-mob'
    'adunit-ihop-window4-scary-face-mpu' 'adunit-ihop-window4-scary-face-mob'
    'adunit-ihop-window4-reeses-mpu' 'adunit-ihop-window4-reeses-mob'
    'adunit-ihop-ihoppy-hour-save-dollar-5-mpu'
    'adunit-ihop-ihoppy-hour-save-dollar-5-mob'
    'adunit-ihop-ihoppy-hour-no-offer-mpu'
    'adunit-ihop-ihoppy-hour-no-offer-mob' ~/ad_optimization/data/


cp -r  "00dfe88c4d3fb60793765d314bf24b7c" ~/ad_optimization/data/
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


cleaner = dc.dataCleaner('object extraction script')

sys.path.append('../observations/')
sys.path.append('../data/')
APP_FOLDER = defs.root_challenge_path + defs.root_assets_path


def extract_objects(col: str):
    """
    A function that extracts the objects from a given image
    """


def extract_color_feature(directory: str) -> pd.DataFrame:
    print(f'{APP_FOLDER}{directory}')
    last_df = pd.DataFrame()
    try:
        for filename in os.listdir(f'{APP_FOLDER}{directory}'):
            f = os.path.join(f'{APP_FOLDER}{directory}', filename)
            # print('fn:', f)
            color_df = identify_color_composition(
                f, tolerance=12, limit=12, visualize=False)
            color_df['Assets'] = directory
            color_df['file_name'] = filename
            last_df = pd.concat([last_df, color_df])
        return last_df
    except Exception as e:
        print(e)
    finally:
        return last_df


def locate_image_on_image(directory: str, locate_image: str, on_image: str, prefix: str = '',
                          visualize: bool = False,
                          color: Tuple[int, int, int] = (0, 0, 255)):
    last_df = pd.DataFrame()
    try:
        image = cv2.imread(f'{APP_FOLDER}{directory}/{on_image}')
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        template = cv2.imread(f'{APP_FOLDER}{directory}/{locate_image}', 0)

        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
        _, _, _, max_loc = cv2.minMaxLoc(result)

        height, width = template.shape[:2]

        top_left = max_loc
        bottom_right = (top_left[0] + width, top_left[1] + height)

        if visualize:
            cv2.rectangle(image, top_left, bottom_right, color, 1)
            plt.figure(figsize=(10, 10))
            plt.axis('off')
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            plt.imshow(image)

        # create dataframe, add position data and return
        last_df['Assets'] = directory
        last_df['located_image'] = locate_image
        last_df['base_image'] = on_image
        last_df['top_left_X'] = top_left[0]
        last_df['top_left_Y'] = top_left[1]
        last_df['bottom_right_X'] = bottom_right[0]
        last_df['bottom_right_Y'] = bottom_right[1]
        last_df['height'] = height
        last_df['width'] = width

        print({f'{prefix}top_left_pos': top_left,
               f'{prefix}bottom_right_pos': bottom_right})
        print(f'top left x: {top_left[0]} type: {type(top_left)}',
              f'top left y: {top_left[1]} type: {type(top_left[1])}')
        print(f'df: {last_df}\ntype: {type(last_df)}')
        return last_df

    except cv2.error as err:
        print(err)


# print(f'started at: {datetime.datetime.now()}')
# perf_df = pd.read_csv('data/performance_data.csv')
# df = pd.DataFrame()
# for i in range(len(perf_df)):
#     # for i in range(100):
#     c_df = extract_objects(perf_df['game_id'][i])
#     df = pd.concat([df, c_df])
#     print(f'Extraction status: {round((i/len(perf_df) * 100), 1)}%')

# # save color composition
# df.to_csv('observations/object_feature.csv', index=False)
# print(f'ended at: {datetime.datetime.now()}')

df1 = locate_image_on_image('4c3bb41d4f40f39842b7b8d3f536366a',
                            'engagement_instruction.png',
                            '_preview.png',
                            prefix='eng_', visualize=True)

df2 = locate_image_on_image('fef95c5e1ee5bc235b56d7c508d3bcd0',
                            'engagement_instruction.png',
                            '_preview.png',
                            prefix='eng_', visualize=True)

print(df1)
print(df2)
