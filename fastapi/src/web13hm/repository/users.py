from typing import Union
from sqlalchemy.orm import Session
from libgravatar import Gravatar
from src.web13hm.database.models import User
from src.web13hm.shemas import UserModel

async def get_user_by_email(email, db):
    user: User = db.query(User).filter(User.email == email).first()

    return user


async def create_user(body: UserModel, db: Session) -> User:
    avatar = None
    try:
        g = Gravatar(body.username)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    try:
        new_user = User(email=body.username, password=body.password, avatar=avatar)
    except Exception as e:
        print(e)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: Union[str, None], db: Session) -> None:
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user
