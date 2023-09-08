import numpy as np
import scipy.signal as ss
from scipy.special import factorial
from back.FilterClass import Filter, ApproxType, FilterType


class Gauss(Filter):
    def __init__(self, filter_type, filter_data, n, Q, nmin, nmax, Qmax, GD, tol):
        super().__init__(filter_type, ApproxType.G, filter_data, n, Q, nmin, nmax, Qmax, None, GD, tol)

    def get_best_n(self, nmin, nmax):
        if self.type == FilterType.GD:
            wpn = self.get_wan()
            if self.data.tol is None: self.data.tol = 0.1
            n = nmin
            for i in range(nmax - nmin):
                [z, p, k] = self.get_fun(n)
                '''w, mod, ph = ss.bode([b, a])
                group_delay = np.divide(-np.diff(ph), np.diff(w))  # d(ph)/d(w)'''
                w = np.linspace(wpn/10, wpn*10, num=1000)
                w, gd = self.get_GD(w, z=z, p=p, k=k)
                closest = (np.abs(w - wpn)).argmin()
                if gd[closest] >= (1 - self.data.tol) * self.data.GD and not np.isnan(gd[closest]):
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
        '''num = np.poly1d([1])
        den = np.poly1d([1])
        for k in range(1, n):
            ak = (-1)**k/factorial(k)
            poly = np.poly1d([1, 0])
            for i in range(k):
                poly = np.polymul(poly, np.poly1d([1, 0]))
            den = np.polyadd(den, ak * poly)
        den = np.polyval(den, [1, 0, 0])
        z, p, k = ss.tf2zpk(num, den)
        p = [pole for pole in p if pole.real < 0]
        '''
        poly = np.poly1d(1)
        for n in np.arange(1, n + 1):
            base = np.zeros(n + 1)
            base[0] = 1 / factorial(n)
            new_poly = np.poly1d(base)
            poly = np.polyadd(poly, new_poly)

        num = [1]
        den = np.polyval(poly, np.poly1d([1, 0, 0]))

        # z, p, k = ss.tf2zpk(num, den)
        # p = [pole for pole in p if pole.real > 0]

        g = 1
        poles = []
        for pole in 1j * den.roots:
            if pole.real < 0:
                new_pole = complex(pole.real if abs(pole.real) > 1e-10 else 0,
                                   pole.imag if abs(pole.imag) > 1e-10 else 0)
                g *= abs(new_pole)
                poles.append(new_pole)

        return [], poles, g
    '''
        return z, p, k'''
