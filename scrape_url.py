from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import Html2TextTransformer


def scrape_url(url):
    loader = AsyncHtmlLoader([url])
    docs = loader.load()

    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    return docs_transformed[0].page_content


# url = "https://python.langchain.com/v0.1/docs/use_cases/web_scraping/"
# print(scrape_url(url))
