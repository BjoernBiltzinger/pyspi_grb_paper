from chainconsumer import ChainConsumer
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("matplotlibrc")

color1 = "#544b3d"
color2 = "#340068"
color3 = "#4cb944"
color4 = "#4f7cac"
color5 = "#6d2e46"

def loadtxt2d(intext):
        try:
            return np.loadtxt(intext, ndmin=2)
        except:
            return np.loadtxt(intext)

c = ChainConsumer()

chain = loadtxt2d('./chains/GBM_SYN_post_equal_weights.dat')

c.add_chain(chain[:,:4], parameters=['K','B', 'p', r'$\gamma_{cool}$'],
            name='GBM', color=color2)

chain = loadtxt2d('./chains/PYSPI_SYN_post_equal_weights.dat')

c.add_chain(chain[:,:4], parameters=['K','B', 'p', r'$\gamma_{cool}$'], name='PYSPI',
            color=color1)

chain = loadtxt2d('./chains/BOTH_SYN_post_equal_weights.dat')

c.add_chain(chain[:,:4], parameters=['K','B', 'p', r'$\gamma_{cool}$'], name='Combined',
            color=color4)

c.configure(plot_hists=False, kde=1.0, shade_alpha=0.5)

c.plotter.plot(filename="pyspi_and_gbm_syn.pdf",
               parameters=['B', 'p', r'$\gamma_{cool}$']);
