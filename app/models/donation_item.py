from app.flask_extensions import csdl

class DonationItem(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    donation_id = csdl.Column(csdl.Integer, csdl.ForeignKey('donation.id'), nullable=False)
    item_category_id = csdl.Column(csdl.Integer, csdl.ForeignKey('item_category.id'), nullable=False)
    item_name = csdl.Column(csdl.String(100), nullable=False)
    quantity = csdl.Column(csdl.Integer)
    
    item_category = csdl.relationship('ItemCategory', backref='donation_items', lazy=True)