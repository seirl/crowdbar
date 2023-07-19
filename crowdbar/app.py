import aiohttp
import aiohttp.web
import babel.numbers
import jinja2

from .scrapers import SCRAPERS


async def bar(request):
    scraper = SCRAPERS[request.query['scraper']]
    slug = request.query['slug']
    goal = int(request.query.get('goal', 1) or 1)
    rainbow = (
        request.query.get('rainbow', '').lower() in ('on', 'yes', 'true')
    )
    animated = (
        request.query.get('animated', '').lower() in ('on', 'yes', 'true')
    )
    use_percent = (
        request.query.get('percent', '').lower() in ('on', 'yes', 'true')
    )
    color_class = {
        'blue': 'primary',
        'green': 'success',
        'cyan': 'info',
        'yellow': 'warning',
        'red': 'danger',
    }.get(request.query.get('color'), 'primary')

    try:
        value = await scraper(request.app['session'], slug).get_value()
    except Exception:
        value = -1
    tpl = request.app['template_env'].get_template('bar.html')
    res = tpl.render(
        bar_value=round(value, 2),
        bar_total=round(goal, 2),
        color_class=color_class,
        rainbow=rainbow,
        animated=animated,
        use_percent=use_percent,
    )
    return aiohttp.web.Response(body=res, content_type='text/html')


async def index(request):
    tpl = request.app['template_env'].get_template('index.html')
    res = tpl.render(scrapers=SCRAPERS)
    return aiohttp.web.Response(body=res, content_type='text/html')


async def get_app(argv=None):
    app = aiohttp.web.Application()
    app['session'] = aiohttp.ClientSession()
    app['template_env'] = jinja2.Environment(
        loader=jinja2.PackageLoader('crowdbar', 'templates'),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    app['template_env'].filters['format_decimal'] = (
        babel.numbers.format_decimal
    )
    app.router.add_get("/", index)
    app.router.add_get("/bar", bar)
    return app
