from parsing.models import Tags, Problems
from parsing.models import Course, Student


"""
graphs
greedy
dp
math
matrices
combinatorics
constructive algorithms
implementation
data structures
sortings
bitmasks
games
probabilities
strings
trees
brute force
number theory
dfs and similar
binary search
flows
geometry
shortest paths
divide and conquer
dsu
interactive
two pointers
fft
hashing
ternary search
2-sat
meet-in-the-middle
graph matchings
string suffix structures
*special
expression parsing
chinese remainder theorem
schedules
"""


class GetProblems:
    def get_problems_by_tag(tag):
        tag ='trees'
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

        # print("tom=", tom)
        # print("courses=", courses)
        # print("students=", students)
        # tags = Tags.objects.get(name=tag)
        # problems = tags.problem.all()

        # print("tags=", tags)
        # print('problems=', problems, len(problems))
        # # new_problems = Tags.objects.filter(name=tag)
        # new_problems = Tags.objects.get(id=1).problem.all()
        # print('new_problems=', new_problems, len(new_problems))
        # for problem in new_problems:
        #     print("problem.name=", problem.name)
        k = Problems.objects.filter(tags__name=tag)
        print("k=", k)


        # problems = tags.problem.all()


        # problem = Problems.objects.get(id=1)  # замените 1 на нужный вам id задачи
        # tag_count = problem.tags.count()

        # tags = Tags.objects.get(name="strings")
        # problems = tags.problem.all()

        # if problems.count() > 0:
        #     print("Связь ManyToMany существует")

        #     # Выводим задачи по заданному тегу
        #     for problem in problems:
        #         print(problem.name)
        # else:
        #     print("Связь ManyToMany не существует")

        # if tag_count == 1:
        #     # У задачи только один тэг
        #     print("Задача имеет только один тэг")
        # else:
        #     # У задачи больше одного тэга
        #     print("Задача имеет более одного тэга")



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
