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


def get_text_results(query_text):
    # Perform text search
    text_results = search_duckduckgo_text(query_text)
    print("Text Search Results:")
    for result in text_results:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Snippet: {result['snippet']}\n")

    return text_results


def get_images_results(image_query):
    # Perform image search
    image_results = search_duckduckgo_images(image_query)
    print("Image Search Results:")
    for result in image_results:
        print(f"Image URL: {result['image_url']}")
        print(f"Thumbnail URL: {result['thumbnail_url']}\n")

    return image_results


# Example usage
# query_text = "OpenAI latest updates"
# query_image = "OpenAI logo"
# text_results = get_text_results(query_text)
# image_results = get_images_results(query_image)
