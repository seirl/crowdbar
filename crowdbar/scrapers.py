import lxml
import lxml.html


class Scraper:
    url_template = None

    def __init__(self, session, slug):
        self.session = session
        self.slug = slug

    def get_url(self):
        if self.url_template is None:
            raise NotImplementedError("url_template not set for scraper.")
        return self.url_template.format(slug=self.slug)

    async def get_value(self):
        raise NotImplementedError


class Ulule(Scraper):
    url_template = 'https://api.ulule.com/v1/projects/{slug}'

    async def get_value(self):
        r = await self.session.get(self.get_url())
        content = await r.json()
        return float(content['committed'])


class Leetchi(Scraper):
    url_template = 'https://www.leetchi.com/c/{slug}'

    async def get_value(self):
        r = await self.session.get(self.get_url())
        html = lxml.html.fromstring(await r.text())
        elt = html.xpath("//span[@class='panel-status__amount']/text()")
        txt = elt[0].strip()
        value = float(txt.split()[0].replace(',', '.'))
        return value


class Cagnotte(Scraper):
    url_template = 'https://cagnotte.me/{slug}/fr'

    async def get_value(self):
        r = await self.session.get(self.get_url())
        html = lxml.html.fromstring(await r.text())
        elt = html.xpath("//div[@class='collected-amount-label']/text()")
        txt = elt[0].strip()
        value = float(txt.split()[0].replace(',', '.'))
        return value


SCRAPERS = {
    cls.__name__.lower(): cls
    for cls in (Ulule, Leetchi, Cagnotte)
}
