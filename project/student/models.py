from django.db import models

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=150, verbose_name="Факультет")

    def __str__(self):
        return self.faculty_name

class Group(models.Model):
    group_name = models.CharField(max_length=100, verbose_name="Группа")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='groups')

    def __str__(self):
        return self.group_name

class Student(models.Model):
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    patronymic = models.CharField(max_length=100, blank=True, null=True, verbose_name="Отчество")
    birth_date = models.DateField(verbose_name="Дата рождения")
    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Мужской'), ('F', 'Женский')],
        verbose_name="Пол"
    )
    phone_number = models.CharField(max_length=20, verbose_name="Телефон")
    course = models.PositiveSmallIntegerField(verbose_name="Курс")
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, related_name='students')
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name='students')

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic or ''}".strip()
