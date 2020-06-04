import json
from urllib.request import urlopen
from urllib.parse import quote
import cogs.resources.UrbanPy.definition as d

DEFINE = 'https://api.urbandictionary.com/v0/define?term='
RANDOM = 'https://api.urbandictionary.com/v0/random'
FROMID = 'https://api.urbandictionary.com/v0/define?defid='


class UrbanDictionary:
    """
    The main class for the wrapper. Creates and returns `Definition` objects.
    """
    def _open_urban_dictionary(self, url):
        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        
        response.close()
        return data

    def _parse_json(self, data):
        definitions = []
        if data is None:
            raise ValueError('Urban Dictionary API returned nothing.')
        if ('list' not in data or len(data['list']) < 1):
            return result
        for item in data['list']:     
            _def = d.Definition(
                definition=item['definition'],
                word=item['word'],
                permalink=item['permalink'],
                thumbs_up=item['thumbs_up'],
                thumbs_down=item['thumbs_down'],
                defid=item['defid'],
                author=item['author'],
                example=item['example']
            )
            definitions.append(_def)
        return definitions


    def define(self, arg=None):
        """
        Search for a term/phrase, or leave the parameters blank for random words.

        :param arg: The word/id to search for (`str`, `int`, `None`)
        :returns: A list of `Definition` objects
        :raises TypeError: If the argument supplied is not `str`, `int`, or `None`
        """
        url = ''
        if isinstance(arg, int):
            url = FROMID + arg
        elif isinstance(arg, str):
            arg = arg.strip()
            url = DEFINE + arg
        elif arg is None:
            url = RANDOM
        else:
            raise TypeError("Invalid argument type, must be str, int, or None.")
        data = self._open_urban_dictionary(url)
        return self._parse_json(data)



            

 