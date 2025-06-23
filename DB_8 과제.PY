from pymongo import MongoClient

def insert_data():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.local  
    
    books = [
        {"title": "Kafka on the Shore", "author": "Haruki Murakami", "year": 2002},
        {"title": "Norwegian Wood", "author": "Haruki Murakami", "year": 1987},
        {"title": "1Q84", "author": "Haruki Murakami", "year": 2009}
    ]
    db.books.insert_many(books)

    
    movies = [
        {"title": "Inception", "director": "Christopher Nolan", "year": 2010, "rating": 8.8},
        {"title": "Interstellar", "director": "Christopher Nolan", "year": 2014, "rating": 8.6},
        {"title": "The Dark Knight", "director": "Christopher Nolan", "year": 2008, "rating": 9.0}
    ]
    db.movies.insert_many(movies)

    
    user_actions = [
        {"user_id": 1, "action": "click", "timestamp": "2023-04-12T08:00:00Z"},
        {"user_id": 1, "action": "view", "timestamp": "2023-04-12T09:00:00Z"},
        {"user_id": 2, "action": "purchase", "timestamp": "2023-04-12T10:00:00Z"}
    ]
    db.user_actions.insert_many(user_actions)

    print("Data inserted successfully")
    client.close()

if __name__ == "__main__":
    insert_data()

from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client.local

# 문제 1: 특정 장르의 책 찾기
books = db.books.find(
    {"genre": "fantasy"},
    {"title": 1, "author": 1, "_id": 0}
)
for book in books:
    print(book)

# 문제 2: 감독별 평균 영화 평점 계산
directors = db.movies.aggregate([
    {
        "$group": {
            "_id": "$director",
            "avg_rating": {"$avg": "$rating"}
        }
    },
    {
        "$sort": {"avg_rating": -1}
    }
])
for director in directors:
    print(director)

# 문제 3: 특정 사용자의 최근 행동 조회
recent_actions = db.user_actions.find(
    {"user_id": 1}
).sort("timestamp", -1).limit(5)
for action in recent_actions:
    print(action)

# 문제 4: 출판 연도별 책의 수 계산
year_counts = db.books.aggregate([
    {
        "$group": {
            "_id": "$year",
            "count": {"$sum": 1}
        }
    },
    {
        "$sort": {"count": -1}
    }
])
for year in year_counts:
    print(year)

# 문제 5: 특정 사용자의 행동 유형 업데이트
update_result = db.user_actions.update_many(
    {
        "user_id": 1,
        "timestamp": "2023-04-10T01:00:00Z",
        "action": "view"
    },
    {
        "$set": {"action": "seen"}
    }
)
print(f"Matched: {update_result.matched_count}, Modified: {update_result.modified_count}")
