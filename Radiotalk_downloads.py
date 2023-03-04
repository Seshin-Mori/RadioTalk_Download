from google.colab import drive
import os
import requests
import re
import xml.etree.ElementTree as ET

# ① RSSのURL(XML)ファイルを設定する。
rss_url = "https://example.com/rss.xml"

# Google Driveをマウントする
drive.mount('/content/drive')

# ② ①で設定したURLから、https://ではじまり.m4aで終わる文字列をすべて抽出する。
response = requests.get(rss_url)
urls = re.findall('https://.*\.m4a', response.text)

# ③ ②のURLにアクセスする。
download_dir = '/content/drive/MyDrive/Downloads/'
if not os.path.exists(download_dir):  # ダウンロード先のフォルダが存在しない場合は作成する
    os.makedirs(download_dir)

for url in urls:
    # ④ m4aファイルをダウンロードする。
    title = ""
    root = ET.fromstring(requests.get(rss_url).text)
    for item in root.findall("./channel/item"):
        if url in item.find("enclosure").get("url"):
            title = item.find("title").text
            break
    file_name = title + ".m4a"
    path = os.path.join(download_dir, file_name)  # ダウンロード先をGoogle Drive内に変更する
    response = requests.get(url)
    with open(path, "wb") as f:
        f.write(response.content)
    
# ⑤ 全てダウンロード完了した際に、完了メッセージを表示
print("ダウンロードが完了しました。")
