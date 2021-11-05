from django.contrib import admin
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


#ReviewInlines для модели Movie выводит внизу привязанные отзывы (admin.StackedInline, admin.TabularInline)
class ReviewInlines(admin.TabularInline):
    """Отзывы на стрнице фильмы"""
    model = Reviews
    # model указываем модель
    extra = 1
    # extra указываем количесто пустых форм для отзывов
    readonly_fields = ("name", "email") 
    # readonly_fields поля которые можно изменить делает только для чтения


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Филмы"""
    list_display = ("title", "category", "url", "draft")
    # list_display указывем какие поля нужно вывести
    list_filter = ("category", "year")
    # фильтрация по полям
    search_fields = ("title", "category__name")
    # поиск по полям
    inlines = [ReviewInlines]
    # inlines для вывода отзывов
    save_on_top = True
    # save_on_top выводит панель для сохранения сверху тоже и внизу по умолчанию
    save_as = True
    # чтобы текущий detail сохранить как новый обьект
    list_editable = ("draft",)
    # list_editable задать поле которую можно редактировать на месте
    # fields = (("actors",'directors', "genres"), )
    # в Форме остаются только нужные поля
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        ("Actors", {
            # 'classes': ("collapse") чтобы сворачивать и разворачивать данный раздел
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        # Options название раздела
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )
    # fieldsets группировка полей на свое усмотрение





@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """ Отзывы"""
    list_display =  ("name", "email", "parent", "movie", "id")
    readonly_fields = ('name', "email")
    


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "ip")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фиьма"""
    list_display = ("title", "movie")

###всех закоментили потомучто использовали декоратор @admin.register(Category)
# admin.site.register(Category, CategoryAdmin)  
# admin.site.register(Genre)
# admin.site.register(Movie)
# admin.site.register(MovieShots)
# admin.site.register(Actor)
# admin.site.register(Rating)
admin.site.register(RatingStar)
# admin.site.register(Reviews)