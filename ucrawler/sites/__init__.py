from .chayu import ChaYuArticleCrawler, ChaYuChaPingCrawler

crawlers = [ChaYuArticleCrawler, ChaYuChaPingCrawler]

crawler_objects = dict([(c.name, c)for c in crawlers])
