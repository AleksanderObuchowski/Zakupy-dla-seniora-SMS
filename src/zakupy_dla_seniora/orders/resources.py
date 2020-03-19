from flask_restful import Resource, reqparse
from zakupy_dla_seniora.orders.models import Order


register_parser = reqparse.RequestParser()
register_parser.add_argument('id_user', help='This field cannot be blank', required=True)
register_parser.add_argument('id_message', help='This field cannot be blank', required=True)
register_parser.add_argument('order_status', help='This field cannot be blank', required=True)
register_parser.add_argument('order_date', help='This field cannot be blank', required=True)



class OrderCreation(Resource):
    def post(self):
        data = register_parser.parse_args()
        new_order = Orders(
            id_user=data['id_user'],
            id_message=data['id_message'],
            order_status=data['order_status'],
            order_date=data['order_date'],
        )
        new_order.save()
        return {'success': True, 'message': 'Order has been added.'}, 200
