import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db 



class Images(db.Model):
    __tablename__= "Images"

    image_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    book_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Books.book_id", ondelete="CASCADE"), nullable=False)
    image_url = db.Column(db.String(), nullable=False)
    image_name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    book = db.relationship("Books", back_populates='images')

    def __init__(self, image_url, image_name, active):
        self.image_url = image_url
        self.image_name = image_name
        self.active = active


    def get_new_image():
        return Images("", "", True)
    

class ImagesSchema(ma.Schema):
    class Meta:
        fields = ["image_id", "book_id", "image_url", "image_name", "active"]

    book = ma.fields.Nested("BooksSchema", exclude=["images"])

image_schema = ImagesSchema()
images_schema = ImagesSchema(many=True)

