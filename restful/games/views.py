from django.contrib.auth.models import User
from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter
from django_filters.rest_framework import FilterSet
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, ListAPIView, \
    RetrieveAPIView
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from .models import Game, GameCategory, PlayerScore, Player
from .permissions import IsOwnerOrReadOnly
from .serializers import GameSerializer, GameCategorySerializer, PlayerScoreSerializer, PlayerSerializer, UserSerializer


class ApiRoot(GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        from rest_framework.reverse import reverse
        return Response({
            'players': reverse(PlayerList.name, request=request),
            'game-categories': reverse(GameCategoryList.name, request=request),
            'games': reverse(GameList.name, request=request),
            'scores': reverse(PlayerScoreList.name, request=request),
            'users': reverse(UserList.name, request=request)
        })


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class GameCategoryList(ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'

    # 뷰 실행전 스로틀 클래스 점검을 하고,
    # 실패하면(요청이 초과하면) 예외가 발생해 뷰를 실행하지 않는다
    # 스로틀 점검 정보는 캐시에 저장된다
    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)

    filter_fields = ('name',)  # 필터링할 수 있는 필드 이름
    search_fields = ('^name',)  # 텍스트 타입 필드. ^ 는 시작 부분 일치로 제한
    ordering_fields = ('name',)  # 결과 정렬에 사용할 수 있는 필드. 지정하지 않으면 뷰 모델의 기본 정렬 필드 사용,


class GameCategoryDetail(RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'

    throttle_scope = 'game-categories'
    throttle_classes = (ScopedRateThrottle,)


class GameList(ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'

    filter_fields = ('name', 'game_category', 'release_date', 'played', 'owner',)
    search_fields = ('^name',)
    ordering_fields = ('name', 'release_date',)

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    # 소유자로 request.user 를 전달하는데,
    # permission_classes 를 통과할 경우에만 게임 생성
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GameDetail(RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )


class PlayerList(ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'

    filter_fields = ('name', 'gender',)
    search_fields = ('^name',)
    ordering_fields = ('name',)


class PlayerDetail(RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


class PlayerScoreFilter(FilterSet):
    # score 보다 크거나 같은 값 필터링
    min_score = NumberFilter(field_name='score', lookup_expr='gte')
    # score 보다 작거나 같은 값 필터링
    max_score = NumberFilter(field_name='score', lookup_expr='lte')
    from_score_date = DateTimeFilter(field_name='score_date', lookup_expr='gte')
    to_score_date = DateTimeFilter(field_name='score_date', lookup_expr='lte')
    # 필터가 적용되는 필드인 player 의 name 필드.
    # 플레이어 이름인 지정 문자열 값과 일치하는 점수 필터링
    # AllValuesFilter 이기 때문에 점수가 등록된 플레이어만 검색 가능
    player_name = AllValuesFilter(field_name='player__name')
    game_name = AllValuesFilter(field_name='game__name')

    class Meta:
        model = PlayerScore
        fields = '__all__'


class PlayerScoreList(ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'

    filter_class = PlayerScoreFilter
    ordering_fields = (
        'score',
        'score_date',
    )


class PlayerScoreDetail(RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'
