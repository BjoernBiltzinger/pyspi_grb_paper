from chainconsumer import ChainConsumer
import numpy as np


def loadtxt2d(intext):
        try:
            return np.loadtxt(intext, ndmin=2)
        except:
            return np.loadtxt(intext)

c = ChainConsumer()
c.configure(plot_hists=False, kde=1.0)
chain = loadtxt2d('./chains/PYSPI_BAND_post_equal_weights.dat')

c.add_chain(chain[:,:4], parameters=['K', r'$\alpha$', r'$E_{peak}$', r'$\beta$'], name='PYSPI')

chain = loadtxt2d('./chains/GBM_BAND_post_equal_weights.dat')

c.add_chain(chain[:,:4], parameters=['K', r'$\alpha$', r'$E_{peak}$', r'$\beta$'], name='GBM')

c.configure(plot_hists=False, kde=1.0, shade_alpha=0.5)

c.plotter.plot(filename="pyspi_vs_gbm_band.pdf",
               parameters=['K', r'$\alpha$', r'$E_{peak}$', r'$\beta$']);
