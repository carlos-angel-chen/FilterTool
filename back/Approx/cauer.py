import numpy as np
import scipy.signal as ss
from back.FilterClass import Filter, ApproxType

class Cauer(Filter):
    def __init__(self, filter_type, filter_data, n, Q, nmin, nmax, Qmax, GD):
        super().__init__(filter_type, ApproxType.C, filter_data, n, Q, nmin, nmax, Qmax, None, GD, None)

    def get_best_n(self, nmin, nmax):
        n, wo = ss.ellipord(self.data.wp, self.data.wa, self.data.Ap, self.data.Aa, True)
        return n

    def get_fun(self, n):
        z, p, k = ss.ellipap(n, self.data.Ap, self.data.Aa)
        return z, p, k
