from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APITestCase

from .models import GameCategory, Player


# python manage.py test -v 2  | -v 2 입력시 테스트러너가 수행중인 모든 작업출력
# coverage report -m  | missing 명령문의 행 표시
# coverage html

class GameCategoryTests(APITestCase):
    def create_game_category(self, name):
        url = reverse('gamecategory-list')
        data = {'name': name}
        response = self.client.post(url, data, format='json')
        return response

    def test_create_and_retrieve_game_category(self):
        new_game_category_name = 'new game cat'
        response = self.create_game_category(new_game_category_name)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GameCategory.objects.count(), 1)
        self.assertEqual(GameCategory.objects.get().name, new_game_category_name)
        print("PK {0}".format(GameCategory.objects.get().pk))

    def test_create_duplicated_game_category(self):
        new_game_category_name = 'new game cat'
        response1 = self.create_game_category(new_game_category_name)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        response2 = self.create_game_category(new_game_category_name)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_game_categories_list(self):
        # given
        new_game_category_name = 'new game cat'
        self.create_game_category(new_game_category_name)
        # when
        url = reverse('gamecategory-list')
        response = self.client.get(url, format='json')
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], new_game_category_name)

    def test_update_game_category(self):
        # given
        new_game_category_name = 'initial name'
        response = self.create_game_category(new_game_category_name)
        url = reverse('gamecategory-detail', None, {response.data['pk']})  # pk 를 포함한 url 가져오기
        # when
        updated_game_category_name = 'updated name'
        data = {'name': updated_game_category_name}
        patch_response = self.client.patch(url, data, format='json')
        # then
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data['name'], updated_game_category_name)

    def test_filter_game_category_by_name(self):
        # given
        game_category_name1 = 'first game cat'
        self.create_game_category(game_category_name1)
        game_category_name2 = 'second game cat'
        self.create_game_category(game_category_name2)
        # when
        filter_by_name = {'name': game_category_name1}
        url = '{0}?{1}'.format(reverse('gamecategory-list'), urlencode(filter_by_name))  # dict 데이터 url 에 encoding
        response = self.client.get(url, format='json')
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], game_category_name1)


class PlayerTest(APITestCase):
    def create_player(self, name, gender):
        url = reverse('player-list')
        data = {'name': name, 'gender': gender}
        response = self.client.post(url, data, format='json')
        return response

    def test_create_and_retrieve_player(self):
        # given
        new_player_name = 'player'
        new_player_gender = Player.MALE
        # when
        response = self.create_player(new_player_name, new_player_gender)
        # then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(Player.objects.get().name, new_player_name)

    def test_create_duplicated_player(self):
        # given
        new_player_name = 'player'
        new_player_gender = Player.MALE
        # when
        response1 = self.create_player(new_player_name, new_player_gender)
        response2 = self.create_player(new_player_name, new_player_gender)
        # then
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_players_list(self):
        # given
        new_player_name = 'player'
        new_player_gender = Player.MALE
        self.create_player(new_player_name, new_player_gender)
        # when
        url = reverse('player-list')
        response = self.client.get(url, format='json')
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], new_player_name)
        self.assertEqual(response.data['results'][0]['gender'], new_player_gender)
