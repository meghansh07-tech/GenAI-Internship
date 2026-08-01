from pathlib import Path
from PIL import Image
import uuid


# Folder to store uploaded images
UPLOAD_DIRECTORY = Path("uploads/images")

# Create folder if it does not exist
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


# Supported image formats
SUPPORTED_FORMATS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}


def save_uploaded_image(uploaded_file):
    """
    Save uploaded image to uploads/images folder.

    Parameters
    ----------
    uploaded_file : Streamlit UploadedFile

    Returns
    -------
    Path
        Path of the saved image.
    """

    extension = Path(uploaded_file.name).suffix.lower()

    if extension not in SUPPORTED_FORMATS:
        raise ValueError(
            "Unsupported image format. "
            "Only JPG, JPEG, PNG and WEBP are allowed."
        )

    image = Image.open(uploaded_file)

    filename = f"{uuid.uuid4()}{extension}"

    image_path = UPLOAD_DIRECTORY / filename

    image.save(image_path)

    return image_path


def load_image(image_path):
    """
    Load image from disk.

    Parameters
    ----------
    image_path : str or Path

    Returns
    -------
    PIL.Image
    """

    return Image.open(image_path)