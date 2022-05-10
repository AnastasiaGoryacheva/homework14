import sqlite3


def actors_cast(name1, name2):
    with sqlite3.connect("netflix.db") as content:
        cursor = content.cursor()
        info = f"""
            SELECT "cast"
            FROM netflix
            WHERE "cast" LIKE '%{name1}%'
            AND "cast" LIKE '%{name2}%' 
        """
        cursor.execute(info)
        result = cursor.fetchall()
        result_cast = []
        for actors in result:
            result_cast.extend(actors[0].split(', '))
        result_finish = []
        for actor in result_cast:
            if actor not in [name1, name2]:
                if result_cast.count(actor) > 2:
                    result_finish.append(actor)
        result_finish = set(result_finish)
        return result_finish


def selected_films(type_, release_year, genre):
    with sqlite3.connect("netflix.db") as content:
        cursor = content.cursor()
        info = f"""
            SELECT title, description
            FROM netflix
            WHERE "type" = '{type_}'
            AND release_year = {release_year}
            AND listed_in LIKE '%{genre}%' 
        """
        cursor.execute(info)
        result = cursor.fetchall()
        result_json = []
        for films in result:
            result_json.append({
                "title": films[0],
                "description": films[1]
            })
        return result_json


print(actors_cast("Rose McIver", "Ben Lamb"))
print(actors_cast("Jack Black", "Dustin Hoffman"))
print(selected_films("Movie", 1996, "Drama"))
print(selected_films("Movie", 2001, "Comedies"))
print(selected_films("TV Show", 2009, "Fantasy"))
