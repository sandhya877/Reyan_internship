import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd
from urllib.parse import urlparse

proxies = {'http': 'http://palivela.srihari@gmail.com:reyandigital@us-wa.proxymesh.com:31280',
           'https': 'http://palivela.srihari@gmail.com:reyandigital@us-wa.proxymesh.com:31280'}

data=pd.read_excel("data.xlsx")
#main_keywords=list(data["Main Keyword"][2458:])
all_top_10_urls = []
main_keywords=["best pellet stove","best wood burning stove"]
for keyword in main_keywords:
    urls_collected = 0
    print(keyword)
    urls_list=set()
    # Construct the Google search URL with the keyword and location parameter
    url = f"https://www.google.com/search?q={keyword}&gl=us"

    # Send the HTTP GET request using the proxy
    response = requests.get(url, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')

    
    result_links1 = soup.find_all('a', attrs={'data-ved': True})
    for idx, link in enumerate(result_links1):
      h3_element = link.find('h3', class_='zBAuLc l97dzf')
      span_element = link.find('span', class_='rQMQod Xb5VRe')
      if span_element:
          # This link contains an h3 element, so you can extract the href
          href = link['href']
          if urls_collected == 0: 
             all_top_10_urls.append([keyword,urls_collected,href])
             urls_collected +=1
      if h3_element:
          # This link contains an h3 element, so you can extract the href
          href = link['href']
          if urls_collected == 0:
             all_top_10_urls.append([keyword,urls_collected,href])
             urls_collected +=1
          else:
             all_top_10_urls.append([" ",urls_collected,href])
             urls_collected +=1
    df = pd.DataFrame(all_top_10_urls, columns=["keyword","position","url"])
    print(df)
    df.to_csv("urls4.csv", index=False)
    #print(result_links)
'''
    for index, link in enumerate(result_links1):
        href = link.get('href')
        if href.startswith('/url?q='):
            url = href.split('/url?q=')[1].split('&')[0]
            parsed_url = urlparse(url)
            website_domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
            print(website_domain)
            if website_domain not in urls_list:
                if website_domain == "https://www.youtube.com/":
                   if urls_collected==0:
                      all_top_10_urls.append([keyword,urls_collected,url])
                      urls_list.add(website_domain)
                      urls_collected +=1
                else:
                   urls_list.add(website_domain)
                if urls_collected >= 10:  # Check if 10 URLs have been collected for this keyword
                    break
                if urls_collected==0:
                  all_top_10_urls.append([keyword,urls_collected,url])
                  urls_collected += 1

                else:
                  all_top_10_urls.append([" ",urls_collected,url])
                  urls_collected +=1
    # Create a DataFrame with the correct structure
    df = pd.DataFrame(all_top_10_urls, columns=["keyword","position","url"])
    print(df)
    df.to_csv("search_results2.csv", index=False)

print(len(urls_list))
'''