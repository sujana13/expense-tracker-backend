import cloudinary
import cloudinary.uploader

from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)

def upload_receipt(file):
    result = cloudinary.uploader.upload(
        file,
        folder="expense-receipts",
        resource_type="auto",
    )

    return result["secure_url"]