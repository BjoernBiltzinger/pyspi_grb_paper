from pyspi.utils.data_builder.time_series_builder import TimeSeriesBuilderSPI
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("matplotlibrc")
color1 = "#544b3d"
color2 = "#340068"
color3 = "#4cb944"
color4 = "#4f7cac"
color5 = "#6d2e46"

ebounds=np.geomspace(20,8000,100)
grb_time = "120711 024453" #(YYMMDD HHMMSS) - from GBM trigger time

tsb_psd = TimeSeriesBuilderSPI.from_spi_grb("SPIDet0",
                                            0,
                                            grb_time,
                                            ebounds=ebounds,
                                            sgl_type="psd",
                                            poly_order=0,
                                            )

tsb_non_psd = TimeSeriesBuilderSPI.from_spi_grb("SPIDet0",
                                            0,
                                            grb_time,
                                            ebounds=ebounds,
                                            sgl_type="sgl",
                                            poly_order=0,
                                            )

counts_psd = tsb_psd.time_series.count_per_channel_over_interval(-1000,0)
counts_non_psd = tsb_non_psd.time_series.count_per_channel_over_interval(-1000,0)

fig, ax = plt.subplots(1,1)
ax.step(ebounds[1:], counts_psd, label="PSD events", color=color1)
ax.step(ebounds[1:], counts_non_psd, label="Non-PSD events", color=color2)
ax.fill_betweenx(np.linspace(0,np.max(counts_non_psd),10),1400, 1900, alpha=0.5, color=color3, label="Main Electronic Noise Region")
ax.set_yscale("log")
ax.set_xscale("log")
ax.set_xlabel("Detected Energy [keV]")
ax.set_ylabel("Counts")
ax.legend()

fig.savefig("electronic_noise.pdf")
