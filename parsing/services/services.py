from parsing.models import Tags, Problems, Contest, Subscriptions
from user_auth.models import User


tag_list = [
    'graphs',
    'greedy',
    'dp',
    'math',
    'matrices',
    'combinatorics',
    'constructive algorithms',
    'implementation',
    'data structures',
    'sortings',
    'bitmasks',
    'games',
    'probabilities',
    'strings',
    'trees',
    'brute force',
    'number theory',
    'dfs and similar',
    'binary search',
    'flows',
    'geometry',
    'shortest paths',
    'divide and conquer',
    'dsu',
    'interactive',
    'two pointers',
    'fft',
    'hashing',
    'ternary search',
    '2-sat',
    'meet-in-the-middle',
    'graph matchings',
    'string suffix structures',
    '*special',
    'expression parsing',
    'chinese remainder',
    'schedules'
    ]
    # list_rating = [0, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400, 3500]


class GetProblems:
    def get_all_tags(self):
        """
        получаем все тэги
        """
        all_tags = Tags.objects.all()
        return all_tags

    def get_all_levels(self):
        """
        получаем все контесты (уровни)
        """
        all_contests = Contest.objects.order_by('name').all()
        return all_contests

    def get_all_rating(self):
        """
        получаем все уникальные значения рейтига
        """
        problems_rating = Problems.objects.order_by('rating').values_list('rating', flat=True).distinct()
        return problems_rating

    def make_subsriptions(self, chat_id: int) -> Subscriptions:
        """
        создать подписку
        """
        # проверяем, есть ли пользователь с таким id в базе и добавляем, если нет
        if not User.objects.filter(chat_id=chat_id).exists():
            user = User.objects.create(chat_id=chat_id)
        else:
            user = User.objects.get(chat_id=chat_id)
        try:
            new_sub = Subscriptions.objects.create(user=user, tag=1)
            return new_sub
        except Exception as error:
            print("Ошибка создания подписки ", error)

    def get_all_subsriptions(self, user_id: int):
        """
        получить все подписки пользователя
        """
        subs = Subscriptions.objects.filter(user=user_id)
        return subs

    def get_problems_by_tag(self, tag='geometry', rating=None):
        # выбираем все задачи с данным тэгом
        if rating:
            problems = Problems.objects.filter(tags__name=tag, rating=rating)
        # rating=2000
        else:
            problems = Problems.objects.filter(tags__name=tag)
            # problems = Problems.objects.filter(rating=rating)
        return problems
            # print("problems=", problems)
        # for problem in problems:
        #     print("problem=", problem, problem.get_url())
        #     # courses = Student.objects.get(id=1).courses.all()
        #     # для каждой задачи проверяем, сколько у нее тэгов
        #     tags = Tags.objects.filter(problem__id=problem.id)
        #     for one_tag in tags:
        #         tag_count = one_tag.problem.count()

        #         if tag_count == 1:
        #             # У задачи только один тэг
        #             print("Задача имеет только один тэг")
        #             print("problem=", problem, problem.get_url())
        #             print("one_tag=", one_tag, 'tag_count=', tag_count, "tags=", tags, "len(tags)=", len(tags))
        #         else:
        #             # У задачи больше одного тэга
        #             print("Задача имеет более одного тэга")
        #             print("problem=", problem, problem.get_url())
        #             print("one_tag=", one_tag, 'tag_count=', tag_count, "tags=", tags, "len(tags)=", len(tags))
        #             pass

    # def get_all_problems():
        # for tag in tag_list:
        # tag ='expression parsing'

        # создадим студента
        # tom = Student.objects.create(name="Tom")
        # tag = Tags.objects.create(name="Tom")
        # tag.problem.create(name="Tom", contestId=55000, index='Э')
        # p = Problems.objects.filter(tags__name=tag)

        # создадим один курс и добавим его в список курсов Тома
        # tom.courses.create(name="Algebra")

        # получим все курсы студента
        # courses = Student.objects.get(id=1).courses.all()

        # получаем всех студентов, которые посещают курс Алгебра
        # students = Student.objects.filter(courses__name="Algebra")

        # # new_problems = Tags.objects.filter(name=tag)
        # new_problems = Tags.objects.get(id=1).problem.all()

            # self.get_problems_by_tag(tag=tag)
            # k = Problems.objects.filter(tags__name=tag)
            # # print("k=", k)
            # for problem in k:
            #     # print("problem=", problem, problem.get_url())
            #     # courses = Student.objects.get(id=1).courses.all()
            #     tags = Tags.objects.filter(problem__id=problem.id)
            #     for one_tag in tags:
            #         tag_count = one_tag.problem.count()


            #         if tag_count == 1:
            #             # У задачи только один тэг
            #             print("Задача имеет только один тэг")
            #             print("problem=", problem, problem.get_url())
            #             print(one_tag, 'tag_count=', tag_count)
            #         else:
            #             # У задачи больше одного тэга
            #             # print("Задача имеет более одного тэга")
            #             pass



        # problems = Problems.objects.filter(name=tag)
        # problems = Problems.objects.all()[:5]
        # # print(problems)
        # # for problem in problems:
        # #     print(problem, problem.__dict__)
        # for tag in tags:
        #     print(tag, tag.__dict__)


    # from django.db import models

    # class Course(models.Model):
    #     name = models.CharField(max_length=30)

    # class Student(models.Model):
    #     name = models.CharField(max_length=30)
    #     courses = models.ManyToManyField(Course)

        # # создадим студента
        # tom = Student.objects.create(name="Tom")

        # # создадим один курс и добавим его в список курсов Тома
        # tom.courses.create(name="Algebra")

        # # получим все курсы студента
        # courses = Student.objects.get(name="Tom").courses.all()

        # # получаем всех студентов, которые посещают курс Алгебра
        # students = Student.objects.filter(courses__name="Algebra")
