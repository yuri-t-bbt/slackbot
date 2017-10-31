import os

DEFAULT_REPLY = u"""
[Command]
pulls プルリクエスト一覧を取得する
"""
API_TOKEN = os.getenv("SLACKBOT_API", "")