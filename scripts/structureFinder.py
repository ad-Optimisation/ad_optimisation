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
    A function that get the structure of a folder
    """
    totalFiles = 0
    totalDir = 0

    asset_folders = []

    for base, dirs, files in os.walk(APP_FOLDER):
        print('Searching in : ', base)
        for directories in dirs:
            # append base
            asset_folders.append(directories)
            totalDir += 1

        for Files in files:
            totalFiles += 1
    data = {'Assets': asset_folders}

    df = pd.DataFrame(data)
    df.to_csv('observations/structure.csv', index=True)

    print('base:', base, '\ndirs:', dirs,
          '\nfiles:', files, '\nlen:', len(files))
    print('Total number of files', totalFiles)
    print('Total Number of directories', totalDir)
    print('Total:', (totalDir + totalFiles))


def get_files_name(directory:  str, filter_extension: list = None) -> list:
    """
    A function to get file names from a given directory

    Parameters
    =--------=
    directory : str
        The directory to search
    filter_extension : list
        A list of file extensions to filter

    Returns
    =-----=
    list
        A list of file names
    """
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


def get_file_numbers(directory:  str, filter_extension: list = None) -> int:
    """
    A function to get file numbers from a given directory

    Parameters
    =--------=
    directory : str
        The directory to search
    filter_extension : list
        A list of file extensions to filter

    Returns
    =-----=
    list
        A file number
    """
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

    return len(files)


def set_up_folder_structure():
    """
    A function to set up the structure of a folder
    """
    df = pd.read_csv('observations/structure.csv')

    df['number_of_files'] = df.Assets.apply(
        lambda x: get_file_numbers(f'{x}/'))
    df['all_files'] = df.Assets.apply(lambda x: get_files_name(f'{x}/'))

    df['concat'] = df.all_files.apply(lambda x: " ".join(x))
    print('logo count: ', df.concat.str.contains("logo").value_counts())

    df = cleaner.remove_unwanted_cols(df, ["Unnamed: 0.1", "Unnamed: 0"],
                                      use_reg_ex=True)
    # print(df.columns)
    df.to_csv('observations/structure.csv', index=False)


get_structure()
set_up_folder_structure()
