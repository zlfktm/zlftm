# Model -> Table 생성
# 게시글 - board
# 유저 - user
# 모델 이름은 단수로 정하는게 보통

from db import db
class User(db.Model) :
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    boards = db.relationship('Board', back_populates='author', lazy='dynamic')  # 역참조 설정 - 양방향 연결

class Board(db.Model) :
    __tablename__ = "boards"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    author = db.relationship('User', back_populates='boards')   # 역참조 설정 - 양방향 연결

