from app.extensions import db
from datetime import datetime


class Pest(db.Model):
    __tablename__ = 'pest'

    id = db.Column(db.Integer, primary_key=True)
    # 基本信息
    name = db.Column(db.String(100), nullable=False, comment='害虫名称')
    alias = db.Column(db.String(255), nullable=True, comment='别名')
    taxonomy = db.Column(db.String(255), nullable=True, comment='分类地位')

    # 形态特征
    adult_features = db.Column(db.Text, nullable=True, comment='成虫特征')
    larval_features = db.Column(db.Text, nullable=True, comment='幼虫特征')
    egg_features = db.Column(db.Text, nullable=True, comment='卵特征')
    pupa_features = db.Column(db.Text, nullable=True, comment='蛹特征')

    # 生态习性
    host_range = db.Column(db.Text, nullable=True, comment='寄主范围')
    habitat = db.Column(db.Text, nullable=True, comment='栖息环境')
    activity_pattern = db.Column(db.Text, nullable=True, comment='活动规律')
    overwintering = db.Column(db.Text, nullable=True, comment='越冬方式')

    # 危害特征
    damage_period = db.Column(db.Text, nullable=True, comment='危害时期')
    damage_method = db.Column(db.Text, nullable=True, comment='危害方式')
    damage_symptoms = db.Column(db.Text, nullable=True, comment='危害症状')

    # 防控管理
    monitoring_methods = db.Column(db.Text, nullable=True, comment='监测方法')
    agricultural_control = db.Column(db.Text, nullable=True, comment='农业防治')
    physical_control = db.Column(db.Text, nullable=True, comment='物理防治')
    biological_control = db.Column(db.Text, nullable=True, comment='生物防治')
    chemical_control = db.Column(db.Text, nullable=True, comment='化学防治')
    quarantine_requirements = db.Column(db.Text, nullable=True, comment='检疫要求')

    # 发生分布
    geographical_distribution = db.Column(db.Text, nullable=True, comment='地理分布')
    generations_per_year = db.Column(db.String(50), nullable=True, comment='发生世代')
    reproductive_characteristics = db.Column(db.Text, nullable=True, comment='繁殖特性')

    # 时间戳
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    cate = db.Column(db.String(50), comment='分类')
    image = db.Column(db.Text, comment='图片URL')

    __table_args__ = (
        db.Index('idx_pest_name', name),
        db.Index('idx_pest_create_at', create_at),
        db.Index('idx_pest_update_at', update_at),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'alias': self.alias,
            'taxonomy': self.taxonomy,
            'adult_features': self.adult_features,
            'larval_features': self.larval_features,
            'egg_features': self.egg_features,
            'pupa_features': self.pupa_features,
            'host_range': self.host_range,
            'habitat': self.habitat,
            'activity_pattern': self.activity_pattern,
            'overwintering': self.overwintering,
            'damage_period': self.damage_period,
            'damage_method': self.damage_method,
            'damage_symptoms': self.damage_symptoms,
            'monitoring_methods': self.monitoring_methods,
            'agricultural_control': self.agricultural_control,
            'physical_control': self.physical_control,
            'biological_control': self.biological_control,
            'chemical_control': self.chemical_control,
            'quarantine_requirements': self.quarantine_requirements,
            'geographical_distribution': self.geographical_distribution,
            'generations_per_year': self.generations_per_year,
            'reproductive_characteristics': self.reproductive_characteristics,
            'create_at': self.create_at,
            'update_at': self.update_at,
            'image': self.image,
        }