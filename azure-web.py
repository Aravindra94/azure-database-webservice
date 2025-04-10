
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Database setup
DATABASE_URL = "mssql+pyodbc://aravin:Admin@123@name-db.database.windows.net/NameDB?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/api', methods=['POST'])
def api():
    data = request.json
    user = User(name=data['name'])
    session.add(user)
    session.commit()
    response = {"message": f"User {data['name']} added to database"}
    return jsonify(response)

@app.route('/api/<name>', methods=['GET'])
def get_user(name):
    user = session.query(User).filter_by(name=name).first()
    if user:
        response = {"message": f"User {user.name} found in database"}
    else:
        response = {"message": "User not found"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
