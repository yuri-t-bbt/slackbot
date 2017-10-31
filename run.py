# coding: utf-8
import os
import re
from slackbot.bot import Bot
from slackbot.bot import respond_to
from github import Github
import psycopg2

def main():
    bot = Bot()
    bot.run()


def get_connection():
    database_uri = github_token = os.getenv("DATABASE_URL", "")
    m = re.search(r'postgres://([a-z]+):([\.\-_a-zA-Z0-9]+)@([\.\-_a-zA-Z0-9]+):([0-9]+)/([a-zA-Z0-9]+)', database_uri)
    user, password, hostname, port, database = m.group(1), m.group(2), m.group(3), m.group(4), m.group(4)
    return psycopg2.connect("host={0} port={1} dbname={2} user={3} password={4}".format(
        hostname, port, database, user, password
    ))


@respond_to('pulls')
def github_pullreq(message):
    github_token = os.getenv("GITHUB_TOKEN", "")
    github_repos = os.getenv("GITHUB_REPOS")
    github_org = os.getenv("GITHUB_ORG")
    if len(github_token) == 0:
        message.reply('Sorry, app error...')
    g = Github(github_token, api_preview=True)
    org = g.get_organization(github_org)
    targets = github_repos.split(',')
    say = '\n'
    for target in targets:
        repo = org.get_repo(target)
        pulls = [pull for pull in repo.get_pulls()]
        if len(pulls) > 0:
            say += '{0}:\n{1}\n\n'.format(target, '\n'.join([' - {0} {1}'.format(p.title, p.html_url) for p in pulls]))
        else:
            say += '{0}: Nothing.\n\n'.format(target)
    message.reply(say)


@respond_to(r'(.*)\+\+')
def good(message, target):



if __name__ == '__main__':
    main()