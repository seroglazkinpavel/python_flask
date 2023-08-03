"""
Создать API для получения списка фильмов по жанру. Приложение должно
иметь возможность получать список фильмов по заданному жанру.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс Movie с полями id, title, description и genre.
Создайте список movies для хранения фильмов.
Создайте маршрут для получения списка фильмов по жанру (метод GET).
Реализуйте валидацию данных запроса и ответа.
"""
from random import choice
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import uvicorn
from pydantic import BaseModel


class Movie(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    genre: str


movies = []
for i in range(1, 20):
    movie = Movie(id=i,
                  title=f'Title{i}',
                  description='Some description',
                  genre=f'{choice(["comedy", "action_movie", "melodrama"])}')
    movies.append(movie)

app = FastAPI()
templates = Jinja2Templates(directory='lesson_5/templates')


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse('index_5.html', {'request': request, 'movies': movies, 'title': 'Movie'})


@app.get('/genres/{genre}', response_class=HTMLResponse)
async def get_movie(request: Request, genre: str):
    genres = [item for item in movies if item.genre == genre]
    return templates.TemplateResponse('index_genres.html',
                                      {'request': request, 'genres': genres, 'title': 'Genres'})


@app.get('/movies/{movie_id}', response_model=Movie)
async def get_task(movie_id: int):
    for movie in movies:
        if movie.id == movie_id:
            return movie


@app.post('/movies/', response_model=Movie)
async def create_task(new_movie: Movie):
    new_movie.id = len(movies) + 1
    movies.append(new_movie)
    return new_movie


@app.put('/movies/{movie_id}', response_model=Movie)
async def update_movie(new_movie: Movie, movie_id: int):
    for idx, movie in enumerate(movies):
        if movie.id == movie_id:
            new_movie.id = movie_id
            movies[idx] = new_movie
            return new_movie
    raise HTTPException(status_code=404, detail="Movie not fount")


@app.delete('/movies/{movie_id}')
async def delete_movie(movie_id: int):
    for idx, movie in enumerate(movies):
        if movie.id == movie_id:
            del movies[idx]
            return {'message': f'Movie with id {movie_id} was deleted'}
    raise HTTPException(status_code=404, detail="Movie not fount")
