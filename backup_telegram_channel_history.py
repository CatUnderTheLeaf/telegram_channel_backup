import json
import os

def main():
    # path to .json file with old posts
    full_path = os.path.dirname(os.path.realpath(__file__))
    dump_f_name = os.path.join(full_path, "json_dump", 'result.json')

    with open(dump_f_name, 'r') as reader:
        data = json.load(reader)
        
        for message in data['messages']:
            # read only 'message' type without 'service'
            if message['type']== "message":
                # f_name = YYYY-MM-DD-name-of-post.ext     
                f_name = message['date'][:10]+'-postId-'+str(message['id'])+'.md'
                full_f_name = os.path.join(full_path, "_posts", f_name)
                
                # convert hashtag dict instance to plain text
                for i in range(len(message['text'])):
                    if isinstance(message['text'][i], dict):
                        message['text'][i] = message['text'][i]['text']
                        
                post = ''.join(message['text'])
                
                with open(full_f_name, 'w') as writer:
                    writer.write(post)



if __name__ == '__main__':
    main()
