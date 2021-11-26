from pyspi.utils.data_builder.time_series_builder import TimeSeriesBuilderSPI
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("matplotlibrc")
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
f.savefig("lightcurve.pdf")
