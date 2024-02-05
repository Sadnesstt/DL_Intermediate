import requests
from os import listdir, mkdir, rename
from os.path import isfile, isdir, join
from zipfile import ZipFile

def download_url(url, save_path, chunk_size = 128):
    r = requests.get(url, stream = True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

    print('Download zip file completed.')

def unzip(zip_path, dataset_path):
    zf = ZipFile(zip_path)
    zf.extractall(path=dataset_path)
    zf.close()
    print('Unzipping completed.')

def restructure_dir(data_path, is_train = True):
    files = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    if is_train:
        for file in files:
            if not isdir(join(data_path, file.split('.')[0])):
                mkdir(join(data_path, file.split('.')[0]))
            rename(
                join(data_path, file), join(data_path, file.split('.')[0], file)
            )
    else:
        for file in files:
            if not isdir(join(data_path, 'dummy')):
                mkdir(join(data_path, 'dummy'))
            rename(
                join(data_path, file), join(data_path, 'dummy', file)
            )
    print('Restructuring completed.')

if __name__ == '__main__':

    # make dataset directory
    dataset_path = './dataset'
    if not isdir(dataset_path):
        print('Making dataset directory on {}'.format(dataset_path))
        mkdir(dataset_path)

    # set hymenoptera dataset
    hymenoptera_url = 'https://download.pytorch.org/tutorial/hymenoptera_data.zip'
    hymenoptera_path = './hymenoptera.zip'

    download_url(hymenoptera_url, hymenoptera_path)
    unzip(hymenoptera_path, dataset_path)
    rename(join(dataset_path, 'hymenoptera_data'), join(dataset_path, 'hymenoptera'))
    rename(join(dataset_path, 'hymenoptera', 'val'), join(dataset_path, 'hymenoptera', 'test'))