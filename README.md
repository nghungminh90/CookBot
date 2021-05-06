# CookBot

Cookpadサイトから情報収集の遊びプロジェクト

利用技術：Python、Scrapy。

実施方法：
scrapy crawl cookpad --set FEED_EXPORT_ENCODING=utf-8 --output=cookpad.json

データ取得先はcookpad.pyにおけるstart_urls変数を編集
ページネーションパターンの編集はrules変数を編集
