import requests
import logging


class BaseCrawler:
    name = None
    host = None
    list_min_id = None
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                      "(KHTML, like Gecko) Version/9.0 Mobile/13B143 "
                      "Safari/601.1",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Host": host,
        "Referer": host,
    }

    def call(self, url, method="get", data=None):
        try:
            if method.lower() == "get":
                return requests.get(url=url, headers=self.headers)
            if method.lower() == "post":
                return requests.post(url=url, headers=self.headers,
                                     data=data)
        except Exception as e:
            logging.error("Crawl erroe: %s" % e)
            return None

    def get_post_list(self, end_id, url):
        """get post list item while item's id lt end_id
        :return: yield post item {
            "cover_image": "http://www.example.com/example.jpeg",
            "title": "this is title",
            "url": "http://www.example.com/post/123",
            "site": "http://www.example.com",
            "_id": 111,
            "category": "category"
            "article_type": ""
        }
        """
        pass

    def get_post_detail(self, _id):
        """get post detail from id
        :return type: dict
        :return {
            "title": "example title",
            "cover_image": "http://www.example.com/example.jpeg",
            "short_content": "this is short content",
            "site": "http://www.example.com",
            "url": "http://www.example.com/post/123",
            "read_count": 324,
            "star_count": 123,
            "_id": 111,
            "content": "",
            "category": "category",
            "published_at": "2017-01-01 13:28:56"
        }
        """
        pass
