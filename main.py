from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False


@app.route("/movie/<title>/")
def search_title(title):
    with sqlite3.connect("netflix.db") as content:
        cursor = content.cursor()
        info = f"""
            SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title = {title}
            ORDER BY release_year DESC
            LIMIT 1
        """
        cursor.execute(info)
        result = cursor.fetchall()[0]
        result_json = {
            "title": result[0],
            "country": result[1],
            "release_year": result[2],
            "genre": result[3],
            "description": result[4]
        }
        return jsonify(result_json)


@app.route("/movie/<int:start>/to/<int:end>/")
def search_year(start, end):
    with sqlite3.connect("netflix.db") as content:
        cursor = content.cursor()
        info = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {start} AND {end}
            ORDER BY release_year
            LIMIT 100
        """
        cursor.execute(info)
        result = cursor.fetchall()
        result_json = []
        for film in result:
            result_json.append({
                "title": film[0],
                "release_year": film[1],
            })
        return jsonify(result_json)


@app.route("/rating/<rating>/")
def search_rating(rating):
    rating_dict = {
        'children': ['G'],
        'family': ['G', 'PG', 'PG-13'],
        'adult': ['R', 'NC-17']
    }
    ratings = '\", \"'.join(rating_dict[rating])
    ratings = f'\"{ratings}\"'

    with sqlite3.connect("netflix.db") as content:
        cursor = content.cursor()
        info = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN ({ratings}) 
        """
        cursor.execute(info)
        result = cursor.fetchall()
        result_json = []
        for film in result:
            result_json.append({
                "title": film[0],
                "rating": film[1],
                "description": film[2]
            })
        return jsonify(result_json)


@app.route("/genre/<genre>/")
def search_genre(genre):
    with sqlite3.connect("netflix.db") as content:
        cursor = content.cursor()
        info = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC 
            LIMIT 10
        """
        cursor.execute(info)
        result = cursor.fetchall()
        result_json = []
        for film in result:
            result_json.append({
                "title": film[0],
                "description": film[1]
            })
        return jsonify(result_json)


app.run()
