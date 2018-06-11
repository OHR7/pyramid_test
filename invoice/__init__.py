from sqlalchemy import engine_from_config
from .models import DBSession, Base
from pyramid.config import Configurator


def main(global_config, **settings):
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')

    config.add_route('home_view', '/')
    config.add_route('invoice', '/invoice')
    config.add_route('invoice_item', '/invoice-item')
    config.add_route('invoice_json', '/invoice.json')
    config.add_route('invoice_item_json', '/invoice-item.json')

    config.scan('.views')
    return config.make_wsgi_app()