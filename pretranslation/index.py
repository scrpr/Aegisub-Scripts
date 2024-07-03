import argparse
import ass
import pre_translate
import config

def handle_files(input_file, context, keywords, model, maxtoken):
        with open(input_file, encoding='utf-8-sig', mode='r') as f:
            doc = ass.parse(f)
            texts_and_names = []
            temp_texts_names = []
            for i in range(len(doc.events)):
                temp_texts_names.append({"speaker": doc.events[i].name, "text": doc.events[i].text})
            
            if model == "sakura":
                texts_and_names = pre_translate.pre_translation_sakura(input_lines=temp_texts_names, context=context, keywords=keywords, model=model)
            else:
                texts_and_names = pre_translate.pre_translation(input_lines=temp_texts_names, context=context, keywords=keywords, model=model, maxtoken=maxtoken)

            for i in range(len(texts_and_names)):
                doc.events[i].text = texts_and_names[i]['text']

            output_file = input_file.replace('.ass', f'_{model}.ass')
            with open(output_file, encoding='utf-8-sig', mode='w+') as f_out:
                doc.dump_file(f_out)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--context', default='', help='background information')
    parser.add_argument('-k', '--keywords', default='', help='keywords that deserve mention')
    parser.add_argument('-m', '--model', default='gpt-3.5-turbo', help='choose which model to use')
    parser.add_argument('-t', '--max-token', default='1000', help='Max context token used in non-sakura models')
    parser.add_argument_group('API Vars')
    parser.add_argument('--openai-key', help='Your own OPENAI API key')
    parser.add_argument('--openai-url', help='OPENAI base url')
    parser.add_argument('--moonshot-key', help='Moonshot API key')
    parser.add_argument('--sakura-key', 'SakuraLLM key, usually unvalidated')
    parser.add_argument('--sakura-url', 'SakuraLLM base url')
    # parser.add_argument('-l', '--list', action='version', version=version)
    parser.add_argument('input', help="the input ass file")
    args = parser.parse_args()

    if args.openai_key:
        config.set_openai_key(args.openai_key)
    if args.openai_url:
        config.set_openai_url(args.openai_url)
    if args.moonshot_key:
        config.set_moonshot_key(args.moonshot_key)
    if args.sakura_key:
        config.set_sakura_key(args.moonshot_url)
    if args.sakura_url:
        config.set_sakura_url(args.sakura_url)

    handle_files(input_file=args.input, context=args.context, keywords=args.keywords, model=args.model, maxtoken=args.max_token)