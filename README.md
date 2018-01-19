# IMDbPY-legacy

**IMDbPY** is a Python package useful to retrieve and manage the data of the [IMDb][imdb] movie database about movies, people, characters and companies.

This is the fork of *imdbpy-legacy* branch of [IMDbPY][imdbpy] python package, still compatible with Python 2.7. An effort is made to downstream merge all changes to parsers and keep it working with current IMDb sites structure.

## Main features

* written in pure Python (and few, optional, C lines)
* platform-independent
* can retrieve data from both the IMDb's web server and a local copy of the whole database
* a simple and complete API
* released under the GPL-2.0+ license
* IMDbPY powers many other softwares and has been used in various research papers. [Curious about that][ecosystem]?

## Code example

    from imdb import IMDb
    ia = IMDb()

    # print the director(s) of a movie
    the_matrix = ia.get_movie('0133093')
    print the_matrix['director']

    # search for a person
    for person in ia.search_person('Mel Gibson'):
        print person.personID, person['name']

## License

Released under the GPL-2.0+ license.

[imdb]: http://imdb.com
[ecosystem]: http://imdbpy.sourceforge.net/ecosystem.html
[imdbpy]: https://github.com/alberanid/imdbpy
