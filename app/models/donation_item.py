from app.flask_extensions import csdl

class DonationItem(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    donation_id = csdl.Column(csdl.Integer, csdl.ForeignKey('donation.id'), nullable=False)
    category_id = csdl.Column(csdl.Integer, csdl.ForeignKey('category.id'), nullable=False)
    item_name = csdl.Column(csdl.String(100), nullable=False)
    quantity = csdl.Column(csdl.Integer)
    image = csdl.Column(csdl.String(100), nullable=True)
    category = csdl.relationship('Category', backref='donation_items', lazy=True)