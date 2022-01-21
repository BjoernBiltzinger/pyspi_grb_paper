from twopc import PPC
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("matplotlibrc")

color1 = "#544b3d"
color2 = "#340068"
color3 = "#4cb944"
color4 = "#4f7cac"
color5 = "#6d2e46"

p = PPC("ppc_output/both_syn_grb.h5")

f = p.detectors["gbmb0"].plot(
    bkg_subtract=False,
    levels=[95,68],
    colors=[color2, color3],
    lc=color4
)

f.savefig("b0_ppc.pdf")

f = p.detectors["gbmb0"].plot_qq(
    channel_energies=[],
    levels=[95,68],
    colors=[color2, color3],
    center_color=color4
)

f.savefig("b0_qq.pdf")
