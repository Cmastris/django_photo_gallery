from django.test import override_settings, tag, TestCase
from unittest.mock import patch

from .settings import get_list_from_env


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
