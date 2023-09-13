from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from profiles.validators import validate_professor, validate_student


# Create your models here.
class Professor(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        validators=[validate_professor],
    )
    title_prefix = models.CharField(_("title prefix"), max_length=8, blank=True)
    title_suffix = models.CharField(_("title suffix"), max_length=16, blank=True)

    def __str__(self):
        return " ".join(
            [self.user.first_name, self.user.middle_name, self.user.last_name]
        )


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
        validators=[validate_student],
    )
    GENDER_CHOICES = [("M", _("Male")), ("F", _("Female"))]
    gender = models.CharField(_("gender"), max_length=1, choices=GENDER_CHOICES)
    weight = models.FloatField(
        _("weight (kg)"),
        blank=True,
        validators=[MinValueValidator(0.0, _("Weight must be a positive number."))],
    )
    height = models.FloatField(
        _("height (cm)"),
        blank=True,
        validators=[MinValueValidator(0.0, _("Height must be a positive number."))],
    )

    def __str__(self):
        return " ".join(
            [self.user.first_name, self.user.middle_name, self.user.last_name]
        )


class Department(models.Model):
    title = models.CharField(_("college department"), max_length=64, unique=True)

    def __str__(self):
        return self.title


class Program(models.Model):
    title = models.CharField(_("program title"), max_length=128, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Course(models.Model):
    code = models.CharField(_("course code"), max_length=16, unique=True)
    title = models.CharField(_("course title"), max_length=64, unique=True)
    units = models.FloatField()
    corequisites = models.ManyToManyField("self", symmetrical=True, blank=True)
    prerequisites = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.title


class Curriculum(models.Model):
    title = models.CharField(_("curriculum title"), max_length=128, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course, "CurriculumCourse")

    def __str__(self):
        return self.title


class CurriculumCourse(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["curriculum", "course"],
                name="unique curriculum and course combination",
            )
        ]

    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    YEAR_LEVELS = [
        (1, _("1st year")),
        (2, _("2nd year")),
        (3, _("3rd year")),
        (4, _("4th year")),
        (5, _("5th year")),
    ]
    year_level = models.IntegerField(choices=YEAR_LEVELS)
    ACADEMIC_TERMS = [(1, _("1st semester")), (2, _("2nd semester")), (3, _("Summer"))]
    academic_term = models.IntegerField(choices=ACADEMIC_TERMS)

    def __str__(self):
        return " | ".join([self.curriculum.__str__(), self.course.__str__()])
