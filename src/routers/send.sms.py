from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from utils.send_sms import generate_code, send_sms
from crud.VerificationCodeCrud import VerificationCodeCrud
from schemas import VerificationCodeModels
from database import get_session
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter("/api")




async def send_sms_to_user(phone_number: str, session:AsyncSession = Depends(get_session)):
    try:
        code = generate_code()
        message = f"Ваш код верификации: {code}"
        status_code =  await send_sms(user_number=phone_number, message=message)
        if status_code == 200:
            verification_code_data = VerificationCodeModels.Create(phone=phone_number,code=code)
            result = await VerificationCodeCrud.create(session=session, **verification_code_data)
            if result:
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={"message":f"Код верификации отправлен на номер {phone_number}"}
                )
    except Exception:
        raise HTTPException(detail={"message":"Ошибка при отправке SMS"})
    

async def check_verification_code(phone_number: str, code: str, session:AsyncSession = Depends(get_session)):
    try:
        #
        #TODO чек на протухание кода?
        # чек на пролив трафика? сколько попыток нужно для ввода?
        #
        user_verification  = await VerificationCodeCrud.get_by_param(session=session,phone_number=phone_number)
        if not (user_verification and user_verification.code == code):
            await VerificationCodeCrud.delete(session=session,record_id=user_verification.id)
            return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={"message":"Неверный код СМС"}
                    )
        
        #
        # TODO присвоение токена пользаку
        #

        await VerificationCodeCrud.delete(session=session,record_id=user_verification.id)
        return JSONResponse(
                        status_code=status.HTTP_200_OK,
                        content={"message":"Верификация успешна"}
                    )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message":"Что-то пошло не так"}
            )
        


