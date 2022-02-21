# Проект YaMDb  
  
**Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title).
На основе отзывов формируется рейтинг произведения.
Произведения делятся на категории (Category): «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр (Genre)**  

![Workflow](https://github.com/yankovskaya-ktr/yamdb/actions/workflows/yamdb_workflow.yml/badge.svg)

После запуска проекта документация доступна по адресу: localhost/redoc/

### Технологии:

Python 3.7, Django 3.0.5, Django REST framework 3.12.4, Simple JWT, PostgreSQL, Docker, Gunicorn, Nginx

### Запуск проекта:
  
Клонировать репозиторий и перейти в него:  
  
```  
git clone https://github.com/yankovskaya-ktr/yamdb.git
cd yamdb
``` 

Создать файл .env по шаблону .env.template:

```
cp .env.template .env
```
Запустить приложение:

``` 
docker-compose up
``` 
Провести миграции:

``` 
docker-compose exec web python manage.py migrate --noinput
``` 

Создать суперпользователя:

``` 
docker-compose exec web python manage.py createsuperuser
``` 

Импортировать данные из CSV в базу данных:  
  
```  
docker-compose exec web python manage.py import_from_csv <csv_файл> <имя_модели>    
```  

  
### Алгоритм регистрации пользователей:  
  
1. Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.  
2. YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.  
3. Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответ на запрос приходит token (JWT-токен).  
4. При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле (описание полей — в документации).  
  
### Пользовательские роли:  
  
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.  
- **Аутентифицированный пользователь (user)** — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.  
- **Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.  
- **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.  
- **Суперюзер Django** — обладет правами администратора (admin)  
  
### Аутентификация:  
  
используется аутентификация по JWT-токену
  
### Ресурсы API YaMDb  
  
base path: /api/v1
  
## AUTH (аутентификация):  
  
 а) Регистрация нового пользователя (auth/signup/): - POST - (Доступно без токена) *Получить код подтверждения на переданный email.  
*использовать имя 'me' в качестве username запрещено.  
*Поля email и username должны быть уникальными.  
  
 а) Регистрация нового пользователя (auth/token/): - POST - (Доступно без токена) *Получение JWT-токена в обмен на username и confirmation code.  
  
## users (пользователи):  
  
 а) List (users/): - GET - (только Администратор) - POST - (только Администратор)
 
 b) retrieve (users/{username}/):  
 - GET - (только Администратор) - PPD - (только Администратор)    
 - GET -  (только Аутентифицированный пользователь) - PPD -  (только Аутентифицированный пользователь)  

## categories (типы произведений):  
  
 а) List (categories/): - GET - любой (в т.ч. и Аноним) - POST - (только Администратор) 
 *Поле slug каждой категории должно быть уникальным  
     
 b) retrieve (categories/{slug}/): - GET - ? - D - (только Администратор)  

## genres (жанры произведений):  
  
 а) List (genres/): - GET - любой (в т.ч. и Аноним) - POST - (только Администратор) 
 *Поле slug каждой категории должно быть уникальным  
     
 b) retrieve (genres/{slug}/): - GET - ? - D - (только Администратор)  

## titles (произведения):  
  
 а) List (titles/): - GET - любой (в т.ч. и Аноним) - POST - (только Администратор) 
*Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).  
*При добавлении нового произведения требуется указать уже существующие категорию и жанр.     
     
 b) retrieve (titles/{title_id}/): - GET - любой (в т.ч. и Аноним) - PPD - (только Администратор)  ## reviews (отзывы на произведения):  
  
 а) List(titles/{title_id}/reviews/): - GET - любой (в т.ч. и Аноним) - POST - (только Аутентифицированный пользователь)
 *Пользователь может оставить только один отзыв на произведение.  
     
 b) retrieve (titles/{title_id}/reviews/{review_id}/): - GET - любой (в т.ч. и Аноним) - PPD - (Автор отзыва, Модератор, Администратор)  
  
## comments (комментарии к отзывам):  
  
 а) List (titles/{title_id}/reviews/{review_id}/comments/): - GET - любой (в т.ч. и Аноним) - POST - (только Аутентифицированный пользователь)
 
 b) retrieve (titles/{title_id}/reviews/{review_id}/comments/{comment_id}/):  
 - GET - любой (в т.ч. и Аноним) - PPD - (Автор комментария, Модератор, Администратор)  

