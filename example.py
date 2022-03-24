import multiprocessing as mp
import requests 
from bs4 import BeautifulSoup
import re
import pandas as pd
import warnings
from tqdm import tqdm
warnings.filterwarnings("ignore")

def process_page(ind):
  r = requests.get('https://www.usamls.net/northernneck/default.asp?content=expanded&this_format=1&page=3&query_id=195163948&sortby=5&search_content=results&mls_number={}'.format((ind)), verify=False)
  res = BeautifulSoup(r.text, "html.parser")
  zed = res.get_text().replace('\n', '').replace('\r', '')
  housedict = {}
  try:
    allstuff = re.findall('(?<=Listing Details).*?(?=Information)', zed)[0].split('    ')
    for i in range(len(allstuff) - 1):
      if ':' in allstuff[i]:
        housedict[allstuff[i]] = allstuff[i+2]
  except:
    pass
  return housedict


idc = []
for i in range(24000):
    idc.append(106000+i)



if __name__ == '__main__':
    houses = []
    with mp.Pool(processes=mp.cpu_count()) as p:
        max_ = len(idc)
        with tqdm(total=max_) as pbar:
            for i, _ in enumerate(p.imap_unordered(process_page, idc)):
                pbar.update()
                houses.append(_)
    houses = list(filter(None, houses))
    res = pd.DataFrame(houses)
    res.to_csv('data.csv')
