from app.flask_extensions import csdl

class DonationCategory(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    dc_name = csdl.Column(csdl.String(50), nullable=False)
    donation_type = csdl.Column(csdl.String(30), nullable=False)
    target_quantity = csdl.Column(csdl.Integer)
    start_date = csdl.Column(csdl.DateTime, nullable=False)
    end_date = csdl.Column(csdl.DateTime, nullable=False)
    event_id = csdl.Column(csdl.Integer, csdl.ForeignKey('event.id'), nullable=False)
    event = csdl.relationship('Event', backref=csdl.backref('donation_categories', lazy='dynamic'))


