from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Use your desired database URL
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_list = [{'id': item.id, 'name': item.name} for item in items]
    return jsonify(items_list)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify({'id': item.id, 'name': item.name})

@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = Item(name=data['name'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'id': new_item.id, 'name': new_item.name}), 201

@app.route('/add_item_form', methods=['GET', 'POST'])
def add_item_form():
    if request.method == 'POST':
        name = request.form.get('name')
        new_item = Item(name=name)
        db.session.add(new_item)
        db.session.commit()
        return render_template('added_successfully.html', name=name)
    return render_template('add_item_form.html')

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    data = request.get_json()
    item.name = data['name']
    db.session.commit()
    return jsonify({'id': item.id, 'name': item.name})

@app.route('/delete_item_form', methods=['GET'])
def delete_item_form():
    items = Item.query.all()
    return render_template('delete_item_form.html', items=items)

@app.route('/delete_item', methods=['POST'])
def delete_item():
    item_id = request.form.get('item_id')
    item = Item.query.get(item_id)

    if item:
        db.session.delete(item)
        db.session.commit()
        return render_template('deleted_successfully.html', item_name=item.name)
    else:
        return render_template('item_not_found.html')



if __name__ == '__main__':
    app.run(debug=True)
