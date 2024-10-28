import os
import re
import argparse
from transformers import GPT2Tokenizer
from openai import OpenAI
from dotenv import load_dotenv


class SmartSearch:
    
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.files = self._read_files()

    def _read_files(self):
        """Read all files in the directory"""
        files = {}
        for file in os.listdir(self.dir_path):
            file_path = os.path.join(self.dir_path, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    files[file] = f.read()
            except Exception as e:
                print(f'Error reading file {file_path}: {e}')
        return files

    def regex_search(self, regex):
        """Search information using regex"""
        results = {}
        for file, text in self.files.items():
            response = ""
            while response not in ("y", "n", "yes", "no"):
                response = input(f'Search in {file} ({len(text)} caracters)? (y/n): ')
            if response in ("n", "no"):
                continue
            matches = re.findall(regex, text, re.IGNORECASE)
            if not matches == []:
                results[file] = matches
        return results

    def ia_search(self, prompt, model_name="gpt-3.5-turbo-0125", max_tokens=100):
        """Search information using IA"""
        results = {}
        for file, text in self.files.items():
            response = ""
            tokens, cost = self._calculate_cost(text, prompt, model_name, max_tokens)
            while response not in ("y", "n", "yes", "no"):
                response = input(f'Search in {file} (tokens: {tokens} | Cost: {cost})? (y/n): ')
                if response in ("n", "no"):
                    continue

                file_segments = self._split_file(text, model_name)
                load_dotenv()

                client = OpenAI()
                results_segments = []
                for index, segment in enumerate(file_segments):
                    print(f"Searching in segment {index + 1} / {len(file_segments)}...")
                    chat_completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "user",
                                "content": f"{prompt}\n\nTexto:\n{segment}"
                            },
                        ],
                        model=model_name,
                        max_tokens=max_tokens,
                        n=1
                    )
                    results_segments.append(chat_completion.choices[0].message.content)
                results[file] = results_segments
        return results


    def _split_file(self, file_text, model_name):
        """Split the file text in parts to avoid the max tokens limit"""
        context_window_sizes = {
            "gpt-4-0125-preview": 128000,
            "gpt-4-1106-preview": 128000,
            "gpt-4": 16000,
            "gpt-4-32k": 32000,
            "gpt-3.5-turbo-0125": 16000,
            "gpt-3.5-turbo-instruct": 4000
        }
        return [
            file_text[i:i+context_window_sizes[model_name]]
            for i in range(0, len(file_text), context_window_sizes[model_name])
        ]

    def _calculate_cost(self, text, prompt, model_name, max_tokens):
        """Calculate the cost of the text"""
        prices = {
            "gpt-4-0125-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4-1106-vision-preview": {"input_cost": 0.01, "output_cost": 0.03},
            "gpt-4": {"input_cost": 0.03, "output_cost": 0.06},
            "gpt-4-32k": {"input_cost": 0.06, "output_cost": 0.12},
            "gpt-3.5-turbo-0125": {"input_cost": 0.0005, "output_cost": 0.0015},
            "gpt-3.5-turbo-instruct": {"input_cost": 0.0015, "output_cost": 0.002}
        }
        tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        len_tokens_prompt = len(tokenizer.tokenize(prompt))
        len_tokens_text = len(tokenizer.tokenize(text))
        input_cost = (len_tokens_prompt + len_tokens_text) / 1000 * prices[model_name]['input_cost']
        output_cost = max_tokens / 1000 * prices[model_name]['output_cost']
        return (len_tokens_prompt + len_tokens_text, input_cost + output_cost)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search information in files using regex.')
    parser.add_argument("dir_path", type=str, help="Directory path to search.")
    parser.add_argument("-r", "--regex", type=str, help="Regex to search.")
    parser.add_argument('-p', '--prompt', type=str, help='Prompt to search.')
    parser.add_argument('-m', '--model', type=str, help='Model to use. Default: gpt-3.5-turbo-0125', default='gpt-3.5-turbo-0125')
    parser.add_argument('--max-tokens', type=int, help='Max tokens to use. Default: 100', default=100)
    args = parser.parse_args()

    if args.regex:
        smart_search = SmartSearch(args.dir_path)
        results = smart_search.regex_search(args.regex)
        for file, results in results.items():
            print(f'File: {file}')
            for r in results:
                print(f"\t- {r}")
    
    if args.prompt and args.model and args.max_tokens:
        smart_search = SmartSearch(args.dir_path)
        results = smart_search.ia_search(args.prompt, args.model, args.max_tokens)
        for file, results in results.items():
            print(f'File: {file}')
            for r in results:
                print(f"\t- {r}")

    if not args.dir_path and not args.regex:
        parser.print_help()
