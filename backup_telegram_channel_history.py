import json
import os

def main():
    # path to .json file with old posts
    full_path = os.path.dirname(os.path.realpath(__file__))
    dump_f_name = os.path.join(full_path, "json_dump", 'result.json')
    dump_images_dir = os.path.join(full_path, "json_dump", 'photos')

    posts_dir = os.path.join(full_path, "_posts")
    images_dir = os.path.join(full_path, "_images")
    # create folder if not exists
    os.makedirs(posts_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)
    # move all images to correct folder
    for file in os.listdir(dump_images_dir):
        os.rename(os.path.join(dump_images_dir, file), os.path.join(images_dir, file))

    with open(dump_f_name, 'r') as reader:
        data = json.load(reader)
        
        for message in data['messages']:
            # read only 'message' type without 'service'
            if message['type']== "message":
                # f_name = YYYY-MM-DD-name-of-post.ext     
                f_name = message['date'][:10]+'-postId-'+str(message['id'])+'.md'
                full_f_name = os.path.join(posts_dir, f_name)
                
                # convert hashtag dict instance to plain text
                for i in range(len(message['text'])):
                    if isinstance(message['text'][i], dict):
                        message['text'][i] = message['text'][i]['text']
                        
                post = ''.join(message['text'])

                # add image link at the beginning of the post
                if 'photo' in message.keys():
                    link = message['photo'].split('/')[-1]

                    post = '![image](../_images/'+link+')\n\n' + post
                
                with open(full_f_name, 'w') as writer:
                    writer.write(post)



if __name__ == '__main__':
    main()
