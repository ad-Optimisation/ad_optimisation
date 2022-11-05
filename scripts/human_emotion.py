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


def extract_human_emotion(directory: str):
    """
    A function that extracts the emotion from a human face.
    """
    for filename in os.listdir(f'{APP_FOLDER}{directory}'):
        result = DeepFace.analyze(filename, actions=['emotion'])
        # TODO : APPEND RESULTS TO A DATAFRAME 

# print(f'started at: {datetime.datetime.now()}')
perf_df = pd.read_csv('data/performance_data.csv')
df = pd.DataFrame()
# for i in range(100):
for i in range(len(perf_df)):
    c_df = extract_human_emotion(perf_df['game_id'][i])
    df = pd.concat([df, c_df])
    print(f'Extraction status: {round((i/len(perf_df) * 100), 1)}%')

# save engagement position composition
df.to_csv('observations/human_emotion.csv', index=False)
print(f'ended at: {datetime.datetime.now()}')