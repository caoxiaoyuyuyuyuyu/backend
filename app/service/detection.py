from datetime import datetime
from app.extensions import db
from app.models.detection import DetectionRecord
from app.models.pest import Pest


class DetectionService:

    @staticmethod
    def create_detection_record(user_id, detection_data):
        """
        创建识别记录
        :param user_id: 用户ID
        :param detection_data: 识别结果数据，格式如：
            {
                "image_url": "/detect/20250714122920_1093.jpg",
                "results": [
                    {
                        "bbox": [x1,y1,x2,y2],
                        "class_id": 16,
                        "class_name": "ewze_larva",
                        "confidence": 0.728
                    }
                ]
            }
        :return: DetectionRecord对象
        """
        records = []
        for result in detection_data['results']:
            # 通过class_name查找害虫
            pest = None
            if result:
                if result.get('class_name'):
<<<<<<< HEAD
                    pest = Pest.query.filter_by(cate=result['class_name']).first()
=======
                    pest = Pest.query.filter_by(name=result['class_name']).first()
>>>>>>> af8b0bfa03b4c11c54596924412a05a4a96b6931

            record = DetectionRecord(
                user_id=user_id,
                pest_id=pest.id if pest else None,
                image_url=detection_data['image_url'],
                confidence=result['confidence'] if result else None,
                bbox=result['bbox'] if result else None,
                detection_time=datetime.utcnow()
            )
            records.append(record.to_dict())

            db.session.add(record)
        db.session.commit()
        return records

    @staticmethod
    def get_user_records(user_id, limit=10, offset=0):
        """
        获取用户的识别记录
        :param user_id: 用户ID
        :param limit: 每页数量
        :param offset: 偏移量
        :return: 记录列表
        """
<<<<<<< HEAD
        records = DetectionRecord.query.filter_by(user_id=user_id) \
            .order_by(DetectionRecord.detection_time.desc()) \
            .offset(offset).limit(limit).all()
        return [record.to_dict() for record in records]
=======
        return DetectionRecord.query.filter_by(user_id=user_id) \
            .order_by(DetectionRecord.detection_time.desc()) \
            .offset(offset).limit(limit).all()
>>>>>>> af8b0bfa03b4c11c54596924412a05a4a96b6931

    @staticmethod
    def update_record_status(record_id, status, user_id=None):
        """
        更新记录状态（用户确认识别结果是否正确）
        :param record_id: 记录ID
        :param status: 新状态 (0/1)
        :param user_id: 可选，验证用户所有权
        :return: 更新后的记录
        """
        query = DetectionRecord.query.filter_by(id=record_id)
        if user_id:
            query = query.filter_by(user_id=user_id)

        record = query.first()
        if record:
            record.status = status
            db.session.commit()
        return record

    @staticmethod
    def get_pest_detection_stats(pest_id):
        """
        获取害虫的识别统计信息
        :param pest_id: 害虫ID
        :return: 统计信息
        """
        from sqlalchemy import func

        stats = db.session.query(
            func.count(DetectionRecord.id).label('total_detections'),
            func.avg(DetectionRecord.confidence).label('avg_confidence'),
            func.max(DetectionRecord.detection_time).label('last_detected')
        ).filter_by(pest_id=pest_id).first()

        return {
            'pest_id': pest_id,
            'total_detections': stats.total_detections or 0,
            'avg_confidence': float(stats.avg_confidence) if stats.avg_confidence else 0,
            'last_detected': stats.last_detected.isoformat() if stats.last_detected else None
        }