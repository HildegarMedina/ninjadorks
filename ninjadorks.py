import os
import argparse
import sys
from dotenv import load_dotenv, set_key
from googlesearch import GoogleSearch
from results_parser import ResultParser

load_dotenv()
API_KEY = os.getenv('API_KEY')
SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')

def env_config():
    """Config env file."""
    api_key = input('Introduce tu API KEY de Google: ')
    engine_id = input('Introduce el ID del buscador personalizado de Google: ')
    set_key('.env', 'API_KEY', api_key)
    set_key('.env', 'SEARCH_ENGINE_ID', engine_id)


def main(query, configure_env, start_page, pages, lang, output_json, output_html):
    env_exists = os.path.exists('.env')

    if not env_exists or configure_env:
        env_config()
        print("Archivo .env configurado correctamente.")
        sys.exit(1)

    gsearch = GoogleSearch(API_KEY, SEARCH_ENGINE_ID)
    results = gsearch.search(query, start_page=start_page, pages=pages, lang=lang)
    
    result_parser = ResultParser(results)
    
    if output_json:
        result_parser.exportar_json(output_json)
    if output_html:
        result_parser.exportar_html(output_html)
    if not output_json and not output_html:
        result_parser.show_screen()

if __name__ == "__main__":
    # Configuración de los argumentos
    parser = argparse.ArgumentParser(
        prog="Ninjadorks",
        description='Esta herramienta permite realizar Hacking con buscadores de manera automática.'
    )
    parser.add_argument('-q', '--query', type=str,
                        help='Especifica el dork que desea buscar.\nEjemplo: -q "filetype:sql \"MySQL dump\" (pass|password|passwd|pwd)"')
    parser.add_argument('-c', '--config', action='store_true',
                        help='Inicia el proceso de configuración del archivo .env\nUtiliza este argumento sin los demás para configurar el archivo .env')
    parser.add_argument('--start-page', type=int, default=1,
                        help='Especifica la página de inicio de la búsqueda.')
    parser.add_argument("--pages", type=int, default=1,
                        help="Especifica la cantidad de páginas a buscar.")
    parser.add_argument("--lang", type=str, default="lang_es",
                        help="Especifica el idioma de la búsqueda.\nPor defecto: 'lang_es'.")
    parser.add_argument("--json", type=str, help="Exporta los resultados a un archivo JSON.")
    parser.add_argument("--html", type=str, help="Exporta los resultados a un archivo HTML.")
    args = parser.parse_args()

    main(query=args.query,
        configure_env=args.config,
        start_page=args.start_page,
        pages=args.pages,
        lang=args.lang,
        output_json=args.json,
        output_html=args.html)
