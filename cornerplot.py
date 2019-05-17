#!/usr/bin/env python3
import emcee
import matplotlib.pyplot as plt
import numpy as np
import pylcurve.mcmc_utils as m
import corner as triangle
import matplotlib

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.size'] = 15
ndim = 14
nameList = np.array(['$T_{1}$', '$T_{2}$', '$M_{1}$', '$M_{2}$', '$i$',
                         '$R_{1}$', '$R_{2}$', r'$(T_{0}-57460.651)\times10^{5}$', r'$(P - 0.09986526)\times10^{9}$', '$\omega_{pulse}$',
                         '$q_{pulse}$', '$T_{pulse}$', r'$A_{pulse}\times10^8$','ln(prob)'])
chain1 = m.readchain('42000_run/chain.txt')
# chain = chain1[:,3000:,:]
# print(chain.shape)
fchain = m.flatchain(chain1, ndim, thin=3)[:, :]
bestPars = np.median(fchain, axis=0)
lolim, uplim = np.percentile(fchain, (16, 84), axis=0)
for name, par, lo, hi in zip(nameList, bestPars, lolim, uplim):
    print('{} = {} + {} - {}'.format(name, par, hi-par, par-lo))

fchain[:,7] = (fchain[:,7] - 57460.651) * 1e5
fchain[:,8] = (fchain[:,8] - 0.09986526) * 1e9
fchain[:,12] = fchain[:,12] * 1e8
bestPars[7] = (bestPars[7] - 57460.651) * 1e5
bestPars[8] = (bestPars[8] - 0.09986526) * 1e9
bestPars[12] = bestPars[12] * 1e8
# fig = m.thumbPlot(fchain, nameList)
fig = triangle.corner(fchain, labels=nameList, quantiles=[0.16,0.50,0.84])
axes = np.array(fig.axes).reshape((ndim, ndim))

for yi in range(ndim):
    for xi in range(yi):
        ax = axes[yi, xi]
        ax.xaxis.set_major_locator(plt.MaxNLocator(4))
        ax.yaxis.set_major_locator(plt.MaxNLocator(4))
#         ax.axvline(value1[xi], color="g")
#         ax.axhline(value1[yi], color="g")
        ax.plot(bestPars[xi], bestPars[yi], "sr")
axes[13,13].xaxis.set_major_locator(plt.MaxNLocator(4))
fig.savefig('42000_run/cornerPlot.pdf')
