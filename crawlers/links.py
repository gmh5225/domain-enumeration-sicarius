from requests_html import AsyncHTMLSession
import sys

class Crawler:
    def __init__(self, url) -> None:
        self.url = url

    async def get_page(self, url):
        if self.url == None or self.url == "":
            pass

        try:
            url_links_dict = {}
            asession = AsyncHTMLSession()
            url_session = await asession.get(url)
            render_session = await url_session.html.arender()

            for abs_links in render_session.html.absolute_links:
                url_links_dict[self.url] = abs_links
            
            if len(url_links_dict.keys()) > 0:
                return url_links_dict
            return None
        except KeyboardInterrupt:
            print("[!] Shuting donw 🔫..")
            sys.exit(1)

