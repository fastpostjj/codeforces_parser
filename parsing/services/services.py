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

    def get_all_subsriptions(self, chat_id: int):
        """
        получить все подписки пользователя
        """
        print("chat_id=", chat_id)
        subs = Subscriptions.objects.filter(user_id=chat_id)
        subs = Subscriptions.objects.all()
        return subs

    def del_all_subsriptions(self, chat_id: int):
        """
        удалить все подписки пользователя
        """
        subs = Subscriptions.objects.filter(user_id=chat_id)
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
