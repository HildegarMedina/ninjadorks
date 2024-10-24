import os
import argparse
import sys
from dotenv import load_dotenv, set_key, get_key
from modules.googlesearch import GoogleSearch
from modules.results_parser import ResultParser
from modules.file_downloader import FileDownloader
from modules.chatgpt import ChatGPT
from modules.lm_studio import LmStudio

load_dotenv()
API_KEY = os.getenv('API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

def env_config():
    """Config env file."""
    api_key = input('Enter your Google API Key: ')
    engine_id = input('Enter your Google Search Engine ID: ')
    set_key('.env', 'API_KEY', api_key)
    set_key('.env', 'SEARCH_ENGINE_ID', engine_id)

def openai_config():
    """Config openai file."""
    openai_key = input('Enter your OpenAI API Key: ')
    set_key('.env', 'OPENAI_API_KEY', openai_key)

def main(query, configure_env, start_page, pages, lang, output_json, output_html, download, gen_dork):
    env_exists = os.path.exists('.env')

    if not env_exists or configure_env:
        env_config()
        print("File .env created successfully.")
        sys.exit(1)

    if not get_key('.env', 'OPENAI_API_KEY') and gen_dork:
        openai_config()
        print("File .env updated successfully.")
        sys.exit(1)

    if gen_dork:
        response = input("Do you want to generate a dork with OpenAI? (y/n): ")
        if response.lower() in ("y", "yes"):
            chatgpt = ChatGPT()
            query = chatgpt.generate_google_dork(gen_dork)
        else:
            lmstudio = LmStudio()
            query = lmstudio.generate_google_dork(gen_dork)
        print(query)
        sys.exit(1)

    gsearch = GoogleSearch(API_KEY, SEARCH_ENGINE_ID)
    results = gsearch.search(query, start_page=start_page, pages=pages, lang=lang)

    result_parser = ResultParser(results)

    if output_json:
        result_parser.export_json(output_json)
    if output_html:
        result_parser.export_html(output_html)
    if not output_json and not output_html:
        result_parser.show_screen()
    if download:
        file_downloader = FileDownloader('downloads')
        file_types = download.split(',')
        urls = [result['link'] for result in results]
        file_downloader.filter_download_files(urls, file_types)

if __name__ == "__main__":
    # Configuración de los argumentos
    parser = argparse.ArgumentParser(
        prog="Ninjadorks",
        description='Ninjadorks it´s a tool to search dorks in Google.',
    )
    parser.add_argument('-q', '--query', type=str,
                        help='Enter the query to search.')
    parser.add_argument('-c', '--config', action='store_true',
                        help='Configure the environment variables.')
    parser.add_argument('--start-page', type=int, default=1,
                        help='Enter the page number to start the search.\nBy default: 1.')
    parser.add_argument("--pages", type=int, default=1,
                        help="Enter the number of pages to search.\nBy default: 1.")
    parser.add_argument("--lang", type=str, default="lang_es",
                        help="Enter the language to search.\nBy default: lang_es.")
    parser.add_argument("--json", type=str, help="Export the results to a JSON file.")
    parser.add_argument("--html", type=str, help="Export the results to a HTML file.")
    parser.add_argument("--download", type=str, default="all", help="Enter the type of download separated by commas.\nBy default: all.\nExample: --download 'json,pdf'")
    parser.add_argument("-gd", "--generate-dork", type=str, help="Generate a dork to search.\n Example: --generate-dork 'Generate a dork to search passwords in .env files'")
    args = parser.parse_args()
        
    if not args.query and not args.generate_dork:
        parser.print_help()
        sys.exit(1)

    main(query=args.query,
        configure_env=args.config,
        start_page=args.start_page,
        pages=args.pages,
        lang=args.lang,
        output_json=args.json,
        output_html=args.html,
        download=args.download,
        gen_dork=args.generate_dork)
