import numpy as np
from back.backend import FilterSpace, FilterType, ApproxType, plot_template
import matplotlib.pyplot as plt

FS = FilterSpace()
#FS.addFilter(FilterType.LP, ApproxType.BW, 1000 * (2 * np.pi), 5000 * (2 * np.pi), 0.5, 30, 100, 1, n=9, rp=1, GD=1, nmin=1, nmax=20, Qmax=150)
#FS.addFilter(FilterType.LP, ApproxType.C, 1000 * (2 * np.pi), 3000 * (2 * np.pi), 3, 30, 0, rp=1, GD=1, nmin=1, nmax=20, Qmax=150)
#FS.addFilter(FilterType.LP, ApproxType.CH1, 1000 * (2 * np.pi), 3000 * (2 * np.pi), 3, 30, 0, rp=1, GD=1, nmin=1, nmax=15, Qmax=150)
#FS.addFilter(FilterType.HP, ApproxType.BW, 4000 * (2 * np.pi), 1000 * (2 * np.pi), 3, 30, 0, 1, rp=1, GD=1, nmin=1, nmax=20, Qmax=150)
#FS.addFilter(FilterType.BP, ApproxType.BW, [2E3 * (2 * np.pi), 3E3 * (2 * np.pi)], [1E3 * (2 * np.pi), 4E3 * (2 * np.pi)], 3, 30, 100, 1, nmin=1, nmax=15, Qmax=150)
#FS.addFilter(FilterType.BP, ApproxType.LG, [2 * (2 * np.pi), 4 * (2 * np.pi)], [1 * (2 * np.pi), 5 * (2 * np.pi)], 3, 20, 0, nmin=1, nmax=15, Qmax=150)
#FS.addFilter(FilterType.BR, ApproxType.CH2, [1 * (2 * np.pi), 5 * (2 * np.pi)], [2 * (2 * np.pi), 4 * (2 * np.pi)], 0.5, 20, 0, 10, rp=1, nmin=1, nmax=15, Qmax=150)
#FS.addFilter(FilterType.BR, ApproxType.C, [1, 5], [2, 4], 3, 20, 100, rp=1, nmin=1, nmax=15, Qmax=150)
FS.addFilter(FilterType.GD, ApproxType.B, 10 * (2 * np.pi), 15 * (2 * np.pi), 3, 30, 0, tol=10, GD=1E-2, nmin=1, nmax=15, Qmax=150)
#FS.addFilter(FilterType.GD, ApproxType.G, 10 * (2 * np.pi), 15 * (2 * np.pi), 3, 30, 0, tol=10, GD=1E-2, nmin=1, nmax=15, Qmax=150)
fil = FS.filters[0]
#fil.print_self()

print("Pole pairs: ", FS.filters[0].get_pole_pairs())
print("Zero pairs: ", FS.filters[0].get_zero_pairs())
#FS.filters[0].add_stage(FS.filters[0].zeros, FS.filters[0].poles)
FS.filters[0].get_stages()

for i in range(len(FS.filters[0].stages)):
    ns = ""
    num = FS.filters[0].stages[i][0]
    if len(num) == 3:
        ns = str(num[0]) + "s^2 + " + str(num[1]) + "s + " + str(num[2])
    elif len(num) == 2:
        ns = str(num[0]) + "s + " + str(num[1])
    elif len(num) == 1:
        ns = str(num[0])
    print(" \t \t  " + ns)
    print(FS.filters[0].stage_names[i] + ": " + "--------------------------------" + " Order: " + str(FS.filters[0].get_stage_n(i)) + " Q: " + str(FS.filters[0].get_stage_Q(i)))
    ds = ""
    den = FS.filters[0].stages[i][1]
    if len(den) == 3:
        ds = str(den[0]) + "s^2 + " + str(den[1]) + "s + " + str(den[2])
    elif len(num) == 2:
        ds = str(den[0]) + "s + " + str(den[1])
    elif len(num) == 1:
        ds = str(den[0])
    print(" \t \t  " + ds)
    print("\n")

# # BODE
# fig, ax = plt.subplots(2, 1)
# axmod, axph = ax
# plot_template(axmod, fil.type, fil.data, False)
# FS.plot_mod(axmod, A=False)
# FS.plot_ph(axph)
'''b, a = fil.num, fil.den
wmin, wmax = fil.get_wminmax()
#wmin = min(fil.data.wp, fil.data.wa)/10 if fil.type <= FilterType.HP elif fil.type <= FilterType.GD else min(fil.data.wp[0], fil.data.wa[0])/10
#wmax = max(fil.data.wp, fil.data.wa)*10 if fil.type <= FilterType.HP else max(fil.data.wp[1], fil.data.wa[1])*10
w = np.linspace(wmin, wmax, int(wmax/wmin * 10))
#H = ss.TransferFunction(b, a)
fil.plot_mod(axmod, w)
fil.plot_ph(axph, w)
fig.suptitle("Filter frequency response")
axmod.set_xlabel('Frequency [radians / second]')
axmod.set_ylabel('Amplitude [dB]')
axmod.grid()
axph.set_xlabel('Frequency [radians / second]')
axph.set_ylabel('Phase [°]')
axph.grid()
#plt.ylim(-60, 10)
#plt.grid(which='both', axis='both')
#plt.show()'''

# BO2
fig3, ax3 = plt.subplots(1, 1)
FS.filters[0].plot_selected_stages(ax3, [1])


# # POLOS Y CEROS
# fig2, ax2 = plt.subplots(1, 1)
# FS.plot_zp(ax2)
'''fig2.suptitle("Poles and Zeros")
ax2.scatter(fil.zeros.real, fil.zeros.imag, marker='o', edgecolors="red", facecolors="None")
ax2.scatter(fil.poles.real, fil.poles.imag, marker='x', color="blue")
ax2.set_xlabel('Real')
ax2.set_ylabel('Imaginary')
ax2.grid()'''

# # RETARDO DE GRUPO
# figGD, axGD = plt.subplots(1, 1)
# FS.plot_gd(axGD)
'''wmin, wmax = fil.get_wminmax()
#wmin = min(fil.data.wp, fil.data.wa)/10 if fil.type <= FilterType.HP elif fil.type <= FilterType.GD else min(fil.data.wp[0], fil.data.wa[0])/10
#wmax = max(fil.data.wp, fil.data.wa)*10 if fil.type <= FilterType.HP else max(fil.data.wp[1], fil.data.wa[1])*10
w = np.linspace(0, wmax*2/3, int(wmax/wmin * 10))
fil.plot_gd(axGD, w)
#axGD.set_ylim([0, 1])
figGD.suptitle("Filter group delay")
axGD.set_xlabel('Frequency [radians / second]')
axGD.set_ylabel('Group Delay')
axGD.grid()'''

plt.show()




