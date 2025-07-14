from flask import Blueprint, request, jsonify, send_from_directory, current_app

from app.models.pest import Pest
from app.extensions import db

pest_bp = Blueprint('pest', __name__, url_prefix='/api/pest')


@pest_bp.route('', methods=['GET'])
def get_pests():
    # Get pagination parameters from request (default to page 1, 10 items per page)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Get optional filter parameters
    name_filter = request.args.get('name', None)

    # Build base query
    query = Pest.query

    # Apply filters if provided
    if name_filter:
        query = query.filter(Pest.name.ilike(f'%{name_filter}%'))

    # Execute paginated query
    paginated_pests = query.order_by(Pest.id).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    # Prepare response data
    pests_data = [{
        'id': pest.id,
        'name': pest.name,
        'image': pest.image,
        'host_range': pest.host_range,
    } for pest in paginated_pests.items]

    response = {
        'data': pests_data,
        'pagination': {
            'total': paginated_pests.total,
            'pages': paginated_pests.pages,
            'current_page': paginated_pests.page,
            'per_page': paginated_pests.per_page,
            'has_next': paginated_pests.has_next,
            'has_prev': paginated_pests.has_prev,
        }
    }

    return jsonify(response)

# 获取单个详情
@pest_bp.route('/<int:pest_id>', methods=['GET'])
def get_pest(pest_id):
    pest = Pest.query.get(pest_id)
    if pest:
        return jsonify({
            "data": pest.to_dict()
        })
    return jsonify({'code': 404, 'message': '找不到该害虫'})

# 获取图片
@pest_bp.route('/images/<string:image>', methods=['GET'])
def get_image(image):
    return send_from_directory(current_app.config['STATIC_DIR'], "logo.png")