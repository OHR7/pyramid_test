import os
import sys
import transaction
from datetime import date

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from invoice.models import (
    DBSession,
    Base,
    Invoice,
    InvoiceItem
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        # Create one item and one invoice
        item = InvoiceItem(units=1, description='car', amount=2)
        invoice = Invoice(date=date.today())
        invoice.items.append(item)
        DBSession.add(item)
        DBSession.add(invoice)
