from django.core.exceptions import ValidationError
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
    permanent_address = models.CharField(_("permanent address"), max_length=128)
    current_address = models.CharField(_("current address"), max_length=128)
    emergency_number = models.CharField(_("emergency contact number"), max_length=16)

    def __str__(self):
        return " ".join(
            [
                self.user.first_name,
                self.user.middle_name,
                self.user.last_name,
                self.user.name_suffix,
            ]
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
        null=True,
        validators=[MinValueValidator(0.0, _("Weight must be a positive number."))],
    )
    height = models.FloatField(
        _("height (cm)"),
        blank=True,
        null=True,
        validators=[MinValueValidator(0.0, _("Height must be a positive number."))],
    )
    permanent_address = models.CharField(_("permanent address"), max_length=128)
    current_address = models.CharField(_("current address"), max_length=128)
    emergency_number = models.CharField(_("emergency contact number"), max_length=16)

    def __str__(self):
        return " ".join(
            [
                self.user.first_name,
                self.user.middle_name,
                self.user.last_name,
                self.user.name_suffix,
            ]
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
    year_level = models.IntegerField(_("year level"), choices=YEAR_LEVELS)
    ACADEMIC_TERMS = [(1, _("1st semester")), (2, _("2nd semester")), (3, _("Summer"))]
    academic_term = models.IntegerField(_("academic term"), choices=ACADEMIC_TERMS)

    def __str__(self):
        return " | ".join([self.curriculum.__str__(), self.course.__str__()])


class Section(models.Model):
    name = models.CharField(_("section name"), max_length=16, unique=True)
    STATUS = [(True, _("Open")), (False, _("Block"))]
    is_open = models.BooleanField(_("section status"), choices=STATUS)

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.CharField(_("room number"), max_length=16, unique=True)

    def __str__(self):
        return self.number


class Record(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "academic_year",
                    "academic_term",
                    "curriculum_course",
                    "section",
                ],
                name="unique academic year, academic term, curriculum course, and block section combination",
            )
        ]

    academic_year = models.IntegerField(_("academic year"))
    academic_term = models.IntegerField(
        _("academic term"), choices=CurriculumCourse.ACADEMIC_TERMS
    )
    curriculum_course = models.ForeignKey(CurriculumCourse, on_delete=models.CASCADE)
    advisor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    schedules = models.ManyToManyField(Room, "Schedule", blank=True)
    students = models.ManyToManyField(Student, "StudentRecord", blank=True)

    def __str__(self):
        return " | ".join(
            [
                str(self.academic_year),
                self.advisor.__str__(),
                self.curriculum_course.course.__str__(),
            ]
        )


class Schedule(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F("end_time")),
                name="start time before end time",
            )
        ]

    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    DAYS = [
        (1, _("Monday")),
        (2, _("Tuesday")),
        (3, _("Wednesday")),
        (4, _("Thursday")),
        (5, _("Friday")),
        (6, _("Saturday")),
        (7, _("Sunday")),
    ]
    day = models.IntegerField(_("day"), choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return "%s | %s | %s - %s" % (
            self.room.__str__(),
            self.DAYS[self.day - 1][1].__str__(),
            self.start_time,
            self.end_time,
        )

    def clean(self):
        try:
            self.room
            self.professor
            self.day
            self.start_time
            self.end_time
        except:
            return
        overlapping_room_schedules = Schedule.objects.filter(
            room=self.room,
            day=self.day,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )
        overlapping_professor_schedules = Schedule.objects.filter(
            professor=self.professor,
            day=self.day,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        )
        if self.pk:
            overlapping_room_schedules = overlapping_room_schedules.exclude(pk=self.pk)
            overlapping_professor_schedules = overlapping_professor_schedules.exclude(
                pk=self.pk
            )
        if (
            overlapping_room_schedules.exists()
            and overlapping_professor_schedules.exists()
        ):
            raise ValidationError(
                _(
                    "The chosen time frame conflicts with an existing room and professor schedule."
                )
            )
        if overlapping_room_schedules.exists():
            raise ValidationError(
                _("The chosen time frame conflicts with an existing room schedule.")
            )
        if overlapping_professor_schedules.exists():
            raise ValidationError(
                _(
                    "The chosen time frame conflicts with an existing professor schedule."
                )
            )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class StudentRecord(models.Model):
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=0, rating__lte=100)
                | models.Q(rating__isnull=True, remark__isnull=True),
                name="rating is between 0 and 100",
            ),
            models.CheckConstraint(
                check=models.Q(rating__gte=75, rating__lte=100, remark="PSD")
                | models.Q(rating__gt=0, rating__lt=75, remark="FLD")
                | models.Q(rating=0, remark="DRP")
                | models.Q(rating=0, remark="INC")
                | models.Q(rating__isnull=True, remark__isnull=True),
                name="rating match with remark",
            ),
        ]

    record = models.ForeignKey(Record, on_delete=models.CASCADE)
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    rating = models.FloatField(blank=True, null=True)
    REMARKS = [
        ("PSD", _("Passed")),
        ("FLD", _("Failed")),
        ("DRP", _("Dropped")),
        ("INC", _("Incomplete")),
    ]
    remark = models.CharField(
        _("remark"), max_length=3, blank=True, null=True, choices=REMARKS
    )

    def __str__(self):
        return self.student.__str__()
