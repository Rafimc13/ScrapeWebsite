import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
from langdetect import detect



class StoringData:

    def get_HTML(self, url):
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        return soup

    def scrape_lastpage(self, url):
        soup = self.get_HTML(url)
        span = soup.find(class_ = "first_last")
        link = span.a["href"]

        pattern = r'page=(\d+)'

        match = re.search(pattern, link)
        last_page = match.group(1)
        return last_page

    def scrape_posts(self, soup):
        all_posts = []
        lang_posts = []
        posts = soup.find_all('a', class_='title')
        for post in posts:
            all_posts.append(post.get_text())
            if detect(post.get_text()) == 'el':
                lang_posts.append("Greek")
            else:
                lang_posts.append("Greeklish")

        return all_posts, lang_posts

    def scrape_authors(self, soup):
        all_authors = []
        authors = soup.find_all('dl', class_='threadauthor td')

        pattern = re.compile(r'\n')
        for author in authors:
            all_authors.append(pattern.sub("", author.get_text()))

        return all_authors

    def scrape_IDpost(self, soup):
        pattern = r'thread_\d{6}'
        id_threads = re.findall(pattern, str(soup))
        my_IDposts = []
        pattern = re.compile(r"thread_")
        for thread in id_threads:
            my_IDposts.append(pattern.sub("", thread))

        return my_IDposts

    def scrape_dates(self, url, idposts):
        dates = []
        for id in idposts:
            repsonse = requests.get(url + id)
            html_content = repsonse.text
            soup = BeautifulSoup(html_content, 'html.parser')
            dates.append(soup.find(class_='date').get_text())

        my_dates = []
        pattern = re.compile(r" \xa0")
        for date in dates:
            my_dates.append(pattern.sub("", date))

        return my_dates


    def create_dataframe(self, posts, authors, dates, language, idposts, columns):
        posts_df = pd.DataFrame(columns=columns)
        posts_df = posts_df.set_index(columns[0])

        for i in range(len(posts)):
            for j in range(len(posts[i])):
                posts_df.loc[posts[i][j]] = [authors[i][j], dates[i][j], language[i][j], idposts[i][j]]

        return posts_df


class WebScraping():

    my_data = StoringData()
    # url = input("Give me the url you want to scrape: ")
    warmane_url = "https://forum.warmane.com/forumdisplay.php?f=20&page=1"


    last_page = int(my_data.scrape_lastpage(warmane_url))
    print(last_page)

    my_soups = []
    for i in range(1, last_page+1):
        url = warmane_url[:len(warmane_url)-1] + str(i)
        my_soups.append(my_data.get_HTML(url))


    all_posts = []
    all_authors = []
    all_IDposts = []
    lang_posts = []
    for soup in my_soups:
        post, lang = my_data.scrape_posts(soup)
        all_posts.append(post)
        lang_posts.append(lang)
        all_authors.append(my_data.scrape_authors(soup))
        all_IDposts.append(my_data.scrape_IDpost(soup))


    url_post =  'https://forum.warmane.com/showthread.php?t='

    all_dates = []
    for id in all_IDposts:
        all_dates.append(my_data.scrape_dates(url_post, id))


    my_columns = ["post", "author", "date of post", "language", "reply-to"]

    posts_df = my_data.create_dataframe(all_posts, all_authors, all_dates,
                                        lang_posts, all_IDposts, my_columns)
    posts_df.to_csv("warmane_post.csv", index=True)
    posts_df.to_html("warmane.html", index=True)

df_gaming = pd.read_csv("warmane_post.csv")
user_choice = int(input(f'Give a number from 0 to {len(df_gaming)}, and I will give you a gaming post: '))
if user_choice>145:
    print("Invalid number. Bye!")
else:
    i = user_choice
    print(f"Author {df_gaming.iloc[i, 1]}, posted at {df_gaming.iloc[i, 2]} the following in "
          f"{df_gaming.iloc[i, 2]}: ")
    print(f"{df_gaming.iloc[i, 0]}.")
    print(f"The replies are in: https://forum.warmane.com/showthread.php?t={df_gaming.iloc[i, 4]}")

