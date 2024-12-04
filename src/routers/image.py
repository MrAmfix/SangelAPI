import os
import io
from fastapi import Depends, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from PIL import Image, UnidentifiedImageError
from pydantic import UUID4
from settings import MAX_FILE_SIZE, UPLOAD_FOLDER
from utils.image import image_name_rename
from crud.UserCrud import UserCrud
from crud.MediaCrud import MediaCrud
from schemas import MediaModels
from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/api")


@router.post(
    "/client/upload_photo",
    summary="Загрузка фотографии",
)
async def uploag_image(
    user_id: UUID4,
    rewrite: bool = True,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):

    try:
        user_in_db = await UserCrud.get_by_id(session=session, record_id=user_id)
        if not user_in_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error: The user with ID{user_id} does not exist",
            )

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
                detail="File size exceeds the maximum limit of 2MB.",
            )

        contents = await file.read()
        with Image.open(io.BytesIO(contents)) as img:
            if img.format not in ["JPEG", "PNG"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid image format. Only JPEG and PNG are allowed.",
                )
            img.verify()

        check_photo = user_in_db.photo_id

        if not check_photo:

            file.filename = image_name_rename(user_id, rewrite, img_name=None)
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)

            with open(file_path, "wb") as buffer:
                buffer.write(contents)

            data = MediaModels.Create(
                media_link=file_path, is_photo=True, user=user_id
            ).model_dump()
            photo_query = await MediaCrud.create(session=session, **data)

            await UserCrud.update(
                session=session, record_id=user_id, photo_id=photo_query.id
            )

        elif rewrite is True:

            photo_query_get = await MediaCrud.get_by_id(
                session=session, record_id=check_photo
            )
            photo_name = photo_query_get.media_link

            if os.path.exists(UPLOAD_FOLDER):
                os.remove(photo_name)

            file.filename = image_name_rename(user_id, rewrite, img_name=photo_name)
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(contents)

            data = MediaModels.Update(
                id=check_photo, media_link=file_path, is_photo=True
            ).model_dump()
            photo_query = await MediaCrud.update(
                session=session, record_id=check_photo, **data
            )

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"photo_id": f"{photo_query.id}"},
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
