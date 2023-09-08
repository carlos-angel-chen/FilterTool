import numpy as np
import scipy.signal as ss
from scipy.special import eval_legendre, legendre
from back.FilterClass import Filter, ApproxType, FilterType

class Legendre(Filter):
    def __init__(self, filter_type, filter_data, n, Q, nmin, nmax, Qmax, GD):
        super().__init__(filter_type, ApproxType.LG, filter_data, n, Q, nmin, nmax, Qmax, None, GD, None)

    def get_best_n(self, nmin, nmax):
        '''wan = self.get_wan()
        comp = np.log10(self.get_eps(self.data.Aa)**2 / self.get_eps(self.data.Ap)**2)'''
        n = nmin
        for i in range(nmax - nmin):
            '''l_n = self.ln(n)
            eva = np.polyval(l_n, [wan**2])[0]
            if eva >= comp:
                break
            '''
            z, p, k = self.get_fun(n)
            wap = np.linspace(min(1, self.get_wan()), max(1, self.get_wan()), 2)
            wap, mod, ph = ss.bode([z, p, k], w=wap)
            if mod[0] >= -self.data.Ap * 1.0001 and mod[1] <= -self.data.Aa * 0.9999:
                break
            n = n + 1
        return n

    def ln(self, n):
        if n == 0:
            return [0]

        if n % 2:  # n impar
            k = (n - 1) // 2
            a0 = 1 / (np.sqrt(2) * (k + 1))

            poly = np.poly1d([a0])
            for i in range(1, k + 1):
                ai = a0 * (2 * i + 1)
                new_poly = ai * legendre(i)
                poly = np.polyadd(poly, new_poly)   # Sumatoria
            poly = np.polymul(poly, poly)  # Elevo al cuadrado

        else:  # n par
            k = (n - 2) // 2
            if k % 2:  # k impar
                a1 = 3 / np.sqrt((k + 1) * (k + 2))
                poly = np.poly1d(0)

                for i in range(1, k + 1):
                    if i % 2:  # i impar
                        ai = a1 * (2 * i + 1)/3
                        new_poly = ai * legendre(i)
                        poly = np.polyadd(poly, new_poly)   # Sumatoria
            else:  # k par
                a0 = 1 / np.sqrt((k + 1) * (k + 2))
                poly = np.poly1d(a0)

                for i in range(1, k + 1):
                    if not i % 2:  # i par
                        ai = a0 * (2 * i + 1)
                        new_poly = ai * legendre(i)
                        poly = np.polyadd(poly, new_poly)   # Sumatoria

            poly = np.polymul(poly, poly)  # Elevo al cuadrado
            poly = np.polymul(poly, np.poly1d([1, 1]))  # Multiplico por (x + 1)

        poly = np.polyint(poly)  # Integro
        x2 = np.poly1d([2, 0, -1])  # Borde superior
        x1 = np.poly1d([-1])  # Borde inferior

        Ln = np.polysub(np.polyval(poly, x2), np.polyval(poly, x1))

        return Ln

    def get_fun(self, n):
        l_n = self.ln(n)
        num = np.poly1d([1])
        den = self.data.eps**2 * np.polyval(l_n, np.poly1d([1, 0, 0]))
        den = np.polyadd(den, 1)
        z, p, g = ss.tf2zpk(num, den)
        p = [pole for pole in p if pole.real < 0]
        num, den = ss.zpk2tf(z, p, g)
        if num[-1] != 0:
            k = den[-1] / num[-1]
        else:
            k = 1
        return z, p, k * g



