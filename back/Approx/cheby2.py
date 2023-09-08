import numpy as np
import scipy.signal as ss
from back.FilterClass import Filter, ApproxType, FilterType

class ChebyII(Filter):
    def __init__(self, filter_type, filter_data, n, Q, nmin, nmax, Qmax, GD):
        super().__init__(filter_type, ApproxType.CH2, filter_data, n, Q, nmin, nmax, Qmax, None, GD, None)

    def get_best_n(self, nmin, nmax):
        n, wo = ss.cheb2ord(self.data.wp, self.data.wa, self.data.Ap, self.data.Aa, True)
        return n

    def get_fun(self, n):
        #if self.data.rp is None: self.data.rp = self.data.Ap
        z, p, k = ss.cheb2ap(n, self.data.Aa)
        return z, p, k

    def denormalize(self):
        if self.type == FilterType.LP:
            z, p, g = ss.lp2lp_zpk(self.zeros, self.poles, self.data.g, self.data.wa / (2 * np.pi))
        elif self.type == FilterType.HP:
            z, p, g = ss.lp2hp_zpk(self.zeros, self.poles, self.data.g, self.data.wa / (2 * np.pi))
        elif self.type == FilterType.BP:
            z, p, g = ss.lp2bp_zpk(self.zeros, self.poles, self.data.g, np.sqrt(self.data.wa[0]*self.data.wa[1]) / (2 * np.pi), (self.data.wa[1] - self.data.wa[0]) / (2 * np.pi))
        elif self.type == FilterType.BR:
            z, p, g = ss.lp2bs_zpk(self.zeros, self.poles, self.data.g, np.sqrt(self.data.wp[0] * self.data.wp[1]) / (2 * np.pi), (self.data.wa[1] - self.data.wa[0]) / (2 * np.pi))
        else:
            self.filter_error()
            z, p, g = [None, None, None]

        return z, p, g