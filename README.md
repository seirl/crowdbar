# Crowdbar

An embeddable crowdfunding progress bar for OBS streams.

## Run

In debug mode:

    python -m aiohttp.web -H localhost -P 8071 crowdbar.app:get_app

With Gunicorn:

    gunicorn -b 127.0.0.1:8071 --worker-class aiohttp.GunicornWebWorker crowdbar.app:get_app
