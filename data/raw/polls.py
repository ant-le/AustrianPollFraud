
from numpy import NaN
from pandas import DataFrame, to_datetime
from datetime import datetime

def _new_entries():
    new = [NaN,datetime(2017,5,12),"Research Affairs",35,21,25,9,600,"https://www.oe24.at/oesterreich/politik/neue-umfrage-kurz-klar-1/282513188"]
    return new
    
    
def _urls():
    urls = { 
        2:"https://www.oe24.at/oesterreich/politik/spoe-gewinnt-nach-kern-rede/266178434",
        3:"https://www.ots.at/presseaussendung/OTS_20170121_OTS0001/profil-umfrage-kanzlerfrage-kern-doppelt-so-stark-wie-strache",
        4:NaN,
        5:NaN,
        6:"https://www.oe24.at/oesterreich/politik/kern-turbo-nach-regierungs-krise/267760374",
        11:"https://www.oe24.at/oesterreich/politik/kurz-bremst-strache-aus/273265891",
        13:"https://www.spectra.at/aktuelles/details/politikbarometer-national-fuer-1-quartal-2017-veroeffentlicht.html",
        15:"https://www.diepresse.com/5197356/oevp-umfrage-spoe-verdraengt-fpoe-von-platz-eins",
        16:NaN,
        21:"https://www.ifes.at/ifes-medien/methodische-informationen-zur-ifes-umfrage-kronen-zeitung",
        22:"https://www.sn.at/politik/innenpolitik/120-bewerber-wollen-auf-die-neos-liste-12235639",
        25:"https://www.heute.at/s/umfrage-beben-kurz-schiesst-auf-33-prozent-57972414",
        34:"https://www.oe24.at/oesterreich/politik/umfrage-kern-rueckt-fpoe-naeher/289199848",
        38:NaN,
        39:"https://www.krone.at/579214",
        40:NaN,
        41:"https://www.oe24.at/oesterreich/politik/kurz-fuehrt-kern-kann-strache-ueberholen/291947735",
        48:"https://www.ots.at/presseaussendung/OTS_20170818_OTS0108/atv-oesterreich-trend-erstmalig-liegen-die-neos-vor-den-gruenen",
        58:"https://kurier.at/politik/inland/wahl/kurz-bleibt-klarer-favorit-kern-holt-minimal-auf/287.918.983",
        63:"https://www.oe24.at/oesterreich/politik/wahl2017/umfrage-oevp-klar-vorne-fpoe-holt-auf/301515462",
        66:"https://kurier.at/politik/inland/kurier-ogm-umfrage-kurz-bleibt-vor-kern-und-strache-kleinparteien-muessen-zittern/290.566.272",
    }
    df = DataFrame(list(urls.items()),columns = ['index','url']) 
    return df
        
        
def _sample_size():
    sample_size = {
        21: 902,
        36: 619,
        39: 1000,
        42: 503,
        55: 659,
        56: NaN,
        58: 470,
        63: 500,                
        66: 470,
    }
    df = DataFrame(list(sample_size.items()),columns = ['index','Sample Size']) 
    return df


def _dates():
    dates = {
        2:"2017-01-20",
        9:"2017-03-03",
        10:"2017-03-19",
        11:"2017-03-16",
        13:"2017-04-01",
        15:"2017-04-07",
        18:"2017-04-27",
        19:"2017-04-28",
        20:"2017-05-08",
        21:"2017-05-14",
        22:"2017-06-15",
        23:"2017-05-21",
        25:"2017-05-19",
        26:"2017-05-20",
        27:"2017-05-26",
        28:"2017-07-29",
        29:"2017-06-03",
        30:"2017-06-09",
        31:"2017-06-17",
        32:"2017-06-25",
        33:"2017-06-24",
        35:"2017-07-08",
        36:"2017-07-09",
        37:"2017-07-16",
        39:"2017-07-19",
        41:"2017-07-21",
        42:"2017-07-23",
        43:"2017-08-03",
        44:"2017-08-04",
        45:"2017-08-14",
        46:"2017-08-13",
        47:"2017-08-16",
        48:"2017-08-18",
        49:"2017-08-26",
        50:"2017-08-26",
        51:"2017-09-01",
        52:"2017-08-31",
        55:"2017-09-10",
        56:"2017-09-16",
        58:"2017-09-24",
        60:"2017-09-23",
        61:"2017-09-22",
        62:"2017-09-30",
        65:"2017-10-06",
        66:"2017-10-08",
        67:"2017-10-05",
        68:"2017-10-09"
    }
    df = DataFrame(list(dates.items()),columns = ['index','Date']) 
    df['Date'] = to_datetime(df["Date"])
    return df     