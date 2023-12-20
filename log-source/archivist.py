"""
Archivist: v1.0
This script is meant to read and query from files, then ship out the data to The Vision Tool.
"""

import argparse
import requests
import tarfile
import json
import re
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning from urllib3 needed for self-signed certificates
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

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
argParser.add_argument("-k","--key", help="API key for this source")

args = argParser.parse_args()

POSITIVE_RESPONSES = [200, 201, 202, 203, 204, 205, 206, 207, 208,
                    300, 301, 302, 303, 304, 305, 306, 307, 308]

NEGATIVE_RESPONSES = [400, 401, 402, 403, 404, 405, 406, 407, 408,
                    409, 410, 411, 412, 413, 414, 415, 416, 417,
                    418, 421, 422, 423, 424, 425, 426, 427, 428,
                    429, 431, 500, 501, 502, 503, 504, 505, 506,
                    507, 508, 510, 511]

class vision_post:
        def __init__(self, key, source):
            self.key = key
            self.source = source

        def new_post(self, message):
            return { 
                "authentication" : {
                    "apikey" : self.key
                }, 
                "content": {
                    "message": message,
                    "containerId":f"{self.source}:archivist"
                }
            }

def post_results(code:int, label:str, file_name:str):
    if code in POSITIVE_RESPONSES:
        return f"FILE[{file_name}]-{code}: {label} sent"
    elif code in NEGATIVE_RESPONSES:
        return f"FILE[{file_name}]-{code}: {label} failed"
    
def lines(file:str=None):
    supported_file_types = [
        "txt", "csv", "xml",
        "json", "html", "css",
        "js", "log", "md", "yaml",
        "yml", "ini", "cfg", "conf",
        "bat", "sh", "sql", "py",
        "ps1", "psm1","gz",
    ]
    extension = file.split('.')[-1]
    if extension in supported_file_types:
        if extension == "gz":
            with tarfile.open(file) as tar:
                for member in tar.getmembers():
                    f = tar.extractfile(member)
                    return [ line.decode('utf-8') for line in f.readlines() ]
        else:
            with open(file, 'r') as f:
                return f.readlines()
    else:
        return None
    

def publish_archive(jsonArguments:str=None, source:str=None, queryType:str=None, query:str=None, files:list=None, url:str=None, key:str=None):
    
    if jsonArguments:
        data = json.loads(jsonArguments)
    else:
        data = {
            "source" : source,
            "query_type" : queryType,
            "query" : query,
            "files" : files,
            "url" : url,
            "key" : key
        }

    if data["query_type"] == "basic_search":
        user_query = re.escape(data['query'])
        user_query = str(user_query.replace('\\*','.*'))
        pattern = re.compile(user_query)
    elif data["query_type"] == "regex_search":
        pattern = re.compile(str(data["query"]))

    for file in data["files"]:
        message = vision_post(data["key"], data["source"])
        response = requests.post(data["url"], json=message.new_post(f"BEGIN: {file}\n"f"{'='*30}"), verify=False)
        print(post_results(response.status_code, "Header", file))
        file_text = lines(file)
        if file_text:
            for line in file_text:
                if re.search(pattern, line):
                    response = requests.post(data["url"], json=message.new_post(f"{file_text.index(line) + 1}:\t{line}"), verify=False)
                    print(post_results(response.status_code, f"line {file_text.index(line)}", file))
        else:
            response = requests.post(data["url"], json=message.new_post(f"Error for {file}: Type not supported!"), verify=False)
            print(post_results(response.status_code, "Error: Type not supported", file))
        response = requests.post(data["url"], json=message.new_post(f"{'='*30}\n"f"END: {file}\n"f"{'='*30}"), verify=False)
        print(post_results(response.status_code, "Footer", file))


if args.jsonArguments and isinstance(args.jsonArguments, str):
    publish_archive(jsonArguments=args.jsonArguments)
else:
    publish_archive(
        source = str(args.source),
        queryType = str(args.queryType),
        query = str(args.query),
        files = args.files,
        url = str(args.url),
        key = str(args.key)
    )
