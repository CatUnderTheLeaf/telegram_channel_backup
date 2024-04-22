import os
import requests
from telegraph import Telegraph
from bs4 import BeautifulSoup

class Posts:
    def __init__(self) -> None:
        self._posts = {}
        self.folders = {
            'posts_dir': "_posts",
            'image_dir': "_images",
            'article_dir': "_telegraph",
            'article_img_dir': "file"
        }
        # create folders if not exist            
        full_path = os.path.dirname(os.path.realpath(__file__))
        for k,v in self.folders.items():            
            v = os.path.join(full_path, v)
            os.makedirs(v, exist_ok=True)
    
    def addPost(self, post):
        self._posts[post.message_id] = {
            'id': post.message_id,
            'text': post.text,
            'date': post.date.strftime('%Y-%m-%d'),
            'caption': post.caption,
            'img_url': '',
            'image_name': '',
            'media_group_id': post.media_group_id
        }
        if post.photo:
            max_size = 0
            for pic in post.photo:
                if pic.file_size > max_size:
                    self._posts[post.message_id]['photo_id'] = pic.file_id
                    max_size = pic.file_size
        
        return self._posts[post.message_id]
    
    def getPosts(self):
        return self._posts
    
    def download_image(self, url, folder):
        img_data = requests.get(url).content
            
        img_name = os.path.join(folder, url.split('/')[-1])
        with open(img_name, 'wb') as handler:
            handler.write(img_data)


    def download_telegraph_article(self, article_name):
        # get page from telegraph and add title
        page = Telegraph().get_page(article_name)
        article_text = "<h1>" + page['title'] + "</h1>" + page['content']
        
        # prettify html, so it has more than one line
        soup = BeautifulSoup(article_text, 'html.parser')

        # save article with html code
        f_name = os.path.join(self.folders['article_dir'], page['path']+'.html')
        with open(f_name, 'w') as writer:
            writer.write(soup.prettify())

        # find all images in html and download them
        for link in soup.find_all('img'):
            url = 'https://telegra.ph' + link.get('src')
            self.download_image(url, self.folders['article_img_dir'])
           
    def saveAsFiles(self):

        for post in self.getPosts().values():
            # f_name = YYYY-MM-DD-name-of-post.ext        
            f_name = post['date'][:10]+'-postId-'+str(post['id'])+'.md'
            full_f_name = os.path.join(self.folders['posts_dir'], f_name)

            # if post has images then all text is in 'caption'
            text = post['text'] if post['text'] else ''
            if post['caption']:
                text = post['caption']

            # download images if needed
            if post['img_url']:
                # get image from url
                self.download_image(post['img_url'], self.folders['image_dir'])
                # add image filename
                post['image_name'] = post['img_url'].split('/')[-1]    

            # add media_group_id if images are grouped
            if post['media_group_id']:
                text = 'media_group_id = ' + post['media_group_id'] + '\n\n' + text

            # update post text with relative links to images
            if post['image_name']:
                text = '![image](../_images/'+post['image_name']+')\n\n' + text

            with open(full_f_name, 'w') as writer:
                writer.write(text)

class HistoryPosts(Posts):
    def __init__(self, dump_dir):
        super().__init__()
        dump_images_dir = os.path.join(dump_dir, 'photos')

        # move all dump images to correct folder
        if os.path.isdir(dump_images_dir):
            for file in os.listdir(dump_images_dir):
                os.rename(os.path.join(dump_images_dir, file), os.path.join(self.folders['image_dir'], file))
    
    def addPost(self, post):
        self._posts[post['id']] = {
            'id': post['id'],
            'date': post['date'][:10],
            'image_name': post['photo'].split('/')[-1] if 'photo' in post.keys() else '',
            'caption': '',
            'img_url': '',
            'media_group_id': ''
        }

        # convert hashtag dict instance to plain text and join string
        # download telegraph article if there is a link to it
        for i in range(len(post['text'])):
            if isinstance(post['text'][i], dict):
                # if there is a telegraph link
                if post['text'][i]['type']=='link':
                    link = post['text'][i]['text'].split('/')
                    if link[2]=='telegra.ph':
                        self.download_telegraph_article(link[-1])
                post['text'][i] = post['text'][i]['text']    
        self._posts[post['id']]['text'] = ''.join(post['text'])

        return self._posts[post['id']]