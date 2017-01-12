from ..base import BaseCrawler
from ..utils import parse_count
from bs4 import BeautifulSoup

from datetime import datetime


class ChaYuArticleCrawler(BaseCrawler):
    host = "http://m.chayu.com/"
    name = "chayu"
    list_url = "http://m.chayu.com/article/lists?order=id" \
               "&p=%s&load=1"
    list_min_id = 19600

    def get_post_detail(self, _id):
        url = "http://m.chayu.com/article/%s" % _id
        response = self.call(url)
        if response and response.ok:
            html_text = response.content.decode().replace("\r\n", "")
        else:
            return

        soup = BeautifulSoup(html_text)
        content = str(soup.find("article", attrs={"class": "wenzhang_content"}))
        title = soup.find("section", attrs={"class": "wenzhang"}).find("h3").string
        info = soup.find(attrs={"class": "wenzhang_info"}).findAll("span")
        publish_at = datetime.strptime(info[0].string.split("：")[-1].strip(),
                                        "%Y-%M-%d")
        read_count = parse_count(info[-1].string.split("：")[-1].strip())
        print(read_count, publish_at)
        return {
            "title": title,
            "cover_image": None,
            "short_content": "",
            "content": content,
            "site": self.host,
            "url": url,
            "read_count": read_count,
            "star_count": 1,
            "_id": _id,
            "category": "",
            "published_at": publish_at,
            "article_type": "文章",
        }

    def get_post_list(self, end_id=list_min_id, url=list_url):
        page = 1
        print(end_id)
        while True:
            _url = url % page
            print(_url)
            page += 1
            response = self.call(_url)
            if response and response.ok:
                data = response.json()
            else:
                yield
                return
            soup = BeautifulSoup(data["html"])
            li_list = soup.findAll("li")
            for li in li_list:
                _url = li.find("a").attrs.get("href")
                _id = _url.split("/")[-1]
                if int(_id) <= end_id:
                    yield
                    return
                title = li.find("a").attrs.get("title")
                cover_image = li.find("img").attrs.get("src")
                item = {
                    "site": self.host,
                    "_id": _id,
                    "title": title,
                    "cover_image": cover_image,
                    "url": _url,
                    "article_type": "文章",
                    "category": "",
                }
                yield item


class ChaYuChaPingCrawler(BaseCrawler):
    host = "http://m.chaping.chayu.com/"
    name = "chaping.chayu"
    list_url = "http://m.chaping.chayu.com/" \
               "lists?order=id&p=%s&load=1"
    list_min_id = 0

    def get_post_list(self, end_id=list_min_id, url=list_url):
        print(end_id)
        page = 1
        while True:
            _url = url % page
            print(_url)
            page += 1
            response = self.call(_url)
            if response and response.ok:
                data = response.json()
            else:
                yield
                return
            soup = BeautifulSoup(data["html"])
            li_list = soup.findAll("li")
            for li in li_list:
                _url = li.find("a").attrs.get("href")
                _id = _url.split("/")[-1]
                if int(_id) <= end_id:
                    yield
                    return
                title = li.find("a").attrs.get("title")
                cover_image = li.find("img").attrs.get("src")
                category = li.findAll('span', attrs={"class": "fl"})[1].string
                item = {
                    "site": self.host,
                    "_id": _id,
                    "title": title,
                    "cover_image": cover_image,
                    "url": _url,
                    "article_type": "茶评",
                    "category": category,
                }
                yield item

    def get_post_detail(self, _id):
        url = "http://m.chaping.chayu.com/tea/%s" % _id
        print(url)
        response = self.call(url)
        if response and response.ok:
            html_text = response.content.decode().replace("\r\n", "")
        else:
            return

        soup = BeautifulSoup(html_text)
        content = str(soup.find(attrs={"class": "chaping-details"}))
        title = soup.find(attrs={"class": "evaluation-info"}).find("h2").text
        cover_image = soup.find(attrs={"class": "swiper-slide"}).find("img").attrs.get("src")
        return {
            "title": title,
            "cover_image": cover_image,
            "short_content": "",
            "content": content,
            "site": self.host,
            "url": url,
            "read_count": 1,
            "star_count": 1,
            "_id": _id,
            "category": None,
            "article_type": "茶评",
            "published_at": None
        }
