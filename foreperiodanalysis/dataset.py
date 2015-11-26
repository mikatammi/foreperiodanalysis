import numpy as np


class TBTFile():
    def __init__(self, filename):
        self.data = np.genfromtxt(filename,
                                  skip_header=1,
                                  delimiter=',',
                                  names=True,
                                  dtype=None)


class GazedataFile():
    def __init__(self, filename):
        # TODO: Make caching optional
        try:
            self.data = np.load(filename + '.npz')['data']
        except IOError:
            self.data = np.genfromtxt(filename,
                                      delimiter='\t',
                                      names=True,
                                      dtype=None,
                                      usecols=range(0, 22))

            # Cache data in numpy format (order of magnitude faster to read)
            np.savez(filename + '.npz', data=self.data)
