from copy import copy
import numpy as np
import scipy.signal as ss
from scipy.spatial import KDTree

def get_stage_pairs(arr):
    pairs = []
    p = copy(arr)
    for i in range(len(p)):
        solo = True
        for j in range(i + 1, len(p)):
            if abs(p[i].real - p[j].real) < 1E-10 and abs(p[i].imag + p[j].imag) < 1E-10:
                pairs.append([p[i], p[j]])
                p = np.delete(p, j)
                solo = False
                break
            else:
                solo = True
        if solo:
            pairs.append([arr[i]])
        if len(pairs) * 2 >= len(arr):
            break
    return pairs

def get_pair_name(p):
    n = len(p)
    if n == 2:
        fo = (p[0] * p[1]).real/(2 * np.pi)**2
        try:
            Q = - ((p[0] + p[1]) / (p[0] * p[1])).real
        except RuntimeWarning: pass
        s = "Order " + str(n) + " - fo = " + format_unit(fo, 3) + " Hz - Q = {:.{p}e}".format(Q, p=3)
    elif n == 1:
        fo = np.abs(p[0].real / (2 * np.pi))
        s = "Order " + str(n) + " - fo = " + format_unit(fo, 3) + " Hz"
    else:
        s = "ERROR: Se ingresó una cantidad de polos o ceros distinta de 1 o 2"
    return s

def get_stage_tf(z, p, g):
    num, den = ss.zpk2tf(z, p, g)
    return num, den

def combine_tf(nums, dens):
    nums = [np.poly1d(num) for num in nums]
    dens = [np.poly1d(den) for den in dens]
    num = np.poly1d(1)
    for i in range(len(nums)):
        num = np.polymul(num, nums[i])
    den = np.poly1d(1)
    for i in range(len(dens)):
        den = np.polymul(den, dens[i])
    return num, den

def plot_stage(ax, num, den, c, n, w=None):
    if w is None:
        w, mod, k = ss.bode([num, den])
    else:
        w, mod, k = ss.bode([num, den], w)
    ax.semilogx(w, mod, color=c, label=n)
    return

def auto_stage(poles, zeross, BR=False):
    zeros = copy(zeross)
    pplus = keep_nonegatives(poles)
    z = keep_nonegatives(zeros)
    p = copy(pplus)
    pairs = [[[], pole] for pole in poles]
    for i in range(len(p)):
        if len(z) == 0:
            break
        p.sort(key=np.real, reverse=True)
        if not BR: ix = np.argmin(np.abs(p[0] - z))
        else: ix = np.argmax(np.abs(p[0] - z))
        pix = pplus.index(p[i])
        zis = zeros[ix]
        pairs[pix][0] = zis
        # pairs[poles.index(p[i])] = zeros[z.index(ix)]
        z.pop(ix)
        zeros.pop(ix)
    return pairs

def keep_nonegatives(arr):
    p = []
    for a in arr:
        if a[0].imag >= -1E-10:
            p.append(a[0])
        else:
            p.append(a[1])
    return p

# format_unit: Obtiene la unidad correcta y escala el número para que sea más fácil de leer
# Recibe a x como número y la devuelve como string
def format_unit(x, d=2):
    y = np.abs(x)
    if y < 1E-12:
        m = ""
    elif y < 1E-9:
        m = "p"         # Pico
        x = x / 1E-12
    elif y < 1E-6:
        m = "n"         # Nano
        x = x / 1E-9
    elif y < 1E-3:
        m = "u"         # Micro
        x = x / 1E-6
    elif y < 1:
        m = "m"         # Mili
        x = x / 1E-3
    elif y < 1E3:
        m = ""          # Normal
    elif y < 1E6:
        m = "k"         # Kilo
        x = x / 1E3
    elif y < 1E9:
        m = "M"         # Mega
        x = x / 1E6
    else:
        m = "G"         # Giga
        x = x / 1E9
    return "{:.{p}f}".format(x, p=d) + m


