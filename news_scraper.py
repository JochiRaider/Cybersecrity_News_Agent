#!/usr/bin/env python3 
'''
This is a Python script that scrapes news articles from various cybersecurity news websites. It uses the BeautifulSoup library to parse HTML code and extract information such as article titles, links, and publication dates. The script consists of a NewsScrapers class, which has several methods to scrape different websites.

The __init__ method initializes the class and sets two instance variables for the current date and yesterday's date. These dates are used to filter out articles that are not from the last two days.

The news_call method is the main method that calls other methods to scrape news articles. It checks whether today's date is even or odd and selects which websites to scrape based on that. It also checks whether the total number of articles scraped is less than six and adds more articles from a different website if necessary. After scraping all the articles, it calls the smmry_api_agent method to summarize each article. Finally, it sorts the list of articles by the length of their summaries and returns the sorted list.

The other methods in the NewsScrapers class are specific to different news websites. They each use the news_site_scraper method to scrape articles from the website and return a list of lists, where each inner list contains the title, link, and publication date of an article.

The request_news_site method sends a GET request to a URL and returns the parsed HTML code as a BeautifulSoup object. It also handles exceptions that may occur during the request and retries the request after waiting five seconds.

The new_news_sort method filters out articles that are not from the last two days based on their publication dates. It uses regular expressions to extract the publication dates from the HTML code.
-chat gpt
'''


import bs4 
import requests
import re
import os
import datetime, time


class NewsScrapers:

    def __init__(self) -> None:
        self.date_pattern = re.compile(r'^20[0-9]{2}.[0-9]{2}.[0-9]{2}')
        self.today_date = self.date_pattern.search(str(datetime.datetime.now())).group().split('-')
        self.yesterday_date = self.date_pattern.search(str(datetime.datetime.now() - datetime.timedelta(days=1))).group().split('-')
    
    def news_call(self) -> list[list[str,str,str]]:
        if int(self.today_date[2])%2 == 0:
            news_art_list = self.infosec_news_scraper() + self.hacker_news_scraper() 
            if len(news_art_list) < 6:
                news_art_list += self.cyber_def_mag_scraper()
        else:
            news_art_list = self.hackread_scraper() + self.cyber_def_mag_scraper()
            if len(news_art_list) < 6:
                news_art_list += self.hacker_news_scraper()
        
        for i in range(len(news_art_list)):
            step = self.smmry_api_agent(news_art_list[i][1])
            news_art_list[i].append(step)
        news_art_list.sort(key=lambda s: -len(s[2]))
        return news_art_list  

    def hackread_scraper(self)->list[list[str,str,str]]:
        url = 'https://www.hackread.com/'
        link_selector = '#top-grid > div > div > article > figure > figcaption > div > h2 > a'
        time_selector = '#top-grid > div > div > article > figure > figcaption > div > div > time'
        title_selector = '#top-grid > div > div > article > figure > figcaption > div > h2 > a'
        date_type = 'datetime'
        output = self.news_site_scraper(url, link_selector, time_selector, title_selector, date_type)

        return output

    def cyber_def_mag_scraper(self)->list[list[str,str,str]]:
        url = 'https://www.cyberdefensemagazine.com/'
        link_selector = '#homecontent > div > div.homepostcontent > h2 > a'
        time_selector = '#homecontent > div > div.homepostcontent > div'
        title_selector = '#homecontent > div > div.homepostcontent > h2 > a'
        date_type = 'day'
        output = self.news_site_scraper(url, link_selector, time_selector, title_selector, date_type)

        return output

    def hacker_news_scraper(self)->list[list[str]]:
        
        url = 'https://thehackernews.com/'
        link_selector = '#Blog1 > div.blog-posts.clear > div > a'
        time_selector = '#Blog1 > div.blog-posts.clear > div > a > div > div.clear.home-right > div.item-label'
        title_selector = '#Blog1 > div.blog-posts.clear > div > a > div > div.clear.home-right > h2'
        date_type = 'day'
        output = self.news_site_scraper(url, link_selector, time_selector, title_selector, date_type)

        return output

    def infosec_news_scraper(self)->list[list[str]]:
       
        url = 'https://www.infosecurity-magazine.com/news/'
        link_selector = 'div.webpage-item> a'
        time_selector = 'div.webpage-item> a> span > time'
        title_selector = 'div.webpage-item> a >h3'
        date_type = 'datetime'
        output = self.news_site_scraper(url, link_selector, time_selector, title_selector, date_type)

        return output
   
    def news_site_scraper(self, url: str, link_selector: str, time_selector: str, title_selector: str, date_type: str)->list[list[str]]:
        soup_object = self.request_news_site(url)
        art_list_link = soup_object.select(link_selector)
        art_list_time = soup_object.select(time_selector)
        art_list_title = soup_object.select(title_selector)
        output = self.new_news_sort(art_list_time, art_list_title, art_list_link, date_type)
        return output

    def request_news_site(self, url:str)->bs4:
        try:
            response_object  = requests.get(url)
            response_object.raise_for_status()  
        except:
            time.sleep(5)
            response_object  = requests.get(url)
            response_object.raise_for_status()
        soup_object = bs4.BeautifulSoup(response_object.text, 'html.parser')
        return soup_object
    
    def new_news_sort(self, art_list_time:list[str], art_list_title:list[str], art_list_link:list[str],date_type:str)->list[list[str]]:
        output = []
        new_news_index = []
        if date_type == 'datetime':
            for i in range(len(art_list_time)):
                pub_time = art_list_time[i].get('datetime')
                pub_date = self.date_pattern.search(pub_time).group().split('-')
                if int(pub_date[2]) == int(self.yesterday_date[2]) or int(pub_date[2]) == int(self.today_date[2]):
                    new_news_index.append(i) 
        elif date_type == 'day':
           day_pattern = re.compile(r'[0-9]{2}')
           for i in range(len(art_list_time)):      
                day_i = day_pattern.search(art_list_time[i].text).group()
                
                if int(day_i) == int(self.yesterday_date[2]) or int(day_i) == int(self.today_date[2]):
                    new_news_index.append(i)
        for i in new_news_index:
            art_href = art_list_link[i].get('href')
            art_title = art_list_title[i].text
            output.append([art_title,art_href])
        return output
    
    def smmry_api_agent(self, url:str, length='5') -> str:
        key = os.environ.get('SMMRY_API')
        response_object  = requests.get(f'https://api.smmry.com/&SM_API_KEY={key}&SM_LENGTH={length}&SM_URL={url}')
        return response_object.json()['sm_api_content']
        
 

def main():
    # print(NewsScrapers().hackread_scraper())
    # 
    # test_dump = [['Couple Arrested Over Sale of Nuclear Secrets', 'https://www.infosecurity-magazine.com/news/couple-arrested-over-sale-of/', 'Jonathan and Diana Toebbe, both of Annapolis, were arrested in Jefferson County, West Virginia, by the FBI and the Naval Criminal Investigative Service on Saturday, October 9. It is alleged that 42-year-old Naval nuclear engineer Jonathan Toebbe, with the help of his 45-year-old wife, sold information classified as Restricted Data to an undercover FBI agent who they believed was a representative of a foreign power. After receiving a $10,000 advance payment, Toebbe and his wife allegedly arranged to leave an SD card containing the data at a pre-arranged location in West Virginia on June 26. The agent retrieved the card and paid Jonathan Toebbe $20,000 for the encryption key. The FBI arrested Jonathan and Diana Toebbe on October 9, after he placed a third SD card at a pre-arranged location in West Virginia.'], ['US Imprisons Man Who Exploited Children Via Social Media', 'https://www.infosecurity-magazine.com/news/imprisons-man-exploited-children/', 'A sexual predator who used social media apps to victimize minors has been sent to prison in the United States. Jacob Blanco, of Fresno, California, used several ruses to manipulate children as young as six years old into producing sexually explicit material and then sharing it with him. In May 2020, Blanco pleaded guilty to five counts of sexual exploitation of a minor and receipt and distribution of material involving sexual exploitation of minors. Acting US Attorney Phillip Talbert for the Eastern District of California said: "The fact that the defendant used social media to sexually exploit the victims serves as a reminder that the internet can be a dangerous place especially for children." Blanco\'s sentencing comes a month after the National Center on Sexual Exploitation urged TikTok to do more to protect minors using its platform.'], ['Hospital Hacker Steals Patients’ Data', 'https://www.infosecurity-magazine.com/news/hospital-hacker-steals-patients/', 'Data belonging to patients of a hospital in New Mexico has been deleted by an unknown cyber-attacker. The hospital said: "Upon learning of the issue, SJRMC immediately took steps to secure the network and mitigate against any additional harm. After an extensive forensic investigation, we determined that as part of this incident, an unauthorized individual removed information from our network September 7-8, 2020.". The hospital discovered on July 13, 2021, that those files had contained "The personal and protected health information of certain patients." The hospital said on October 7 that it is notifying the patients whose data was affected by the incident. "Nevertheless, in addition to providing this website notice, SJRMC is sending notification to all affected patients for whom we have enough information to determine a physical address. We have also set up a dedicated call center," said the hospital.'], ['Android Phones Sharing Significant User Data Without Opt-Outs', 'https://www.infosecurity-magazine.com/news/android-user-data-opt-outs/', 'Roid mobile phones are undertaking significant data sharing without offering opt-outs for users, according to a new report by researchers at Trinity College Dublin and the University of Edinburgh. For the study, the team analyzed six variants of the Android OS to determine the amount of data they are sending to developers and third parties with pre-installed system apps, such as Google, Microsoft, LinkedIn and Facebook. The researchers noted that third-party system apps from companies such as Google, Microsoft, LinkedIn and Facebook are pre-installed on most handsets analyzed and silently collected data without opt-out. "Prof Doug Leith, chair of computer systems at the School of Computer Science and Statistics, Trinity College Dublin, commented:"I think we have completely missed the massive and ongoing data collection by our phones, for which there is no opt out. "The business impact is the financial cost associated with legal fees and potential privacy regulatory fines as a result of not adhering to GDPR compliance requirements. There are also financial implications with employee compensation if found that the privacy of their data was not adhered to both from a business collection purpose and/or if adequate protection controls were not in place leading to the result of their data being breached."'], ['Most Insurers Mandate MFA, But Premiums Are Still Soaring ', 'https://www.infosecurity-magazine.com/news/most-insurers-mandate-mfa-premiums/', 'US cyber-insurers are increasing premiums and lowering coverage limits despite mandating stricter security controls as a pre-requisite for coverage, according to a new report. The US Cyber Market Outlook from wholesale insurance broker Risk Placement Services warns that providers have been "Battered" by higher-than-anticipated recent losses and are now generally charging much more for less coverage. Sectors hit hard over the past year, including education, government, healthcare, construction and manufacturing, have seen premiums increase by 300% or more at renewal time. Such controls are becoming increasingly widespread, according to RPS. Multi-factor authentication is now described as a "Must-have" to even qualify for coverage. A Government Accountability Office study from May claimed that take-up of cyber-specific insurance policies had doubled to around half in 2020, but that successful attacks had also led to rising premiums and reduced coverage limits for some.'], ['Banking Insider Accused of Role in $1m BEC Scheme', 'https://www.infosecurity-magazine.com/news/banking-insider-accused-role-bec/', "Three men including one former bank employee have been indicted by a federal grand jury for their alleged role in a business email compromise conspiracy. Onyewuchi Ibeh, 21, of Bowie, Maryland, Jason Joyner, 42, of Washington, DC and Mouaaz Elkhebri, 30, of Alexandria, Virginia, were charged with money laundering and aggravated identity theft, according to a superseding indictment late last week. At least five businesses lost over $1.1m in total over the period, with the co-conspirators laundering the funds through dozens of bank accounts, according to the Department of Justice. Ibeh apparently managed the money laundering process, directing the others to open accounts which he used to wire money around the world. Elkhebri is charged with conspiracy to commit money laundering, money laundering, false entries in a bank's books, and aggravated identity theft - charges which carry a maximum of 52 years."], ['Ransomware Intrusion Group FIN12 Ramps-Up in Europe', 'https://www.infosecurity-magazine.com/news/ransomware-intrusion-group-fin12/', 'A long-running threat group with a track record of rapid ransomware deployment and healthcare sector victims is ramping up its operations in Europe and APAC, Mandiant has warned. In a new report detailing the work of FIN12, the threat intelligence firm claimed that the prolific threat group had focused mainly on North American targets since its activities were first recorded in 2018. The bad news for organizations elsewhere in the world is that FIN12 appears to be changing its geographical focus. The group apparently uses Ryuk ransomware to target organizations with over $300m in revenue, partnering with other actors in the cyber underground for initial access, especially those affiliated with Trickbot and BazarLoader malware. Through these partnerships and by eschewing double extortion tactics, FIN12 has dramatically cut the time it takes to deploy ransomware to victim networks.']]
    # test_res = tf(xkcd()).xkcd_comic()
    # soup_object = newsScrapers().request_news_site('https://thehackernews.com/')
    # art_list_link = soup_object.select('#Blog1 > div.blog-posts.clear > div > a')
    # print(art_list_link[0].get('href'))
    # art_list_time = soup_object.select('#Blog1 > div.blog-posts.clear > div > a > div > div.clear.home-right > div.item-label')
    # print(art_list_time[0].text)
    # art_list_title = soup_object.select('#Blog1 > div.blog-posts.clear > div > a > div > div.clear.home-right > h2')
    # print(art_list_title[0].text)

    # # art_list_link = soup_object.select('#Blog1 > div.blog-posts.clear > div > a')
    # # art_list_time = soup_object.select('#Blog1 > div.blog-posts.clear > div > a > div > div.clear.home-right > div.item-label')
    # # art_list_title = soup_object.select('#Blog1 > div.blog-posts.clear > div > a > div > div.clear.home-right > h2')
    
    # print(newsScrapers().hacker_news_scraper())
    #
    # test = newsScrapers().hacker_news_scraper() + newsScrapers().infosec_news_scraper()
    
    # for i in range(len(test)):
    #     step = smmry_api_agent(test[i][1])
    #     test[i].append(step)



    # with open('test.txt','w') as f:
    #     f.write(str(test))
    pass
    

if __name__=='__main__':
    main()
