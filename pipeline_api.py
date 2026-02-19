import config as app_config
import openai
import time
from gdeltdoc import GdeltDoc, Filters  # type: ignore[import-untyped]
from gdeltdoc.errors import RateLimitError  # type: ignore[import-untyped]
from newspaper import Article, Config

open_ai_key = app_config.OPEN_AI_API_KEY
openai.api_key = open_ai_key

model = "gpt-4o-mini"

news_config = Config()
news_config.browser_user_agent = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

gd = GdeltDoc()

def chatgpt_generate(query):
  response = openai.chat.completions.create(
    model=model,
    messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": query}]
  )
  return response.choices[0].message.content

def get_url(keyword, max_retries=3):
  f = Filters(
      keyword=keyword,
      start_date="2025-01-01",
      end_date="2025-03-31",
      num_records=10,
      domain="techcrunch.com",
      country="US",
  )
  for attempt in range(max_retries):
    try:
      articles = gd.article_search(f)
      if articles.empty:
        print(f"[Retry {attempt+1}/{max_retries}] 빈 결과 반환, 60초 대기...")
        time.sleep(60)
        continue
      return articles
    except RateLimitError:
      print(f"[Retry {attempt+1}/{max_retries}] Rate limit, 60초 대기...")
      time.sleep(60)
  print("GDELT API 결과를 가져오지 못했습니다.")
  return None

prompt = f'''
  아래 뉴스에서 기업명을 모두 추출하고, 기업에 해당하는 감성을 분석하시오.
  출력 포맷은 다음과 같습니다.
  반드시 출력포맷만을 생성하고, 다른 텍스트는 생성하지 마시오.
  {{"기업명": <기업명>, "감성": <긍정/부정>}}
  뉴스: '''

def url_crawling(df):
  urls = df["url"]
  titles = df["title"]
  texts = []
  for url in urls:
    try:
      article = Article(url, config=news_config)
      article.download()
      article.parse()
      texts.append(article.text)
    except Exception as e:
      print(f"[SKIP] {url} - {e}")
  return texts

df = get_url("microsoft")
texts = url_crawling(df)
for text in texts:
  print(chatgpt_generate(prompt + text))