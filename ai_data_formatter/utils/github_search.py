import os
import requests
from typing import List
from .search import SearchRequest, SearchResponse, SearchResult

BASE_URL = 'https://api.github.com/search/code'


def get_html(search: SearchRequest, num_results=5) -> SearchResponse:
    query = search.query
    github_token = os.environ.get("GITHUB_SECRET", None)
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    query_logic = f"{query}+org:ksmc"
    response = requests.get(f'{BASE_URL}?q={query_logic}', headers=headers)
    # print(headers)
    # print(f'{BASE_URL}?q={query_logic}')
    result_list = []
    if response.ok:
        query_results = response.json().get("items", [])
        if len(query_results) > num_results:
            query_results = query_results[: num_results-1]
        for item in query_results:
            path_array = item.get("html_url", "").split("/")
            repository_name = item.get("repository", {}).get("name")
            raw_file_path = os.path.join(*path_array[path_array.index('blob')+1:])
            raw_url = f"https://raw.githubusercontent.com/ksmc/{repository_name}/{raw_file_path}"
            raw_file_content = requests.get(raw_url, headers=headers).text
            result_list.append({
                # "title": f"{repository_name}/{item.get("path", None)}",
                "html": raw_file_content,
                "url": item.get("html_url", "")
            })
    else:
        raise Exception(f'Failed to fetch: {response.status_code} {response.reason}')
    return [SearchResponse(200, result.get("html"), result.get("url")) for result in result_list]


def file2summary(content):
    """
    extract the useful part from the full content
    """
    #TODO
    return f"""
    ```python
    {content}
    ```
    """

def html_to_summary(search_response: SearchResponse) -> SearchResult:
    body = file2summary(search_response.html)
    return SearchResult(os.path.basename(search_response.url), body, search_response.url)

def request_github_search(search: SearchRequest, num_results=5) -> List[SearchResult]:
    response_list = get_html(search, num_results)
    result_list = []
    for response in response_list:
        result_list.append(
            html_to_summary(response)
        )
    return result_list