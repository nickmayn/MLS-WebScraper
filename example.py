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
  try:
    allstuff = re.findall('(?<=Listing Details).*?(?=Information)', zed)[0].split('    ')
    for word in allstuff:
      if word == '' or word == ' ':
        continue
      else:
        print(word)
  except:
    pass


idc = []
for i in range(1000):
    idc.append(110132+i)


def main():
  pool = mp.Pool(mp.cpu_count())
  result = tqdm(pool.imap(process_page, idc), total=len(idc))

if __name__ == '__main__':
    with mp.Pool(processes=mp.cpu_count()) as p:
        max_ = len(idc)
        with tqdm(total=max_) as pbar:
            for i, _ in enumerate(p.imap_unordered(process_page, idc)):
                pbar.update()
