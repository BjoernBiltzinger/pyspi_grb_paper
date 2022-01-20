from threeML import load_analysis_results
import numpy as np

res_spi2 = load_analysis_results("results/paper_band_pyspi.fits")
res_gbm2 = load_analysis_results("results/paper_band_gbm.fits")
res_osa2 = load_analysis_results("results/paper_band_osa.fits")

num_samples = 300
samples_spi = res_spi2.samples.T
np.random.shuffle(samples_spi)
samples_sel_spi = samples_spi[:num_samples]

samples_gbm = res_gbm2.samples.T
np.random.shuffle(samples_gbm)
samples_sel_gbm = samples_gbm[:num_samples]

samples_osa = res_osa2.samples.T
np.random.shuffle(samples_osa)
samples_sel_osa = samples_osa[:num_samples]

from astromodels import Band, Log_uniform_prior, Uniform_prior,PointSource, Model
band1 = Band()
band1.K.prior = Log_uniform_prior(lower_bound=1e-6, upper_bound=1e4)
band1.alpha.set_uninformative_prior(Uniform_prior)
band1.beta.set_uninformative_prior(Uniform_prior)
band1.xp.prior = Uniform_prior(lower_bound=10,upper_bound=8000)
ps1 = PointSource('PySPI',ra=94.67830, dec=-70.99905, spectral_shape=band1)

model1 = Model(ps1)


e = np.geomspace(10,5000, 1000)
fig, ax = plt.subplots()
vals_spi = np.zeros((num_samples, len(e)))
for i, s in enumerate(samples_sel_spi):
    band1.K = s[0]
    band1.alpha = s[1]
    band1.xp = s[2]
    band1.beta = s[3]
    #ax.loglog(e, e*e*synch(e), color="red")
    vals_spi[i] = band1(e)

vals_gbm = np.zeros((num_samples, len(e)))
for i, s in enumerate(samples_sel_gbm):
    band1.K = s[0]
    band1.alpha = s[1]
    band1.xp = s[2]
    band1.beta = s[3]
    #ax.loglog(e, e*e*synch(e), color="blue")
    vals_gbm[i] = band1(e)

vals_osa = np.zeros((num_samples, len(e)))
for i, s in enumerate(samples_sel_osa):
    band1.K = s[0]
    band1.alpha = s[1]
    band1.xp = s[2]
    band1.beta = s[3]
    vals_osa[i] = band1(e)
    #ax.loglog(e, e*e*synch(e), color="green")

import matplotlib.pyplot as plt
plt.style.use("mplplotlibrc")
q = 95
fig, ax = plt.subplots()
color1 = "#544b3dff"
color2 = "#340068ff"
color3 = "#4cb944ff"
color4 = "#4f7cacff"
color5 = "#6d2e46ff"
mi = np.percentile(vals_spi, 50-q/2, axis=0)
ma = np.percentile(vals_spi, 50+q/2, axis=0)
ax.fill_between(e, e**2*mi, e**2*ma, color=color3, alpha=1, label="PySPI")

#mi = np.percentile(vals_gbm, 50-q/2, axis=0)
#ma = np.percentile(vals_gbm, 50+q/2, axis=0)
#ax.fill_between(e, e**2*mi, e**2*ma, color="blue", alpha=0.5)

mi = np.percentile(vals_osa, 50-q/2, axis=0)
ma = np.percentile(vals_osa, 50+q/2, axis=0)
ax.fill_between(e, e**2*mi, e**2*ma, color=color2, alpha=0.5, label="Official Tools")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(100,4000)
ax.set_ylim(300,5000)
ax.legend(loc=2)
ax.set_xlabel("Energy [keV]")
ax.set_ylabel(r"$\nu F \nu$ [keV cm$^{-2}$ s$^{-1}$]")
fig.savefig("band_pyspi_osa.pdf")

q = 95
fig, ax = plt.subplots()
color1 = "#544b3dff"
color2 = "#340068ff"
color3 = "#4cb944ff"
color4 = "#4f7cacff"
color5 = "#6d2e46ff"
mi = np.percentile(vals_spi, 50-q/2, axis=0)
ma = np.percentile(vals_spi, 50+q/2, axis=0)
ax.fill_between(e, e**2*mi, e**2*ma, color=color3, alpha=1, label="PySPI")


mi = np.percentile(vals_gbm, 50-q/2, axis=0)
ma = np.percentile(vals_gbm, 50+q/2, axis=0)
ax.fill_between(e, e**2*mi, e**2*ma, color=color2, alpha=0.5, label="GBM")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(100,4000)
ax.set_ylim(300,5000)
ax.legend(loc=2)
ax.set_xlabel("Energy [keV]")
ax.set_ylabel(r"$\nu F \nu$ [keV cm$^{-2}$ s$^{-1}$]")
fig.savefig("band_pyspi_gbm.pdf")
