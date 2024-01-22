#!/usr/bin/env python3

import asyncio
import telegram
import os, sys

class Posts:
    def __init__(self) -> None:
        self._posts = {}
    
    def addPost(self, post):
        self._posts[post.message_id] = {
            'id': post.message_id,
            'text': post.text,
            'date': post.date
        }
    
    def getPosts(self):
        return self._posts
    
    def saveAsFiles(self):
        full_path = os.path.dirname(os.path.realpath(__file__))
        for post in self.getPosts().values():
            # f_name = YYYY-MM-DD-name-of-post.ext        
            f_name = post['date'].strftime('%Y-%m-%d-postId-')+str(post['id'])+'.md'
            full_f_name = os.path.join(full_path, "_posts", f_name)

            with open(full_f_name, 'w') as writer:
                writer.write(post['text'])


async def main(BOT_TOKEN):
    bot = telegram.Bot(BOT_TOKEN)
    posts = Posts()
    async with bot:
        updates = (await bot.get_updates())
        for update in updates:
            # take into account only new and updated posts
            if update.channel_post:
                posts.addPost(update.channel_post)
            if update.edited_channel_post:
                posts.addPost(update.edited_channel_post)
    
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
