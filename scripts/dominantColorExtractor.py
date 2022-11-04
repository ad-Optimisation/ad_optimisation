"""
A starter script for color feature extraction
"""

# from timeit import default_timer as timer
# import numpy as np
# from numba import jit, cuda
import os
import sys
import datetime
import extcolors
import pandas as pd
from PIL import Image
import defaults as defs
import dataCleaner as ds
from colormap import rgb2hex
from matplotlib import pyplot as plt

cleaner = ds.dataCleaner('color feature extraction script')

sys.path.append('../observations/')
sys.path.append('../data/')
APP_FOLDER = defs.root_challenge_path + defs.root_assets_path


# @jit(target_backend='cuda')
def identify_color_composition(image,
                               tolerance: int = 12,
                               limit: int = 1,
                               visualize: bool = False) -> pd.DataFrame:
    """
    Function that identifies the color composition of a
    given image path.

    Parameters
    =--------=
    image: str
        Path to the image.
    tolerance: int, optional
        Tolerance for the color composition.
        Defaults to 12.
    visualize: bool, optional
        Whether to visualize the color composition.
        Defaults to False.

    Returns
    =-----=
        identified_colors: pd.Dataframe
    """

    extracted_colors = extcolors.extract_from_path(
        image, tolerance=tolerance, limit=limit)

    identified_colors = color_to_df(extracted_colors)

    if not visualize:
        return identified_colors

    list_color = list(identified_colors['c_code'])
    list_percent = [int(i) for i in list(identified_colors['occurrence'])]

    text_c = [c + ' ' + str(round(p*100/sum(list_percent), 1)) + '%' for c, p in zip(list_color, list_percent)]
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(100, 100), dpi=10)
    wedges, _ = ax[0].pie(list_percent,
                          labels=text_c,
                          labeldistance=1.05,
                          colors=list_color,
                          textprops={'fontsize': 60, 'color': 'black'}
                          )

    plt.setp(wedges, width=0.3)

    # create space in the center
    plt.setp(wedges, width=0.36)

    ax[0].set_aspect("equal")
    fig.set_facecolor('grey')

    ax[1].imshow(Image.open(image))

    plt.show()

    return identified_colors[:1]


# @jit(target_backend='cuda')
def color_to_df(extracted_colors: tuple) -> pd.DataFrame:
    """
    Converts RGB Color values from extcolors output to HEX Values.

    Parameters
    =--------=
    extracted_colors: tuple
        RGB Color values from extcolors output.

    Returns
    =-----=
    colors_df: pandas dataframe
        A data frame that contains the hex values and the RGB values
    """

    colors_pre_list = str(extracted_colors).replace(
        '([(', '').replace(')],', '), (').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')', '')
                  for i in colors_pre_list]

    # convert RGB to HEX code
    df_rgb_values = [(int(i.split(", ")[0].replace("(", "")),
                      int(i.split(", ")[1]),
                      int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]

    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(", "")),
                           int(i.split(", ")[1]),
                           int(i.split(", ")[2].replace(")", ""))) for i in df_rgb]

    colors_df = pd.DataFrame(zip(df_color_up, df_rgb_values, df_percent),
                             columns=['c_code', 'rgb', 'occurrence'])

    return colors_df


# @jit(target_backend='cuda')
def extract_color_feature(directory: str) -> pd.DataFrame:
    """
    A function to extract color feature

    Parameters
    =--------=
    directory: str
        The path to the directory where the color features are stored.

    Returns
    =-----=
    extracted_colors: pandas dataframe
        A data frame that contains the hex values and the RGB values
    """
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


print(f'started at: {datetime.datetime.now()}')
perf_df = pd.read_csv('data/performance_data.csv')
df = pd.DataFrame()
for i in range(len(perf_df)):
    # for i in range(100):
    c_df = extract_color_feature(perf_df['game_id'][i])
    df = pd.concat([df, c_df])

# save color composition
df.to_csv('observations/color_feature.csv', index=False)
print(f'ended at: {datetime.datetime.now()}')
