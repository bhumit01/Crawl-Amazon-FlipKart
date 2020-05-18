from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

keyword = input('Enter a keywork you want to search for (ex. Iphone X) ==> ')

print('How many pages you want to search? (please enter number)==> ')
while True:
    try:
        no_pages = int(
            input())
        break
    except ValueError:
        print('Oops...Kindly enter a **Number** to proceed: ')


def get_data_from_flipkart(pageNo):
    with requests.Session() as f_s:
        f_headers = {
            'User-Agent': 'Mozilla/60.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.2171.95 Safari/537.36'}
        f_page = f_s.get(
            f'https://www.flipkart.com/search?q={keyword}&marketplace=FLIPKART&otracker=start&as-show=on&as=off&page={pageNo}', headers=f_headers)
        f_soup = BeautifulSoup(f_page.content, "lxml")

        alls = []
        for items in f_soup.findAll('div', attrs={'class': '_3liAhj'}):
            title = items.find('a', attrs={'class': '_2cLu-l'})
            seller_author = items.find('div', attrs={'class': '_1rcHFq'})
            rating = items.find('div', attrs={'class': 'hGSR34'})
            price = items.find('div', attrs={'class': '_1vC4OE'})

            all1 = []

            if title is not None:
                all1.append(title.text)
            else:
                all1.append("unknown-product")

            if seller_author is not None:
                all1.append(seller_author.text)
            else:
                all1.append("unknown-author/seller")

            if rating is not None:
                all1.append(rating.text)
            else:
                all1.append("unknown-rating")

            if price is not None:
                all1.append(price.text)
            else:
                all1.append("0")

            alls.append(all1)
        return alls


def get_data_from_amazon(pageNo):
    with requests.Session() as a_s:
        a_headers = {
            'User-Agent': 'Mozilla/60.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.2171.95 Safari/537.36'}
        a_page = a_s.get(
            f'https://www.amazon.in/s/ref=nb_sb_noss_2?url=search-alias%3Daps&field-keywords={keyword}&page={pageNo}', headers=a_headers)
        a_soup = BeautifulSoup(a_page.content, "lxml")

        alls = []
        for items in a_soup.findAll('div', attrs={'class': 'a-section a-spacing-medium'}):
            # print(d)
            title = items.find(
                'span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
            # print(n[0]['alt'])
            price = items.find('span', attrs={'class': 'a-price-whole'})

            all1 = []

            if title is not None:
                # print(n[0]['alt'])
                all1.append(title.text)
            else:
                all1.append("unknown-product")

            if price is not None:
                # print(author.text)
                all1.append(price.text)
            else:
                all1.append('0')

            alls.append(all1)
        return alls

def get_data_from_flipkart2(pageNo):
        with requests.Session() as f_s:
            f_headers = {
                'User-Agent': 'Mozilla/60.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.2171.95 Safari/537.36'}
            f_page = f_s.get(
                f'https://www.flipkart.com/search?q={keyword}&marketplace=FLIPKART&otracker=start&as-show=on&as=off&page={pageNo}', headers=f_headers)
            f_soup = BeautifulSoup(f_page.content, "lxml")

            alls = []
            for items in f_soup.findAll('div', attrs={'class': 'bhgxx2 col-12-12'}):
                title = items.find('div', attrs={'class': '_3wU53n'})
                seller_author = None
                rating = items.find('div', attrs={'class': 'hGSR34'})
                price = items.find('div', attrs={'class': '_1vC4OE'})

                all1 = []

                if title is not None:
                    all1.append(title.text)
                else:
                    all1.append("unknown-product")

                if seller_author is not None:
                    all1.append(seller_author.text)
                else:
                    all1.append("unknown-author/seller")

                if rating is not None:
                    all1.append(rating.text)
                else:
                    all1.append("unknown-rating")

                if price is not None:
                    all1.append(price.text)
                else:
                    all1.append("0")

                alls.append(all1)
            return alls

def flatten(l): return [item for sublist in l for item in sublist]


def flatten(list): return [item for sublist in list for item in sublist]


# def flatten(list):
#     for sublist in list:
#         for item in sublist:
#             return [item]
""" Extracting data from Amazon """
a_results = []
for i in range(1, no_pages + 1):
    a_results.append(get_data_from_amazon(i))

time.sleep(1)
df_amazon = pd.DataFrame(flatten(a_results), columns=[
    'title', 'price'])
#df.to_csv('amazon_products.csv', index=False, encoding='utf-8')
print(df_amazon)

time.sleep(1)
""" Extracting data from Flipkart"""
f_results = []
for i in range(1, no_pages + 1):
    f_results.append(get_data_from_flipkart(i))

time.sleep(1)
df_flipkart = pd.DataFrame(flatten(f_results), columns=[
    'title', 'seller_author', 'rating', 'price'])
if df_flipkart.empty:
    results2 = []
    for i in range(1, no_pages + 1):
        results2.append(get_data_from_flipkart2(i))

    # flatten = lambda l: [item for sublist in l for item in sublist]
    def flatten(list): return [item for sublist in list for item in sublist]


    df_flipkart2 = pd.DataFrame(flatten(results2), columns=[
        'title', 'seller_author', 'rating', 'price'])
    #print(df_flipkart2)
#df.to_csv('amazon_products.csv', index=False, encoding='utf-8')
# print(df_flipkart)
time.sleep(1)
with pd.ExcelWriter('ecommerce_results.xlsx') as writer:
    df_amazon.to_excel(writer, sheet_name='Amazon')
    df_flipkart.to_excel(writer, sheet_name='Flipkart')

print()
print()
print()
print()
print('Operation completed...Excel saved in the BASE_DIR')
print(r"""

___                ___
| _ )_  _ ___      | _ )_  _ ___
| _ \ || / -_)_ _ _| _ \ || / -_)
|___/\_, \___(_|_|_)___/\_, \___|
  |__/               |__/

    """)
