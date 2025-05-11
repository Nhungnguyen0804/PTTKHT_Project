from app.flask_extensions import csdl, login_manager

class Event(csdl.Model):
    id = csdl.Column(csdl.Integer, primary_key=True)
    name = csdl.Column(csdl.String(50), unique=True, nullable=False)
    start_time = csdl.Column(csdl.DateTime, nullable=False)
    end_time = csdl.Column(csdl.DateTime, nullable=False)
    event_type  = csdl.Column(csdl.String(30), nullable=False)
    
    fee = csdl.Column(csdl.Integer, nullable=True)
    image = csdl.Column(csdl.String(50), nullable=True)
    managed_by = csdl.relationship(
        'User',
        secondary='event_manager',
        backref=csdl.backref('managed_events', lazy='dynamic')  # ← sửa ở đây
    )
    buyable_items = csdl.relationship('BuyableItem', backref='event', lazy=True)
    status_id = csdl.Column(csdl.Integer, csdl.ForeignKey('event_status.id'), nullable=False)
    status = csdl.relationship('EventStatus', backref='events')
    donation_categories = csdl.relationship(
        'DonationCategory',
        back_populates='event',
        lazy='select'  # Hoặc để mặc định
    )

event_manager = csdl.Table('event_manager',
    csdl.Column('user_id', csdl.Integer, csdl.ForeignKey('user.id'), primary_key=True),
    csdl.Column('event_id', csdl.Integer, csdl.ForeignKey('event.id'), primary_key=True)
)
