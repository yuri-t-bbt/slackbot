import os

DEFAULT_REPLY = u"""
使い方

[Command]
pulls プルリクエスト一覧を取得する
"""
API_TOKEN = os.getenv("SLACKBOT_API", "")