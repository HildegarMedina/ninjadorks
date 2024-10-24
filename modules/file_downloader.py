import os
import requests

class FileDownloader:
    
    def __init__(self, path):
        self.path = path

    def create_directory(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def download_file(self, url):
        try:
            response = requests.get(url, timeout=10)
            name_file = url.split('/')[-1]
            complete_path = os.path.join(self.path, name_file)
            with open(complete_path, 'wb') as file:
                file.write(response.content)
            print(f'File {name_file} downloaded successfully!')
        except Exception as e:
            print(f'Error downloading file: {e}')

    def filter_download_files(self, urls, types=["all"]):
        if type == ["all"]:
            for url in urls:
                self.download_file(url)
        else:
            for url in urls:
                if url.split('.')[-1] in types:
                    self.download_file(url)
