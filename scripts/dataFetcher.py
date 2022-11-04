import boto3
import zipfile
import defaults as defs


def fetch_data(_bucket_name: str = defs.bucket_name,
               _from_path: str = defs.from_path, _to_path: str = defs.to_path):
    """
    A function to fetch data from S3 bucket

    Parameters
    ----------
    _bucket_name: str
        Name of the S3 bucket
    _from_path: str
        Path to the file to be downloaded
    _to_path: str
        Path where the file will be saved

    Returns
    -------
    None
    """
    s3 = boto3.client('s3')
    s3.download_file(_bucket_name, _from_path, _to_path)


def extract_data(file_name: str, from_path: str, to_path: str):
    """
    A function to extract data from S3 bucket

    Parameters
    ----------
    file_name: str
        Path to the file to be downloaded
    from_path: str
        Path where the file will be saved
    to_path: str
        Path where the file will be saved

    Returns
    -------
        None
    """
    with zipfile.ZipFile(from_path + file_name, 'r') as zip_ref:
        zip_ref.extractall(to_path)
