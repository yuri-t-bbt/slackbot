# Slackbot

## 環境変数

| 変数定義 | 説明 |
| --- | --- |
| API_TOKEN(必須) | slackのAPIトークンを設定 |
| GITHUB_TOKEN(必須) | githubのAPIトークンを設定 |
| GITHUB_REPOS(必須) | 表示したいリポジトリ(カンマ区切りで複数) |
| GITHUB_ORG(必須) | 組織名を設定 |


## Herokuへのアップロード

```
git push heroku HEAD
```


## Herokuでのサービス


### 起動コマンド

```
heroku ps:scale portalbot=1
```

### 停止コマンド

```
heroku ps:scale portalbot=0
```
