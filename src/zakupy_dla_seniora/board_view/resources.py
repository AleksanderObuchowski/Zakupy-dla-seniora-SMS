from flask_restful import Resource, reqparse
from zakupy_dla_seniora.sms_handler.models import Messages
from zakupy_dla_seniora.board_view.functions import get_min_max_coordinates

board_view_parser = reqparse.RequestParser()
board_view_parser.add_argument('latitude', required=False, type=float)
board_view_parser.add_argument('longitude', required=False, type=float)
board_view_parser.add_argument('radius', required=False, type=float)


class BoardView(Resource):
    def get(self):
        data = board_view_parser.parse_args()
        if data['latitude'] is not None and data['longitude'] is not None and data['radius'] is not None:
            latitude = data['latitude']
            longitude = data['longitude']
            radius = data['radius']

            min_latitude, max_latitude = get_min_max_coordinates(radius, latitude)
            min_longitude, max_longitude = get_min_max_coordinates(radius, longitude)

            messages = Messages.query.filter(
                Messages.message_location_lat > min_latitude,
                Messages.message_location_lat < max_latitude,
                Messages.message_location_lon > min_longitude,
                Messages.message_location_lon < max_longitude,
                Messages.message_status == 'Received'
            ).all()
        else:
            messages = Messages.query.filter(Messages.message_status == 'Received').all()
        messages = [message.prepare_board_view() for message in messages]

        return {'success': True, 'data': messages}, 200
