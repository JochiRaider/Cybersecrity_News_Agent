#!/usr/bin/env python3 

import re
import datetime
import ezgmail
from gmail_formatter import ComposeEmail
from news_scraper import NewsScrapers
from xkcd_scraper import xkcd_rng_scraper
from cve_agent import cve_api_agent



def main():
    
    comic = xkcd_rng_scraper() 
    
    cve_list = cve_api_agent()
    
    news_art_list = NewsScrapers().news_call()
    
    out_email = ComposeEmail(xkcd_list=comic,cve_list=cve_list,news_art_list=news_art_list).final_draft()
    
    today_date = re.compile(r'^2[0-9]{3}.[0-9]{2}.[0-9]{2}').search(str(datetime.datetime.now())).group()

    local_name = f'nes_email_{today_date}.html'
    
    with open(local_name,'w') as f:
        f.write(out_email)
   
    out_subject = f'News email service for {today_date}'
    
    ezgmail.send('+@.com', out_subject, out_email, mimeSubtype='html')

if __name__=='__main__':
    main()

