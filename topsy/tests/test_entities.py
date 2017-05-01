import unittest

import attr

from topsy.entities import Entity


class EntityTestCase(unittest.TestCase):
    def setUp(self):
        @attr.s(frozen=True)
        class SomeEntity(Entity):
            title = attr.ib()
            body = attr.ib(default='what')

        self.some_entity = SomeEntity(title='nah')

    def test_asdict(self):
        """asdict should return dictionary."""
        ent_dict = self.some_entity.asdict()
        self.assertEqual(ent_dict, attr.asdict(self.some_entity))

    def test_replace(self):
        """replace should return new instance with updated attribute(s)."""
        new_title = 'yep'

        new_ent = self.some_entity.replace(title=new_title)

        self.assertEqual(new_ent.title, new_title)
        self.assertNotEqual(new_ent, self.some_entity)
