#-*- encoding: utf-8 -*-
"""
parser.sql.dbschema module (imdb.parser.sql package).

This module provides the schema used to describe the layout of the
database used by the imdb.parser.sql package; functions to create/drop
tables and indexes are also provided.

Copyright 2005-2009 Davide Alberani <da@erlug.linux.it>
               2006 Giuseppe "Cowo" Corbelli <cowo --> lugbs.linux.it>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

# Placeholders for column types.
INTCOL = 1
UNICODECOL = 2
STRINGCOL = 3

class DBCol(object):
    """Define column objects."""
    def __init__(self, name, kind, **params):
        self.name = name
        self.kind = kind
        self.index = None
        self.indexLen = None
        # If not None, two notations are accepted: 'TableName'
        # and 'TableName.ColName'; in the first case, 'id' is assumed
        # as the name of the pointed column.
        self.foreignKey = None
        if 'index' in params:
            self.index = params['index']
            del params['index']
        if 'indexLen' in params:
            self.indexLen = params['indexLen']
            del params['indexLen']
        if 'foreignKey' in params:
            self.foreignKey = params['foreignKey']
            del params['foreignKey']
        self.params = params

class DBTable(object):
    """Define table objects."""
    def __init__(self, name, *cols, **kwds):
        self.name = name
        self.cols = cols
        # Default values.
        self.values = kwds.get('values', {})
        # Indexes.
        self.indexes = kwds.get('indexes', {})

# Default values to insert in some tables: {'column': (list, of, values, ...)}
kindTypeDefs = {'kind': ('movie', 'tv series', 'tv movie', 'video movie',
                        'tv mini series', 'video game', 'episode')}
companyTypeDefs = {'kind': ('distributors', 'production companies',
                        'special effects companies', 'miscellaneous companies')}
infoTypeDefs = {'info': ('runtimes', 'color info', 'genres', 'languages',
    'certificates', 'sound mix', 'tech info', 'countries', 'taglines',
    'keywords', 'alternate versions', 'crazy credits', 'goofs',
    'soundtrack', 'quotes', 'release dates', 'trivia', 'locations',
    'mini biography', 'birth notes', 'birth date', 'height',
    'death date', 'spouse', 'other works', 'birth name',
    'salary history', 'nick names', 'books', 'agent address',
    'biographical movies', 'portrayed', 'where now', 'trademarks',
    'interviews', 'articles', 'magazine covers', 'pictorials',
    'death notes', 'LD disc format', 'LD year', 'LD digital sound',
    'LD official retail price', 'LD frequency response', 'LD pressing plant',
    'LD length', 'LD language', 'LD review', 'LD spaciality', 'LD release date',
    'LD production country', 'LD contrast', 'LD color rendition',
    'LD picture format', 'LD video noise', 'LD video artifacts',
    'LD release country', 'LD sharpness', 'LD dynamic range',
    'LD audio noise', 'LD color information', 'LD group genre',
    'LD quality program', 'LD close captions-teletext-ld-g',
    'LD category', 'LD analog left', 'LD certification',
    'LD audio quality', 'LD video quality', 'LD aspect ratio',
    'LD analog right', 'LD additional information',
    'LD number of chapter stops', 'LD dialogue intellegibility',
    'LD disc size', 'LD master format', 'LD subtitles',
    'LD status of availablility', 'LD quality of source',
    'LD number of sides', 'LD video standard', 'LD supplement',
    'LD original title', 'LD sound encoding', 'LD number', 'LD label',
    'LD catalog number', 'LD laserdisc title', 'screenplay-teleplay',
    'novel', 'adaption', 'book', 'production process protocol',
    'printed media reviews', 'essays', 'other literature', 'mpaa',
    'plot', 'votes distribution', 'votes', 'rating',
    'production dates', 'copyright holder', 'filming dates', 'budget',
    'weekend gross', 'gross', 'opening weekend', 'rentals',
    'admissions', 'studios', 'top 250 rank', 'bottom 10 rank')}
compCastTypeDefs = {'kind': ('cast', 'crew', 'complete', 'complete+verified')}
linkTypeDefs = {'link': ('follows', 'followed by', 'remake of', 'remade as',
                        'references', 'referenced in', 'spoofs', 'spoofed in',
                        'features', 'featured in', 'spin off from', 'spin off',
                        'version of', 'similar to', 'edited into',
                        'edited from', 'alternate language version of',
                        'unknown link')}
roleTypeDefs = {'role': ('actor', 'actress', 'producer', 'writer',
                        'cinematographer', 'composer', 'costume designer',
                        'director', 'editor', 'miscellaneous crew',
                        'production designer', 'guest')}

# Schema of tables in our database.
# XXX: Foreign keys can be used to create constrains between tables,
#      but they create indexes in the database, and this
#      means poor performances at insert-time.
DB_SCHEMA = [
    DBTable('Name',
        # namePcodeCf is the soundex of the name in the canonical format.
        # namePcodeNf is the soundex of the name in the normal format, if
        # different from namePcodeCf.
        # surnamePcode is the soundex of the surname, if different from the
        # other two values.

        # The 'id' column is simply skipped by SQLObject (it's a default);
        # the alternateID attribute here will be ignored by SQLAlchemy.
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('name', UNICODECOL, notNone=True, index='idx_name', indexLen=6),
        DBCol('imdbIndex', UNICODECOL, length=12, default=None),
        DBCol('imdbID', INTCOL, default=None),
        DBCol('namePcodeCf', STRINGCOL, length=5, default=None,
                index='idx_pcodecf'),
        DBCol('namePcodeNf', STRINGCOL, length=5, default=None,
                index='idx_pcodenf'),
        DBCol('surnamePcode', STRINGCOL, length=5, default=None,
                index='idx_pcode')
    ),

    DBTable('CharName',
        # namePcodeNf is the soundex of the name in the normal format.
        # surnamePcode is the soundex of the surname, if different
        # from namePcodeNf.
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('name', UNICODECOL, notNone=True, index='idx_name', indexLen=6),
        DBCol('imdbIndex', UNICODECOL, length=12, default=None),
        DBCol('imdbID', INTCOL, default=None),
        DBCol('namePcodeNf', STRINGCOL, length=5, default=None,
                index='idx_pcodenf'),
        DBCol('surnamePcode', STRINGCOL, length=5, default=None,
                index='idx_pcode')
    ),

    DBTable('CompanyName',
        # namePcodeNf is the soundex of the name in the normal format.
        # namePcodeSf is the soundex of the name plus the country code.
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('name', UNICODECOL, notNone=True, index='idx_name', indexLen=6),
        DBCol('countryCode', UNICODECOL, length=255, default=None),
        DBCol('imdbID', INTCOL, default=None),
        DBCol('namePcodeNf', STRINGCOL, length=5, default=None,
                index='idx_pcodenf'),
        DBCol('namePcodeSf', STRINGCOL, length=5, default=None,
                index='idx_pcodesf')
    ),

    DBTable('KindType',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('kind', STRINGCOL, length=15, default=None, alternateID=True),
        values=kindTypeDefs
    ),

    DBTable('Title',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('title', UNICODECOL, notNone=True,
                index='idx_title', indexLen=10),
        DBCol('imdbIndex', UNICODECOL, length=12, default=None),
        DBCol('kindID', INTCOL, notNone=True, foreignKey='KindType'),
        DBCol('productionYear', INTCOL, default=None),
        DBCol('imdbID', INTCOL, default=None),
        DBCol('phoneticCode', STRINGCOL, length=5, default=None,
                index='idx_pcode'),
        DBCol('episodeOfID', INTCOL, default=None, index='idx_epof',
                foreignKey='Title'),
        DBCol('seasonNr', INTCOL, default=None),
        DBCol('episodeNr', INTCOL, default=None),
        # Maximum observed length is 44; 49 can store 5 comma-separated
        # year-year pairs.
        DBCol('seriesYears', STRINGCOL, length=49, default=None)
    ),

    DBTable('CompanyType',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('kind', STRINGCOL, length=32, default=None, alternateID=True),
        values=companyTypeDefs
    ),

    DBTable('AkaName',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('personID', INTCOL, notNone=True, index='idx_person',
                foreignKey='Name'),
        DBCol('name', UNICODECOL, notNone=True),
        DBCol('imdbIndex', UNICODECOL, length=12, default=None),
        DBCol('namePcodeCf',  STRINGCOL, length=5, default=None,
                index='idx_pcodecf'),
        DBCol('namePcodeNf',  STRINGCOL, length=5, default=None,
                index='idx_pcodenf'),
        DBCol('surnamePcode',  STRINGCOL, length=5, default=None,
                index='idx_pcode')
    ),

    DBTable('AkaTitle',
        # XXX: It's safer to set notNone to False, here.
        #      alias for akas are stored completely in the AkaTitle table;
        #      this means that episodes will set also a "tv series" alias name.
        #      Reading the aka-title.list file it looks like there are
        #      episode titles with aliases to different titles for both
        #      the episode and the series title, while for just the series
        #      there are no aliases.
        #      E.g.:
        #      aka title                                 original title
        # "Series, The" (2005) {The Episode}  "Other Title" (2005) {Other Title}
        # But there is no:
        # "Series, The" (2005)                "Other Title" (2005)
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('movieID', INTCOL, notNone=True, index='idx_movieid',
                foreignKey='Title'),
        DBCol('title', UNICODECOL, notNone=True),
        DBCol('imdbIndex', UNICODECOL, length=12, default=None),
        DBCol('kindID', INTCOL, notNone=True, foreignKey='KindType'),
        DBCol('productionYear', INTCOL, default=None),
        DBCol('phoneticCode',  STRINGCOL, length=5, default=None,
                index='idx_pcode'),
        DBCol('episodeOfID', INTCOL, default=None, index='idx_epof',
                foreignKey='AkaTitle'),
        DBCol('seasonNr', INTCOL, default=None),
        DBCol('episodeNr', INTCOL, default=None),
        DBCol('note', UNICODECOL, default=None)
    ),

    DBTable('RoleType',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('role', STRINGCOL, length=32, notNone=True, alternateID=True),
        values=roleTypeDefs
    ),

    DBTable('CastInfo',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('personID', INTCOL, notNone=True, index='idx_pid',
                foreignKey='Name'),
        DBCol('movieID', INTCOL, notNone=True, index='idx_mid',
                foreignKey='Title'),
        DBCol('personRoleID', INTCOL, default=None, index='idx_cid',
                foreignKey='CharName'),
        DBCol('note', UNICODECOL, default=None),
        DBCol('nrOrder', INTCOL, default=None),
        DBCol('roleID', INTCOL, notNone=True, foreignKey='RoleType')
    ),

    DBTable('CompCastType',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('kind', STRINGCOL, length=32, notNone=True, alternateID=True),
        values=compCastTypeDefs
    ),

    DBTable('CompleteCast',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('movieID', INTCOL, index='idx_mid', foreignKey='Title'),
        DBCol('subjectID', INTCOL, notNone=True, foreignKey='CompCastType'),
        DBCol('statusID', INTCOL, notNone=True, foreignKey='CompCastType')
    ),

    DBTable('InfoType',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('info', STRINGCOL, length=32, notNone=True, alternateID=True),
        values=infoTypeDefs
    ),

    DBTable('LinkType',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('link', STRINGCOL, length=32, notNone=True, alternateID=True),
        values=linkTypeDefs
    ),

    DBTable('Keyword',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        # XXX: can't use alternateID=True, because it would create
        #      a UNIQUE index; unfortunately (at least with a common
        #      collation like utf8_unicode_ci) MySQL will consider
        #      some different keywords identical - like
        #      "fiancée" and "fiancee".
        DBCol('keyword', UNICODECOL, length=255, notNone=True,
                index='idx_keyword', indexLen=5),
        DBCol('phoneticCode', STRINGCOL, length=5, default=None,
                index='idx_pcode')
    ),

    DBTable('MovieKeyword',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('movieID', INTCOL, notNone=True, index='idx_mid',
                foreignKey='Title'),
        DBCol('keywordID', INTCOL, notNone=True, index='idx_keywordid',
                foreignKey='Keyword')
    ),

    DBTable('MovieLink',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('movieID', INTCOL, notNone=True, index='idx_mid',
                foreignKey='Title'),
        DBCol('linkedMovieID', INTCOL, notNone=True, foreignKey='Title'),
        DBCol('linkTypeID', INTCOL, notNone=True, foreignKey='LinkType')
    ),

    DBTable('MovieInfo',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('movieID', INTCOL, notNone=True, index='idx_mid',
                foreignKey='Title'),
        DBCol('infoTypeID', INTCOL, notNone=True, foreignKey='InfoType'),
        DBCol('info', UNICODECOL, notNone=True),
        DBCol('note', UNICODECOL, default=None)
    ),

    # This table is identical to MovieInfo, except that both 'infoTypeID'
    # and 'info' are indexed.
    DBTable('MovieInfoIdx',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('movieID', INTCOL, notNone=True, index='idx_mid',
                foreignKey='Title'),
        DBCol('infoTypeID', INTCOL, notNone=True, index='idx_infotypeid',
                foreignKey='InfoType'),
        DBCol('info', UNICODECOL, notNone=True, index='idx_info', indexLen=10),
        DBCol('note', UNICODECOL, default=None)
    ),

    DBTable('MovieCompanies',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('movieID', INTCOL, notNone=True, index='idx_mid',
                foreignKey='Title'),
        DBCol('companyID', INTCOL, notNone=True, index='idx_cid',
                foreignKey='CompanyName'),
        DBCol('companyTypeID', INTCOL, notNone=True, foreignKey='CompanyType'),
        DBCol('note', UNICODECOL, default=None)
    ),

    DBTable('PersonInfo',
        DBCol('id', INTCOL, notNone=True, alternateID=True),
        DBCol('personID', INTCOL, notNone=True, index='idx_pid',
                foreignKey='Name'),
        DBCol('infoTypeID', INTCOL, notNone=True, foreignKey='InfoType'),
        DBCol('info', UNICODECOL, notNone=True),
        DBCol('note', UNICODECOL, default=None)
    )
]


# Functions to manage tables.
def dropTables(tables, ifExists=True):
    """Drop the tables."""
    # In reverse order (is still useful?  We don't use foreign keys anymore).
    DB_TABLES_DROP = list(tables)
    DB_TABLES_DROP.reverse()
    for table in DB_TABLES_DROP:
        table.dropTable(ifExists)

def createTables(tables, ifNotExists=True):
    """Create the tables and insert default values."""
    for table in tables:
        # Create the table.
        table.createTable(ifNotExists)
        # Insert default values, if any.
        for key in table._imdbpySchema.values:
            for value in table._imdbpySchema.values[key]:
                table(**{key: unicode(value)})

def createIndexes(tables, ifNotExists=True):
    """Create the indexes in the database."""
    for table in tables:
        table.addIndexes(ifNotExists)

def createForeignKeys(tables, ifNotExists=True):
    """Create Foreign Keys."""
    mapTables = {}
    for table in tables:
        mapTables[table._imdbpyName] = table
    for table in tables:
        table.addForeignKeys(mapTables, ifNotExists)

