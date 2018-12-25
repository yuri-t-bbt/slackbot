# coding: utf-8
import os
import re
from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
from github import Github
import psycopg2
import requests
import json


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


@respond_to('backlog')
def backlog_issues(message):
    backlog_key = os.getenv("BACKLOG_API", "")
    url = 'https://bbt757.backlog.com/api/v2/issues?&apiKey={0}&projectId[]=18268&statusId[]=1&statusId[]=2&statusId[]=3&createdUserId[]=86613'.format(backlog_key)
    response = requests.get(url)
    if (response.status_code % 100) == 2:
        # Success
        say = '\n'
        issues = json.loads(response.text)
        for issue in issues:
            summary = issue['summary']
            issueKey = issue['issueKey']
            status_name = issue['status']['name']
            priority_name = issue['priority']['name']
            create_date = issue['created']
            due_date = issue['dueDate']
            issue_type = issue['issueType']['name']
            url = 'https://bbt757.backlog.com/view/' + issueKey
            say += '[{0}][{1}] {2} {3} {4} 期限：{5}\n'.format(status_name, priority_name, issue_type, summary, url, due_date)
        message.reply(say)
    else:
        # error!!
        message.reply("backlog api error!! {0}".format(response.status_code))


#@respond_to('neko')
#def neko_usage(message):
#    message.reply('''lgtm: LGTM
#    kirei: コードがきれい
#    hello: Hello World
#    sasuga: さすがです
#    shinchoku: 進捗どうですか
#    dame: 進捗ダメです
#    teiji: 定時上がり
#    kitaku: VR帰宅
#    hayai: 仕事はやい
#    genki: 元気出して
#    kami: 神
#    sugoi: すごい
#    arigato: ありがとうございます
#    tasukaru: いつも助かります
#    ryokai: 了解です
#    onegai: おねがいします
#    yarushika: やるしかない
#    ''')
#
#@listen_to('lgtm')
#def neko_lgtm(message):
#    message.send('https://lh6.googleusercontent.com/MqtR2yK6E5AzcV_tjEPfgZZUAkynpbm4y_X6BMOuOrIkMdArPf_SQpazErGu9Gfq2eK8smfPmhwZjDR_2QPi=w1514-h699')
#
#@listen_to('kirei')
#def neko_kirei(message):
#    message.send('https://lh6.googleusercontent.com/MqtR2yK6E5AzcV_tjEPfgZZUAkynpbm4y_X6BMOuOrIkMdArPf_SQpazErGu9Gfq2eK8smfPmhwZjDR_2QPi=w1514-h699')
#
#@listen_to('hello')
#def neko_kirei(message):
#    message.send('https://lh5.googleusercontent.com/d6iwSiL-_ywxQjTFff5nVMQ5U6AacqA1SYv8kfS-Pb2zPQwiKZcMVYuRD68hrZPdulQByjQwvPHVBPsTKh-F=w1514-h699')
#
#@listen_to('sasuga')
#def neko_sasuga(message):
#    message.send('https://lh4.googleusercontent.com/3FovYg0dYY7EqIcrNrav-H0TUL0sAtM0A_bWSaFeep-l7gAuGGwbghydDKDs8veJIs7LfHOwtLy3Rslz0PFq=w1514-h699')
#
#@listen_to('shinchoku')
#def neko_shinchoku(message):
#    message.send('https://lh5.googleusercontent.com/PRnIs03FEAS-m_jXzbODO6F4kEVQ2tzaDEf-076bj9gwd59w0HBt7sE8VQraOID9jrmMzkRu6rzo91wZ_Nqd=w1514-h699')
#
#@listen_to('dame')
#def neko_dame(message):
#    message.send('https://lh3.googleusercontent.com/2FVXlj6He68Kr4GoYs22XCp9XOdzyqrHNwtOjFD6Rdd5rrWeQAojQ95y_AznswzsUWSp_f5FBPP_C-2nwStz=w1514-h699')
#
#@listen_to('teiji')
#def neko_teiji(message):
#    message.send('https://lh4.googleusercontent.com/2hlYZhV9xxZJAYLfhUsPcF_3FvG2LbCupAWCVTXEgbiUxB2lMVFyUTZAjB9FeCX5uuIVak1cQnor6jt4poek=w1514-h699')
#
#@listen_to('kitaku')
#def neko_kitaku(message):
#    message.send('https://lh5.googleusercontent.com/8kP7T_l_wn--q5elq89T6UkgUpeJOZ91wCkqguLYfeTwHzS3eAkUzrPgc2LgUTEXoN68bm7xhLv6_HhGr8jI=w1514-h699')
#
#@listen_to('hayai')
#def neko_kitaku(message):
#    message.send('https://lh3.googleusercontent.com/WoBpZpX0SaDXGaybiUPJJNK0yoFppKRW4swbNP9sBvFjvRel4wOwcV4pbRKItBCX4v1SaqIv39uyRxniDatc=w1514-h699')
#
#@listen_to('genki')
#def neko_genki(message):
#    message.send('https://lh5.googleusercontent.com/KwjXrTcTRRPMUWigstMh2FgMYn6urD1QO0s1VbTMxI9LM6UBUXCbrNUCuPkr668XtlAUN_auPDwcHO44jzv0=w1514-h699')
#
#@listen_to('kami')
#def neko_kami(message):
#    message.send('https://lh5.googleusercontent.com/o_RRDSQhQcPQ3lhmnuyLK29qr9Uob82LFm84gOgegxtrj-8HrdP6MydvVJ7qqWYKGpE-h__Td62R6cChHTn3=w1514-h699')
#
#@listen_to('sugoi')
#def neko_sugoi(message):
#    message.send('https://lh4.googleusercontent.com/2n2TDYoLSA_rH_F2aALem2rz588GCLw8qSo8CbQWg74XYeDNXhf3kGRpCKo2q7el_W2uy_MCTTUU3CcQRacP=w1514-h699')
#
#@listen_to('arigato')
#def neko_arigato(message):
#    message.send('https://lh6.googleusercontent.com/C4bAEDE7XwDjhwLqbp0gEQnbutV17P5HckZ_cNg35LGUW37avKUeA32ilK0T90Z2RJkJ7XpT6JAVDFAI5tD2=w1514-h699')
#
#@listen_to('tasukaru')
#def neko_arigato(message):
#    message.send('https://lh5.googleusercontent.com/s__-lOlyjY5iA77UUJQVieXW_zkhzOiS-cNTE3tOuD5VW7siMsFMfGp8ZBYxGnFoB2csruhdO_STePi-bHRm=w1514-h699')
#
#@listen_to('ryokai')
#def neko_ryokai(message):
#    message.send('https://lh6.googleusercontent.com/64yMjd95WrBj-vMVoiBpaWtwIad_icTGcRXoCs-ROZFXKr52wZY0KhSqbgKMib_jv5A4z33v6LJgUmqloxrZ=w1514-h699')
#
#@listen_to('onegai')
#def neko_onegai(message):
#    message.send('https://lh4.googleusercontent.com/6b1Gwl7MmMLxUcIBdR-1CFRYVWNGifBCAgK2WluqZZEvfJM7c2phn2A5gFIngk9-LUwH1HReRTFXvWnGzlZC=w1514-h699')
#
#@listen_to('yarushika')
#def neko_yarushika(message):
#    message.send('https://lh5.googleusercontent.com/XSMrRQEnji4i41QdlSTcNMDHyRWsWeHEsB5X-rePguaIuUmtzLpSHTw35dxDX5QFjTT5BI2G2_zNgAFoMcG2=w1514-h699')


if __name__ == '__main__':
    main()
