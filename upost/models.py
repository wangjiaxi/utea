from django.db import models
from ucrawler.sites import crawler_objects
from ckeditor.fields import RichTextField


class SourceManager(models.Manager):
    def init(self):
        for k, v in crawler_objects.items():
            self.update_or_create(name=k,
                                  defaults={"site": v.host})


class Source(models.Model):
    name = models.CharField(max_length=63)
    site = models.URLField()

    objects = SourceManager()

    @property
    def crawler(self):
        """get crawler instance"""
        return crawler_objects.get(self.name)()

    def __str__(self):
        return self.name + ">>" + self.site


class PostListManager(models.Manager):

    @classmethod
    def parse_item_from_crawl_data(cls, item):
        """parse date tha format same as model PostList"""
        return {
            "title": item.get("title"),
            "url": item.get("url"),
            "category": item.get("category"),
            "cover_image": item.get("cover_image"),
            "article_type": item.get("article_type"),
        }

    def crawl_init(self):
        """get post list in crawler, and save it local"""
        sources = Source.objects.all()
        for source in sources:
            post = PostList.objects.filter(source=source).order_by("_id").last()

            # get post list
            if post:
                post_list = source.crawler.get_post_list(end_id=post._id)
            else:
                post_list = source.crawler.get_post_list()

            # save post list item local
            for item in post_list:
                print(item)
                if item:
                    self.get_or_create(source=source, _id=item.get("_id"),
                                       defaults=self.parse_item_from_crawl_data(item))


class PostList(models.Model):
    source = models.ForeignKey(Source, related_name="post_source")
    _id = models.IntegerField()
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=63,
                                blank=True, null=True)
    article_type = models.CharField(max_length=63)
    cover_image = models.URLField(blank=True, null=True)
    url = models.URLField()
    crawler_at = models.DateTimeField(auto_now_add=True)
    has_crawled = models.BooleanField(default=False)

    objects = PostListManager()

    def crawl_post(self):
        return self.source.crawler.get_post_detail(self._id)

    def __str__(self):
        return self.source.name + "-" + str(self._id)


class PostManager(models.Manager):
    @classmethod
    def parse_item_from_crawl_data(cls, item):
        """parse date tha format same as model PostList"""
        return {
            "title": item.get("title"),
            "url": item.get("url"),
            "category": item.get("category"),
            "cover_image": item.get("cover_image"),
            "article_type": item.get("article_type"),
            "read_count": item.get("read_count"),
            "star_count": item.get("star_count"),
            "tags": item.get("tags"),
            "content": item.get("content"),
            "short_content": item.get("short_content"),
        }

    def post_init(self):
        """get post list form model PostList witch not crawled,
            crawl post detail  and save it.
        """
        sources = Source.objects.all()
        for source in sources:
            list_items = PostList.objects.filter(source=source, has_crawled=False)
            for item in list_items:
                data = item.crawl_post()
                if data:
                    if data.get("category") is None:
                        data["category"] = item.category
                    if data.get("cover_image") is None:
                        data["cover_image"] = item.cover_image

                    self.get_or_create(source=source, _id=data.get("_id"),
                                       defaults=self.parse_item_from_crawl_data(data))
                    item.has_crawled = True
                    item.save()


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    short_content = models.TextField()
    _id = models.IntegerField()
    url = models.URLField()
    tags = models.CharField(blank=True, null=True, max_length=63,
                            help_text="spilt use common")
    category = models.CharField(max_length=63, blank=True, null=True)
    cover_image = models.URLField(blank=True, null=True)
    article_type = models.CharField(max_length=63)
    source = models.ForeignKey(Source)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_count = models.IntegerField(default=1)
    star_count = models.IntegerField(default=1)
    has_posted = models.BooleanField(default=False)

    objects = PostManager()

    def __str__(self):
        return self.title

