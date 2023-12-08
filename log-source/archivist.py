import argparse
import requests
import json
import regex as re

argParser = argparse.ArgumentParser(
    prog="Vision Archivist Publisher",
    description="Publish all search results within files based on a provided query"
)
argParser.add_argument("-j", "--jsonArguments", help="Input arguments as JSON string")
argParser.add_argument("-s", "--source", help="The name of the source (this host)")
argParser.add_argument("-t", "--queryType", help="The type of query; Basic or RegEx")
argParser.add_argument("-q", "--query", help="The query")
argParser.add_argument("-f", "--files", help="The files to search (List)")
argParser.add_argument("-u", "--url", help="The URL to the Vision instance")

args = argParser.parse_args()

def publish_archive(jsonArguments:str=None, source:str=None, queryType:str=None, query:str=None, files:list=None, url:str=None):
    if jsonArguments:
        data = json.loads(jsonArguments)
    else:
        data = {
            "source" : source,
            "query_type" : queryType,
            "query" : query,
            "files" : files
        }

    if data["query_type"] == "basic_search":
        char_list = '.^$+?|()[]{}'
        terminated_query = data["query"]
        for char in data["query"]:
            if char in char_list:
                terminated_query.replace(char, f"\\{char}")
        pattern = f"^{data['query']}$"
    elif data["query_type"] == "regex_search":
        pattern = str(data["query"])

    for file in data["files"]:
        header = (f"{'='*30}\n"f"BEGIN: {file}\n"f"{'='*30}")
        requests.post(url, json={ "message" : header }, verify=False)
        with open(file, "r"):
            matches = re.findall(pattern, file.read())
            requests.post(url, json={ "message" : matches }, verify=False)
        footer = (f"{'='*30}\n"f"BEGIN: {file}\n"f"{'='*30}")
        requests.post(url, json={ "message" : footer }, verify=False)

if args.jsonArguments and isinstance(args.jsonArguments, str):
    publish_archive(jsonArguments=args.jsonArguments)
else:
    publish_archive(
        source = str(args.source),
        queryType = str(args.queryType),
        query = str(args.query),
        files = args.files,
        url = str(args.url)
    )