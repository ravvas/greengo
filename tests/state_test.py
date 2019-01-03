import unittest
import shutil
import os

from greengo.state import State


class StateTest(unittest.TestCase):
    def setUp(self):
        self.state = State(file=None)
        self.body = {'a': {'b': 'c'}, 'x': {'y': 'z'}}
        self.state._state = self.body

    def tearDown(self):
        pass

    def test_update(self):
        body = {'foo': 'bar'}
        self.state.update('key', body)

        self.assertDictEqual(body, self.state.get('key'))

    def test_get(self):
        self.assertDictEqual(self.body, self.state.get())
        self.assertDictEqual(self.body['a'], self.state.get('a'))

    def test_remove(self):
        self.assertDictEqual(self.body['a'], self.state.get('a'))
        self.state.remove('a')
        self.assertEqual(self.state.get('a'), None)
        self.assertEqual(self.state.get('a', 1), 1)

        # Should not blow
        self.state.remove('key_doesnt_exist')

        self.state.remove()
        self.assertDictEqual({}, self.state.get())


class StateTestWithFile(unittest.TestCase):
    def setUp(self):
        self.file = "./tests/.gg/gg_test_state.json"
        self.state = State(self.file)
        self.body = {'a': {'b': 'c'}, 'x': {'y': 'z'}}
        self.state._state = self.body

    def tearDown(self):
        shutil.rmtree(os.path.dirname(self.file))

        # try:
        #     shutil.rmtree(os.path.dirname(self.file))
        #     # os.remove(self.file)
        # except OSError:
        #     pass

    def test_load(self):
        body = {'foo': 'bar'}
        self.state.update('key', body)

        self.assertDictEqual(body, self.state.get('key'))

    def test_save(self):
        self.state.save()
        state = State(self.file)
        self.assertDictEqual(self.state.get(), state.get())

    def test_remove(self):
        self.assertDictEqual(self.body['a'], self.state.get('a'))
        self.state.remove('a')
        self.assertEqual(self.state.get('a'), None)
        self.assertEqual(self.state.get('a', 1), 1)

        # Should not blow
        self.state.remove('key_doesnt_exist')

        self.state.remove()
        self.assertDictEqual({}, self.state.get())