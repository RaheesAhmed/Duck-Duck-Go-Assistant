from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer
import asyncio


async def scrape_url(url):
    loader = AsyncHtmlLoader([url])
    docs = loader.load()

    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    data = docs_transformed[0].page_content
    save_content_to_file(data, "scraped_content.txt")
    return data


def save_content_to_file(content, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


# url = "https://python.langchain.com/v0.1/docs/use_cases/web_scraping/"
# asyncio.run(scrape_url(url))
