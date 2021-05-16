import aiohttp
import aiohttp.web
import babel
import jinja2

from scrapers import SCRAPERS, Ulule


async def bar(request):
    scraper = SCRAPERS[request.query['scraper']]
    slug = request.query['slug']
    goal = int(request.query.get('goal', 1))
    rainbow = (
        request.query.get('rainbow', '').lower() in ('on', 'yes', 'true')
    )

    try:
        value = await scraper(request.app['session'], slug).get_value()
    except Exception:
        value = -1
    tpl = request.app['template_env'].get_template('bar.html')
    res = tpl.render(
        bar_value=value,
        bar_total=goal,
        rainbow=rainbow,
    )
    return aiohttp.web.Response(body=res, content_type='text/html')


async def index(request):
    tpl = request.app['template_env'].get_template('index.html')
    res = tpl.render(scrapers=SCRAPERS)
    return aiohttp.web.Response(body=res, content_type='text/html')


def get_app(argv):
    app = aiohttp.web.Application()
    app['session'] = aiohttp.ClientSession()
    app['template_env'] = env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('templates'),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    app.router.add_get("/", index)
    app.router.add_get("/bar", bar)
    return app
