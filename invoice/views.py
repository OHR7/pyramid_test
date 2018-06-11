import decimal
from json import JSONDecodeError
from datetime import date
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config, view_defaults
from .models import DBSession, Invoice, InvoiceItem


@view_config(route_name='home_view', renderer='templates/invoice.jinja2')
def home_view(request):
    invoice = DBSession.query(Invoice).first()

    return dict(invoice=invoice)


@view_defaults(route_name='invoice')
class InvoiceViews(object):
    def __init__(self, request):
        self.request = request

    @view_config(renderer='templates/invoice.jinja2', request_method='GET')
    @view_config(route_name='invoice_json', renderer='json')
    def invoice_view(self):
        invoices = DBSession.query(Invoice)
        items = DBSession.query(InvoiceItem)

        return {
            'results': [
                {
                    'id': invoice.id,
                    'date': invoice.date.__str__(),     # Cant use Date directly so used the str rep
                }
                for invoice in invoices
            ],
            # Here I also return the items to be render in the Form Options
            'items': [
                {
                    'id': item.id,
                    'description': item.description,
                }
                for item in items
            ]

        }

    @view_config(renderer='templates/invoice.jinja2', request_method='POST')
    def new_invoice_view(self):
        invoice = Invoice(date=date.today())

        # Check if it is a normal request or a JSON request
        try:
            print(self.request.json_body)
            item_ids = self.request.json_body['items']

        # Normal POST Request from HTML Form
        except JSONDecodeError:
            item_ids = self.request.params.getall('items')  # Get the list from Multidict obj
            print(item_ids)

        # Append one by one to invoice obj
        for item_id in item_ids:
            try:
                item = DBSession.query(InvoiceItem).filter_by(id=item_id).one()
                invoice.items.append(item)
            except Exception as e:
                print(e)

        DBSession.add(invoice)

        # Return to same URL
        next_url = self.request.route_url('invoice')
        return HTTPFound(location=next_url)


@view_defaults(route_name='invoice_item')
class InvoiceItemsViews(object):
    def __init__(self, request):
        self.request = request

    @view_config(route_name='invoice_item_json', renderer='json')
    def invoice_item_api_view(self):

        invoice_id = self.request.params['invoice_id']
        invoice = DBSession.query(Invoice).filter_by(id=invoice_id).one()

        return {
            'results': [
                {
                    'id': item.id,
                    'amount': float(item.amount),   # Cant use Decimal directly so casted to float
                    'units': item.units,
                    'description': item.description,
                }
                for item in invoice.items
            ]
        }

    # This view can recieve GET and POST requests
    @view_config(renderer='templates/invoice-item.jinja2')
    def new_invoice_item_view(self):

        # Check if it is a POST request
        if self.request.method == 'POST':

            # Check if it is a normal request or a JSON request
            try:
                print(self.request.json_body)
                item_json = self.request.json_body
                units = int(item_json['units'])
                description = item_json['description']
                amount = decimal.Decimal(item_json['amount'])

            # Normal POST Request from HTML Form
            except JSONDecodeError:
                units = int(self.request.params['units'])
                description = self.request.params['description']
                amount = decimal.Decimal(self.request.params['amount'])

            item = InvoiceItem(units=units, description=description, amount=amount)
            DBSession.add(item)

            next_url = self.request.route_url('invoice_item')
            return HTTPFound(location=next_url)
        # If not return GET view
        else:
            return {}
