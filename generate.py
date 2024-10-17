from datetime import datetime
import markdown
import sys
import os

# (feed, ps)
PAGE_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
  </head>
  <body>
    <h1><span class="g">G</span>Блог</h1>
    <ul class="feed">
%s
    </ul>
    <div class="ps">
%s
    </div>
  </body>
</html>
""".strip()

# (title, meta, link)
ARTICLE_PREVIEW_TEMPLATE = """
<div class="article-preview">
  <h2 class="article-preview_title">%s</h2>
  <hr>
  <div class="article-preview_inner">
    <div class="article-preview_meta">
%s
    </div>
  <button class="article-preview_link" onclick="window.location.href='%s'">Читать</button>
  </div>
</div>
""".strip()

# (text)
META_TEMPLATE = """
<p class="article-preview_meta_item">%s</p>
""".strip()

# (text)
PS_TEMPLATE = """
<p class="ps_inner">%s</p>
""".strip()

# (text, ps)
ARTICLE_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <link rel="stylesheet" href="../style.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/styles/default.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/languages/rust.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.10.0/languages/python.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
  </head>
  <body>
    <h1><span class="g">G</span>Блог</h1>
    <div class="article">
      <div class="article_navigation">
        <button class="article_navigation_back" onclick="window.location.href='../index.html'">Назад</button>
      </div>
      <hr>
      <div class="article_content">
%s
      </div>
    </div>
    <script>hljs.highlightAll();</script>
  </body>
</html>
""".strip()

class Meta:
    def __init__(self, read_time):
        self.date = datetime.today().strftime("%d.%m.%Y")
        self.read_time = read_time

    def __repr__(self):
        return META_TEMPLATE % ("Дата: " + self.date) + "\n" + \
               META_TEMPLATE % ("Время чтения: " + str(self.read_time) + "м")

class Article:
    def __init__(self, title, meta, link):
        self.title = title
        self.meta = meta
        self.link = link

    def __repr__(self):
        return ARTICLE_PREVIEW_TEMPLATE % (self.title, self.meta, self.link)

def main():
    try:
        feed_directory = sys.argv[1]
    except:
        print("error: specify feed directory")
        exit(1)
    try:
        output_directory = sys.argv[2]
    except:
        print("error: specify output directory")
        exit(1)
    
    if os.path.exists(output_directory):
        print(f"info: removing old output directory")
        os.system("rm -rf " + output_directory)

    print(f"info: creating new output directory")
    os.mkdir(output_directory)
    os.mkdir(output_directory + "/feed")

    os.system(f"cp style.css {output_directory}/style.css")

    feed_list = os.listdir(feed_directory)
    feed_list = [file_path for file_path in feed_list if file_path.endswith(".md")]
    feed_files = [open(feed_directory + "/" + file_path).read() for file_path in feed_list]

    main_page_html = ""
    for file_name, file_content in zip(feed_list, feed_files):
        output_file_path = "feed" + "/" + file_name.rsplit(".", 1)[0] + ".html"
        print(f"info: generating html for '{file_name}' at '{output_directory + '/' + output_file_path}'")

        title, content = file_content.split("\n\n", 1)
        title = title[1:].strip()
        content = content.strip()

        with open(output_directory + "/" + output_file_path, "w") as file:
            content_html = markdown.markdown(content, extensions=["markdown.extensions.fenced_code"])
            file.write(ARTICLE_TEMPLATE % (content_html))
        
        read_time = int((len(file_content) / 5.28) / 250)
        article = Article(title, Meta(read_time), output_file_path)
        main_page_html += str(article) + "\n"

    main_page_html = PAGE_TEMPLATE % (main_page_html, "")

    print(f"info: generating main page html at '{output_directory + '/index.html'}'")
    with open(output_directory + "/" + "index.html", "w") as main_page_file:
        main_page_file.write(main_page_html)

if __name__ == "__main__":
    main()
