import os
import io
from fastapi import File, UploadFile, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi import APIRouter
from PIL import Image, UnidentifiedImageError
from settings import MAX_FILE_SIZE, UPLOAD_FOLDER
from utils.image import image_name_rename




router = APIRouter(prefix="/api")


@router.post("/client/upload_photo", summary="Загрузка фотографии")
async def uploag_image(
    file: UploadFile = File(...),
):

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only .jpeg and .png files are allowed.",
        )

    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0, os.SEEK_SET)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds the maximum limit of 8MB.",
        )
    try:
        contents = await file.read()
        with Image.open(io.BytesIO(contents)) as img:
            if img.format not in ["JPEG", "PNG"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid image format. Only JPEG and PNG are allowed.",
                ) 
            img.verify()

        file.filename = image_name_rename()
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(contents)

        #
        # TODO  взаимодействие с бд
        #

        return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": f"File successfully saved as {file_path}."},
            )
        
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File is not a valid image."
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: The directory '{UPLOAD_FOLDER}' does not exist.",
        )
    except IOError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"IOError occurred: {str(e)}",
        )
    except OSError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"OS error occurred: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
