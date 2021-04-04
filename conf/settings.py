import os

# 自动获取绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
DATABASE_DIR = os.path.join(BASE_DIR, 'db')
DATA_ANALYZE_DIR = os.path.join(BASE_DIR, 'data_analyze')
IMAGE_DIR = os.path.join(STATIC_DIR, 'images')
FONT_DIR = os.path.join(STATIC_DIR, 'fonts')
