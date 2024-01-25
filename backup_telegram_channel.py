#!/usr/bin/env python3

import asyncio
import telegram
import os, sys
import requests

class Posts:
    def __init__(self) -> None:
        self._posts = {}
    
    def addPost(self, post):
        # print(post)
        self._posts[post.message_id] = {
            'id': post.message_id,
            'text': post.text,
            'date': post.date,
            'caption': post.caption
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
    
    
    
    def saveAsFiles(self):
        full_path = os.path.dirname(os.path.realpath(__file__))
        folder = os.path.join(full_path, "_posts")
        # create folder if not exists
        os.makedirs(folder, exist_ok=True)

        for post in self.getPosts().values():
            # f_name = YYYY-MM-DD-name-of-post.ext        
            f_name = post['date'].strftime('%Y-%m-%d-postId-')+str(post['id'])+'.md'
            full_f_name = os.path.join(full_path, "_posts", f_name)

            # if post has images then all text is in 'caption'
            text = post['text'] if post['text'] else post['caption']

            # download images if needed
            if 'img_url' in post.keys():
                # create HTTP response object
                r = requests.get(post['img_url'])
                
                # create folder if not exists
                image_dir = os.path.join(full_path, "_images")
                os.makedirs(image_dir, exist_ok=True)

                # save image
                f_name = post['img_url'].split('/')[-1]                
                full_image_name = os.path.join(image_dir, f_name)
                with open(full_image_name,'wb') as f: 
                    f.write(r.content)

                # update post text with relative links to images
                text = '![image](../_images/'+f_name+')\n\n' + text

            with open(full_f_name, 'w') as writer:
                writer.write(text)

async def main(BOT_TOKEN):
    bot = telegram.Bot(BOT_TOKEN)
    posts = Posts()
    async with bot:
        updates = (await bot.get_updates())
        for update in updates:
            # take into account only new and updated posts
            if update.channel_post:
                post = posts.addPost(update.channel_post)
            if update.edited_channel_post:
                post = posts.addPost(update.edited_channel_post)
            
            # retrieve image urls if needed
            if 'photo_id' in post.keys():
                ret = (await bot.getFile(file_id=post['photo_id']))
                url = ret.file_path
                post['img_url'] = url
    
    # print(posts.getPosts())
    posts.saveAsFiles()

if __name__ == '__main__':
    # read bot_token as command line arg
    # so that it can be passed as secret through github actions
    
    args = sys.argv[1:]
    config = {x.split("=")[0]:x.split("=")[1] for x in args}
    
    keys = ['bot_token']
    for k in keys:
        if k not in config:
            print(f'{k} is not in command line args. please specify this arg as {k}="your {k} name"')
            exit(1)

    asyncio.run(main(config['bot_token']))
