import flask
from flask import jsonify, make_response, request

from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs/<int:user_id>', methods=['PUT'])
def put_user(job_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'email', 'hashed_password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(job_id)
    db_sess.delete(users)
    newusers = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password'],
    )
    db_sess.add(newusers)
    db_sess.commit()
    return jsonify({'id': users.id})


@blueprint.route('/api/users', methods=['GET'])
def get_user():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'users':
                [item.to_dict()
                 for item in users]
        }
    )


@blueprint.route('/api/jobs/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    print(users, user_id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'users': users.to_dict()
        }
    )


@blueprint.route('/api/jobs/<int:user_id>', methods=['DELETE'])
def delete_one_user(user_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(user_id)
    if not users:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['surname', 'name', 'age', 'position', 'speciality', 'email', 'hashed_password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    users = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password'],
    )
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'id': users.id})
