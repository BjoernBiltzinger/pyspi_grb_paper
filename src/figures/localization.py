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

chain = loadtxt2d('./chains/PYSPI_BAND_loc2_post_equal_weights.dat')

c.add_chain(chain[:,:6], parameters=['ra', 'dec', 'K', r'$\alpha$', r'$E_{peak}$', r'$\beta$'],
            name='PYSPI', color=color3)

c.configure(plot_hists=False, kde=1.0, shade_alpha=0.5)

c.plotter.plot(filename="loc.pdf",
               parameters=['ra', 'dec'],
               truth=[94.67830, -70.99905]);
