import aiohttp.web

from .app import get_app

if __name__ == '__main__':
    aiohttp.web.run_app(get_app())
