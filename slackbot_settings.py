import os

DEFAULT_REPLY = u"""
使い方

[Command]
pulls プルリクエスト一覧を表示する
backlog 未解決課題を一覧を表示する
"""
API_TOKEN = os.getenv("SLACKBOT_API", "")