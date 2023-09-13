from django.test import TestCase
from parsing.models import Subscriptions, Problems, Tags, Contest
from parsing.services.services import GetProblems
from parsing.services.bot_message import Bot_message
from parsing.services.message_creator import MessageCreator, send_messages
from parsing.services.codeforces_parser import CodeforcesParser
from config.settings import URL, URL_PROBLEM, LOG_FILE
import requests
import json
import os
from django.utils import timezone
from parsing.models import Problems, Tags, Contest


TEST_USER_ID = 1
data1 = {
    'name': 'Mighty Rock Tower',
    'index': 'M',
    'points': 0,
    'rating': 800,
    'contestId': 1866,
    'type': 'PROGRAMMING',
    'solved_count': 322,
    'tags': ['brute force', 'combinatorics', 'dp', 'math', 'probabilities']}
data2 = {
    'name': 'Lihmuf Balling', 'index': 'L', 'points': 0, 'rating': 2800, 'contestId': 1866, 'type': 'PROGRAMMING', 'solved_count': 418, 'tags': ['binary search', 'brute force', 'math']}
# , 'contest': '<Contest: Уровень 3>'}
data3 = {
    'name': 'Keen Tree Calculation',
    'index': 'K',
    'points': 0,
    'rating': 3200,
    'contestId': 1866,
    'type': 'PROGRAMMING',
    'solved_count': 241,
    'tags': ['binary search', 'data structures', 'dp', 'geometry', 'graphs', 'implementation', 'trees']}
    # ,    'contest': '<Contest: Уровень 3>'}


class TestGetProblems(TestCase):
    def setUp(self):
        self.test_creator = GetProblems()
        self.parser = CodeforcesParser()
        CodeforcesParser().create_contests()
        data1['contest'] = Contest.objects.get(name="2")
        data2['contest'] = Contest.objects.get(name="3")
        self.parser.problem1 = self.parser.create_problem(data1)
        self.parser.problem2 = self.parser.create_problem(data2)

    def test_get_all_tags(self):
        """
        получаем все тэги
        """
        count_tag = self.test_creator.get_all_tags().count()
        self.assertEqual(count_tag, 6)

    def test_get_all_levels(self):
        """
        получаем все контесты (уровни)
        """
        count_levels = self.test_creator.get_all_levels().count()
        self.assertEqual(count_levels, 7)

    def test_get_all_rating(self):
        """
        получаем все уникальные значения рейтига
        """
        count_rating = self.test_creator.get_all_rating().count()
        self.assertEqual(count_rating, 2)

    def test_get_sub_from_str(self):
        text1 = "/subscribe тема 1 уровень 2 рейтинг 4"
        data1 = self.test_creator.get_sub_from_str(text1)
        self.assertEqual(data1, {'theme': '1', 'contest': '2', 'rating': '4'})

        text2 = "/subscribe"
        data2 = self.test_creator.get_sub_from_str(text2)
        self.assertEqual(data2, {})

        text3 = "/subscribe уровень 2 тема 1"
        data3 = self.test_creator.get_sub_from_str(text3)
        self.assertEqual(data3, {'theme': '1', 'contest': '2'})

    def test_check_subscriptions(self):
        """
        проверить правильность задания атрибутов подписки
        """
        tag = Tags.objects.all()[0].id
        subscriptions1 = {}

        # no keys - False
        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions1)
        self.assertFalse(is_correct)

        # all keys - True
        subscriptions1['theme'] = tag
        subscriptions1['rating'] = self.parser.problem1.rating
        subscriptions1['contest'] = self.parser.problem1.contest.name
        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions1)
        self.assertTrue(is_correct)

        # wrong tag - False
        subscriptions2 = {}
        subscriptions2['theme'] = 250387
        subscriptions2['rating'] = self.parser.problem1.rating
        subscriptions2['contest'] = self.parser.problem1.contest.name
        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions2)
        self.assertFalse(is_correct)

        # wrong rating - False
        subscriptions3 = {}
        subscriptions3['theme'] = tag
        subscriptions3['rating'] = 185634
        subscriptions3['contest'] = self.parser.problem1.contest.name
        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions3)
        self.assertFalse(is_correct)

        # wrong contest - False
        subscriptions4 = {}
        subscriptions4['theme'] = tag
        subscriptions4['rating'] = self.parser.problem1.rating
        subscriptions4['contest'] = "adsfb"
        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions4)
        self.assertFalse(is_correct)

        # no rating - True
        subscriptions5 = {}
        subscriptions5['theme'] = tag
        subscriptions5['contest'] = self.parser.problem1.contest.name
        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions5)
        self.assertTrue(is_correct)

        # no contest - False
        subscriptions6 = {}
        subscriptions6['theme'] = tag
        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions6)
        self.assertFalse(is_correct)

        # no tag - False
        subscriptions7 = {}
        subscriptions7['rating'] = self.parser.problem1.rating
        subscriptions7['contest'] = self.parser.problem1.contest.name
        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions7)
        self.assertFalse(is_correct)

    def test_get_all_subscriptions(self):
        """
        получить все подписки пользователя
        """
        subs_count = self.test_creator.get_all_subscriptions(chat_id=TEST_USER_ID).count()
        tag_id = Tags.objects.get(name='combinatorics').id
        contest = "3"
        test_data = {
            'chat_id': TEST_USER_ID,
            'theme': tag_id,
            'contest': contest,
            'rating': 800,
        }
        self.test_creator.make_subscriptions(test_data)
        new_subs_count = self.test_creator.get_all_subscriptions(chat_id=TEST_USER_ID).count()
        self.assertEqual(new_subs_count, subs_count + 1)

    def test_make_subscriptions(self):
        subscriptions = {}
        tag = Tags.objects.all()[0].id
        subscriptions['theme'] = tag
        subscriptions['rating'] = self.parser.problem1.rating
        subscriptions['contest'] = self.parser.problem1.contest.name
        subscriptions['chat_id'] = TEST_USER_ID

        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions)
        if is_correct:
            sub = self.test_creator.make_subscriptions(subscriptions=subscriptions)
        print(sub)



    """
    del_all_subscriptions
    get_all_tags_for_problem
    get_problems_by_tag
        """


class TestCodeforcesParser(TestCase):
    def setUp(self):
        self.GOOD_URL = URL
        self.BAD_URL = URL + "smth"
        self.parser = CodeforcesParser()
        CodeforcesParser().create_contests()
        self.test_problem1 = Problems.objects.create(
            name=data1['name'],
            index=data1['index'],
            contestId=data1['contestId'],
            solved_count=15
        )

    def test_get_solved_count(self):
        """
        проверяем количество решений задачи
        """
        problemstatistics = [
            {
                'contestId': 1866,
                'index': 'M',
                'solvedCount': 895
            },
            {
                'contestId': 629,
                'index': 'D',
                'solvedCount': 3658
            }
        ]
        solved = self.parser.get_solved_count(
            problemstatistics=problemstatistics,
            contestId=self.test_problem1.contestId,
            index=self.test_problem1.index
            )
        self.assertEqual(solved, 895)

    def test_get_contest_level(self):
        # Проверка для различных значений переменной solved
        self.assertEqual(self.parser.get_contest_level(5).name, "1")
        self.assertEqual(self.parser.get_contest_level(50).name, "2")
        self.assertEqual(self.parser.get_contest_level(200).name, "3")
        self.assertEqual(self.parser.get_contest_level(800).name, "4")
        self.assertEqual(self.parser.get_contest_level(5000).name, "5")
        self.assertEqual(self.parser.get_contest_level(50000).name, "6")
        self.assertEqual(self.parser.get_contest_level(150000).name, "7")

        # Проверка для граничных значений
        self.assertEqual(self.parser.get_contest_level(10).name, "1")
        self.assertEqual(self.parser.get_contest_level(100).name, "2")
        self.assertEqual(self.parser.get_contest_level(500).name, "3")
        self.assertEqual(self.parser.get_contest_level(1000).name, "4")
        self.assertEqual(self.parser.get_contest_level(10000).name, "5")
        self.assertEqual(self.parser.get_contest_level(100000).name, "6")
        self.assertEqual(self.parser.get_contest_level(1000000).name, "7")

    def test_set_contest_level(self) -> None:
        """
        заполнение поля contest
        """
        self.test_problem2 = Problems.objects.create(
            name=data2['name'],
            index=data2['index'],
            contestId=data2['contestId'],
            solved_count=443

        )
        self.parser.set_contest_level()
        number = Problems.objects.filter(contest__isnull=True).count()
        self.assertEqual(number, 0)

    def test_create_problem(self):
        count_problems = Problems.objects.all().count()
        count_tags = Tags.objects.all().count()
        contest = self.parser.get_contest_level(data3["solved_count"])
        data = {
                        "name": data3["name"],
                        "index": data3["index"],
                        "points": data3["points"],
                        "rating": data3["rating"],
                        "contestId": data3["contestId"],
                        "type": data3["type"],
                        "solved_count": data3["solved_count"],
                        "tags": data3["tags"],
                        "contest": contest,
                    }
        self.parser.create_problem(data)
        self.assertEqual(count_problems + 1, Problems.objects.all().count())
        self.assertEqual(count_tags + len(data3["tags"]), Tags.objects.all().count())


class TestCodeforcesParserAPI(TestCase):
    def setUp(self):
        self.GOOD_URL = URL
        self.BAD_URL = URL + "smth"
        self.parser = CodeforcesParser()
        self.test_problem1 = Problems.objects.create(
            name=data1['name'],
            index=data1['index'],
            contestId=data1['contestId'],
            solved_count=15
        )

    def test_get_data_from_site(self):
        response = self.parser.get_data_from_site()
        self.assertIsNotNone(response)

        self.parser.url = self.BAD_URL
        response = self.parser.get_data_from_site()
        self.assertIsNone(response)


class TestCodeforcesParserSaveLog(TestCase):
    def setUp(self):
        self.parser = CodeforcesParser()
        self.filename = "test_json.json"
        with open(self.filename, mode="w", encoding="utf-8") as file:
            file.write("")

    def test_save_log(self) -> None:
        self.parser.log_file_name = "testfile.txt"
        datetime_now = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        self.parser.save_log("test")
        expected_text = datetime_now + " test"
        with open(self.parser.log_file_name) as file:
            real_text = file.read()
        self.assertEqual(expected_text + '\n', real_text)

    def test_get_from_file(self):
        data = {
            'name': 'Test Problem',
            'index': 'A',
            'contestId': 1
        }

        with open(self.filename, mode="w", encoding="utf-8") as file:
            json.dump(data, file)

        result = self.parser.get_from_file(filename=self.filename)
        expected_result = {
            'name': 'Test Problem',
            'index': 'A',
            'contestId': 1
        }
        self.assertEqual(result, expected_result)

    def tearDown(self):
        try:
            os.remove(self.parser.log_file_name)
        except OSError as error:
            print(f"Ошибка при удалении файла: {self.parser.log_file_name}: {error}")

        try:
            os.remove(self.filename)
        except OSError as error:
            print(f"Ошибка при удалении файла {self.filename}: {error}")


class MessageCreatorTest(TestCase):

    def setUp(self):
        self.creator = MessageCreator()

    def test_make_text_for_send(self):
        contest = Contest.objects.create(
            name="Test contest",
            annotation="Test annotation"
        )
        problem1 = Problems.objects.create(
            name="name1",
            contestId=5674,
            index="A",
            points=10,
            rating=100,
            type_problem="Test type",
            solved_count=50,
            contest=contest
        )

        url = problem1.get_url()

        expected_text = "Задача 5674A name1. Сложность: 100, решений: 50, контест: Уровень" +\
            " Test contest\nhttps://codeforces.com/problemset/problem/5674/A\n"
        actual_text = self.creator.make_text_for_send(problem1)
        self.assertEqual(actual_text, expected_text)
        self.assertEqual(url, "https://codeforces.com/problemset/problem/5674/A")


# def create_contests():
#         """
#         создание уровней
#         """
#         try:
#             Contest.objects.get(name="1").exists()
#         except Contest.DoesNotExist:
#             Contest.objects.create(name="1")
#         try:
#             Contest.objects.get(name="2").exists()
#         except Contest.DoesNotExist:
#             Contest.objects.create(name="2")
#         try:
#             Contest.objects.get(name="3").exists()
#         except Contest.DoesNotExist:
#             Contest.objects.create(name="3")
#         try:
#             Contest.objects.get(name="4").exists()
#         except Contest.DoesNotExist:
#             Contest.objects.create(name="4")
#         try:
#             Contest.objects.get(name="5").exists()
#         except Contest.DoesNotExist:
#             Contest.objects.create(name="5")
#         try:
#             Contest.objects.get(name="6").exists()
#         except Contest.DoesNotExist:
#             Contest.objects.create(name="6")
#         try:
#             Contest.objects.get(name="7").exists()
#         except Contest.DoesNotExist:
#             Contest.objects.create(name="7")


if __name__ == '__main__':
    # создаем уровни
    CodeforcesParser().create_contests()
