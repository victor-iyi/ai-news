import os
from newsapi import NewsApiClient
from dotenv import load_dotenv
from pprint import pprint


load_dotenv()


def main() -> None:
    newsapi = NewsApiClient(api_key=os.environ['NEWS_API_KEY'])

    top_headlines = newsapi.get_top_headlines(
        q='ai',
        sources='bbc-news,the-verge',
        language='en',
    )
    pprint(top_headlines)   # {articles:[], status: ok, totalResult: 0}

    print(f'\n{"--" * 50}\n')

    # sources = newsapi.get_sources()
    # pprint(sources.keys())


if __name__ == '__main__':
    main()
