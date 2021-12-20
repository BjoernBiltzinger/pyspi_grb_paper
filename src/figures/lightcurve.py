from pyspi.utils.data_builder.time_series_builder import TimeSeriesBuilderSPI
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("matplotlibrc")

color1 = "#544b3d"
color2 = "#340068"
color3 = "#4cb944"
color4 = "#4f7cac"
color5 = "#6d2e46"

grb_time = "120711 024453" #(YYMMDD HHMMSS) - from GBM trigger time
background_time_interval_1_spi = "-500--10"
background_time_interval_2_spi = "150-1000"

tsb_sgl = TimeSeriesBuilderSPI.from_spi_grb("SPIDet0",
                                            0,
                                            grb_time,
                                            ebounds=np.linspace(20,8000,100),
                                            sgl_type="both",
                                            poly_order=0,
                                            )
tsb_sgl.set_background_interval(background_time_interval_1_spi,
                                background_time_interval_2_spi,
                                fit_poly=False
                               )

f = tsb_sgl.view_lightcurve(-300,500);

axis = f.axes[0]

axis.get_lines()[0].set_color(color1)
axis.collections[0].set_color(color3)
axis.collections[1].set_color(color3)
axis.get_lines()[0].set_label(None)
axis.collections[0].set_label(None)
axis.collections[1].set_label(None)

axis.legend()
axis.get_legend().remove()

f.savefig("lightcurve.pdf")
