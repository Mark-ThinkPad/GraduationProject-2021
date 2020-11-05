import os

# 自动获取绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
DATABASE_DIR = os.path.join(BASE_DIR, 'db')
UPLOAD_DIR = os.path.join(STATIC_DIR, 'upload')
UPLOAD_IMAGE_DIR = os.path.join(UPLOAD_DIR, 'images')