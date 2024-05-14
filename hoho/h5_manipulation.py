import os, gzip, re, shutil

class CustomError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def get_latest_version(original_name):
    pattern = re.compile(rf'{original_name}_(\d+)_.*\.h5\.gz')
    with os.scandir() as entries:
        files = [entry.name for entry in entries if entry.name.startswith(original_name)]
    latest_version_number = 0
    for filename in files:
        match = pattern.match(filename)
        if match:
            version_number = int(match.group(1))
            if version_number > latest_version_number:
                latest_version_number = version_number
    return latest_version_number


def removedoth5(filename):
    os.remove(f'{filename}.h5')

def decompress_gz(filename):
    with gzip.open(f'{filename}.h5.gz', 'rb') as f_in, open(f'{filename}.h5', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def compress_to_gz(filename):
    with open(f'{filename}.h5', 'rb') as f_in, gzip.open(f'{filename}.h5.gz', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    removedoth5(filename)

def find_profile_with_delta(file, delta):
    res = None
    for profile in file['scan'].keys():
        if abs(round((file['scan'][profile]['delta'][0]),5) - delta) < 0.0001:
            return profile
    raise CustomError(f'No profile in {file} with the given delta {delta} - discrepancy between the delta list from the hdf5, and the different delta of each profile')