from django.test import override_settings, tag, TestCase
from unittest.mock import patch

from .settings import get_bool_from_env, get_list_from_env


@tag('settings')
@override_settings(SECURE_SSL_REDIRECT=False)
class SettingsTests(TestCase):

    @tag('get_list_from_env')
    def test_get_list_from_env_empty(self):
        """Test that an empty list is returned for an empty env val."""
        with patch.dict('os.environ', {'EMPTY_VAL': ''}):
            self.assertEqual(get_list_from_env('EMPTY_VAL'), [])

    @tag('get_list_from_env')
    def test_get_list_from_env_single(self):
        """Test that a single-item list is returned for an env val."""
        with patch.dict('os.environ', {'SINGLE_VAL': 'val'}):
            self.assertEqual(get_list_from_env('SINGLE_VAL'), ['val'])

    @tag('get_list_from_env')
    def test_get_list_from_env_multiple(self):
        """Test that a multiple-item list is returned for an env val."""
        with patch.dict('os.environ', {'MULTI_VAL': 'val1,val2,val3'}):
            self.assertEqual(get_list_from_env('MULTI_VAL'), 
                             ['val1', 'val2', 'val3'])
            
    @tag('get_list_from_env')
    def test_get_list_from_env_multiple_trailing_comma(self):
        """Test that a multiple-item list is returned for an env val.
        
        This version includes a trailing comma in the env val. This 
        should be ignored rather than adding an empty str to the list.
        """
        with patch.dict('os.environ', {'MULTI_VAL': 'val1,val2,val3,'}):
            self.assertEqual(get_list_from_env('MULTI_VAL'), 
                             ['val1', 'val2', 'val3'])
            
    @tag('get_bool_from_env')
    def test_get_bool_from_env_true(self):
        """Test that `True` is returned for a 'True' env val."""
        with patch.dict('os.environ', {'TRUE_VAL': 'True'}):
            self.assertEqual(get_bool_from_env('TRUE_VAL'), True)

    @tag('get_bool_from_env')
    def test_get_bool_from_env_false(self):
        """Test that `False` is returned for a 'False' env val."""
        with patch.dict('os.environ', {'FALSE_VAL': 'False'}):
            self.assertEqual(get_bool_from_env('FALSE_VAL'), False)

    @tag('get_bool_from_env')
    def test_get_bool_from_env_default_val(self):
        """Test that the default val is used if the key doesn't exist."""
        with patch.dict('os.environ', {}):
            self.assertEqual(get_bool_from_env('UNSET_KEY', 'True'), True)

    @tag('get_bool_from_env')
    def test_get_bool_from_env_invalid(self):
        """Test that an exception is raised for an invalid env val."""
        with patch.dict('os.environ', {'INVALID_VAL': 'not a bool'}):
            self.assertRaises(AssertionError, get_bool_from_env, 'INVALID_VAL')
