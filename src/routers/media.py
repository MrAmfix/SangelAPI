import os
import io
from fastapi import Depends, File, UploadFile, HTTPException, status
from fastapi import APIRouter
from PIL import Image, UnidentifiedImageError
from src.settings import MAX_FILE_SIZE, UPLOAD_FOLDER
from src.utils.image import image_name_rename
from src.crud.UserCrud import UserCrud
from src.crud.MediaCrud import MediaCrud
from src.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.auth import access_token_auth
from src.utils.loggers import api_logs


media = APIRouter(prefix="/media")


@api_logs(media.post("/edit_photo"))
async def upload_image(
    auth_data: dict = Depends(access_token_auth),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
):

    try:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ошибка: Недопустимый тип файла. Только .jpeg and .png разрешены.",
            )

        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        file.file.seek(0, os.SEEK_SET)

        max_file_size_converted = int(MAX_FILE_SIZE)*1024*1024

        if file_size > max_file_size_converted:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка: Размер файла превышает {MAX_FILE_SIZE} МБ.",
            )

        contents = await file.read()
        with Image.open(io.BytesIO(contents)) as img:
            if img.format not in ["JPEG", "PNG"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ошибка: Недопустимый формат. Только JPEG и PNG разрешены",
                )
            img.verify()

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        if not auth_data['user'].photo_id:

            file.filename = image_name_rename(auth_data['user'].id)
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(contents)

            photo_query = await MediaCrud.create(session=session,
                                                 media_link=file.filename,
                                                 is_photo=True)

            await UserCrud.update(
                session=session,
                record_id=auth_data['user'].id,
                photo_id=photo_query.id
            )

        else:

            photo_query_get = await MediaCrud.get_by_id(
                session=session, record_id=auth_data['user'].photo_id,
            )
            if not photo_query_get:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ошибка: Нет фотографии."
                )
            photo_name = photo_query_get.media_link

            if os.path.exists(UPLOAD_FOLDER):
                os.remove("img/"+photo_name)

            file.filename = photo_name
            file_path = os.path.join(UPLOAD_FOLDER, photo_name)
            with open(file_path, "wb") as buffer:
                buffer.write(contents)

            photo_query = await MediaCrud.update(
                session=session,
                record_id=auth_data['user'].photo_id,
                id=auth_data['user'].photo_id,
                media_link=file.filename,
                is_photo=True
            )

        return {
            "detail": "Фото успешно загружено",
            "photo_id": photo_query.id
        }

    except UnidentifiedImageError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка: Файл не является изображением."
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка: Директории '{UPLOAD_FOLDER}' не существует.",
        )
    except OSError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка: Системная ошибка: {str(e)}" ,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка: {str(e)}"
        )
