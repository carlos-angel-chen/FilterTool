import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from copy import copy
from back.FilterClass import FilterType, FilterData, ApproxType
from back.Approx.butterworth import Butterworth
from back.Approx.bessel import Bessel
from back.Approx.legendre import Legendre
from back.Approx.cheby1 import ChebyI
from back.Approx.cheby2 import ChebyII
from back.Approx.cauer import Cauer
from back.Approx.gauss import Gauss

class FilterSpace:
    def __init__(self):
        self.filters = []       # Arreglo de filtros
        self.w_unit = "Hz"      # Unidad de frecuencia
        self.mod_unit = "dB"    # Unidad de módulo
        self.ph_unit = "°"      # Unidad de fase

    # addFilter: Recibe parámetros para el filtro y si tienen sentido, lo crea.
    # Devuelve True si pudo crearlo, False si no.
    # OJO: LAS FRECUENCIAS SE INGRESAN EN RAD/S (Chaquear esto desde el front)
    def addFilter(self, filter_type, approx, wp, wa, Ap, Aa, des, G=1, n=None, Q=None, nmin=None, nmax=None, Qmax=None, rp=None, GD=None, tol=None):
        m = self.check_filter(filter_type, approx, wp, wa, Ap, Aa)
        if m != "":
            print("No se pudo crear el filtro")
            return m
        wp, wa = self.check_symmetry(filter_type, wp, wa)
        f = switch_atypes.get(approx)(filter_type, wp, wa, Ap, Aa, des/100, G, n, Q, nmin, nmax, Qmax, rp, GD, tol)
        f.add_name_index(self.get_name_index())
        if f.type != FilterType.ERR:
            self.filters.append(f)
        else:
            print("Error al crear el filtro")
            del f
        return ""

    # delFilter: Saca el filtro del FilterSpace y lo destruye
    # Recibe el filtro (elemento) (Lo puedo cambiar al índice o nombre, lo que resulte más cómodo)
    def delFilter(self, f):
        self.filters.remove(f)
        del f
        return

    def get_name_index(self):
        index = None
        ixs = []
        for i in range(len(self.filters)):
            ixs.append(int(self.filters[i].name[1]))
        ixs.sort()
        for i in range(len(ixs)):
            if ixs[i] != i:
                index = i
                break
        if index is None:
            index = len(self.filters)
        return index

    def get_wminmax(self):
        wmin = []
        wmax = []
        for i in range(len(self.filters)):
            if self.filters[i].visibility:
                w = self.filters[i].get_wminmax()
                wmin.append(w[0])
                wmax.append(w[1])
        wmin = min(wmin)
        wmax = max(wmax)
        return wmin, wmax

    def plot_mod(self, ax, A=False):
        wmin, wmax = self.get_wminmax()
        wmin = wmin / (2 * np.pi)
        wmax = wmax / (2 * np.pi)
        w = np.linspace(wmin, wmax, int(100*wmax/wmin))
        cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        ax.grid()
        for i in range(len(self.filters)):
            if self.filters[i].visibility:
                self.filters[i].plot_mod(ax, cycle[i % len(cycle)], w, A)
        ax.legend(loc="best")
        if not A: ax.set_title("Frequency response - Module")
        else: ax.set_title("Attenuation")
        ax.set_xlabel("$f$ [Hz]")
        if not A: ax.set_ylabel("$|H(s)|$ [dB]")
        else: ax.set_ylabel("A [dB]")
        ax.set_xlim([wmin, wmax])
        return

    def plot_ph(self, ax):
        wmin, wmax = self.get_wminmax()
        wmin = wmin / (2 * np.pi)
        wmax = wmax / (2 * np.pi)
        w = np.linspace(wmin, wmax, int(100*wmax/wmin))
        cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        ax.grid()
        for i in range(len(self.filters)):
            if self.filters[i].visibility:
                self.filters[i].plot_ph(ax, cycle[i % len(cycle)], w)
        ax.legend(loc="best")
        ax.set_title("Frequency response - Phase")
        ax.set_xlabel("$f$ [Hz]")
        ax.set_ylabel("$\\angle{H(s)}$ [dB]")
        ax.set_xlim([wmin, wmax])
        return

    def plot_zp(self, ax):
        cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        ax.grid()
        ax.scatter(0, 0, marker='.', edgecolors="None", facecolors="None")
        for i in range(len(self.filters)):
            if self.filters[i].visibility:
                self.filters[i].plot_zp(ax, cycle[i % len(cycle)])
        ax.legend(loc="best")
        ax.set_title("Poles and Zeros")
        ax.set_xlabel("$\\alpha$ $[\\frac{rad}{s}]$")
        ax.set_ylabel("$j \omega$ $[\\frac{rad}{s}]$")
        return

    def plot_gd(self, ax):
        wmin, wmax = self.get_wminmax()
        wmin = wmin / (2 * np.pi)
        wmax = wmax / (2 * np.pi) / 3
        w = np.linspace(wmin, wmax, int(100 * wmax / wmin))
        cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
        ax.grid()
        for i in range(len(self.filters)):
            if self.filters[i].visibility:
                self.filters[i].plot_gd(ax, cycle[i % len(cycle)], w)
        ax.legend(loc="best")
        ax.set_title("Group Delay")
        ax.set_xlabel("$f$ [Hz]")
        ax.set_ylabel("$\\frac{d(\\angle{H(s)})}{d (f)}$ [dB]")
        ax.set_xlim([wmin, wmax])
        return

    # check_filter: Revisa que el filtro sea válido. Devuelve True si lo es, False si no.
    def check_filter(self, filter_type, approx, wp, wa, Ap, Aa):
        m = ""
        m = self.check_freq(filter_type, wp)
        if m == "":
            m = self.check_freq(filter_type, wa)
        if m == "" and filter_type == FilterType.LP and not wp < wa:
            m = "El orden de las frecuencias de atenuación y paso no corresponde al de un filtro pasa bajos"
        if m == "" and filter_type == FilterType.HP and not wa < wp:
            m = "El orden de las frecuencias de atenuación y paso no corresponde al de un filtro pasa altos"
        if m == "" and filter_type == FilterType.BP and not (wa[0] < wp[0] < wp[1] < wa[1]):
            m = "El orden de las frecuencias de atenuación y paso no corresponde al de un filtro pasa banda"
        elif m == "" and filter_type == FilterType.BR and not (wp[0] < wa[0] < wa[1] < wp[1]):
            m = "El orden de las frecuencias de atenuación y paso está mal"
        elif m == "" and filter_type == FilterType.GD and not (approx != ApproxType.B or approx != ApproxType.G):
            m = "Sólo se permiten filtros de retardo de grupo con aproximaciones de Bessel o de Gauss"
        #elif m == "" and (approx == ApproxType.B or approx == ApproxType.G) and filter_type != FilterType.GD:
        #    m = "Las aproximaciones de Bessel o Gauss deben ser de retardo de grupo"
        if filter_type != FilterType.GD and Ap > Aa:
            m = "Ap no puede ser mayor que Aa"
        return m

    # check_freq: Revisa que el formato de la frecuencia sea consistente con el tipo.
    def check_freq(self, filter_type, w):
        m = ""
        try:
            len_w = len(w)
        except TypeError:
            len_w = 1
        if (filter_type == FilterType.LP or filter_type == FilterType.HP or filter_type == FilterType.GD) and len_w != 1:
            m = "ERROR: La frecuencia de paso o atenuación ingresada no es un único número"
        elif (filter_type == FilterType.BP or filter_type == FilterType.BR) and len_w != 2:
            m = "ERROR: Las frecuencias de paso o atenuación ingresadas no son un arreglo"
        return m

    def check_symmetry(self, filter_type, wp, wa):
        if filter_type == FilterType.BP:
            if wp[0] * wp[1] <= wa[0] * wa[1]:
                wa[1] = (wp[0] * wp[1]) / wa[0]
            else:
                wa[0] = (wp[0] * wp[1]) / wa[1]
        elif filter_type == FilterType.BR:
            if wa[0] * wa[1] <= wp[0] * wp[1]:
                wp[1] = (wa[0] * wa[1]) / wp[0]
            else:
                wp[0] = (wa[0] * wa[1]) / wp[1]
        return wp, wa

def butterworth(filter_type, wp, wa, Ap, Aa, des, G, n, Q, nmin, nmax, Qmax, rp, GD, tol):
    data = FilterData(wp, wa, Ap, Aa, des, G)
    f = Butterworth(filter_type, data, n, Q, nmin, nmax, Qmax, GD)
    return f

def cheby1(filter_type, wp, wa, Ap, Aa, des, G, n, Q, nmin, nmax, Qmax, rp, GD, tol):
    data = FilterData(wp, wa, Ap, Aa, des, G)
    f = ChebyI(filter_type, data, n, Q, nmin, nmax, Qmax, rp, GD)
    return f

def cheby2(filter_type, wp, wa, Ap, Aa, des, G, n, Q, nmin, nmax, Qmax, rp, GD, tol):
    data = FilterData(wp, wa, Ap, Aa, des, G)
    f = ChebyII(filter_type, data, n, Q, nmin, nmax, Qmax, GD)
    return f

def legendre(filter_type, wp, wa, Ap, Aa, des, G, n, Q, nmin, nmax, Qmax, rp, GD, tol):
    data = FilterData(wp, wa, Ap, Aa, des, G)
    f = Legendre(filter_type, data, n, Q, nmin, nmax, Qmax, GD)
    return f

def cauer(filter_type, wp, wa, Ap, Aa, des, G, n, Q, nmin, nmax, Qmax, rp, GD, tol):
    data = FilterData(wp, wa, Ap, Aa, des, G)
    f = Cauer(filter_type, data, n, Q, nmin, nmax, Qmax, GD)
    return f

def bessel(filter_type, wp, wa, Ap, Aa, des, G, n, Q, nmin, nmax, Qmax, rp, GD, tol):
    data = FilterData(wp, wa, Ap, Aa, des, G)
    f = Bessel(filter_type, data, n, Q, nmin, nmax, Qmax, GD, tol/100 if tol is not None else None)
    return f

def gauss(filter_type, wp, wa, Ap, Aa, des, G, n, Q, nmin, nmax, Qmax, rp, GD, tol):
    data = FilterData(wp, wa, Ap, Aa, des, G)
    f = Gauss(filter_type, data, n, Q, nmin, nmax, Qmax, GD, tol/100 if tol is not None else None)
    return f

# SWITCH
switch_atypes = {
    0: butterworth,
    1: cheby1,
    2: cheby2,
    3: legendre,
    4: cauer,
    5: bessel,
    6: gauss
}

# plot_template: Dibuja la plantilla.
# Recibe: - ax (axis)
#         - ftype (Tipo de filtro)
#         - fdata (FilterData: wp, wa, Aa, Ap, des)
#         - A: Atenuación (True) o Ganancia (False)
def plot_template(ax, ftype, fdata, A=True, N=False):
    if not A:
        Ap = - copy(fdata.Ap)
        Aa = - copy(fdata.Aa)
        G = fdata.G
        #ax.set_ylim([Aa*4 - Ap, Aa/Ap])
    else:
        Ap = copy(fdata.Ap)
        Aa = copy(fdata.Aa)
        G = 1
        #ax.set_ylim([-Aa/Ap, Aa * 4 - Ap])

    rp = None
    ra = None
    r2 = None

    wp = np.array(fdata.wp) / (2 * np.pi)
    wa = np.array(fdata.wa) / (2 * np.pi)

    if ftype == FilterType.LP:
        if N:
            wp = np.array(1)
            wa = np.array(fdata.wan)
        rp = Rectangle((wp/10, Ap + 20 * np.log10(G)), wp - wp/10, Aa*4, color="orange", alpha=0.4)
        ra = Rectangle((wa, 20 * np.log10(G)), wa*10 - wa, Aa, color="orange", alpha=0.4)
        ax.set_xlim([wp/10, wa * 10 - wa])

    elif ftype == FilterType.HP:
        if N:
            wp = np.array(fdata.wan)
            wa = np.array(1)
        ra = Rectangle((wa / 10, 20 * np.log10(G)), wa - wa / 10, Aa, color="orange", alpha=0.4)
        rp = Rectangle((wp, Ap + 20 * np.log10(G)), wp * 10 - wp, Aa*4 - Ap, color="orange", alpha=0.4)
        ax.set_xlim([wa/10, wp * 10 - wp])

    elif ftype == FilterType.BP:
        ra = Rectangle((wa[0] / 10, 20 * np.log10(G)), wa[0] - wa[0] / 10, Aa, color="orange", alpha=0.4)
        rp = Rectangle((wp[0], Ap + 20 * np.log10(G)), wp[1] - wp[0], Aa * 4 - Ap, color="orange", alpha=0.4)
        r2 = Rectangle((wa[1], 20 * np.log10(G)), wa[1]*10 - wa[1], Aa, color="orange", alpha=0.4)
        ax.set_xlim([wa[0]/10, wa[1]*10 - wa[1]])

    elif ftype == FilterType.BR:
        rp = Rectangle((wp[0]/10, Ap + 20 * np.log10(G)), wp[0] - wp[0]/10, Aa*4 - Ap, color="orange", alpha=0.4)
        ra = Rectangle((wa[0], 20 * np.log10(G)), wa[1] - wa[0], Aa, color="orange", alpha=0.4)
        r2 = Rectangle((wp[1], Ap + 20 * np.log10(G)), wp[1] * 10 - wp[1], Aa*4 - Ap, color="orange", alpha=0.4)
        ax.set_xlim([wp[0]/10, wp[1]*10 - wp[1]])

    elif ftype == FilterType.GD:
        ax.set_xlim([wp/10, wp * 10])

    if ftype != FilterType.GD:
        ax.add_patch(rp)
        ax.add_patch(ra)
    if r2 is not None: ax.add_patch(r2)

    return

