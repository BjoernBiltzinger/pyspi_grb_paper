from pyspi.utils.data_builder.time_series_builder import TimeSeriesBuilderSPI
from pyspi.utils.response.spi_response_data import ResponseDataRMF
from pyspi.utils.response.spi_response import ResponseRMFGenerator
from pyspi.utils.response.spi_drm import SPIDRM
from pyspi.utils.livedets import get_live_dets
from pyspi.SPILike import SPILikeGRB

import numpy as np
import matplotlib.pyplot as plt


#### General Input #####

grb_time = "120711 024453" #(YYMMDD HHMMSS) - from GBM trigger time
background_time_interval_1_spi = "-500--10"
background_time_interval_2_spi = "150-1000"
background_time_interval_1_gbm = "-30--10"
background_time_interval_2_gbm = "150-200"
active_time = '65-73'
ebounds = np.geomspace(25, 8000, 200)
ebounds_sgl = ebounds[ebounds<400]
ebounds_psd = ebounds[np.logical_and(ebounds>400, ebounds<2700)]
ebounds_sgl2 = ebounds[ebounds>2700]
ein = np.geomspace(20,8000,100)

#### INIT PYSPI plugins #####
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

#### INIT GBM plugins #####
from threeML import TimeSeriesBuilder
# General Input
dets = ["n0","n1","n2","n4","b0"]
sls1 = []
tss1 = []
for det in dets:
    tte_file = "glg_tte_{}_bn120711115_v00.fit".format(det)
    rsp2_file="glg_cspec_{}_bn120711115_v00.rsp2".format(det)
    ts = TimeSeriesBuilder.from_gbm_tte('gbm{}'.format(det), tte_file, rsp2_file,poly_order=0)
    ts.set_active_time_interval(active_time)
    ts.set_background_interval(background_time_interval_1_gbm, background_time_interval_2_gbm)
    sl = ts.to_spectrumlike()
    if det[0]=="b":
        print("hallo")
        sl.set_active_measurements('250-25000')
    else:
        sl.set_active_measurements('8.1-700')
    sls1.append(sl)
    tss1.append(ts)
from astromodels import Band, Log_uniform_prior, Uniform_prior,PointSource, Model
band1 = Band()
band1.K.prior = Log_uniform_prior(lower_bound=1e-6, upper_bound=1e4)
band1.alpha.set_uninformative_prior(Uniform_prior)
band1.beta.set_uninformative_prior(Uniform_prior)
band1.xp.prior = Uniform_prior(lower_bound=10,upper_bound=8000)
ps1 = PointSource('PySPI',ra=94.67830, dec=-70.99905, spectral_shape=band1)

model1 = Model(ps1)

#### INIT OSA plugin #####

from threeML import OGIPLike
spi = OGIPLike("spi",
               observation="/home/bjorn/Downloads/spectra_GRB_peak.fits",
               response="/home/bjorn/Downloads/spectral_response_peak.rmf.fits")

########################### FITS ##################################

#### OSA ###########
from threeML import DataList, BayesianAnalysis
from astromodels import clone_model
model_osa = clone_model(model1)
datalist = DataList(spi)
ba_osa_band_1 = BayesianAnalysis(model_osa, datalist)
name_fit = 'OSA_BAND'
ba_osa_band_1.set_sampler("multinest", share_spectrum=True)
ba_osa_band_1.sampler.setup(800,
                    chain_name='chains/{}_'.format(name_fit),
                    resume=False,
                    verbose=True,
                    importance_nested_sampling=False)
ba_osa_band_1.sample()

#### PYSPI ###########
model_pyspi = clone_model(model1)
datalist_spi = DataList(*spilikes_sgl, *spilikes_sgl2, *spilikes_psd)#, *spilikes_sgl2)
ba_spi_new_band = BayesianAnalysis(model_pyspi, datalist_spi)
for i, s in enumerate(spilikes_psd):
    s.use_effective_area_correction(0,1)

name_fit = 'PYSPI_BAND'
ba_spi_new_band.set_sampler("multinest", share_spectrum=True)
ba_spi_new_band.sampler.setup(800,
                    chain_name='chains/{}_'.format(name_fit),
                    resume=False,
                    verbose=True,
                    importance_nested_sampling=False)
ba_spi_new_band.sample()


####  GBM ###########

model_gbm = clone_model(model1)

from threeML import DataList, BayesianAnalysis
datalist_gbm = DataList(*sls1)#, *spilikes_sgl2)
ba_gbm_band = BayesianAnalysis(model_gbm, datalist_gbm)
for i, s in enumerate(sls1):
    if i!=0:
        s.use_effective_area_correction(0.7,1.3)
name_fit = 'GBM_BAND'
ba_gbm_band.set_sampler("multinest", share_spectrum=True)
ba_gbm_band.sampler.setup(800,
                    chain_name='/home/bjorn/chains/{}_'.format(name_fit),
                    resume=False,
                    verbose=True,
                    importance_nested_sampling=False)
ba_gbm_band.sample()

#### PYSPI + GBM ###########

model_both = clone_model(model1)

from threeML import DataList, BayesianAnalysis
datalist_both = DataList(*sls1,*spilikes_sgl, *spilikes_sgl2, *spilikes_psd)#, *spilikes_sgl2)
ba_both_band = BayesianAnalysis(model_both, datalist_both)
for i, s in enumerate(sls1):
    s.use_effective_area_correction(0.7,1.3)
for i, s in enumerate(spilikes_psd):
    s.use_effective_area_correction(0,1)
name_fit = 'BOTH_BAND'
ba_both_band.set_sampler("multinest", share_spectrum=True)
ba_both_band.sampler.setup(800,
                    chain_name='chains/{}_'.format(name_fit),
                    resume=False,
                    verbose=True,
                    importance_nested_sampling=False)
ba_both_band.sample()
