from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from datetime import datetime

from app.models.pest import Pest
from app.service.detection import DetectionService
from app.utils.detect import detect  # 导入您的检测函数

# 配置
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# 创建蓝图
detect_bp = Blueprint('detect', __name__, url_prefix='/api/detect')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@detect_bp.route('/image', methods=['POST'])
def detect_image():
    """
    图片检测接口
    接收: multipart/form-data 文件上传
    返回: JSON格式的检测结果
    """
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
            user_id=1)

        # 创建识别记录
        records = DetectionService.create_detection_record(1, {
                'results': results,
                'image_url': f"/detect/{filename}"  # 返回可访问的图片URL
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
        }), 500