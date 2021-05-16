import lxml
import lxml.html
import re


class Scraper:
    url_template = None

    def __init__(self, session, slug):
        self.session = session
        self.slug = slug

    def get_url(self):
        return self.url_template.format(slug=self.slug)

    async def get_value(self):
        raise NotImplementedError


class Ulule(Scraper):
    url_template = 'https://www.ulule.com/{slug}'

    async def get_value(self):
        r = await self.session.get(self.get_url())
        content = await r.text()
        m = re.search(r'"committed": (\d+),', content)
        if m is not None:
            val = float(m.group(1))
            return val
        raise ValueError("Not found in text")


class Leetchi:
    url_template = 'https://www.leetchi.com/c/{slug}'

    async def get_value(self):
        r = await self.session.get(self.get_url())
        html = lxml.html.fromstring(await r.text())
        elt = html.xpath("//span[@class='panel-status__amount']/text()")
        txt = elt[0].strip()
        value = float(txt.split()[0].replace(',', '.'))
        return value


class Cagnotte:
    url_template = 'https://cagnotte.me/{slug}/fr'

    async def get_value(self):
        r = await self.session.get(self.get_url())
        html = lxml.html.fromstring(await r.text())
        elt = html.xpath("//span[@class='collected-amount-label']/text()")
        txt = elt[0].strip()
        value = float(txt.split()[0].replace(',', '.'))
        return value


SCRAPERS = {
    cls.__name__.lower(): cls
    for cls in (Ulule, Leetchi, Cagnotte)
}
