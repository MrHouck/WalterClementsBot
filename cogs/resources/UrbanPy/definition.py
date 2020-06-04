class Definition(object):
    """
    Represents an Urban Dictionary definition.

    Attributes
    -----
    `author`: The definition's author's name.\n
    `definition`: The actual definition of the term/phrase, limited to 100 chars.\n
    `definitionId`: The Urban Dictionary defintion ID.\n
    `example`: The example provided for the term/phrase, limited to 100 chars.\n
    `permalink`: A permanent link to the definition.\n
    `thumbs_up`: The amount of times other users have 'thumbs-upped' the definition.\n
    `thumbs_down`: The amount of times other users have 'thumbs-downed' the definition.\n
    `word`: The word/phrase being defined.
    """
    def __init__(self, word, definition, permalink, thumbs_up, thumbs_down, author, defid, example):        
        self.author = author
        _def = definition[:100] 
        if len(definition) > 100:
            _def += '...' 
        self.definition = _def
        self.definitionId = defid 
        exm = example[:100] 
        if len(example)  > 100:
            exm += '...'
        self.example = exm
        self.permalink = permalink
        self.thumbs_up = thumbs_up
        self.thumbs_down = thumbs_down
        self.word = word

    def __str__(self):
        return '%s %s%s Example: %s%s (%d Thumbs Up, %d Thumbs Down) ' % {
            self.word,
            self.defintion[:100],
            '...' if len(self.definition) > 100 else '',
            self.example[:100],
            '...' if len(self.example) > 100 else '',
            self.thumbs_up,
            self.thumbs_down
        }