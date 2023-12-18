import argparse
import requests
import tarfile
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
argParser.add_argument("-k","--key", help="API key for this source")

args = argParser.parse_args()

plain_file_types = [
    "txt", "csv", "xml",
    "json", "html", "css",
    "js", "log", "md", "yaml",
    "yml", "ini", "cfg", "conf",
    "bat", "sh", "sql", "py",
]

supported_file_types = [
    "gz",
]

class file_sorter:
    def __init__(self, files:list):
        self.plain_file_types = [
            "txt", "csv", "xml",
            "json", "html", "css",
            "js", "log", "md", "yaml",
            "yml", "ini", "cfg", "conf",
            "bat", "sh", "sql", "py",
            "ps1", "psm1",
        ]
        self.special_file_types = [
            "gz",
        ]
        self.special_files =[]
        self.plain_files = []
        self.unsupported_files = []

        for file in files:
            file_extension = file.split('.')[-1]
            if file_extension in self.plain_file_types:
                self.plain_files.append(file)
            elif file_extension in self.special_file_types:
                self.special_files.append(file)
            else:
                self.unsupported_files.append(file)


class post:
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
        user_query = user_query.replace('\\*','.*')
        user_query = f"{user_query}"
        pattern = re.compile(user_query)
    elif data["query_type"] == "regex_search":
        pattern = re.compile(str(data["query"]))

    for file in data["files"]:
        data = post(data["key"], data["source"])
        print(requests.post(url, json=data.new_post(f"BEGIN: {file}\n"f"{'='*30}"), verify=False).text)
        with open(file, "r") as file_object:
            file_text = file_object.readlines()
            for line in file_text:
                if re.search(pattern, line):
                    print(requests.post(url, json=data.new_post(f"{file_text.index(line) + 1}:\t{line}"), verify=False))
        print(requests.post(url, json=data.new_post(f"{'='*30}\n"f"END: {file}\n"f"{'='*30}"), verify=False))


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