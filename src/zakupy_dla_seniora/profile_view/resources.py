from flask_restful import Resource, reqparse
from zakupy_dla_seniora.board_view.functions import get_min_max_coordinates
from zakupy_dla_seniora.sms_handler.models import Messages
from zakupy_dla_seniora.users.models import User
from zakupy_dla_seniora.placings.models import Placings


profile_view_parser = reqparse.RequestParser()
profile_view_parser.add_argument('user_id', required=True)


class ProfileView(Resource):
    def get(self):
        user_id = profile_view_parser.parse_args()['user_id']

        placings = Placings.query.filter(Placings.user_id == user_id).all()

        data = []

        placings = [placing.prepare_board_view() for placing in placings]
        for placing in placings:

            info = Messages.query.filter(Messages.id == placing['message_id']).first().prepare_board_view()
            info['placing_status'] = placing['placing_status']
            del info['id']
            data.append(info)


        return {'success': True, 'data': data}, 200
