from pyspi.utils.data_builder.time_series_builder import TimeSeriesBuilderSPI
from pyspi.utils.response.spi_response_data import ResponseDataRMF
from pyspi.utils.response.spi_response import ResponseRMFGenerator
from pyspi.utils.response.spi_drm import SPIDRM
import numpy as np
import matplotlib.pyplot as plt
plt.style.use("matplotlibrc")

color1 = "#544b3dff"
color2 = "#340068ff"
color3 = "#4cb944ff"
color4 = "#4f7cacff"
color5 = "#6d2e46ff"

grb_time = "120711 024453" #(YYMMDD HHMMSS) - from GBM trigger time
background_time_interval_1_spi = "-500--10"
background_time_interval_2_spi = "150-1000"
active_time = '65-73'
det_spi = 0
det_gbm = "n2"
ebounds_spi = np.linspace(20,8000,100)
ein = np.geomspace(20,8000,100)

rsp_base = ResponseDataRMF.from_version(4)
drm_gen = ResponseRMFGenerator.from_time(grb_time,  0,
                                        ebounds_spi, ein,
                                        rsp_base)

sd = SPIDRM(drm_gen, 94.67830, -70.99905)

tsb = TimeSeriesBuilderSPI.from_spi_grb("SPIDet0",
                                            det_spi,
                                            grb_time,
                                            response=sd,
                                            sgl_type="both",
                                            )
tsb.set_background_interval(background_time_interval_1_spi,
                                background_time_interval_2_spi,
                                fit_poly=False
                               )
tsb.set_active_time_interval(active_time)
f_spi = tsb.view_lightcurve(-20,200,0.5)

from threeML.utils.data_builders.time_series_builder import TimeSeriesBuilder
from threeML import silence_warnings
silence_warnings()
# GBM Specific Input
background_time_interval_1_gbm = "-30--10"
background_time_interval_2_gbm = "150-200"

# General Input
active_time_gbm = '65-73'
det = "n2"
sls1 = []
tss1 = []

from threeML.utils.data_download.Fermi_GBM.download_GBM_data import download_GBM_trigger_data
download_GBM_trigger_data("bn120711115", [det], ".")
tte_file = "glg_tte_{}_bn120711115_v00.fit.gz".format(det)
rsp2_file="glg_cspec_{}_bn120711115_v00.rsp2".format(det)
ts = TimeSeriesBuilder.from_gbm_tte('gbm{}'.format(det), tte_file, rsp2_file)
ts.set_active_time_interval(active_time_gbm)
ts.set_background_interval(background_time_interval_1_gbm,
                           background_time_interval_2_gbm,
                           fit_poly=False)
f_gbm = ts.view_lightcurve(-20,200,0.5)

fig, ax = plt.subplots(1,1,sharex=True)

lines = f_gbm.axes[0].get_lines()
x, y = lines[0].get_xydata().T
ax.plot(x,y, color=color1, label="Light Curve")
active_mask = np.logical_and(x>=ts.time_series.time_intervals.absolute_start,
                             x<=ts.time_series.time_intervals.absolute_stop)
ax.fill_between(x[active_mask], y[active_mask], 0, color=color4, alpha=0.4, label="Selection")
bkg_mask = np.logical_and(x>=ts.time_series.bkg_intervals[0].start,
                          x<=ts.time_series.bkg_intervals[0].stop)
ax.fill_between(x[bkg_mask], y[bkg_mask], 0, color=color3, alpha=0.4, label="Bkg. Selection")
bkg_mask = np.logical_and(x>=ts.time_series.bkg_intervals[1].start,
                          x<=ts.time_series.bkg_intervals[1].stop)
ax.fill_between(x[bkg_mask], y[bkg_mask], 0, color=color3, alpha=0.4)
ax.legend()
ax.set_title("GBM detector n2")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Rate (cnts/s)")
ax.set_ylim(1000)
ax.set_xlim(-20,200)
fig.savefig("gbm_lightcurve_ts.pdf")

fig, ax2 = plt.subplots(1,1,sharex=True)

lines = f_spi.axes[0].get_lines()
x, y = lines[0].get_xydata().T
ax2.plot(x,y, color=color1, label="Light Curve")
active_mask = np.logical_and(x>=tsb.time_series.time_intervals.absolute_start,
                             x<=tsb.time_series.time_intervals.absolute_stop)
ax2.fill_between(x[active_mask], y[active_mask], 0, color=color4, alpha=0.4, label="Selection")
bkg_mask = np.logical_and(x>=tsb.time_series.bkg_intervals[0].start,
                          x<=tsb.time_series.bkg_intervals[0].stop)
ax2.fill_between(x[bkg_mask], y[bkg_mask], 0, color=color3, alpha=0.4)
bkg_mask = np.logical_and(x>=tsb.time_series.bkg_intervals[1].start,
                          x<=tsb.time_series.bkg_intervals[1].stop)
ax2.fill_between(x[bkg_mask], y[bkg_mask], 0, color=color3, alpha=0.4, label="Bkg. Selection")
ax2.legend()
ax2.set_title("SPI detector 0")
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Rate (cnts/s)")
ax2.set_ylim(30)
ax2.set_xlim(-20,200)
fig.savefig("spi_lightcurve_ts.pdf")
