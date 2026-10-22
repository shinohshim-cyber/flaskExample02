# 사전 설치 : pip install pymysql DBUtils python-dotenv
from flask import Flask
from config import Config
from backend.models.db import close_db
from backend.routes.main_routes import main_bp

def create_app():
    """애플리케이션 팩토리 함수"""
    # 팩토리 내에서 Flask 앱 초기화
    # app.py가 루트 폴더에 있으므로 템플릿과 정적 파일 경로가 기본값으로 적용됨
    app = Flask(__name__)
    
    # 설정 로드 (config.py 및 .env 활용)
    app.config.from_object(Config)
    
    # HTTP 요청 종료 시 DB 커넥션을 풀(Pool)로 자동 반납하는 훅 등록
    app.teardown_appcontext(close_db)
    
    # Blueprint 등록
    app.register_blueprint(main_bp)
    
    return app

# 애플리케이션 생성
app = create_app()

if __name__ == '__main__':
    # .env 설정을 바탕으로 실행 (DEBUG 모드 반영)
    app.run(host='0.0.0.0', port=5000, debug=app.config.get('DEBUG', False))