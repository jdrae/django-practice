from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Game, GameCategory, PlayerScore, Player


class UserGameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = (
            'url',
            'name'
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    games = UserGameSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
            'games'
        )


# game = Game()
# game_ser = GameSerializer(game)
# print(game_ser.data) -> dict 형식으로
# renderer = JSONRenderer()
# game_rend = renderer.render(game_ser.data) -> JSON 형식으로

class GameCategorySerializer(serializers.HyperlinkedModelSerializer):
    # 카테고리에 속한 각 게임에 대한 하이퍼링크 배열 제공
    games = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='game-detail'  # 하이퍼링크를 클릭하면 게임 세부사항 뷰 제공
    )

    class Meta:
        model = GameCategory
        fields = (
            'url',
            'pk',
            'name',
            'games'
        )


class GameSerializer(serializers.HyperlinkedModelSerializer):
    # 게임을 생성하면 소유자가 자동으로 채워지고, 변경할 수 없으므로 readonly
    owner = serializers.ReadOnlyField(source='owner.username')
    # 카테고리의 이름만
    game_category = serializers.SlugRelatedField(queryset=GameCategory.objects.all(), slug_field='name')

    class Meta:
        model = Game
        # id 값 대신 json 객체를 여러개 포함할 수 있도록 ?
        depth = 4
        fields = (
            'url',
            'owner',
            'game_category',
            'name',
            'release_date',
            'played'
        )


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    # 게임에 대한 모든 정보
    game = GameSerializer()

    # 점수가 player 에 표시될 것이기 때문에 여기에 player 를 추가하지 않는다
    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_date',
            'game',
        )


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    scores = ScoreSerializer(many=True, read_only=True)

    gender = serializers.ChoiceField(choices=Player.GENDER_CHOICES)
    gender_description = serializers.CharField(
        source='get_gender_display',  # source 규칙 get_ + gender + _display
        read_only=True
    )

    class Meta:
        model = Player
        fields = (
            'url',
            'name',
            'gender',
            'gender_description',
            'scores',
        )


class PlayerScoreSerializer(serializers.ModelSerializer):
    player = serializers.SlugRelatedField(queryset=Player.objects.all(), slug_field='name')
    game = serializers.SlugRelatedField(queryset=Game.objects.all(), slug_field='name')

    class Meta:
        model = PlayerScore
        fields = (
            'url',
            'pk',
            'score',
            'score_date',
            'player',
            'game',
        )
