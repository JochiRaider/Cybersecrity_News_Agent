#!/usr/bin/env python3 

import bs4
import requests
import random

def xkcd_rng_scraper()->list[str]:
    issue_num = random.choice(range(1,2000))
    response_obj = requests.get(f'https://xkcd.com/{issue_num}')
    response_obj.raise_for_status()
    soup_obj = bs4.BeautifulSoup(response_obj.text,'html.parser')
    comic = soup_obj.select('#comic > img')
    output = [comic[0].get('alt'),'https:'+comic[0].get('src'),comic[0].get('title')]
    return output
    
    
def main():
    # print(xkcd_rng_scraper())
    pass

if __name__ == '__main__':
    main()
