from flask_restful import Resource, reqparse
from zakupy_dla_seniora.users.models import User

leaderboards_parser = reqparse.RequestParser()
leaderboards_parser.add_argument('count', default=10, required=False, type=int)

class Leaderboards(Resource):
    def get(self):
        data = leaderboards_parser.parse_args()
        count = data['count']
        users =  User.query.order_by(User.points.desc()).get(count)
        return {'success': True, 'users': users, 'count': count}, 200