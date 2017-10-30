# coding: utf-8
import os
from slackbot.bot import Bot
from slackbot.bot import respond_to
from github import Github

def main():
    bot = Bot()
    bot.run()

@respond_to('pulls')
def github_pullreq(message):
    github_token = os.getenv("GITHUB_TOKEN", "")
    if len(github_token) == 0:
        message.reply('Sorry, app error...')
    g = Github(github_token, api_preview=True)
    org = g.get_organization('bbtinc')
    targets = ("portal", "portalapi", "texas", "mypage", "accontent")
    say = '\n'
    for target in targets:
        repo = org.get_repo(target)
        pulls = [(pull.title, pull.url) for pull in repo.get_pulls()]
        if len(pulls) > 0:
            say += '{0}:\n{1}\n\n'.format(target, '\n'.join([' - {0} {1}'.format(p[0],p[1]) for p in pulls]))
        else:
            say += '{0}: Nothing.\n\n'.format(target)
    message.reply(say)


if __name__ == '__main__':
    main()