from __future__ import print_function

import click

class testclass(object):
    """Test Class to be used as a template

    Attributes:
        attrib_1: Sample sting
        attrib_2: Sample int
    """

    def __init__(self, default_string='Mancoon'):
        """Set attributes"""
        self.attrib_1 = f'{default_string}'
        self.attrib_2 = 42

    def test_function(self):
        click.echo(f'This is only a test. {self.attrib_2}')