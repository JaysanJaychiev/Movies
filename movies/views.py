from django.shortcuts import render
from .models import Movie
from django.views.generic.base import View
from django.views.generic import ListView, DetailView



class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    # template_name = "movies/movies.html"


class MovieDetailView(DetailView):
    """Полное описани фильма"""
    model = Movie
    slug_field = "url"



    # def get(self, request, slug):
    #     movie = Movie.objects.get(url=slug)
    #     return render(request, "movies/movie_detail.html", {'movie': movie})