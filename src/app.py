# Author: Boden Kahn
# Date created: 11/20/23
# Description: This file defines the API for our game database project. It only allows for reading of data because we don't want people to be able to add, update, or delete records. For the documentation view apiDocumentation.html

from flask import Flask,  jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('CMSC508_USER')}:{os.getenv('CMSC508_PASSWORD')}@{os.getenv('CMSC508_HOST')}/{os.getenv('DB_NAME')}"
db = SQLAlchemy(app)

# API key
API_KEY = '123456789'
def require_api_key(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != API_KEY:
            abort(401)
        return func(*args, **kwargs)
    return decorated_function

class Game(db.Model):
    #__tablename__ = '23FA_groups_group50/game'
    __tablename__ = 'Game'
    __table_args__ = {'schema': '23FA_groups_group50'}
    Game_ID = db.Column(db.Integer, primary_key=True)
    Game_name = db.Column(db.String(255), nullable=False)
    Game_age_rating = db.Column(db.String(10))
    Game_release_date = db.Column(db.Date)
    Game_DLC = db.Column(db.String(255))

    def serialize(self):
        # Define how to serialize the Game model to JSON
        return {
            'Game_ID': self.Game_ID,
            'Game_name': self.Game_name,
            'Game_age_rating': self.Game_age_rating,
            'Game_release_date': self.Game_release_date,
            'Game_DLC': self.Game_DLC
        }

class Tag(db.Model):
    __tablename__ = 'Tag'
    __table_args__ = {'schema': '23FA_groups_group50'}
    Tag_ID = db.Column(db.Integer, primary_key=True)
    Tag_name = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'Tag_ID': self.Tag_ID,
            'Tag_name': self.Tag_name
        }

class Review(db.Model):
    __tablename__ = 'Review'
    __table_args__ = {'schema': '23FA_groups_group50'}
    
    Review_ID = db.Column(db.Integer, primary_key=True)
    Review_title = db.Column(db.String(255), nullable=False)
    Review_ReviewerName = db.Column(db.String(255), nullable=False)
    Review_Comment = db.Column(db.String(255))

    def serialize(self):
        return {
            'Review_ID': self.Review_ID,
            'Review_title': self.Review_title,
            'Review_ReviewerName': self.Review_ReviewerName,
            'Review_Comment': self.Review_Comment,
        }

class Developer(db.Model):
    __tablename__ = 'Developer'
    __table_args__ = {'schema': '23FA_groups_group50'}
    Developer_ID = db.Column(db.Integer, primary_key=True)
    Developer_name = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'Developer_ID': self.Developer_ID,
            'Developer_name': self.Developer_name
        }

class Publisher(db.Model):
    __tablename__ = 'Publisher'
    __table_args__ = {'schema': '23FA_groups_group50'}
    Publisher_ID = db.Column(db.Integer, primary_key=True)
    Publisher_name = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'Publisher_ID': self.Publisher_ID,
            'Publisher_name': self.Publisher_name
        }

class Engine(db.Model):
    __tablename__ = 'Engine'
    __table_args__ = {'schema': '23FA_groups_group50'}
    Engine_ID = db.Column(db.Integer, primary_key=True)
    Engine_Name = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'Engine_ID': self.Engine_ID,
            'Engine_Name': self.Engine_Name
        }

class Devices(db.Model):
    __tablename__ = 'Devices'
    __table_args__ = {'schema': '23FA_groups_group50'}
    Devices_ID = db.Column(db.Integer, primary_key=True)
    Devices_Name = db.Column(db.String(255), nullable=False)

    def serialize(self):
        return {
            'Devices_ID': self.Devices_ID,
            'Devices_Name': self.Devices_Name
        }
    
class Final(db.Model):
    __tablename__ = 'Final'
    __table_args__ = {'schema': '23FA_groups_group50'}
    Final_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Game_ID = db.Column(db.Integer, db.ForeignKey('23FA_groups_group50.Game.Game_ID'), nullable=False)
    Final_GameName = db.Column(db.String(255))
    Tag_ID = db.Column(db.Integer, db.ForeignKey('23FA_groups_group50.Tag.Tag_ID'),nullable=False)
    Devices_ID = db.Column(db.Integer, db.ForeignKey('23FA_groups_group50.Devices.Devices_ID'),nullable=False)
    Engine_ID = db.Column(db.Integer, db.ForeignKey('23FA_groups_group50.Engine.Engine_ID'),nullable=False)
    Review_ID = db.Column(db.Integer, db.ForeignKey('23FA_groups_group50.Review.Review_ID'),nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
        
### Game
# Get all or filter by name
@app.route('/api/games', methods=['GET'])
def get_games():
    game_name = request.args.get('name')
    print("Request Parameters:", request.args)
    if game_name:
        # Filter games by name (case-sensitive) (optional)
        games = Game.query.filter(Game.Game_name == game_name).all()
    else:
        # Get all games
        games = Game.query.all()
    return jsonify([game.serialize() for game in games])

# Insert
@app.route('/api/games', methods=['POST'])
@require_api_key
def create_game():
    data = request.get_json()
    new_game = Game(**data)
    db.session.add(new_game)
    db.session.commit()
    return jsonify({'message': 'Game created successfully'}), 201

# Update
@app.route('/api/games/<int:game_id>', methods=['PUT'])
@require_api_key
def update_game(game_id):
    game = Game.query.get_or_404(game_id)
    data = request.get_json()
    game.Game_name = data.get('Game_name', game.Game_name)
    game.Game_age_rating = data.get('Game_age_rating', game.Game_age_rating)
    game.Game_release_date = data.get('Game_release_date', game.Game_release_date)
    game.Game_DLC = data.get('Game_DLC', game.Game_DLC)
    db.session.commit()
    return jsonify({'message': 'Game updated successfully'})

# Delete
@app.route('/api/games/<int:game_id>', methods=['DELETE'])
@require_api_key
def delete_game(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return jsonify({'message': 'Game deleted successfully'})

# Get Game by ID
@app.route('/api/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get_or_404(game_id)
    return jsonify(game.serialize())

### Tag
# Get all tags or filter by name
@app.route('/api/tags', methods=['GET'])
def get_tags():
    tag_name = request.args.get('name')
    if tag_name:
        # Filter tags by name
        tags = Tag.query.filter(Tag.Tag_name.ilike(f"%{tag_name}%")).all()
    else:
        # Get all tags
        tags = Tag.query.all()

    return jsonify([tag.serialize() for tag in tags])

# Get tag by ID
@app.route('/api/tags/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return jsonify(tag.serialize())

# Insert
@app.route('/api/tags', methods=['POST'])
@require_api_key
def create_tag():
    data = request.get_json()
    new_tag = Tag(**data)
    db.session.add(new_tag)
    db.session.commit()
    return jsonify({'message': 'Tag created successfully'}), 201

# Update
@app.route('/api/tags/<int:tag_id>', methods=['PUT'])
@require_api_key
def update_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    data = request.get_json()
    tag.Tag_name = data.get('Tag_name', tag.Tag_name)
    db.session.commit()
    return jsonify({'message': 'Tag updated successfully'})

# Delete
@app.route('/api/tags/<int:tag_id>', methods=['DELETE'])
@require_api_key
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'message': 'Tag deleted successfully'})

### Review
# Get all reviews or filter by title, reviewer name, or comment
@app.route('/api/reviews', methods=['GET'])
def get_reviews():
    review_title = request.args.get('title')
    reviewer_name = request.args.get('reviewer_name')
    review_comment = request.args.get('comment')
    # Filter reviews based on parameters
    query = Review.query
    if review_title:
        query = query.filter(Review.Review_title.ilike(f"%{review_title}%"))
    if reviewer_name:
        query = query.filter(Review.Review_ReviewerName.ilike(f"%{reviewer_name}%"))
    if review_comment:
        query = query.filter(Review.Review_Comment.ilike(f"%{review_comment}%"))
    reviews = query.all()
    return jsonify([review.serialize() for review in reviews])

# Get review by ID
@app.route('/api/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get_or_404(review_id)
    return jsonify(review.serialize())

# Insert
@app.route('/api/reviews', methods=['POST'])
@require_api_key
@require_api_key
def create_review():
    data = request.get_json()
    new_review = Review(**data)
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'message': 'Review created successfully'}), 201

# Update 
@app.route('/api/reviews/<int:review_id>', methods=['PUT'])
@require_api_key
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    data = request.get_json()
    review.Review_title = data.get('Review_title', review.Review_title)
    review.Review_ReviewerName = data.get('Review_ReviewerName', review.Review_ReviewerName)
    review.Review_Comment = data.get('Review_Comment', review.Review_Comment)
    review.Review_game = data.get('Review_game', review.Review_game)

    db.session.commit()

    return jsonify({'message': 'Review updated successfully'})

# Delete
@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
@require_api_key
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review deleted successfully'})

### Developer
# Get all developers or filter by name
@app.route('/api/developers', methods=['GET'])
def get_developers():
    developer_name = request.args.get('name')
    if developer_name:
        # Filter developers by name
        developers = Developer.query.filter(Developer.Developer_name.ilike(f"%{developer_name}%")).all()
    else:
        # Get all developers
        developers = Developer.query.all()
    return jsonify([developer.serialize() for developer in developers])

# Get Developer by ID
@app.route('/api/developers/<int:developer_id>', methods=['GET'])
def get_developer(developer_id):
    developer = Developer.query.get_or_404(developer_id)
    return jsonify(developer.serialize())

# Insert
@app.route('/api/developers', methods=['POST'])
@require_api_key
def create_developer():
    data = request.get_json()
    new_developer = Developer(**data)
    db.session.add(new_developer)
    db.session.commit()

    return jsonify({'message': 'Developer created successfully'}), 201

# Update
@app.route('/api/developers/<int:developer_id>', methods=['PUT'])
@require_api_key
def update_developer(developer_id):
    developer = Developer.query.get_or_404(developer_id)
    data = request.get_json()
    developer.Developer_name = data.get('Developer_name', developer.Developer_name)
    db.session.commit()
    return jsonify({'message': 'Developer updated successfully'})

# Delete
@app.route('/api/developers/<int:developer_id>', methods=['DELETE'])
@require_api_key
def delete_developer(developer_id):
    developer = Developer.query.get_or_404(developer_id)
    db.session.delete(developer)
    db.session.commit()
    return jsonify({'message': 'Developer deleted successfully'})

### Publisher
# Get all publishers or filter by name
@app.route('/api/publishers', methods=['GET'])
def get_publishers():
    publisher_name = request.args.get('name')
    if publisher_name:
        # Filter publishers by name
        publishers = Publisher.query.filter(Publisher.Publisher_name.ilike(f"%{publisher_name}%")).all()
    else:
        # Get all publishers
        publishers = Publisher.query.all()
    return jsonify([publisher.serialize() for publisher in publishers])

# Get Publisher by ID
@app.route('/api/publishers/<int:publisher_id>', methods=['GET'])
def get_publisher(publisher_id):
    publisher = Publisher.query.get_or_404(publisher_id)
    return jsonify(publisher.serialize())

# Insert
@app.route('/api/publishers', methods=['POST'])
@require_api_key
def create_publisher():
    data = request.get_json()
    new_publisher = Publisher(**data)
    db.session.add(new_publisher)
    db.session.commit()
    return jsonify({'message': 'Publisher created successfully'}), 201

# Update
@app.route('/api/publishers/<int:publisher_id>', methods=['PUT'])
@require_api_key
def update_publisher(publisher_id):
    publisher = Publisher.query.get_or_404(publisher_id)
    data = request.get_json()
    publisher.Publisher_name = data.get('Publisher_name', publisher.Publisher_name)
    db.session.commit()
    return jsonify({'message': 'Publisher updated successfully'})

# Delete
@app.route('/api/publishers/<int:publisher_id>', methods=['DELETE'])
@require_api_key
def delete_publisher(publisher_id):
    publisher = Publisher.query.get_or_404(publisher_id)
    db.session.delete(publisher)
    db.session.commit()
    return jsonify({'message': 'Publisher deleted successfully'})

### Engine
# Get all engines or filter engines by name
@app.route('/api/engines', methods=['GET'])
def get_engines():
    engine_name = request.args.get('name')
    if engine_name:
        # Filter engines by name
        engines = Engine.query.filter(Engine.Engine_Name.ilike(f"%{engine_name}%")).all()
    else:
        # Get all engines
        engines = Engine.query.all()
    return jsonify([engine.serialize() for engine in engines])

# Get Engine by ID
@app.route('/api/engines/<int:engine_id>', methods=['GET'])
def get_engine(engine_id):
    engine = Engine.query.get_or_404(engine_id)
    return jsonify(engine.serialize())

# Insert
@app.route('/api/engines', methods=['POST'])
@require_api_key
def create_engine():
    data = request.get_json()
    new_engine = Engine(**data)
    db.session.add(new_engine)
    db.session.commit()
    return jsonify({'message': 'Engine created successfully'}), 201

# Update
@app.route('/api/engines/<int:engine_id>', methods=['PUT'])
@require_api_key
def update_engine(engine_id):
    engine = Engine.query.get_or_404(engine_id)
    data = request.get_json()
    engine.Engine_Name = data.get('Engine_Name', engine.Engine_Name)
    db.session.commit()
    return jsonify({'message': 'Engine updated successfully'})

# Delete
@app.route('/api/engines/<int:engine_id>', methods=['DELETE'])
@require_api_key
def delete_engine(engine_id):
    engine = Engine.query.get_or_404(engine_id)
    
    db.session.delete(engine)
    db.session.commit()

    return jsonify({'message': 'Engine deleted successfully'})

### Devices
# Get all devices or filter devices by name
@app.route('/api/devices', methods=['GET'])
def get_devices():
    device_name = request.args.get('name')
    if device_name:
        # Filter devices by name
        devices = Devices.query.filter(Devices.Devices_Name.ilike(f"%{device_name}%")).all()
    else:
        # Get all devices
        devices = Devices.query.all()
    return jsonify([device.serialize() for device in devices])

# Get Device by ID
@app.route('/api/devices/<int:device_id>', methods=['GET'])
def get_device(device_id):
    device = Devices.query.get_or_404(device_id)
    return jsonify(device.serialize())

# Insert
@app.route('/api/devices', methods=['POST'])
@require_api_key
def create_device():
    data = request.get_json()
    new_device = Devices(**data)
    db.session.add(new_device)
    db.session.commit()
    return jsonify({'message': 'Device created successfully'}), 201

# Update
@app.route('/api/devices/<int:device_id>', methods=['PUT'])
@require_api_key
def update_device(device_id):
    device = Devices.query.get_or_404(device_id)
    data = request.get_json()
    device.Devices_Name = data.get('Devices_Name', device.Devices_Name)
    db.session.commit()
    return jsonify({'message': 'Device updated successfully'})

# Delete
@app.route('/api/devices/<int:device_id>', methods=['DELETE'])
@require_api_key
def delete_device(device_id):
    device = Devices.query.get_or_404(device_id)
    db.session.delete(device)
    db.session.commit()
    return jsonify({'message': 'Device deleted successfully'})

### Final
# Get all final records or filter final records by Game_ID, Tag_ID, Devices_ID, Engine_ID, or Review_ID
@app.route('/api/final', methods=['GET'])
def get_all_final():
    game_id = request.args.get('game_id')
    tag_id = request.args.get('tag_id')
    devices_id = request.args.get('devices_id')
    engine_id = request.args.get('engine_id')
    review_id = request.args.get('review_id')
    # Filter final records based on parameters
    query = Final.query
    if game_id:
        query = query.filter(Final.Game_ID == game_id)
    if tag_id:
        query = query.filter(Final.Tag_ID == tag_id)
    if devices_id:
        query = query.filter(Final.Devices_ID == devices_id)
    if engine_id:
        query = query.filter(Final.Engine_ID == engine_id)
    if review_id:
        query = query.filter(Final.Review_ID == review_id)
    final_records = query.all()
    return jsonify([record.as_dict() for record in final_records])

# Get Final record by ID
@app.route('/api/final/<int:final_id>', methods=['GET'])
def get_final(final_id):
    final_record = Final.query.get(final_id)
    if final_record:
        return jsonify(final_record.as_dict())
    else:
        return jsonify({'message': 'Final record not found'}), 404

# Insert
@app.route('/api/final', methods=['POST'])
@require_api_key
def create_final():
    data = request.get_json()
    new_final = Final(**data)
    db.session.add(new_final)
    db.session.commit()
    return jsonify({'message': 'Final record created successfully'}), 201

# Update
@app.route('/api/final/<int:final_id>', methods=['PUT'])
@require_api_key
def update_final(final_id):
    final_record = Final.query.get_or_404(final_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(final_record, key, value)
    db.session.commit()
    return jsonify({'message': 'Final record updated successfully'})

# Delete
@app.route('/api/final/<int:final_id>', methods=['DELETE'])
@require_api_key
def delete_final(final_id):
    final_record = Final.query.get_or_404(final_id)
    db.session.delete(final_record)
    db.session.commit()
    return jsonify({'message': 'Final record deleted successfully'})

### Get IDs Associated with a Specific Game
@app.route('/api/game_ids/<int:game_id>', methods=['GET'])
def get_game_ids(game_id):
    # Query the Final table to get all the records for the specified game
    final_records = Final.query.filter_by(Game_ID=game_id).all()

    if final_records:
        # Extract the IDs from the final records and convert to sets to remove duplicates
        ids_associated_with_game = {
            'Final_IDs': list(set(record.Final_ID for record in final_records)),
            'Tag_IDs': list(set(record.Tag_ID for record in final_records)),
            'Devices_IDs': list(set(record.Devices_ID for record in final_records)),
            'Engine_IDs': list(set(record.Engine_ID for record in final_records)),
            'Review_IDs': list(set(record.Review_ID for record in final_records)),
        }

        return jsonify(ids_associated_with_game)
    else:
        return jsonify({'message': 'No records found for the specified game ID'}), 404
    
if __name__ == '__main__':
    app.run(debug=True) 