from datetime import datetime
from app.extensions import db


class DetectionRecord(db.Model):
    """用户害虫识别记录表"""
    __tablename__ = 'detection_records'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    pest_id = db.Column(db.Integer, db.ForeignKey('pest.id'), nullable=True, index=True)  # 可能识别不到
    image_url = db.Column(db.String(255), nullable=False)
    detection_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    confidence = db.Column(db.Float, nullable=True)  # 识别置信度
    bbox = db.Column(db.JSON, nullable=True)  # 边界框坐标 [x1, y1, x2, y2]
    status = db.Column(db.Integer, default=1, comment='0-无效 1-有效')  # 用户标记是否有效

    # 关系定义
    user = db.relationship('User', backref='detection_records')
    pest = db.relationship('Pest', backref='detection_records')

    __table_args__ = (
        db.Index('idx_detection_user_pest', user_id, pest_id),
        db.Index('idx_detection_time', detection_time),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pest_id': self.pest_id,
            'pest_name': self.pest.name if self.pest else None,
            'image_url': self.image_url,
            'detection_time': self.detection_time.isoformat(),
            'confidence': self.confidence,
            'bbox': self.bbox,
            'status': self.status
        }