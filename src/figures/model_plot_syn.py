from threeML import load_analysis_results
import numpy as np

import pynchrotron
res_spi = load_analysis_results("results/result_pyspi4_syn_grb.fits")
res_gbm = load_analysis_results("results/result_gbm3_syn_grb.fits")
res_both = load_analysis_results("results/result_both3_syn_grb.fits")

num_samples = 300
samples_spi = res_spi.samples.T
np.random.shuffle(samples_spi)
samples_sel_spi = samples_spi[:num_samples]

samples_gbm = res_gbm.samples.T
np.random.shuffle(samples_gbm)
samples_sel_gbm = samples_gbm[:num_samples]

samples_both = res_both.samples.T
np.random.shuffle(samples_both)
samples_sel_both = samples_both[:num_samples]

synch = pynchrotron.SynchrotronNumericalNormPeak()
synch.K = 100
synch.B = 1000
synch.index=4
synch.gamma_min= 1E5
cool_frac = 1E-2
max_frac = 1E2
synch.gamma_max.free = False
synch.index.bounds = (0, None)


e = np.geomspace(10,5000, 1000)
vals_spi = np.zeros((num_samples, len(e)))
for i, s in enumerate(samples_sel_spi):
    synch.K = s[0]
    synch.B = s[1]
    synch.index = s[2]
    synch.gamma_cool = s[3]
    vals_spi[i] = synch(e)

vals_gbm = np.zeros((num_samples, len(e)))
for i, s in enumerate(samples_sel_gbm):
    synch.K = s[0]
    synch.B = s[1]
    synch.index = s[2]
    synch.gamma_cool = s[3]

    vals_gbm[i] = synch(e)

vals_both = np.zeros((num_samples, len(e)))
for i, s in enumerate(samples_sel_both):
    synch.K = s[0]
    synch.B = s[1]
    synch.index = s[2]
    synch.gamma_cool = s[3]
    vals_both[i] = synch(e)

import matplotlib.pyplot as plt
plt.style.use("matplotlibrc")
q = 95
fig, ax = plt.subplots()
color1 = "#544b3dff"
color2 = "#340068ff"
color3 = "#4cb944ff"
color4 = "#4f7cacff"
color5 = "#6d2e46ff"
mi = np.percentile(vals_spi, 50-q/2, axis=0)
ma = np.percentile(vals_spi, 50+q/2, axis=0)
ax.fill_between(e, e**2*mi, e**2*ma, color=color3, alpha=1, label="SPI")


mi = np.percentile(vals_both, 50-q/2, axis=0)
ma = np.percentile(vals_both, 50+q/2, axis=0)
ax.fill_between(e, e**2*mi, e**2*ma, color=color2, alpha=0.5, label="GBM+SPI")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(100,4000)
ax.set_ylim(300,5000)
ax.legend(loc=2)
ax.set_xlabel("Energy [keV]")
ax.set_ylabel(r"$\nu F \nu$ [keV cm$^{-2}$ s$^{-1}$]")
fig.savefig("spi_combined.pdf")

q = 95
fig, ax = plt.subplots()


mi = np.percentile(vals_gbm, 50-q/2, axis=0)
ma = np.percentile(vals_gbm, 50+q/2, axis=0)
ax.fill_between(e, e**2*mi, e**2*ma, color=color3, alpha=1, label="GBM")

mi = np.percentile(vals_both, 50-q/2, axis=0)
ma = np.percentile(vals_both, 50+q/2, axis=0)
ax.fill_between(e, e**2*mi, e**2*ma, color=color2, alpha=0.6, label="GBM+SPI")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(100,4000)
ax.set_ylim(300,5000)
ax.set_xlabel("Energy [keV]")
ax.set_ylabel(r"$\nu F \nu$ [keV cm$^{-2}$ s$^{-1}$]")
ax.legend(loc=2)
fig.savefig("gbm_combined.pdf")
