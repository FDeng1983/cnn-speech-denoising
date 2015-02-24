import os
import numpy as np
import h5py

class SpectrogramPair(object):

    def __init__(self, noisy_mat, clean_mat):
        with h5py.File(noisy_mat, 'r') as f:
            self.noisy_mat = f['ps/value'].value
        with h5py.File(clean_mat, 'r') as f:
            self.clean_mat = f['ps/value'].value

    def sample_patch(self, y_len, x_len):

        y_max, x_max = self.clean_mat.shape

        y_start = np.random.randint(low=0, high=y_max-y_len)
        x_start = np.random.randint(low=0, high=x_max-x_len)

        clean_patch = self.clean_mat[y_start:y_start+y_len, x_start:x_start+x_len]
        noisy_patch = self.noisy_mat[y_start:y_start+y_len, x_start:x_start+x_len]

        yield noisy_patch.reshape(1, 1, y_len, x_len), clean_patch.reshape(1, 1, y_len, x_len)


class PatchSampler(object):

    def __init__(self, clean_dir, noisy_dir, samples_per_spectrogram=10, x_len=100, y_len=100):
        self.clean_dir = clean_dir
        self.noisy_dir = noisy_dir
        self.n = samples_per_spectrogram
        self.x_len = x_len
        self.y_len = y_len

    def __iter__(self):
        for root, dirs, files in os.walk(self.clean_dir, topdown=False):
            for name in files:
                if not name.endswith('.hdf5'): continue
                clean = os.path.join(root, name)
                noisy = clean.replace(self.clean_dir, self.noisy_dir)
                assert os.path.isfile(clean)
                assert os.path.isfile(noisy)

                pair = SpectrogramPair(noisy, clean)
                for idx, patches in enumerate(pair.sample_patch(x_len=self.x_len, y_len=self.y_len)):
                    yield patches


def write_out(data, label, fname):

    # HDF5 is pretty efficient, but can be further compressed.
    comp_kwargs = {'compression': 'gzip', 'compression_opts': 1}
    with h5py.File(fname, 'w') as f:
        f.create_dataset('data', data=data, **comp_kwargs)
        f.create_dataset('label', data=label, **comp_kwargs)


def get_fname(fname, fnum):
    return filename+'.'+str(fnum)+'.h5'


if __name__ == '__main__':


    # the number of examples to write to the output hdf5 file before switching to a new one
    max_examples_per_file = 2000

    times = 0
    data = None
    label = None
    filename = 'train'
    filenum = 0

    # change this to direct to the clean directory and the noisy directory
    clean_dir = 'spec/clean'
    noisy_dir = 'spec/isolated'
    samples_per_spectrogram = 15 # how many samples to fetch from each spectrogram
    sampler = PatchSampler(clean_dir, noisy_dir, samples_per_spectrogram)

    for noisy_path, clean_patch in sampler:
        times += 1

        data = noisy_path if data is None else np.concatenate((data, noisy_path), axis=0)
        label = clean_patch if data is None else np.concatenate((data, clean_patch), axis=0)

        if data.shape[0] == max_examples_per_file:
            # write a new file
            print 'writing out', get_fname(filename, filenum)
            write_out(data.astype('float32'), label.astype('float32'), get_fname(filename, filenum))
            filenum += 1
            data = None
            label = None

    if data is not None:
        fname = filename+str(filenum)+'.h5'
        print 'writing out', fname
        write_out(data.astype('float32'), label.astype('float32'), fname)

    with open(filename+'.txt', 'wb') as f:
        for i in xrange(filenum):
            f.write(get_fname(filename, i) + '\n')
