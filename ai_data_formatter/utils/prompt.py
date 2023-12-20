import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from .duckduckgo_search import request_web_search
from .search import compile_prompt, SearchRequest
from .github_search import request_github_search

def structured_prompt(input, prompt):
    """
    Preprocess input to construct a structured prompt to feed to 
    the model prediction endpoint
    """
    if prompt:
        examples = "\n\n".join(
            [f"input: {e.input}\noutput: {e.output}" for e in prompt.examples]) if prompt.examples else ""
        if prompt.input_template:
            input = prompt.input_template.format(input)
        input_text = f"""{prompt.context if prompt.context else ""}\n\n{examples}\n\ninput: {input}\noutput:"""
    else:
        input_text = f"""input: {input}\noutput:"""
    return input_text


def freeform_prompt(input, prompt):
    """
    Preprocess input to construct a freeform prompt to feed to 
    the model prediction endpoint
    """
    if prompt:
        if prompt.input_template:
            input = prompt.input_template.format(input)
    input_text = f"""{input}"""
    return input_text


def web_search_prompt(input, prompt, ua="ua", number_results=5):
    """
    Search the web
    """
    search_results = request_web_search(SearchRequest(f"code example: {input}", ua=ua), num_results=number_results)
    input_text = compile_prompt(search_results, input, default_prompt=prompt.web_search_template)
    return input_text


def proprietary_search_prompt(input, prompt, number_results=5):
    """
    Search the private github repositories
    """
    search_results = request_github_search(SearchRequest(input), num_results=number_results)
    input_text = compile_prompt(search_results, input, default_prompt=prompt.proprietary_search_template)
    return input_text


def finetune_prompt(model_inputs):
    """
    Output as a JSONL file with following format in each line.
    {
        "input_text": "
            question: How many parishes are there in Louisiana? 
            context: The U.S. state of Louisiana is divided into 64 parishes (French: paroisses) in the same manner that 48 other states of the United States are divided into counties, and Alaska is divided into boroughs.", 
        "output_text": "64"
    }
    """
