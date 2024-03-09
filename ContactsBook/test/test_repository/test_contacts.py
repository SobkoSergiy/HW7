import unittest
from unittest.mock import MagicMock
from datetime import date, timedelta
from sqlalchemy.orm import Session
from schemas import ContactBase
from database.models import Contact, User
from repository.contacts import (get_contacts, get_contact, create_contact, remove_contact, update_contact, soon_birthdays, get_contacts_by_first_name)


class TestContactsRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)


    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, limit=10, user=self.user, db=self.session)
        self.assertEqual(result, contacts)


    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)
        

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


    async def test_create_contact(self):
        body = ContactBase(
            first_name="First",
            last_name="Last",
            phone="+380001234567",
            birthday=date(year=1999, month=12, day=12), #.date(),
            inform='Some inform',
            email="first.last@example.com")
        
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.inform, body.inform)
        self.assertEqual(result.email, body.email)


    async def test_remove_contact(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)
        

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)


    async def test_update_contact(self):
        body = ContactBase(
            first_name="First",
            last_name="Last",
            phone="+380001234567",
            birthday=date(year=1999, month=12, day=12),
            inform='Some inform',
            email="first.last@example.com")
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)


    async def test_update_contact_not_found(self):
        body = ContactBase(
            first_name="First",
            last_name="Last",
            phone="+380001234567",
            birthday=date(year=1999, month=12, day=12),
            inform='Some inform',
            email="first.last@example.com")
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)


    async def test_get_contacts_by_first_name(self):
        contacts = [Contact(), Contact(), Contact()]
        db_query_mock = MagicMock()
        db_query_mock.filter.return_value.all.return_value = contacts
        self.session.query.return_value = db_query_mock
        result = await get_contacts_by_first_name(first_name="First", db=self.session, user=self.user)
        self.assertEqual(result, contacts)


    async def test_get_contacts_by_first_name_not_found(self):
        db_query_mock = MagicMock()
        db_query_mock.filter().all.return_value = None
        self.session.query.return_value = db_query_mock
        result = await get_contacts_by_first_name(first_name="First", db=self.session, user=self.user)
        self.assertIsNone(result)


    async def test_soon_birthdays(self):
        contacts = [Contact(birthday=date.today() + timedelta(days=3)), 
                    Contact(birthday=date.today() + timedelta(days=5)), 
                    Contact(birthday=date.today() + timedelta(days=7))]
        db_query_mock = MagicMock()
        db_query_mock.filter().all.return_value = contacts
        self.session.query.return_value = db_query_mock
        result = await soon_birthdays(days=12, db=self.session, user=self.user)
        self.assertEqual(result, contacts)

    async def test_soon_birthdays_not_found(self):
        contacts = [Contact(birthday=date.today() - timedelta(days=3)), 
                    Contact(birthday=date.today() - timedelta(days=5)), 
                    Contact(birthday=date.today() - timedelta(days=7))]
        db_query_mock = MagicMock()
        db_query_mock.filter().all.return_value = contacts
        self.session.query.return_value = db_query_mock
        result = await soon_birthdays(days=12, db=self.session, user=self.user)
        self.assertEqual(result, [])



if __name__ == '__main__':
    unittest.main()
