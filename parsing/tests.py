from django.test import TestCase
from parsing.models import Subscriptions, Problems, Tags, Contest
from parsing.services.services import GetProblems
from parsing.services.message_creator import MessageCreator
from parsing.services.codeforces_parser import CodeforcesParser
from config.settings import URL
import json
import os
from django.utils import timezone


TEST_USER_ID = 1
data1 = {
    'name': 'Mighty Rock Tower',
    'index': 'M',
    'points': 0,
    'rating': 800,
    'contestId': 1866,
    'type': 'PROGRAMMING',
    'solved_count': 322,
    'tags': ['brute force', 'combinatorics', 'dp', 'math', 'probabilities']
    }
data2 = {
    'name': 'Lihmuf Balling',
    'index': 'L',
    'points': 0,
    'rating': 2800,
    'contestId': 1866,
    'type': 'PROGRAMMING',
    'solved_count': 418,
    'tags': ['binary search', 'brute force', 'math']
    }
data3 = {
    'name': 'Keen Tree Calculation',
    'index': 'K',
    'points': 0,
    'rating': 3200,
    'contestId': 1866,
    'type': 'PROGRAMMING',
    'solved_count': 241,
    'tags': ['binary search', 'data structures', 'dp', 'geometry', 'graphs', 'implementation', 'trees']
    }
data4 = {
    'name': 'В поисках истины (простая версия).',
    'index': 'G1',
    'points': 0,
    'rating': 2200,
    'contestId': 1840,
    'type': 'PROGRAMMING',
    'solved_count': 1954,
    'tags': ['binary search', 'implementation', 'trees']
    }
data5 = {
    'name': 'В поисках истины (простая версия).new',
    'index': 'G1',
    'points': 0,
    'rating': 2500,
    'contestId': 1840,
    'type': 'PROGRAMMING',
    'solved_count': 1954,
    'tags': ['binary search', 'implementation', 'trees', 'geometry']
    }


class TestCodeforcesParser_create_contests(TestCase):
    def setUp(self):
        self.parser = CodeforcesParser()

    def test_create_contests(self):
        self.parser.create_contests()

        for i in range(1, 8):
            contest = Contest.objects.get(name=str(i))
            self.assertIsNotNone(contest)
            self.assertEqual(contest.name, str(i))

    def tearDown(self):
        # Очищаем базу данных после теста
        Contest.objects.all().delete()


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

        text4 = "/subscribe тема 31  уровень 4 рейтинг 800"
        data4 = self.test_creator.get_sub_from_str(text4)
        self.assertEqual(data4, {'theme': '31', 'contest': '4', 'rating': '800'})

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
        data3['contest'] = Contest.objects.get(name="4")
        self.parser.problem3 = self.parser.create_problem(data3)
        subscriptions3 = {}
        subscriptions3['theme'] = tag
        subscriptions3['rating'] = self.parser.problem3.rating
        subscriptions3['contest'] = self.parser.problem3.contest.name
        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions3)
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
        tag = Tags.objects.all()[0]
        tag_id = tag.id
        subscriptions['theme'] = tag_id
        subscriptions['contest'] = self.parser.problem1.contest.name
        subscriptions['chat_id'] = TEST_USER_ID

        # 1-й вариант без рейтинга
        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions)
        if is_correct:
            # self.assertEqual(sub.rating, None)
            sub = self.test_creator.make_subscriptions(subscriptions=subscriptions)
            self.assertEqual(sub.tag, tag)
            # self.assertEqual(sub.rating, subscriptions['rating'])
            self.assertEqual(sub.contest.name, subscriptions['contest'])
            self.assertEqual(sub.user.chat_id, TEST_USER_ID)
            sub.delete()

        # 2-й вариант с рейтингом
        subscriptions['rating'] = self.parser.problem1.rating
        is_correct = self.test_creator.check_subscriptions(subscriptions=subscriptions)
        if is_correct:
            self.assertEqual(sub.rating, None)
            sub = self.test_creator.make_subscriptions(subscriptions=subscriptions)
            self.assertEqual(sub.tag, tag)
            self.assertEqual(sub.rating, subscriptions['rating'])
            self.assertEqual(sub.contest.name, subscriptions['contest'])
            self.assertEqual(sub.user.chat_id, TEST_USER_ID)
            sub.delete()

    def test_del_all_subscriptions(self):
        subscriptions = {
            'chat_id': TEST_USER_ID,
            'theme': Tags.objects.all().order_by('id')[0].id,
            'contest': self.parser.problem1.contest.name,
            'rating': self.parser.problem1.rating
        }
        self.test_creator.make_subscriptions(subscriptions=subscriptions)
        self.test_creator.del_all_subscriptions(TEST_USER_ID)
        self.assertEquals(Subscriptions.objects.filter(user=TEST_USER_ID).count(), 0)

    def test_get_problems_by_tag(self):
        number = 5

        # Создаем тестовые тэги и задачи
        tag = "test_tag"
        problem_name = "test problem name"
        contest = Contest.objects.get(name=3)
        if not Tags.objects.filter(name=tag).exists():
            tag_instanсe = Tags.objects.create(
                name=tag
            )
        else:
            tag_instanсe = Tags.objects.get(name=tag)

        try:
            problem_instance = Problems.objects.get(contestId=1515, index="T")
        except Problems.DoesNotExist:
            problem_instance = Problems.objects.create(
                name=problem_name,
                contestId=1515,
                index="T",
                points=30,
                rating=None,
                type_problem="type_problem",
                solved_count=500,
                contest=contest
            )
            # Проверяем, есть ли уже связь между задачей и тэгом, если нет - создаем
        if problem_instance and problem_instance not in tag_instanсe.problem.all():
            tag_instanсe.problem.add(problem_instance)

        try:
            problem_instance = Problems.objects.get(contestId=1616, index="T")
        except Problems.DoesNotExist:
            problem_instance = Problems.objects.create(
                name="Test2 problem_name",
                contestId=1616,
                index="T",
                points=30,
                rating=700,
                type_problem="type_problem",
                solved_count=500,
                contest=contest
            )
            # Проверяем, есть ли уже связь между задачей и тэгом, если нет - создаем
        if problem_instance and problem_instance not in tag_instanсe.problem.all():
            tag_instanсe.problem.add(problem_instance)

        pr = self.test_creator.get_problems_by_tag(
            tag=tag,
            contest=contest.name,
            rating=700,
            number=number)
        self.assertEqual(pr.count(), 1)

        pr = self.test_creator.get_problems_by_tag(
            tag=tag,
            contest=contest.name,
            number=number)
        self.assertEqual(pr.count(), 2)


class Test_CodeforcesParser(TestCase):
    def setUp(self) -> None:
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

    def test_get_solved_count(self) -> None:
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

    def test_get_contest_level(self) -> None:
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

    def test_create_problem(self) -> None:
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

    def test_create_problem_no_tags(self):
        count_problems = Problems.objects.all().count()
        contest = self.parser.get_contest_level(data3["solved_count"])
        data = {
                        "name": data3["name"],
                        "index": data3["index"],
                        "points": data3["points"],
                        "rating": data3["rating"],
                        "contestId": data3["contestId"],
                        "type": data3["type"],
                        "solved_count": data3["solved_count"],
                        "tags": [],
                        "contest": contest,
                    }
        new_problem = self.parser.create_problem(data)
        self.assertEqual(new_problem.name, data['name'])
        self.assertEqual(new_problem.index, data['index'])
        self.assertEqual(new_problem.points, data['points'])
        self.assertEqual(new_problem.contestId, data['contestId'])
        self.assertEqual(new_problem.type_problem, data['type'])
        self.assertEqual(new_problem.solved_count, data['solved_count'])
        self.assertEqual(new_problem.contest, data['contest'])
        self.assertEqual(count_problems + 1, Problems.objects.all().count())

    def test_update_problem(self) -> None:
        data4['contest'] = self.parser.get_contest_level(data4['solved_count'])
        data5['contest'] = self.parser.get_contest_level(data5['solved_count'])

        test_update_problem = self.parser.create_problem(data4)

        test_update_problem_new = self.parser.update_problem(test_update_problem, data5)
        self.assertEqual(test_update_problem_new.name, data5['name'])
        self.assertEqual(test_update_problem_new.points, data5['points'])
        self.assertEqual(test_update_problem_new.rating, data5['rating'])
        self.assertEqual(test_update_problem_new.type_problem, data5['type'])
        self.assertEqual(test_update_problem_new.solved_count, data5['solved_count'])
        self.assertEqual(test_update_problem_new.contest, data5['contest'])


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
    def setUp(self) -> None:
        self.parser = CodeforcesParser()
        self.filename = "test_json.json"
        self.parser.log_file_name = "test_json.json"
        with open(self.filename, mode="w", encoding="utf-8") as file:
            file.write("")

    def test_save_log(self) -> None:
        self.parser.log_file_name = "testfile.log"
        datetime_now = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M:%S")
        self.parser.save_log("test")
        expected_text = datetime_now + " test"
        with open(self.parser.log_file_name, "r") as file:
            real_text = file.read()
        self.assertEqual(expected_text + '\n', real_text)
        try:
            os.remove(self.parser.log_file_name)
        except OSError as error:
            print(f"Ошибка при удалении файла {self.parser.log_file_name}: {error}")

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

    def tearDown(self) -> None:
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
