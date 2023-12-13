import argparse
import requests
import json
import re

argParser = argparse.ArgumentParser(
    prog="Vision Archivist Publisher",
    description="Publish all search results within files based on a provided query"
)
argParser.add_argument("-j", "--jsonArguments", help="Input arguments as JSON string")
argParser.add_argument("-s", "--source", help="The name of the source (this host)")
argParser.add_argument("-t", "--queryType", help="The type of query; Basic or RegEx")
argParser.add_argument("-q", "--query", help="The query")
argParser.add_argument("-f", "--files", nargs='*', help="The files to search (List)")
argParser.add_argument("-u", "--url", help="The URL to the Vision instance")
# argParser.add_argument("-k","--key", help="API key for this source")

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
        user_query = re.escape(data['query'])
        user_query = user_query.replace('\\*','.*')
        user_query = f"{user_query}"
        pattern = re.compile(user_query)
    elif data["query_type"] == "regex_search":
        pattern = str(data["query"])

    for file in data["files"]:
        header = (f"BEGIN: {file}\n"f"{'='*30}")
        # requests.post(url, json={ "message" : header }, verify=False)
        print(header)
        with open(file, "r") as file_object:
            file_text = file_object.read()
            matches = re.findall(pattern, file_text)
            # requests.post(url, json={ "message" : matches }, verify=False)
            print(matches)
        footer = (f"{'='*30}\n"f"END: {file}\n"f"{'='*30}")
        # requests.post(url, json={ "message" : footer }, verify=False)
        print(footer)

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