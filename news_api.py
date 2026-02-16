import time
from gdeltdoc import GdeltDoc, Filters  # type: ignore[import-untyped]
from gdeltdoc.errors import RateLimitError  # type: ignore[import-untyped]
from newspaper import Article, Config

config = Config()
config.browser_user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

f = Filters(
    keyword="microsoft",
    start_date="2025-01-01",
    end_date="2025-03-31",
    num_records=250,
    domain="nytimes.com",
    country="US",
)

gd = GdeltDoc()

def with_retry(fn, max_attempts=3, wait_seconds=60):
    for attempt in range(max_attempts):
        try:
            return fn()
        except RateLimitError:
            if attempt + 1 == max_attempts:
                raise
            print(f"Rate limited. Waiting {wait_seconds}s before retry {attempt + 2}/{max_attempts}...")
            time.sleep(wait_seconds)

articles = with_retry(lambda: gd.article_search(f))
print(articles)

timeline = with_retry(lambda: gd.timeline_search("timelinevol", f))

from newspaper.article import ArticleException

def fetch_article_text(config, max_tries=5):
    """Try up to max_tries URLs from the dataframe until one downloads."""
    for i in range(min(max_tries, len(articles))):
        u = articles.loc[i, "url"]
        title = articles.loc[i, "title"]
        a = Article(u, config=config)
        try:
            a.download()
            a.parse()
            if a.text and len(a.text.strip()) > 100:
                return a.text, title, u
        except ArticleException as e:
            print(f"Skip ({i+1}/{max_tries}): {title[:50]}... — {e}")
            continue
    return None, None, None

article_text, article_title, article_url = fetch_article_text(config)
if article_text:
    print(article_title)
    print(article_text[:2000] if len(article_text) > 2000 else article_text)
else:
    print("Could not download full text from any article (e.g. 403 from NYTimes).")
    print("Try removing domain='nytimes.com' to use other sources, or use the 'snippet' column from the GDELT results.")