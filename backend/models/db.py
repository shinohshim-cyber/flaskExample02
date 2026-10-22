import pymysql
from pymysql import Error
from dbutils.pooled_db import PooledDB
from flask import g
from config import Config

# 1. 서버 구동 시 전체 애플리케이션에서 공유할 커넥션 풀 생성 (Thread-Safe)
pool = PooledDB(
    creator=pymysql,
    mincached=Config.DB_POOL_MIN_CACHED,
    maxconnections=Config.DB_POOL_MAX_CONNECTIONS,
    blocking=True,  # 풀에 커넥션이 부족할 경우 대기
    host=Config.DB_HOST,
    database=Config.DB_NAME,
    user=Config.DB_USER,
    password=Config.DB_PASSWORD,
    port=Config.DB_PORT,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

def get_db():
    """현재 HTTP 요청(스레드) 전용 DB 커넥션을 Flask g 컨텍스트에서 가져오거나 풀에서 대여"""
    if 'db_conn' not in g:
        g.db_conn = pool.connection()
    return g.db_conn

def close_db(e=None):
    """HTTP 요청 처리가 완료되면 g에 할당된 커넥션을 커넥션 풀로 자동 반납"""
    conn = g.pop('db_conn', None)
    if conn is not None:
        conn.close()  # 커넥션을 끊는 것이 아니라 풀(Pool)로 반납됨

class Database:
    """데이터베이스 연동 클래스 (방식 B: Flask g 컨텍스트 & 커넥션 풀 적용 버전)"""

    @staticmethod
    def save_bmi_record(weight, height, bmi, category):
        """BMI 기록을 데이터베이스에 저장"""
        try:
            conn = get_db()
            if conn is None:
                print("데이터베이스 연결이 없습니다.")
                return False
                
            with conn.cursor() as cursor:
                query = """
                INSERT INTO bmi_records (weight, height, bmi, category)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (weight, height, bmi, category))
            
            conn.commit()
            print("BMI 기록이 성공적으로 저장되었습니다.")
            return True
        except Error as e:
            print(f"데이터 저장 중 오류 발생: {e}")
            conn = g.get('db_conn')
            if conn:
                conn.rollback()  # 오류 발생 시 트랜잭션 롤백
            return False

    @staticmethod
    def get_bmi_records(limit=10):
        """최근 BMI 기록을 가져옵니다"""
        try:
            conn = get_db()
            if conn is None:
                print("데이터베이스 연결이 없습니다.")
                return []
                
            with conn.cursor() as cursor:
                query = """
                SELECT * FROM bmi_records
                ORDER BY created_at DESC
                LIMIT %s
                """
                cursor.execute(query, (limit,))
                records = cursor.fetchall()
            
            return records
        except Error as e:
            print(f"데이터 조회 중 오류 발생: {e}")
            return []