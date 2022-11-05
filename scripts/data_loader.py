import pandas as pd


def read_csv(file_name):
    """
    Reads a csv file.

    Parameters
    =--------=
    file_name : str
      Name of the csv file.

    Returns
    =-----=
    df : pd.DataFrame
      Dataframe of the csv file.
    """
    try:
        null_values = ["n/a", "na", "undefined"]
        df = pd.read_csv(f'../data/{file_name}', na_values=null_values)
        return df
    except Exception as e:
        print("Log:-> File Not Found")
        print(e)


def save_file(file_name):
    """
      Saves a csv file.

      Parameters
      =--------=
      file_name : str
        Name of the csv file.

      Returns
      =-----=
      None
      """
    try:
        pass
    except Exception as e:
        print(e)
