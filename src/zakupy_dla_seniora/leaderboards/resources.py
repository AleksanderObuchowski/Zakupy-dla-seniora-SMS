from flask_restful import Resource, reqparse
from zakupy_dla_seniora.users.models import User

leaderboards_parser = reqparse.RequestParser()
leaderboards_parser.add_argument('count', help='Number of cases.', required=False, type=int)


class Leaderboards(Resource):
    def get(self):
        count = leaderboards_parser.parse_args()['count']
        users = User.query.order_by(User.points.desc()).limit(count)
        if users:
            users = [user.as_json() for user in users]
        else:
            users = None
        return {'success': True, 'users': users, 'count': count}, 200
