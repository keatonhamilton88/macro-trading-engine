from layer0.sensors.copper_gold import copper_gold
from layer0.sensors.hg_tio import hg_tio
from layer0.sensors.hg_cl import hg_cl
from layer0.sensors.oil_gold import oil_gold
from layer0.sensors.gc_si import gc_si

from layer0.sensors.sox_spy import sox_spy
from layer0.sensors.ashr_spy import ashr_spy
from layer0.sensors.eem_spy import eem_spy
from layer0.sensors.fxi import fxi

from layer0.sensors.aud_jpy import aud_jpy
from layer0.sensors.spy_tlt import spy_tlt
from layer0.sensors.hyg_tlt import hyg_tlt

from layer0.sensors.vix import vix
from layer0.sensors.vix_vol import vix_vol
from layer0.sensors.vix_slope import vix_slope

from layer0.sensors.gamma_flip import gamma_flip
from layer0.sensors.spx_gex import spx_gex
from layer0.sensors.put_call_ratio import put_call_ratio
from layer0.sensors._0dte_vol import zero_dte_vol

from layer0.sensors.dx import dx
from layer0.sensors.usd_cnh import usd_cnh
from layer0.sensors.usd_jpy import usd_jpy
from layer0.sensors.eur_usd import eur_usd
from layer0.sensors.eur_chf import eur_chf

from layer0.sensors.zn_sr3 import zn_sr3
from layer0.sensors.zn_zt import zn_zt


SENSOR_REGISTRY = {

    "copper_gold": copper_gold,
    "hg_tio": hg_tio,
    "hg_cl": hg_cl,
    "oil_gold": oil_gold,
    "gc_si": gc_si,

    "sox_spy": sox_spy,
    "ashr_spy": ashr_spy,
    "eem_spy": eem_spy,
    "fxi": fxi,

    "aud_jpy": aud_jpy,
    "spy_tlt": spy_tlt,
    "hyg_tlt": hyg_tlt,

    "vix": vix,
    "vix_vol": vix_vol,
    "vix_slope": vix_slope,

    "gamma_flip": gamma_flip,
    "spx_gex": spx_gex,
    "put_call_ratio": put_call_ratio,
    "0dte_vol": zero_dte_vol,

    "dx": dx,
    "usd_cnh": usd_cnh,
    "usd_jpy": usd_jpy,
    "eur_usd": eur_usd,
    "eur_chf": eur_chf,

    "zn_sr3": zn_sr3,
    "zn_zt": zn_zt
}
