import feedparser
import telegram
import time
import os

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']

bot = telegram.Bot(token=BOT_TOKEN)

FEEDS = {
    'MyAnimeList': 'https://myanimelist.net/rss/news.xml',
    'Anime News Network': 'https://www.animenewsnetwork.com/all/rss.xml',
    'AniTrendz': 'https://anitrendz.net/news/feed'
}

POSTED_FILE = 'posted_links.txt'

if os.path.exists(POSTED_FILE):
    with open(POSTED_FILE, 'r') as f:
        posted_links = set(f.read().splitlines())
else:
    posted_links = set()

def save_posted(link):
    with open(POSTED_FILE, 'a') as f:
        f.write(link + '\n')
    posted_links.add(link)

def fetch_and_send():
    for src, url in FEEDS.items():
        feed = feedparser.parse(url)
        if not feed.entries:
            continue
        for entry in feed.entries[:3]:
            link = entry.link
            if link in posted_links:
                continue
            title = entry.title
            summary = entry.summary[:300].split('<')[0] + '...'
            msg = f"📰 *{title}*\n_Source: {src}_\n\n{summary}\n\n🔗 [Read More]({link})"
            bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
            save_posted(link)
            time.sleep(2)

if __name__ == '__main__':
    while True:
        fetch_and_send()
        time.sleep(1800)
