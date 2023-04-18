#All imports
import time
import requests
from requests import Session
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

years = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1993', '1992']
makes = ['acura', 'audi', 'buick', 'cadillac', 'chevy', 'chrysler', 'chevrolet', 'dodge', 'ferrari', 'fiat', 'ford', 'gmc', 'honda', 'hyundai', 'infiniti', 'isuzu', 'izusu', 'jaguar', 'jeep', 'kia', 'lamborghini', 'land rover', 'landrover', 'lexus', 'lotus', 'lincoln', 'maserati', 'mazda', 'mercedes', 'mercury', 'mini', 'mitsubishi', 'nissan', 'pontiac', 'porsche', 'plymouth', 'range rover', 'rangerover', 'saab', 'saturn', 'scion', 'smart', 'subaru', 'suzuki', 'tesla', 'toyota', 'volkswagen', 'volkswagon', 'volvo']
models = ['is f', 'lfa', 's-type', 'x-type', 'f-pace', 'f-type', 'xk', 'q40', 'q50', 'q60', 'q70', 'gto', 'qx30', 'qx50', 'qx60', 'qx70', 'qx80', 'nsx', 'rsx', 'mdx', 'tsx', 'rdx', 'ilx', 'rdx', 'zdx', '100', '900', '500', 'ion', 'cla', 'cls', 'gla', 'glc', 'gle', 'gls', 'clk', 'slc', 'slk', 'cabrio', 'cabriolet', 'allroad', 'mks', 'mkz', 'mkc', 'mkt', 'mkx', 'rs 3', 'rs 4', 'rs 5', 'rs 6', 'rs 7', 'sq5', '200', 'hardtop', 'coupe', 'century', 'cascada', 'lacrosse', 'lesabre', 'lucerne', 'cayman', 'park avenue', 'regal', 'regal sportback', 'regal tourx', 'riviera', 'roadmaster', 'skylark', 'verano', 'enclave', 'encore', 'envision', 'rainier', 'rendezvous', 'terraza', 'allante', 'ats', 'ats-v', 'brougham', 'catera', 'ct6', 'cts', 'cts-v', 'deville', 'dts', 'eldorado', 'elr', 'fleetwood', 'seville', 'sixty special', 'sts', 'tundra', 'xts', 'xlr', 'srx', 'xt5', 'escalade esv', 'escalade ext', 'aveo', 'avalanche', 'avalanche 1500', 'avalanche 2500', 'blazer', 'bolt ev', 'spark ev', 'caprice', 'caprice classic', 'captiva sport', 'cavalier', 'classic', 'cobalt', 'cruze', 'cruze limited', 'impala', 'impala limited', 'lumina', 'malibu', 'metro', 'prizm', 'sonic', 'volt', 'equinox', 's10 blazer', 'suburban', 'suburban 1500', 'suburban 2500', 'suburban 3500', 'tahoe', 'tracker', 'trailblazer', 'traverse', 'trax', 'colorado', 'silverado 1500', 'silverado 2500', 'silverado 3500', 'ssr', 'apv', 'astro', 'express', 'city express', 'g-series', 'sportvan', 'uplander', 'venture', 'beretta', 'camaro', 'corvette', 'monte carlo', 'hhr', '300', '300m', 'cirrus', 'concorde', 'crossfire', 'fifth ave', 'imperial', 'lebaron', 'lhs', 'new yorker', 'sebring', 'aspen', 'pacifica', 'voyager', 'grand voyager', 'pacifica hybrid', 'town & country', 'pt cruiser', 'prowler', 'avenger', 'charger', 'colt', 'dart', 'dynasty', 'intrepid', 'monaco', 'neon', 'shadow', 'spirit', 'stratus', 'durango', 'journey', 'nitro', 'ramcharger', 'd150', 'd250', 'd350', 'dakota', 'caravan', 'grand caravan', 'challenger', 'stealth', 'viper', 'daytona', 'caliber', 'magnum', '430 scuderia', '458 italia', '458 speciale', '458 spider', '488 gtb', '488 spider', '599 gtb fiorano', '599 gto', '612 scagiletti', 'california', 'f12 berlinetta', 'f430', 'gtc4lusso', '500l', '500e', '500x', '500 abarth', '124 spider', '500c', '500c abarth', 'aspire', 'contour', 'crown victoria', 'escort', 'fiesta', 'festiva', 'five hundred', 'focus', 'focus st', 'fusion', 'fusion energi', 'taurus', 'tempo', 'bronco', 'edge', 'escape', 'excursion', 'expedition', 'expedition el', 'expedition max', 'explorer', 'explorer sport', 'explorer sport trac', 'flex', 'taurus x', 'freestyle', 'c-max energi', 'c-max hybrid', 'mustang', 'probe', 'thunderbird', 'zx2', 'acadia', 'acadia limited', 'envoy', 'envoy xl', 'envoy xuv', 'jimmy', 'terrain', 'yukon', 'yukon xl 1500', 'yukon xl 2500', 'odyssey', 'accord', 'accord hybrid', 'civic', 'cr-z', 'insight', 'del sol', 'prelude', 'crosstour', 'civic type r', 'accord crosstour', 'S2000', 'element', 'hr-v', 'passport', 'pilot', 'ridgeline', 'accent', 'azera', 'elantra', 'elantra gt', 'equus', 'excel', 'genesis', 'genesis coupe', 'scoupe', 'tiburon', 'veloster', 'ioniq electric', 'ioniq hybrid', 'sonata', 'sonata hybrid', 'sonata plug-in hybrid', 'xg300', 'xg350', 'santa fe', 'santa fe sport', 'tucson', 'tucson fuel cell', 'veracruz', 'entourage', 'stylus', 'amigo', 'ascender', 'axiom', 'rodeo', 'rodeo sport', 'trooper', 'vehicross', 'oasis', 'impulse', 'cherokee', 'commander', 'compass', 'grand cherokee', 'liberty', 'patriot', 'renegade', 'wrangler', 'wrangler unlimited', 'comanche regular cab', 'amanti', 'cadenza', 'forte', 'k900', 'optima', 'optima hybrid', 'optima plug-in hybrid', 'rio', 'sephia', 'spectra', 'borrego', 'sorento', 'sportage', 'sedona', 'niro', 'soul', 'soul ev', 'forte', 'forte5', 'forte koup', 'rondo', 'aventador', 'gallardo', 'huracan', 'murcielago', 'murcielago lp640', 'defender 110', 'defender 90', 'discovery', 'discovery series ii', 'discovery sport', 'freelander', 'lr2', 'lr3', 'lr4', 'evoque', 'sport', 'velar', 'continental', 'town car', 'zephyr', 'aviator', 'blackwood', 'navigator', 'navigator l', 'mark lt', 'mark vii', 'mark viii', 'elise', 'evora', 'evora 400', 'exige', 'exige s', 'ghibli', 'quattroporte', 'levante', 'gransporte', 'granturismo', 'coupe', '626', '929', 'mazda2', 'mazda3', 'mazda3', 'mazda5', 'mazda6', 'millenia', 'protege', 'protege5', 'cx-3', 'cx-5', 'cx-7', 'cx-9', 'navajo', 'tribute', 'mpv', '323', 'mx-3', 'mx-5 miata', 'mx-5 miata rf', 'mx-6', 'rx-7', 'rx-8', 'c-class', 'cla-class', 'cls-class', 'e-class', 'amg c-class', 'amg cla', 'amg cls', 'amg e-class', 'amg s-cass', 'maybach s 600', 'maybach s-class', 's-class', 'g-class', 'gl-class', 'gla-class', 'glc coupe', 'gle coupe', 'glk-class', 'm-class', 'amg g-class', 'amg gla', 'amg glc', 'amg glc coupe', 'amg gle', 'amg gle coupe', 'amg gls', 'amg gt', 'amg sl', 'amg slc', 'amg slk', 'r-class', 'b-class', 'cl-class', 'clk-class', 'sl-class', 'slk-class', 'sls-class', 'slr mclaren', 'cougar', 'grand marquis', 'marauder', 'milan', 'montego', 'mystique', 'sable', 'topaz', 'tracer', 'mariner', 'mountaineer', 'monterey', 'villager', 'capri', 'clubman', 'hardtop 4 door', 'countryman', 'paceman', 'cooper', 'hardtop 2 door', 'convertible', 'roadster', 'diamante', 'galant', 'lancer', 'lancer evolution', 'mirage', 'mirage g4', 'endeavor', 'montero', 'montero sport', 'outlander', 'outlander sport', 'i-miev', '3000gt', 'eclipse', 'precis', 'expo', 'altima', 'maxima', 'sentra', 'stanza', 'versa', 'versa note', 'armada', 'juke', 'murano', 'pathfinder', 'pathfinder armada', 'rogue', 'rogue select', 'rogue sport', 'xterra', 'leaf', '350z', '370z', 'gt-r', 'cube', 'acclaim', 'breeze', 'sundance', 'laser', 'colt vista', 'prowler', 'bonneville', 'grand am', 'grand prix', 'lemans', 'sunbird', 'sunfire', 'aztek', 'torrent', 'firebird', 'solstice', 'vibe', 'panamera', 'cayenne', 'macan', 'boxster', '718 cayman', '911', '928', '968', '718 boxster', 'carrera gt', '9-3', '9-5', '9-4x', '9000', '9-7x', '9-2x', 'astra', 'aura', 'l-series', 's-series', 'outlook', 'vue', 'relay', 'sky', 'xa', 'xd', 'fr-s', 'tc', 'xb', 'fortwo', 'fortwo cabrio', 'fortwo electric drive', 'fortwo electric drive cabrio', 'impreza', 'justy', 'legacy', 'loyale', 'outback', 'wrx', 'tribeca', 'baja', 'b9 tribeca', 'crosstrek', 'forester', 'xv crosstrek', 'brz', 'aerio', 'esteem', 'forenza', 'kizashi', 'reno', 'swift', 'sx4', 'verona', 'vitara', 'samurai', 'sidekick', 'grand vitara', 'x-90', 'xl-7', 'xl7', 'model 3', 'model s', 'model x', 'avalon', 'avalon hybrid', 'camry', 'camry hybrid', 'corolla', 'echo', 'prius', 'prius prime', 'tercel', 'yaris', 'yaris ia', '4runner', 'c-hr', 'fj cruiser', 'highlander', 'highlander hybrid', 'land cruiser', 'sierra', 'rav4', 'rav4 hybrid', 'sequoia', 'venza', 'sienna', 'prius c', 'prius v', 'celica', 'mr2', 'solara', 'supra', 'corolla im', 'matrix', 'paseo', '86', 'golf', 'e-golf', 'fox', 'gli', 'golf gti', 'golf iii', 'golf r', 'gti', 'jetta', 'passat', 'phaeton', 'rabbit', 'atlas', 'tiguan', 'tiguan limited', 'touareg', 'touareg 2', 'eos', 'eurovan', 'routan', 'beetle', 'r32', 'golf alltrack', 'golf sportwagen', 'jetta sportwagen', '240', '740', '850', '940', '960', 's40', 's60', 's70', 's80', 's90', 'v40', 'v50', 'v60', 'v70', 'v90', 'xc60', 'xc70', 'xc90', 'c30', 'c70']
models2 = ['ct', 'es', 'gs', 'hs', 'is', 'ls', 'gx', 'lx', 'nx', 'rx', 'lc', 'rc', 'sc', 'ia', 'iq', 'im', 'xe', 'xf', 'xj', 'g6', 'g8', 'g5', 'g3', 'ex', 'fx', 'jx', 'cc', 'qx', 'gt', 's5', 'rl', 'tl', 'cl', '90', '80', 'sl', 'q3', 'q5', 'q7', 's3', 's4', 's5', 's6', 's7', 's8', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8', 'r8', 'tt', 'ff', 'tc', 'fit']
models3 = ['g', 'i', 'j', 'm', 'q']



url = "https://myrtlebeach.craigslist.org/d/cars-trucks/search/cta?postal=29582&postedToday=1&s=360&search_distance=300&sort=date"
headers = {'User-Agent':'Mozilla/5.0'}
page = requests.get(url)
grab = soup(page.text, "html.parser")

time.sleep(2)

containers = grab.findAll('li',{'class':'result-row'})

print(grab)
print(containers)

container = containers[0]

filename = 'cars.csv'
f = open(filename, 'w')

headers = "Year, Make, Model, Price \n"
f.write(headers)

for container in containers:

    year = ""
    make = ""
    model = ""

    price_container = container.findAll('span',{'class':'result-price'})
    if len(price_container) == 0:
        price = "spam"

    else:
        price = price_container[0].text
        
    if price == "$1":
        price = "spam"

        
    title_container = container.findAll('a',{'class':'result-title'})
    title = title_container[0].text 
    if "FINANCE" in title:
        price = "spam"
    for item in years:
        if item in title:
            year = item
            title2 = title.replace(year, "")
            for item in makes:
                if item in title2.lower():
                    if item == "chevy":
                        make = "chevrolet"
                    elif item == "izusu":
                        make = "isuzu"
                    elif item == "rangerover":
                        make = "range rover"
                    elif item == "landrover":
                        make = "land rover"
                    elif item == "volkswagon":
                        make = "volkswagen"
                    elif item == "mercedes":
                        make = "mercedes-benz"
                    else:
                        make = item
                    title3 = title2.lower().replace(make, "")
                    for item in models3:
                        if item in title3.lower() and year != "":
                            model = item
                        for item in models2:
                            if item in title3.lower() and year != "":
                                model = item
                            for item in models:
                                if item in title3.lower() and year != "":
                                    model = item
    if make != "lexus" and (model == "ct" or model == "es" or model == "gs" or model == "hs" or model == "is" or model == "ls" or model == "gx" or model == "lx" or model == "nx" or model == "rx" or model == "lc" or model == "rc" or model == "sc"):
        model = ""
    elif make != "infiniti" and (model == "ex" or model == "fx" or model == "jx" or model == "qx" or model == "g" or model == "i" or model == "j" or model == "m" or model == "q"):
        model = ""
    elif make != "audi" and (model == "100" or model == "90" or model == "80"):
        model = ""
    elif make != "acura" and (model == "tl" or model == "cl" or model == "rl"):
        model = ""
    elif make != "chrysler" and (model == "200" or model == "300" or model == "300m" or model == "lhs"):
        model = ""
    elif make != "fiat" and (model == "500" or model == "500x" or model == "500l" or model == "500e" or model == "500c"):
        model = ""
    elif make != "hyundai" and (model == "excel"):
        model = ""
    elif make != "lincoln" and (model == "ls"):
        model = ""
    elif make != "volvo" and (model == "240" or model == "740" or model == "850" or model == "940" or model == "960"):
        model = ""
    elif make != "scion" and (model == "ia" or model == "xa" or model == "xd" or model == "tc" or model == "im" or model == "iq" or model == "xb"):
        model = ""
    elif make != "mini" and (model == "convertible"):
        model = ""
    elif make != "kia" and (model == "rio" or model == "niro"):
        model = ""
    elif make != "range rover" and (model == "sport"):
        model = ""
    if model == '' or make == '' or year == '' or price == "spam":
        price = "."
    elif model == "journey" or model == "tahoe" or model == "yukon" or model == "impala" or model == "malibu" or make == "subaru":
        print(year + " " + make + " " + model)
        print(title)
        print(price)
        print(" ")
    else:
        price = "."
    if make != "hhhhhhhhhhhh":
        price = "."
    elif make == "gmc":
        make = "GMC"
        print(year + " " + make + " " + model)
        print(title)
        print(price)
        print(" ")
        f.write(year)
        f.write(",")
        f.write(make)
        f.write(",")
        f.write(model)
        f.write(",")
        f.write(price)
        f.write("\n")
    elif make == "infiniti":
        make = "INFINITI"
        print(year + " " + make + " " + model)
        print(title)
        print(price)
        print(" ")
        f.write(year)
        f.write(",")
        f.write(make)
        f.write(",")
        f.write(model)
        f.write(",")
        f.write(price)
        f.write("\n")
    elif make == "mini":
        make = "MINI"
        print(year + " " + make + " " + model)
        print(title)
        print(price)
        print(" ")
        f.write(year)
        f.write(",")
        f.write(make)
        f.write(",")
        f.write(model)
        f.write(",")
        f.write(price)
        f.write("\n")
    else:
        print(year + " " + make + " " + model)
        print(title)
        print(price)
        print(" ")
        f.write(year)
        f.write(",")
        f.write(make)
        f.write(",")
        f.write(model)
        f.write(",")
        f.write(price)
        f.write("\n")
#
#    if model != "" and year != "" and make != "" and model != "sierra" and model != "outback" and price != "spam":
#        
#
#        URL = "https://uat.api.manheim.com/valuations/search/" + year + "/" + make + "/" + model
#        r = requests.get(url = URL)
#        price = r.json()
#        print(price)

f.close()