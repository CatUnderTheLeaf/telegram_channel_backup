import json
import os
from telegraph import Telegraph
from bs4 import BeautifulSoup
import requests
       

def main():
    telegraph = Telegraph()

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
    if os.path.isdir(dump_images_dir):
        for file in os.listdir(dump_images_dir):
            os.rename(os.path.join(dump_images_dir, file), os.path.join(images_dir, file))

    def download_telegraph_article(article_name):
        # get page from telegraph and add title
        page = telegraph.get_page(article_name)
        article_text = "<h1>" + page['title'] + "</h1>" + page['content']
        
        # prettify html, so it has more than one line
        soup = BeautifulSoup(article_text, 'html.parser')
        # create telegraph articles folder
        article_dir = os.path.join(full_path, "_telegraph")
        # create folder if not exists
        os.makedirs(article_dir, exist_ok=True)

        # save article with html code
        f_name = os.path.join(article_dir, page['path']+'.html')
        with open(f_name, 'w') as writer:
            writer.write(soup.prettify())

        # create article image folder
        article_img_dir = os.path.join(full_path, "_files")
        os.makedirs(article_img_dir, exist_ok=True)

        # find all images in html and download them
        for link in soup.find_all('img'):
            url = link.get('src')
            img_data = requests.get('https://telegra.ph' + url).content
            
            img_name = os.path.join(article_img_dir, url.split('/')[-1])
            with open(img_name, 'wb') as handler:
                handler.write(img_data)

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
                        # if there is a telegraph link
                        if message['text'][i]['type']=='link':
                            link = message['text'][i]['text'].split('/')
                            if link[2]=='telegra.ph':
                                download_telegraph_article(link[-1])
                        message['text'][i] = message['text'][i]['text']
                        
                post = ''.join(message['text'])

                # add image link at the beginning of the post
                if 'photo' in message.keys():
                    link = message['photo'].split('/')[-1]

                    post = '![image](../_images/'+link+')\n\n' + post
                
                # print(post)
                # print("--------------------------")
                with open(full_f_name, 'w') as writer:
                    writer.write(post)


if __name__ == '__main__':
    main()
