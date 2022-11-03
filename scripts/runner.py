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

import os
import sys
import defaults as defs
import dataCleaner as ds
import pandas as pd

cleaner = ds.dataCleaner('runner script')

sys.path.append('../observations/')
APP_FOLDER = defs.root_challenge_path + defs.root_assets_path


def get_structure():
    """

    """
    totalFiles = 0
    totalDir = 0

    asset_folders = []
    asset_counts = []

    for base, dirs, files in os.walk(APP_FOLDER):
        print('Searching in : ', base)
        for directories in dirs:
            # append base
            asset_folders.append(directories)
            totalDir += 1

        for Files in files:
            asset_counts.append(len(Files))
            totalFiles += 1

    data = {'Assets': asset_folders,
            'number_of_files': asset_counts}

    df = pd.DataFrame(data)
    df.to_csv('observations/structure.csv', index=True)

    print('base:', base, '\ndirs:', dirs,
          '\nfiles:', files, '\nlen:', len(files))
    print('Total number of files', totalFiles)
    print('Total Number of directories', totalDir)
    print('Total:', (totalDir + totalFiles))


def get_proper_structure():
    print('get_proper_Structure')


def get_files_name(directory:  str, filter_extension: list = None) -> list:

    directory = f'{APP_FOLDER}/{directory}/'

    files = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        # checking if it is a file
        if filter_extension is not None:
            if os.path.isfile(f):
                if filename.split('.')[-1].upper() in filter_extension:
                    files.append(filename)
        else:
            if os.path.isfile(f):
                files.append(filename)

    return files


def set_up_folder_structure():
    df = pd.read_csv('observations/structure.csv')

    df['all_files'] = df.Assets.apply(lambda x: get_files_name(f'{x}/'))

    df['concat'] = df.all_files.apply(lambda x: " ".join(x))
    df.concat.str.contains("logo").value_counts()

    df = cleaner.remove_unwanted_cols(df, ["Unnamed: 0.1", "Unnamed: 0"],
                                      use_reg_ex=True)
    # print(df.columns)
    df.to_csv('observations/structure.csv', index=False)


set_up_folder_structure()
