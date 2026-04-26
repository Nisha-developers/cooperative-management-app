"""
Shared Cloudinary upload/delete helpers.
Used by users, listings, and wallet apps.
"""
import cloudinary.uploader
from rest_framework.exceptions import ValidationError

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def _validate_image(image_file):
    if image_file.content_type not in ALLOWED_TYPES:
        raise ValidationError("Only JPEG, PNG, and WEBP images are supported.")
    if image_file.size > MAX_SIZE_BYTES:
        raise ValidationError("Image file size must not exceed 5 MB.")


def upload_avatar(image_file, user_id: int) -> str:
    """
    Upload a profile picture to Cloudinary.
    Returns the secure URL.
    """
    _validate_image(image_file)
    result = cloudinary.uploader.upload(
        image_file,
        folder="bethel/avatars",
        public_id=f"user_{user_id}",
        overwrite=True,               # replaces existing avatar for the same user
        resource_type="image",
        transformation=[
            {"width": 400, "height": 400, "crop": "fill", "gravity": "face"},
            {"quality": "auto", "fetch_format": "auto"},
        ],
    )
    return result["secure_url"]


def upload_listing_image(image_file, listing_id: str) -> dict:
    """
    Upload a listing photo to Cloudinary.
    Returns {"url": ..., "public_id": ...} so we can delete it later.
    """
    _validate_image(image_file)
    result = cloudinary.uploader.upload(
        image_file,
        folder=f"bethel/listings/{listing_id}",
        overwrite=False,
        resource_type="image",
        transformation=[
            {"quality": "auto", "fetch_format": "auto"},
        ],
    )
    return {"url": result["secure_url"], "public_id": result["public_id"]}


def upload_payment_proof(image_file, reference: str) -> str:
    """
    Upload a wallet payment proof image to Cloudinary.
    Returns the secure URL.
    """
    _validate_image(image_file)
    result = cloudinary.uploader.upload(
        image_file,
        folder="bethel/payment_proofs",
        public_id=reference,
        overwrite=True,
        resource_type="image",
        transformation=[
            {"quality": "auto", "fetch_format": "auto"},
        ],
    )
    return result["secure_url"]


def delete_image(public_id: str):
    """Delete an image from Cloudinary by its public_id."""
    cloudinary.uploader.destroy(public_id, resource_type="image")