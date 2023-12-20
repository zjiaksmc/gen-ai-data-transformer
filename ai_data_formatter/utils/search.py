import re
from typing import List
from datetime import datetime


class SearchRequest:
    def __init__(self, query: str, timerange: str = None, region: str = None, ua: str = None):
        self.query = query
        self.timerange = timerange
        self.region = region
        self.ua = ua


class SearchResponse:
    def __init__(self, status: int, html: str, url: str):
        self.status = status
        self.html = html
        self.url = url


class SearchResult:
    def __init__(self, title: str, body: str, url: str):
        self.title = title
        self.body = body
        self.url = url


def remove_commands(query: str) -> str:
    query = re.sub(r'\/page:(\S+)\s+', '', query)
    query = re.sub(r'\/site:(\S+)\s+', '', query)
    return query


def compile_prompt(results: List[SearchResult], query: str, default_prompt: str) -> str:
    formatted_results = format_results(results)
    current_date = datetime.now().strftime("%m/%d/%Y")
    prompt = replace_variables(default_prompt, {
        '[search_results]': formatted_results,
        '[query]': remove_commands(query),
        '[current_date]': current_date
    })
    return prompt


def format_results(results: List[SearchResult]) -> str:
    if len(results) == 0:
        return "No results found.\n"
    formatted_results = ""
    counter = 1
    for result in results:
        formatted_results += f"[{counter}] \"{result.body}\"\nURL: {result.url}\n\n"
        counter += 1
    return formatted_results


def replace_variables(prompt: str, variables: dict) -> str:
    new_prompt = prompt
    for key, value in variables.items():
        try:
            new_prompt = new_prompt.replace(key, value)
        except Exception as error:
            print("Search prompt error: ", error)
    return new_prompt