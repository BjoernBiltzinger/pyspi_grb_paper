from pyspi.utils.data_builder.time_series_builder import TimeSeriesBuilderSPI
from pyspi.utils.response.spi_response_data import ResponseDataRMF
from pyspi.utils.response.spi_response import ResponseRMFGenerator
from pyspi.utils.response.spi_drm import SPIDRM
from pyspi.utils.livedets import get_live_dets
from pyspi.SPILike import SPILikeGRB

import numpy as np
import matplotlib.pyplot as plt

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
ebounds = np.geomspace(25, 8000, 200)
ebounds_sgl = ebounds[ebounds<400]
ebounds_psd = ebounds[np.logical_and(ebounds>400, ebounds<2700)]
ebounds_sgl2 = ebounds[ebounds>2700]
ein = np.geomspace(20,8000,100)

rsp_base = ResponseDataRMF.from_version(4)
spilikes_sgl = []
spilikes_sgl2 = []
spilikes_psd = []

for d in get_live_dets(time=grb_time, event_types=["single"]):
    drm_gen_sgl = ResponseRMFGenerator.from_time(grb_time,  d,
                                            ebounds_sgl, ein,
                                            rsp_base)

    sd_sgl = SPIDRM(drm_gen_sgl, 94.67830, -70.99905)

    tsb_sgl = TimeSeriesBuilderSPI.from_spi_grb(f"SPIDet{d}",
                                                d,
                                                grb_time,
                                                response=sd_sgl,
                                                sgl_type="both",
                                                )
    #tsb_sgl.set_active_time_interval(active_time)
    tsb_sgl.set_background_interval(background_time_interval_1_spi,
                                    background_time_interval_2_spi,
                                    fit_poly=False
                                   )
    tsb_sgl.set_active_time_interval(active_time)
    sl_sgl = tsb_sgl.to_spectrumlike(extract_measured_background=True)
    spilikes_sgl.append(SPILikeGRB.from_spectrumlike(sl_sgl,
                                                      free_position=False))

    drm_gen_sgl2 = ResponseRMFGenerator.from_time(grb_time,  d,
                                            ebounds_sgl2, ein,
                                            rsp_base)

    sd_sgl2 = SPIDRM(drm_gen_sgl2, 94.67830, -70.99905)

    tsb_sgl2 = TimeSeriesBuilderSPI.from_spi_grb(f"SPIDet{d}High",
                                                d,
                                                grb_time,
                                                response=sd_sgl2,
                                                sgl_type="both",
                                                )
    #tsb_sgl.set_active_time_interval(active_time)
    tsb_sgl2.set_background_interval(background_time_interval_1_spi,
                                    background_time_interval_2_spi,
                                    fit_poly=False
                                   )
    tsb_sgl2.set_active_time_interval(active_time)
    sl_sgl2 = tsb_sgl2.to_spectrumlike(extract_measured_background=True)
    spilikes_sgl2.append(SPILikeGRB.from_spectrumlike(sl_sgl2,
                                                      free_position=False))
    drm_gen_psd = ResponseRMFGenerator.from_time(grb_time,  d,
                                            ebounds_psd, ein,
                                            rsp_base)

    sd_psd = SPIDRM(drm_gen_psd, 94.67830, -70.99905)

    tsb_psd = TimeSeriesBuilderSPI.from_spi_grb(f"SPIDet{d}MID",
                                                d,
                                                grb_time,
                                                response=sd_psd,
                                                sgl_type="psd",
                                                )
    #tsb_sgl.set_active_time_interval(active_time)
    tsb_psd.set_background_interval(background_time_interval_1_spi,
                                    background_time_interval_2_spi,
                                    fit_poly=False
                                   )
    tsb_psd.set_active_time_interval(active_time)
    sl_psd = tsb_psd.to_spectrumlike(extract_measured_background=True)
    spilikes_psd.append(SPILikeGRB.from_spectrumlike(sl_psd,
                                                      free_position=False))


from threeML import TimeSeriesBuilder, DataList, BayesianAnalysis
# GBM Specific Input
background_time_interval_1_gbm = "-30--10"
background_time_interval_2_gbm = "150-200"

# General Input
active_time_gbm = '65-73'#'67-72'
dets = ["n0","n1","n2","n4","b0"]
sls1 = []
tss1 = []
for det in dets:
    tte_file = "gbmfiles/glg_tte_{}_bn120711115_v00.fit".format(det)
    rsp2_file="gbmfiles/glg_cspec_{}_bn120711115_v00.rsp2".format(det)
    ts = TimeSeriesBuilder.from_gbm_tte('gbm{}'.format(det), tte_file, rsp2_file,poly_order=0)
    ts.set_active_time_interval(active_time_gbm)
    ts.set_background_interval(background_time_interval_1_gbm, background_time_interval_2_gbm)
    sl = ts.to_spectrumlike()
    if det[0]=="b":
        print("hallo")
        sl.set_active_measurements('250-25000')
    else:
        sl.set_active_measurements('8.1-700')
    sls1.append(sl)
    tss1.append(ts)

from threeML import load_analysis_results
res_both = load_analysis_results("/home/bjorn/Downloads/result_both3_syn_grb.fits")
datalist = DataList(*spilikes_sgl, *spilikes_sgl2, *spilikes_psd, *sls1)
ba_gbm_band_1 = BayesianAnalysis(res_both.optimized_model, datalist)
for i, s in enumerate(sls1):
    if i!=0:
        s.use_effective_area_correction(0.6,1.4)
for i, s in enumerate(spilikes_sgl):
    s.use_effective_area_correction(0.7,1.3)

for i, s in enumerate(spilikes_psd):
    s.use_effective_area_correction(0,1)

from threeML import display_spectrum_model_counts

plt.style.use("mplplotlibrc")
colors=[color1,color4,color2,color3,color5]
f = display_spectrum_model_counts(ba_gbm_band_1,
                                     data=['SPIDet13', 'SPIDet14', 'SPIDet15', 'SPIDet16'],
                                     data_per_plot=5, min_rate=0.3,
                                     model_colors=colors, data_colors=colors,
                                     show_residuals=False);

f.axes[0].get_legend().remove()
lgd = f.legend(loc='center left', bbox_to_anchor=(1, 0.6))
f.savefig("fit_plot.pdf")
