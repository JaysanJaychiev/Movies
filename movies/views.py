from django import template
from django.http import request
# from django.http import request
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.views.generic import ListView, DetailView

from django.db.models import Q

from .models import Movie, Category, Actor, Genre, Rating
from .forms import ReviewForm, RatingForm


class GenreYear():
    """Жанры и года выхода фиьмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")
        



class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 1




class MovieDetailView(GenreYear, DetailView):
    """Полное описани фильма"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = "url"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context['form'] = ReviewForm()
        return context



class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save() 
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = "movies/actor.html"
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""

    paginate_by = 2

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist('year')])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist('genre')])
        return context


    


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        # distinct исключает повторения, values задаем нужные нам поля
        return queryset
        
        
    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        # get_queryset оборачиваем в список
        return JsonResponse({"movies": queryset}, safe=False)

    
class AddStarRating(View):
    """добавление рейтинга к фильму"""
    def get_client_ip(self, request):
        # Возвращает ip адрес клиента зароса
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
    
    # для пост запроса
    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            # Проверка на валидность
            Rating.objects.update_or_create(
            # если рейтинг создан позволяет обновить данные рейтинга
                ip=self.get_client_ip(request),
                # здесь мы получаем ip адрес клиента который отправил нам запрос
                movie_id=int(request.POST.get("movie")),
                # к movie_id присваивается поле из нашего пост запроса и оборачиваем в int
                # это все приходит из скрытого поля name='movie'
                defaults={'star_id': int(request.POST.get('star'))}
                # в том случае если мы найдем такую запись к полe star_id 
                # передаем star из нашего пост запроса и оборачиваем в инт
                # type="radio" name="star"
            )
            return HttpResponse(status=201)
            # При успешного выполнения данного кода 201
        else:
            return HttpResponse(status=400)
            # если форма не валидна статус 400

class Search(ListView):
    """Поиск фильмов"""

    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))
        # icontains не учитывает регистр
        
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        # context - это словарь и сравниваем с GET запросом
        return context
 
    
