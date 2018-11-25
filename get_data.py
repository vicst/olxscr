from app.scrap import simple_get
from bs4 import BeautifulSoup
import re

olx_page = r"https://www.olx.ro"


#print (raw_html)

#raw_html = open(raw_html).read()

def parse_html(page_url):
    raw_html = simple_get(page_url)
    try:
        html = BeautifulSoup(raw_html, "html.parser")
        return html
    except:
        print("Nu a parsat url-ul: " + str(page_url))


def get_links(page_url, select_value, to_find, *args):
    if "www" in page_url:
        html = parse_html(page_url)
        urls = []
        for item in html.select(select_value): # ex. for link in html.select('a'):
            for attr in args:
                if attr in item.attrs:
                    joined_attr = ''.join(item[attr])
                    to_find_joined = to_find.replace(" ", "")
                    if joined_attr.find(to_find_joined) != -1:
                        urls.append(item['href'])
                        break
        return urls

def get_details(item_url):
    # details for a item
    html = parse_html(item_url)
    details_dict = {}

    categories = html.select('td.middle > ul > li > a > span')
    details_dict['categories'] = [category.text for category in categories]

    title = html.select('div.offer-titlebox > h1')[0].text
    title = title.replace("\n",'').strip()
    details_dict['title'] = title

    item_meta = html.select('div.offer-titlebox__details > em')
    item_meta_match = re.search(r'(?P<hour>\d+:\d+), (?P<date>\d+ \w+ \d+).+?(?P<number>\d+)', item_meta[0].text)
    hour = item_meta_match.group('hour')
    date = item_meta_match.group('date')
    number = item_meta_match.group('number')
    details_dict['hour'] = hour
    details_dict['date'] = date
    details_dict['number'] = int(number)

    price = html.select("div.price-label > strong")[0].text
    details_dict['price'] = price
    print(details_dict)

def remove_duplicates(list_item):
    return list(set(list_item))

def remove_error_urls(url_list):
    for url in url_list:
        if "www" not in url:
            url_list.remove(url)

#main_categories_list = remove_duplicates(get_links(olx_page, 'a', 'oferta', "href"))


def subcategory_links(main_categories_list):
    all_categories = []
    for category in main_categories_list:
        subcategory_list = remove_duplicates(get_links(category, 'a', 'topLink', "class"))
        remove_error_urls(subcategory_list)
        for subcategory in subcategory_list:
            sub_subcategory_list = remove_duplicates(get_links(subcategory,
                                             'a', 'topLink', "class"))
            remove_error_urls(sub_subcategory_list)
            all_categories = all_categories + sub_subcategory_list
    return remove_duplicates(all_categories)

#def

# main_categories_list = remove_duplicates(get_links(olx_page, 'a', 'link parent', "class"))
# subcategory_links = subcategory_links(main_categories_list)
# print (subcategory_links)

page_links = get_links(olx_page, 'a', 'oferta', "href")
print(page_links)




# get_details(r'https://www.olx.ro/oferta/iphone-5se-32gb-sigilat-IDbL1dU.html#4d8fa82544;promoted')


