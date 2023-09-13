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

    def make_subscriptions(self, subscriptions: dict) -> Subscriptions:
        """
        Создание подписки. Данные должны быть в словаре вида:
        {
            'chat_id': chat_id: int,
            'theme': tag_id: int,
            'contest': contest_name: str,
            'rating': rating: int | None
        }
        """
        chat_id = subscriptions.get('chat_id')
        tag_id = subscriptions.get('theme')
        contest = subscriptions.get('contest')
        rating = subscriptions.get('rating')
        print("rating=", rating)

        # проверяем, есть ли пользователь с таким id в базе и добавляем, если нет
        if not User.objects.filter(chat_id=chat_id).exists():
            user = User.objects.create(chat_id=chat_id)
        else:
            user = User.objects.get(chat_id=chat_id)
        print("user=", user, "tag=", tag_id, "contest=", contest, "rating=", rating)
        tag = Tags.objects.get(id=tag_id)
        contest_id = Contest.objects.get(name=contest)

        # Проверить, что такая подписка существует

        # subs = self.test_creator.get_all_subscriptions(chat_id=TEST_USER_ID)

        if rating:
            data = {
                    "user":user,
                    "tag": tag,
                    "contest": contest_id,
                    "rating": int(rating),
                    "is_active": True
            }
            try:
                new_sub = Subscriptions.objects.create(
                    # data)
                    user=user,
                    tag=tag,
                    contest=contest_id,
                    rating=int(rating),
                    is_active=True
                    )
                return new_sub
            except Exception as error:
                print("Ошибка создания подписки ", error)
        else:
            try:
                new_sub = Subscriptions.objects.create(
                    user=user,
                    tag=tag,
                    contest=contest_id,
                    is_active=True
                    )
                return new_sub
            except Exception as error:
                print("Ошибка создания подписки ", error)

    def check_subscriptions(self, subscriptions: dict) -> bool:
        """
        проверить правильность задания атрибутов подписки
        rating - необязательное поле
        """
        tag = subscriptions.get('theme')
        contest = subscriptions.get('contest')
        rating = subscriptions.get('rating')
        sub_is_correct = True
        if not tag or not contest:
            sub_is_correct = False
        if tag and not Tags.objects.filter(id=int(tag)).exists():
            sub_is_correct = False
        if rating and rating not in self.get_all_rating():
            sub_is_correct = False
        if contest and not Contest.objects.filter(name=contest).exists():
            sub_is_correct = False
        return sub_is_correct

    def get_sub_from_str(self, text: str) -> dict:
        """
        находим в строке ключевые слова и заполняем словарь полученными значениями
        """
        list_sub = text.split(' ')[1:]
        subscriptions = {}

        # Проверка наличия ключевых слов
        if "тема" in list_sub and len(list_sub) > list_sub.index("тема") + 1:
            subscriptions['theme'] = list_sub[list_sub.index("тема") + 1]
        if 'уровень' in list_sub and len(list_sub) > list_sub.index("уровень") + 1:
            subscriptions['contest'] = list_sub[list_sub.index("уровень") + 1]
        if 'рейтинг' in list_sub and len(list_sub) > list_sub.index("рейтинг") + 1:
            subscriptions['rating'] = list_sub[list_sub.index("рейтинг") + 1]
        return subscriptions

    def get_all_subscriptions(self, chat_id: int):
        """
        получить все подписки пользователя
        """
        subs = Subscriptions.objects.filter(user__chat_id=chat_id)
        return subs

    def del_all_subscriptions(self, chat_id: int):
        """
        удалить все подписки пользователя
        """
        subs = Subscriptions.objects.filter(user__chat_id=chat_id)
        subs.delete()
        return subs

    def get_all_tags_for_problem(self, problem):
        task_id = problem.id

        task = Problems.objects.get(id=task_id)
        tags = task.tags.all()

        for tag in tags:
            print(tag)

    def get_problems_by_tag(self, tag='geometry', contest=None, number=5):
        # выбираем задачи с данным тэгом
        if contest:
            problems = Problems.objects.filter(tags__name=tag, contest__name=contest).order_by('?')[:number]
        else:
            problems = Problems.objects.filter(tags__name=tag).order_by('?')[:number]
            #.exclude(sendedproblems__isnull=False)  # Исключение уже отправленных задач
        return problems
