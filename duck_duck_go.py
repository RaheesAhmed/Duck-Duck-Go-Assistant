from duckduckgo_search import DDGS


def search_duckduckgo_text(query):
    ddgs = DDGS()
    results = ddgs.text(query)
    search_results = []
    for result in results:
        if "title" in result and "href" in result and "body" in result:
            search_results.append(
                {
                    "title": result["title"],
                    "url": result["href"],
                    "snippet": result["body"],
                }
            )
    return search_results


def search_duckduckgo_images(query):
    ddgs = DDGS()
    results = ddgs.images(query)
    search_results = []
    for result in results:
        if "image" in result and "thumbnail" in result:
            search_results.append(
                {"image_url": result["image"], "thumbnail_url": result["thumbnail"]}
            )
    return search_results


def get_text_results(query):
    # Perform text search
    text_results = search_duckduckgo_text(query)
    return text_results


def get_images_results(query):
    # Perform image search
    image_results = search_duckduckgo_images(query)
    return image_results
