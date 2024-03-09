import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from schemas import UserCreate
from database.models import User
from repository.users import (get_user_by_email, create_user, remove_user, update_token, verify_email, patch_avatar)


class TestUsersRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)


    async def test_get_user_by_email(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email="test_mail@example.com", db=self.session)
        self.assertEqual(result, user)


    async def test_get_user_by_email_none(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email="non_existent_mail@example.com", db=self.session)
        self.assertIsNone(result)


    async def test_create_user(self):
        body = UserCreate(username="fake_user", email="test@example.com", password="password123")
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.email, body.email)
    
    
    async def test_remove_user(self):
        user = User(id=1, email="test_mail@example.com")
        self.session.query().filter().first.return_value = user
        result = await remove_user(user_id=user.id, db=self.session)
        self.assertEqual(result, user)


    async def test_update_token(self):
        reftoken = "new_refresh_token"
        user = User(id=1, email="test_mail@example.com")
        self.session.query().filter().first.return_value = user
        await update_token(user=user, token=reftoken, db=self.session)
        self.assertEqual(user.refresh, reftoken)


    async def test_verify_email(self):
        user = User(id=1, email="test_mail@example.com", verified=True)
        self.session.query().filter().first.return_value = user
        await verify_email(email="test_mail@example.com", db=self.session)
        self.assertTrue(user.verified)


    async def test_patch_avatar(self):
        avatar_url = "https://fake.com/avatar.png"
        user = User(id=1, email="test_mail@example.com", avatar=avatar_url)
        self.session.query().filter().first.return_value = user
        result = await patch_avatar(user=user, avatar=avatar_url, db=self.session)
        self.assertEqual(result, user)



if __name__ == '__main__':
    unittest.main()
