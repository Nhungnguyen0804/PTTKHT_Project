from app.flask_extensions import csdl

class Donation(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    donation_category_id = csdl.Column(csdl.Integer, csdl.ForeignKey('donation_category.id'), nullable=False)
    donor_name = csdl.Column(csdl.String(50), nullable=False)
    donor_email = csdl.Column(csdl.String(30), nullable=False)
    create_time = csdl.Column(csdl.DateTime, nullable=False)
    status_id = csdl.Column(csdl.Integer, csdl.ForeignKey('donation_status'), nullable=False)


