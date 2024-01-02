from bs4 import BeautifulSoup
import requests

amazon = requests.get("https://www.amazon.in/gp/bestsellers").text

soup = BeautifulSoup(amazon, 'html.parser')

elements = soup.select('div[class="_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-small__nleKL"] a[href]')
base_url = "https://www.amazon.in"
for element in elements:
    href = element.get('href')
    print(href)
    parts = href.split('/')
    category = parts[-1]
    link=base_url+href+"/ref=zg_bs_nav_"+category+"_0"
    amazon = requests.get(link).text
    soup1 = BeautifulSoup(amazon, 'html.parser')
    print(link)
    div_elements = soup1.find_all('div', class_='_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-large__1z5B8', role='treeitem')
    for div_element in div_elements:
        a_element = div_element.find('a', href=True)
        if a_element:
            href = a_element['href']
            print(href)
            link=base_url+href+"/ref=zg_bs_nav_boost_2_10894224031"
            print(link)



link="https://www.amazon.in/gp/bestsellers/boost/ref=zg_bs_nav_boost_0"
amazon = requests.get(link).text
soup1 = BeautifulSoup(amazon, 'html.parser')
base_url = "https://www.amazon.in"
div_elements = soup1.find_all('div', class_='_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-large__1z5B8', role='treeitem')
print(div_elements)
for div_element in div_elements:
    a_element = div_element.find('a', href=True)
    if a_element:
        href = a_element['href']
        print(href)
        link=base_url+href+"/ref=zg_bs_nav_boost_2_10894224031"
        print(link)


link="https://www.amazon.in/gp/bestsellers/boost/10894224031/ref=zg_bs_nav_boost_2_10894224031"
amazon = requests.get(link).text
soup1 = BeautifulSoup(amazon, 'html.parser')
base_url = "https://www.amazon.in"
# Extract all product names with the specified class
product_names = soup1.find_all('div', class_='_cDEzb_p13n-sc-css-line-clamp-3_g3dy1')
print(product_names)
for product_name in product_names[:50]:
  pass
  #print(product_name.get_text())

span_element = soup.find('span', class_='a-icon-alt')

rating_text = span_element.get_text()
print(rating_text)
span_elements = soup1.find_all('span', class_="a-icon-alt")
print(span_elements)
for span_element in span_elements:
  print(span_element)
span_elements = soup1.find_all('span', class_='p13n-sc-price')
print(span_elements)
for span_element in span_elements:
  print(span_element)