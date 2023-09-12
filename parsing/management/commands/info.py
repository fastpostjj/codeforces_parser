from django.core.management import BaseCommand
from parsing.models import Problems, Tags, Contest
from parsing.services.services import GetProblems
from parsing.services.codeforces_parser import CodeforcesParser
from parsing.services.message_creator import MessageCreator


class Command(BaseCommand):
    def handle(self, *args, **options):
        problems = Problems.objects.all().count()
        tags = Tags.objects.all().count()
        print(f"Всего задач: {problems}, всего тэгов: {tags}")


        pr = GetProblems().get_problems_by_tag(tag='geometry', contest="Уровень 6")
        # print(GetProblems.get_all_rating())
        for p in pr:
            print(p, p.get_url())
        # parser = CodeforcesParser()
        # parser.set_contest_level()

        msg = MessageCreator()
        contest=Contest.objects.get(name="Уровень 6")
        tags = Tags.objects.all()
        contests = Contest.objects.all()
        counter = 0
        tag = Tags.objects.get(name="graph matchings")
        for tag in tags:
        # for contest in contests:
            # problems1 = Problems.objects.filter(tags__name="graph matchings").count()
            # problems = Problems.objects.filter(tags__name="graph matchings", contest=contest).count()
            # problems = Problems.objects.filter(contest=contest).count()
            pr = GetProblems().get_problems_by_tag(tag=tag, contest="Уровень 6")
            print("contest=", contest, " tag=", tag, pr.count())
            # print(GetProblems.get_all_rating())
            for p in pr:
                print(p, p.get_url())
            counter += pr.count()
        print("counter=", counter)

            # problems = msg.make_problems_for_send(
            #     tags=tag,
            #     contest=contest,
            # #     rating=800
            # ).count()
            # print("tag=", tag, " problems=", problems)
        # msg.make_text(problems)
