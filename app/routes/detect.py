<<<<<<< HEAD
from flask import Blueprint, request, jsonify, current_app, send_from_directory
=======
from flask import Blueprint, request, jsonify, current_app
>>>>>>> af8b0bfa03b4c11c54596924412a05a4a96b6931
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from app.models.pest import Pest
from app.service.detection import DetectionService
<<<<<<< HEAD
from app.utils.auth import token_required
=======
>>>>>>> af8b0bfa03b4c11c54596924412a05a4a96b6931
from app.utils.detect import detect  # 导入您的检测函数

# 配置
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# 创建蓝图
detect_bp = Blueprint('detect', __name__, url_prefix='/api/detect')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@detect_bp.route('/image', methods=['POST'])
<<<<<<< HEAD
@token_required
=======
>>>>>>> af8b0bfa03b4c11c54596924412a05a4a96b6931
def detect_image():
    """
    图片检测接口
    接收: multipart/form-data 文件上传
    返回: JSON格式的检测结果
    """
<<<<<<< HEAD
    user_id = request.current_user_id
=======
>>>>>>> af8b0bfa03b4c11c54596924412a05a4a96b6931
    # 1. 检查文件是否存在
    if 'file' not in request.files:
        return jsonify({'code': 400, 'message': '未上传文件'}), 400

    file = request.files['file']

    # 2. 验证文件
    if file.filename == '':
        return jsonify({'code': 400, 'message': '未选择文件'}), 400

    if not allowed_file(file.filename):
        return jsonify({'code': 400, 'message': '不支持的文件类型'}), 400

    # 3. 保存文件
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{secure_filename(file.filename)}"
    filepath = os.path.join(current_app.config['UPLOADS_DIR'], filename)
    file.save(filepath)

    try:
        # 4. 加载模型并检测 (修改为您的实际模型路径)
        model_path = current_app.config['MODEL_PATH']
        results = detect(
            model_path=model_path,
            image_path=filepath,
            output_dir=current_app.config['DETECT_DIR'],
<<<<<<< HEAD
            user_id=user_id)

        # 创建识别记录
        records = DetectionService.create_detection_record(user_id, {
                'results': results,
                'image_url': str(user_id) + '/' +filename  # 返回可访问的图片URL
=======
            user_id=1)

        # 创建识别记录
        records = DetectionService.create_detection_record(1, {
                'results': results,
                'image_url': f"/detect/{filename}"  # 返回可访问的图片URL
>>>>>>> af8b0bfa03b4c11c54596924412a05a4a96b6931
            })

        return jsonify({
            'code': 200,
            'data': records,
        })

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': '检测失败',
            'error': str(e)
<<<<<<< HEAD
        }), 500

# 检测记录
@detect_bp.route('/records', methods=['GET'])
@token_required
def get_detection_records():
    user_id = request.current_user_id
    records = DetectionService.get_user_records(user_id)
    return jsonify({
        'code': 200,
        'data': records,
    })


# 获取图片
@detect_bp.route('/images/<path:image>', methods=['GET'])
def get_image(image):
    # image 参数将包含类似 '1/20250714143538_1093.jpg' 的路径
    return send_from_directory(current_app.config['DETECT_DIR'], image)
=======
        }), 500
>>>>>>> af8b0bfa03b4c11c54596924412a05a4a96b6931
