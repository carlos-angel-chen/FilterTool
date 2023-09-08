import numpy as np
import scipy.signal as ss
from back.FilterClass import Filter, ApproxType, FilterType


class Bessel(Filter):
    def __init__(self, filter_type, filter_data, n, Q, nmin, nmax, Qmax, GD, tol):
        super().__init__(filter_type, ApproxType.B, filter_data, n, Q, nmin, nmax, Qmax, None, GD, tol)

    def get_best_n(self, nmin, nmax):
        if self.type == FilterType.GD:
            wpn = self.get_wan()
            if self.data.tol is None: self.data.tol = 0.1
            n = nmin
            for i in range(nmax - nmin):
                [z, p, g] = ss.bessel(n, 1, analog=True, output="zpk", norm='delay')
                # num, den = ss.zpk2tf(z, p, g)
                # if num[-1] != 0:
                #     k = den[-1] / num[-1]
                # else:
                #     k = 1
                # g = k * g
                '''w, mod, ph = ss.bode([b, a])
                group_delay = np.divide(-np.diff(ph), np.diff(w))  # d(ph)/d(w)'''
                w = np.linspace(wpn/10, wpn*10, num=1000)
                w, gd = self.get_GD(w, z=z, p=p, k=g)
                closest = (np.abs(w - wpn)).argmin()
                if gd[closest] >= (1 - self.data.tol)*self.data.GD:
                    break
                n = n + 1
        else:
            n = nmin
            for i in range(nmax - nmin):
                z, p, k = self.get_fun(n)
                #k = k * self.fix_gain(ss.zpk2tf(z, p, k), FilterType.LP)
                wap = np.linspace(min(1, self.get_wan()), max(1, self.get_wan()), 2)
                wap, mod, ph = ss.bode([z, p, k], w=wap)
                if np.around(mod[0]) >= -self.data.Ap and np.around(mod[1]) <= -self.data.Aa:
                    break
                n = n + 1
        return n


    def get_fun(self, n):
        #z, p, k = ss.bessel(n, self.data.wp*self.data.GD, 'lowpass', analog=True, output='zpk', norm='delay')
        if self.type == FilterType.GD:
            z, p, k = ss.bessel(n, 1, 'lowpass', analog=True, output='zpk', norm='delay')
        else:
            z, p, k = ss.bessel(n, 1 / self.get_wan(), 'lowpass', analog=True, output='zpk', norm='delay')
        #z, p, k = ss.besselap(n, norm='delay')
        return z, p, k
