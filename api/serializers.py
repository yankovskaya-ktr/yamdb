import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Регистрация с таким username запрещена')
        return value


class MeSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]

    )
    username = serializers.CharField(
        max_length=200,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Регистрация с таким username запрещена')
        return value


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, required=True)
    confirmation_code = serializers.CharField(required=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=None)

    class Meta:
        model = Review
        read_only_fields = ('author', 'title')
        fields = '__all__'

    def validate_score(self, value):
        if not (0 < value <= 10):
            raise serializers.ValidationError(
                'Оценка должна быть целым числом'
                ' в диапазоне от 1 до 10'
            )
        return value

    def validate(self, data):
        request = self.context['request']
        title_id = request.parser_context['kwargs']['title_id']
        title = get_object_or_404(Title, pk=title_id)
        if (request.method == 'POST'
                and title.reviews.filter(author=request.user).exists()):
            raise ValidationError('На произведение можно'
                                  ' оставить только 1 отзыв')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.HiddenField(default=None)

    class Meta:
        fields = '__all__'
        read_only_fields = ('author', 'review')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Title-Сериализатор для dont_safe методов"""
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(many=True, slug_field='slug',
                                         queryset=Genre.objects.all())

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        """Проверка на указание года больше текущего."""
        if value > dt.datetime.now().year:
            raise ValidationError('Год выпуска не может быть больше текущего')
        return value


class TitleSerializerGet(serializers.ModelSerializer):
    """Title-Сериализатор для метода GET."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = '__all__'
