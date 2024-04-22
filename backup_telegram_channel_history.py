import json
import os, sys

from telegram_post import HistoryPosts

def main(dump_dir='json_dump'):
    posts = HistoryPosts(dump_dir)

    # path to .json file with old posts
    full_path = os.path.dirname(os.path.realpath(__file__))
    dump_f_name = os.path.join(full_path, dump_dir, 'result.json')

    with open(dump_f_name, 'r') as reader:
        data = json.load(reader)
        
        for message in data['messages']:
            # read only 'message' type without 'service'
            if message['type']== "message":
                posts.addPost(message)
        
        posts.saveAsFiles()


if __name__ == '__main__':
    args = sys.argv[1:]
    config = {x.split("=")[0]:x.split("=")[1] for x in args}
    
    keys = ['dump_dir']
    for k in keys:
        if k not in config:
            print(f'{k} is not in command line args. please specify this arg as {k}="your {k} name"')
            exit(1)
    main(config['dump_dir'])
