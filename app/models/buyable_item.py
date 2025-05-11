from app.flask_extensions import csdl

class BuyableItem(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    event_id = csdl.Column(csdl.Integer, csdl.ForeignKey('event.id'), nullable=False)
    item_name = csdl.Column(csdl.String(100), nullable=False)
    price = csdl.Column(csdl.Integer)
    image = csdl.Column(csdl.String(100), nullable=True)
    item_category_id = csdl.Column(csdl.Integer, csdl.ForeignKey('category.id'), nullable=False)
    status = csdl.Column(csdl.Integer, csdl.ForeignKey('buyable_item_status.id'), nullable=False)
    status_obj = csdl.relationship('BuyableItemStatus', backref='items', lazy=True)
