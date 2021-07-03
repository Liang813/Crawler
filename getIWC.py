# -*- coding: utf-8 -*-
# get <issue,commit>
import re
import random
from time import sleep

from github import Github
import pandas as pd

# Enter your Github token
user_token = [
    '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',
    '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',
    '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'
]

g = Github(user_token[random.randint(0, len(user_token) - 1)])


# calling the search repo API
def get_repositories(keywords):
    repositories = g.search_repositories(query=keywords)
    print('get repositories {}'.format(repositories.totalCount))

    return repositories


# 遍历issues，获取issue与commit信息
def get_relations(repo_issues, repo_name, repo_owner):
    relations = []
    for issue in repo_issues:
        issue_number = issue.number
        issue_title = issue.title
        issue_title.encode('utf-8', 'ignore')
        issue_label = ''
        if issue.labels is not None:
            for label in issue.labels:
                issue_label = label.name
                issue_label.encode('utf-8', 'ignore')
        issue_html_url = issue.html_url
        issue_html_url.encode('utf-8', 'ignore')
        # 去除掉Pull Request，只要issue
        if 'pull' not in issue_html_url:
            issue_events = issue.get_events()
            commit_ids = []
            for issue_event in issue_events:
                if issue_event.commit_id is not None:
                    commit_id = issue_event.commit_id
                    commit_ids.append(commit_id)

            if len(commit_ids) == 1:
                relation_tup = tuple()
                commit_info = repo.get_commit(commit_id)
                commit_message = commit_info.commit.message
                if '#' or 'issue' in commit_message and str(issue_number) in commit_message:
                    # commit_number = re.findall(r"(?<=\#)\d+", commit_message)
                    commit_url = commit_info.html_url
                    relation_tup = (issue_html_url, commit_url)
                    relations.append(relation_tup)
            else:
                relation_tup = tuple()
                for cid in commit_ids:
                    commit_info = repo.get_commit(commit_id)
                    commit_message = commit_info.commit.message
                    if '#' or 'issue' in commit_message and str(issue_number) in commit_message:
                        # commit_number = re.findall(r"(?<=\#)\d+", commit_message)
                        commit_url = commit_info.html_url
                        relation_tup = (issue_html_url, commit_url)
                        relations.append(relation_tup)
                    break

    print(relations)
    return relations


if __name__ == '__main__':
    keywords = input('Enter your keywords:')
    repositories = get_repositories(keywords)
    flag = 0
    for repo in repositories:
        if repo.fork:
            continue
        repo_name = repo.name
        repo_name.encode('utf-8', 'ignore')
        print(repo_name)
        repo_owner = repo.owner.login
        repo_owner.encode('utf-8', 'ignore')

        repo_issues = repo.get_issues(state='closed')
        relations_info = []

        # try:
        #     relations_info = get_relations(repo_issues, repo_name, repo_owner)
        # except Exception as e:
        #     sleep(180)
        #     g = Github(user_token[random.randint(0, len(user_token) - 1)])
        relations_info = get_relations(repo_issues, repo_name, repo_owner)

        if len(relations_info) == 0:
            continue

        fileName = 'relations_of_' + keywords + '.csv'
        data = pd.DataFrame(relations_info)
        try:
            if flag == 0:
                csv_headers = ['issue_url', 'commit_url']
                data.to_csv(fileName, header=csv_headers, index=False,
                            mode='a+', encoding='utf-8-sig')

            else:
                data.to_csv(fileName, header=False, index=False,
                            mode='a+', encoding='utf-8-sig')
                flag += 1
        except UnicodeEncodeError:
            print('Encode error drop the data')
