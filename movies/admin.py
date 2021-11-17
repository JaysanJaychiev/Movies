from django.contrib import admin
from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews
from django.utils.safestring import mark_safe
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

class MovieAdminForm(forms.ModelForm):
    """ФОРМ-Виджет в админке для редактирование описания"""
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Movie
        fields = "__all__"




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    # list_display указывем какие поля нужно вывести
    list_display_links = ("name",)
    # Текущее поле становится ссылкой


#ReviewInlines для модели Movie выводит внизу привязанные отзывы 
class ReviewInlines(admin.StackedInline):
    # admin.StackedInline, вертикально в разные строки
    # admin.TabularInline, горизонтально в одну строку
    """Отзывы на стрнице фильмы"""
    model = Reviews
    # model указываем модель
    extra = 1
    # extra указываем количесто пустых форм для отзывов
    readonly_fields = ("name", "email") 
    # readonly_fields поля которые можно изменить делает только для чтения


class MovieShotsInline(admin.StackedInline):
    # admin.StackedInline, вертикально в разные строки
    # admin.TabularInline, горизонтально в одну строку
    model = MovieShots
    # model указываем модель
    extra = 1
    # extra указываем количесто пустых форм для отзывов
    readonly_fields = ("get_image", )
    # выводит изображение при изменении

    # возвращает изображение вместо ссылки
    def get_image(self, obj):
        # from django.utils.safestring import mark_safe
        return mark_safe(f'<img src={obj.image.url} width="200" height="200"')

    get_image.short_description = "Изображение"
    # переименовывает поле get_image на "Изображение"



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Филмы"""
    list_display = ("title", "category", "url", "draft")
    # list_display указывем какие поля нужно вывести
    list_filter = ("category", "year")
    # фильтрация по полям
    search_fields = ("title", "category__name")
    # поиск по полям
    inlines = [MovieShotsInline, ReviewInlines]
    # inlines для вывода полей
    # ReviewInlines - Отзывы
    # MovieShotsInline - Кадры из фильма
    save_on_top = True
    # save_on_top выводит панель для сохранения сверху тоже и внизу по умолчанию
    save_as = True
    # чтобы текущий detail сохранить как новый обьект
    list_editable = ("draft",)
    # list_editable задать поле которую можно редактировать на месте
    # fields = (("actors",'directors', "genres"), )
    # в Форме остаются только нужные поля
    actions = ['publish', 'unpublish']
    # actions передаем и региструруем наши экшины
    form = MovieAdminForm
    # для вывода виджет форм
    readonly_fields = ("get_image",)
    # выводит изображение при изменении
    fieldsets = (
        # fieldsets группировка полей на свое усмотрение
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
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
    # возвращает изображение вместо ссылки
    def get_image(self, obj):
        # from django.utils.safestring import mark_safe
        return mark_safe(f'<img src={obj.poster.url} width="auto" height="200"')


    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        # обновляем поле draft и ставим значение true
        if row_update == 1:
        # проверка обновили одну запись или несколько
            message_bit = "1 запись была обнавлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")
        # В request передаем сообщение для вывода в админке
    

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
         # обновляем поле draft и ставим значение false
        if row_update == 1:
        # проверка обновили одну запись или несколько
            message_bit = "1 запись была обнавлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")
        # В request передаем сообщение для вывода в админке
    
    publish.short_description = "Опубликовать"
    # переименовываем поле на "Опубликовать"
    publish.allowed_permission = ("change", )
    # "Права на доступ"


    unpublish.short_description = "Снять с публикации"
    # переименовываем поле на "Снять с публикации"
    unpublish.allowed_permission = ("change", )
    # "Права на доступ"

    get_image.short_description = "Постер"
    # переименовывает поле get_image на "Изображение"



@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """ Отзывы"""
    list_display =  ("name", "email", "parent", "movie", "id")
    # list_display указывем какие поля нужно вывести
    readonly_fields = ('name', "email")
    # readonly_fields поля которые можно изменить делает только для чтения
    


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")
    # list_display указывем какие поля нужно вывести


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_image")
    # list_display указывем какие поля нужно вывести
    readonly_fields = ("get_image", )
    # выводит изображение при изменении

    # возвращает изображение вместо ссылки
    def get_image(self, obj):
        # from django.utils.safestring import mark_safe
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"
    # переименовывает поле get_image на "Изображение"
 


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "movie", "ip")
    # list_display указывем какие поля нужно вывести


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фиьма"""
    list_display = ("title", "movie", "get_image")
    # list_display указывем какие поля нужно вывести
    readonly_fields = ("get_image", )
    # readonly_fields поля которые можно изменить делает только для чтения
    def get_image(self, obj):
        # from django.utils.safestring import mark_safe
        return mark_safe(f'<img src={obj.image.url} width="auto" height="100"')
    get_image.short_description = "Изображение"
    # переименовывает поле get_image на "Изображение"

###всех закоментили потомучто использовали декоратор @admin.register(Category, и.т.д)
# admin.site.register(Category, CategoryAdmin)  
# admin.site.register(Genre)
# admin.site.register(Movie)
# admin.site.register(MovieShots)
# admin.site.register(Actor)
# admin.site.register(Rating)
admin.site.register(RatingStar)
# admin.site.register(Reviews)


admin.site.site_title = "Django Movies"
# Переименовывает заголовок 
admin.site.site_header = "Django Movies"

