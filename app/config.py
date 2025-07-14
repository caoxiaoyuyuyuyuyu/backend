from pathlib import Path
from dotenv import load_dotenv
import os

# 确保从项目根目录加载.env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)  # 显式加载

class Config:
    """
    配置类，用于加载环境变量并设置默认值。
    """
    # 数据库配置
    DB_CONNECTION = os.getenv("DB_CONNECTION", "mysql")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_DATABASE = os.getenv("DB_DATABASE", "pest")
    DB_USERNAME = os.getenv("DB_USERNAME", "root")
    # DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    from urllib.parse import quote_plus

    # 修改配置类中的连接字符串
    password = os.getenv("DB_PASSWORD", "")
    encoded_password = quote_plus(password)  # 编码特殊字符

    SQLALCHEMY_DATABASE_URI = f"{DB_CONNECTION}://{DB_USERNAME}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    # SQLALCHEMY_DATABASE_URI = f"{DB_CONNECTION}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 300,
        'pool_pre_ping': True
    }

    # LLM Configuration
    LLM_MODEL = "qwen-plus"
    LLM_API_KEY = "sk-1d8575bdb4ab4b64abde2da910ef578b"
    LLM_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    LLM_SYSTEM_PROMPT = """你是一名专业的农业病虫害防治智能专家，具备深厚的植物保护学知识和田间实践经验。请严格按照以下要求回答：\n
                        1. 身份定位：\n
                        - 角色：省级农科院植保所研究员\n
                        - 风格：专业严谨但通俗易懂\n
                        - 语言：中文（必要时标注拉丁学名）\n
                        \n
                        2. 回答规范：\n
                        √ 必须包含：病虫害识别特征、发生规律、防治措施（农业/生物/化学）\n
                        √ 作物生育期标注（如：水稻分蘖期）\n
                        √ 地区适应性说明（如：适用于长江流域）\n
                        × 禁止：模糊表述、未经证实的偏方\n
                        \n
                        3. 知识边界：\n
                        - 仅回答与农作物病虫害相关的问题\n
                        - 不确定时回答："该病虫害需要进一步实验室诊断，建议联系当地农技站"\n
                        \n
                        4. 输出格式：\n
                        【病虫害名称】中英文+拉丁学名\n
                        【典型症状】分点描述（叶片/茎秆/果实等部位）\n
                        【防治方案】按优先级排序：\n
                          ① 农业防治（轮作/抗病品种等）\n
                          ② 生物防治（天敌/生物农药）\n
                          ③ 化学防治（推荐3种药剂+安全间隔期）\n
                        【预防建议】下季种植注意事项\n
                        """

    # Redis Configuration
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0

    # 嵌入模型配置
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-v3")
    EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "sk-1d8575bdb4ab4b64abde2da910ef578b")

    # 获取项目根目录 (Flask应用的上层目录)
    PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # 上传目录路径
    UPLOADS_DIR = os.path.join(PROJECT_ROOT, 'uploads')
    STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')
    DETECT_DIR = os.path.join(PROJECT_ROOT, 'detect')

    WX_APPID = 'wxaefe7c5d5c36c81c'
    WX_SECRET = '8c5e8f62131f2b877b2e1323bdee5e60'
    JWT_SECRET = 'wxaefe7c5d5c36c81c8c5e8f62131f2b877b2e1323bdee5e60'

    MODEL_PATH = r"D:\Projects\PythonProject\runs\detect\insect_detection_optimized\weights\best.pt"