import numpy as np
import scipy.signal as ss
from back.FilterClass import Filter, ApproxType

class ChebyI(Filter):
    def __init__(self, filter_type, filter_data, n, Q, nmin, nmax, Qmax, rp, GD):
        super().__init__(filter_type, ApproxType.CH1, filter_data, n, Q, nmin, nmax, Qmax, rp, GD, None)

    def get_best_n(self, nmin, nmax):
        n, wo = ss.cheb1ord(self.data.wp, self.data.wa, self.data.Ap, self.data.Aa, True)
        return n

    def get_fun(self, n):
        if self.data.rp is None: self.data.rp = self.data.Ap/2
        z, p, k = ss.cheb1ap(n, self.data.rp)
        return z, p, k
