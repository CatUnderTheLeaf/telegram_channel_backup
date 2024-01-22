#!/usr/bin/env python3

from github import Github, Auth
import os
import sys

def main(TOKEN, GITHUB_REPO, branch):
    # create a Github instance using an access token
    auth = Auth.Token(TOKEN)
    g = Github(auth=auth)

    # get set (the lookup will be O(1)) of files in repo
    repo = g.get_user().get_repo(GITHUB_REPO)
    # repo = g.get_user().get_repo(GITHUB_REPO)
    # repo = g.get_repo("CatUnderTheLeaf/"+GITHUB_REPO)
    all_files = set()
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.add(str(file).replace('ContentFile(path="','').replace('")',''))

    # upload to github each post as seperate commit
    full_path = os.path.dirname(os.path.realpath(__file__))
    dir_prefix = '_posts'
    full_dir_name = os.path.join(full_path, dir_prefix)
    file_list = os.listdir(full_dir_name)

    for file in file_list:
        file_with_dir = os.path.join(dir_prefix, file)
        full_f_name = os.path.join(full_path, file_with_dir)
        with open(full_f_name, 'r') as reader:
            content = reader.read()

        # get post id from filename
        postId = file.split('-')[-1].split('.')[0]

        if file_with_dir in all_files:
            contents = repo.get_contents(file_with_dir)
            repo.update_file(contents.path, "updating post " + postId, content, contents.sha, branch)
            print(file_with_dir + ' UPDATED')
        else:
            repo.create_file(file_with_dir, "creating post " + postId, content, branch)
            print(file_with_dir + ' CREATED')

    # close connections after use
    g.close()

if __name__ == '__main__':
    # read auth_token, repo and branch as command line arg
    args = sys.argv[1:]
    config = {x.split("=")[0]:x.split("=")[1] for x in args}
    
    keys = ['repo', 'branch', 'auth_token']
    for k in keys:
        if k not in config:
            print(f'{k} is not in command line args. please specify this arg as {k}="your {k} name"')
            exit(1)
    
    main(config['auth_token'], config['repo'], config['branch'])
