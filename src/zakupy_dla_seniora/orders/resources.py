from flask_restful import Resource, reqparse
from zakupy_dla_seniora.orders.models import Orders


register_parser = reqparse.RequestParser()
register_parser.add_argument('user_id', help='This field cannot be blank', required=True)
register_parser.add_argument('message_id', help='This field cannot be blank', required=True)


class OrderCreation(Resource):
    def post(self):
        data = register_parser.parse_args()
        new_order = Orders(
            user_id=data['user_id'],
            message_id=data['message_id'],
        )
        new_order.save()

        # call function to

        

        return {'success': True, 'message': 'Order has been added.'}, 200
