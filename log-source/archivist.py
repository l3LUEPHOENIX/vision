import argparse
import requests
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
validated_args = ""

if args.jsonArguments and isinstance(args.jsonArguments, str):
    pass

def publish_archive(jsonArguments:str=None, source:str=None, queryType:str=None, query:str=None, files:list=None, url:str=None):
    if jsonArguments:
        data = jsonArguments
    else:
        data = {
            "source" : source,
            "query_type" : queryType,
            "query" : query,
            "files" : files
        }

    for file in files:
        header = """
        BEGIN: file_name.txt
        ========================================
        """
        requests.post(url, json=header, verify=False)

        with open(file, "r"):
            matches = re.findall(query, file.read())

        footer = """
        ========================================
        END: file_name.txt
        ========================================
        """
        requests.post(url, json=footer, verify=False)
    
    requests.post(url, json=data, verify=False)