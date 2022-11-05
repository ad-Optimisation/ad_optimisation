"""
A starter script for position extraction
"""

import os
import cv2
import sys
import datetime
import pandas as pd
import defaults as defs
import dataCleaner as dc
from typing import List, Tuple
from matplotlib import pyplot as plt


cleaner = dc.dataCleaner('position extraction script')

sys.path.append('../observations/')
sys.path.append('../data/')
APP_FOLDER = defs.root_challenge_path + defs.root_assets_path


def locate_image_on_image(directory: str, locate_image: str, on_image: str,
                          prefix: str = '', visualize: bool = False,
                          color: Tuple[int, int, int] = (0, 0, 255)) -> pd.DataFrame:
    """
    Locate an image in an image

    Parameters
    =--------=
    directory: string
        The path to the directory
    locate_image: string
        The path to the image to locate
    on_image: string
        The path to the base image to locate
    prefix: string
        The prefix
        For printing purpose
    visualize: bool
        An indicator to visualize the image or not
    color: tuple
        The color of the visualizer box

    Returns
    =-----=

    last_df: pandas dataframe
        A data frame containing position information
    """
    last_df = pd.DataFrame(columns=['Assets', 'located_image', 'base_image',
                                    'top_left_X', 'top_left_Y',
                                    'bottom_right_X', 'top_right_Y', 'height',
                                    'width', 'total_image_height',
                                    'total_image_width'])

    locate_image_ = ''
    match_count = 0
    match_count_list = []
    try:
        print(f'inside: {directory}')
        for filename in os.listdir(f'{APP_FOLDER}{directory}'):
            print(f'current file name: {filename}')
            if locate_image in filename.lower():
                if 'mp4' in filename.lower():
                    continue
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
                                 'cta',
                                 '_preview.png', prefix='eng_')
    df = pd.concat([df, c_df])
    print(f'Extraction status: {round((i/len(perf_df) * 100), 1)}%')

# save cta position composition
df.to_csv('observations/cta_position.csv', index=False)
print(f'ended at: {datetime.datetime.now()}')
