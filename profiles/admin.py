from django.contrib import admin
from accounts.models import CustomUser
from .models import (
    Professor,
    Student,
    Department,
    Program,
    Course,
    Curriculum,
    CurriculumCourse,
    Section,
    Room,
    Schedule,
    Record,
    StudentRecord,
)


# Register your models here.
class ProfessorAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
        if kwargs["change"]:
            context["adminform"].form.fields[
                "user"
            ].queryset = CustomUser.objects.filter(pk=context["object_id"])
            return super(ProfessorAdmin, self).render_change_form(
                request, context, *args, **kwargs
            )
        context["adminform"].form.fields["user"].queryset = CustomUser.objects.filter(
            is_staff=True, is_superuser=False
        ).exclude(id__in=Professor.objects.values("user"))
        return super(ProfessorAdmin, self).render_change_form(
            request, context, *args, **kwargs
        )


class StudentAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
        if kwargs["change"]:
            context["adminform"].form.fields[
                "user"
            ].queryset = CustomUser.objects.filter(pk=context["object_id"])
            return super(StudentAdmin, self).render_change_form(
                request, context, *args, **kwargs
            )
        context["adminform"].form.fields["user"].queryset = CustomUser.objects.filter(
            is_staff=False, is_superuser=False
        ).exclude(pk__in=Student.objects.values("user"))
        return super(StudentAdmin, self).render_change_form(
            request, context, *args, **kwargs
        )


class DepartmentAdmin(admin.ModelAdmin):
    ordering = ("title",)


class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "department")
    list_filter = ("department",)
    ordering = ("department", "title")


class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "title", "units")
    search_fields = ("code", "title")
    ordering = ("code", "title")

    def render_change_form(self, request, context, *args, **kwargs):
        context["adminform"].form.fields[
            "corequisites"
        ].queryset = Course.objects.exclude(pk=context["object_id"])
        context["adminform"].form.fields[
            "prerequisites"
        ].queryset = Course.objects.exclude(pk=context["object_id"])
        return super(CourseAdmin, self).render_change_form(
            request, context, *args, **kwargs
        )


class CurriculumCourseInline(admin.TabularInline):
    model = CurriculumCourse
    extra = 1


class CurriculumAdmin(admin.ModelAdmin):
    fields = ("title", "program")
    inlines = (CurriculumCourseInline,)
    list_display = ("title", "program")
    list_filter = ("program",)
    ordering = ("program", "title")


class CurriculumCourseAdmin(admin.ModelAdmin):
    list_display = ("course", "year_level", "academic_term", "curriculum")
    search_fields = ("curriculum__title", "course__title")
    ordering = ("curriculum", "year_level", "academic_term", "course")


class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_open")
    ordering = ("name",)


class RoomAdmin(admin.ModelAdmin):
    ordering = ("number",)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("record", "room", "day", "start_time", "end_time")
    list_filter = ("day", "record__academic_term", "record__academic_year",)
    search_fields = (
        "record__curriculum_course__curriculum__program__department__title",
        "record__curriculum_course__curriculum__program__title",
        "record__section__name",
        "room__number",
        "professor__user__first_name",
        "professor__user__middle_name",
        "professor__user__last_name",
        "professor__user__name_suffix",
    )
    ordering = (
        "-record__academic_year",
        "-record__academic_term",
        "professor",
        "day",
        "start_time",
        "end_time",
    )


class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1


class StudentRecordInline(admin.TabularInline):
    model = StudentRecord
    extra = 1


class RecordAdmin(admin.ModelAdmin):
    fields = (
        "academic_year",
        "academic_term",
        "curriculum_course",
        "advisor",
        "section",
    )
    inlines = (
        ScheduleInline,
        StudentRecordInline,
    )
    list_display = (
        "curriculum_course",
        "advisor",
        "section",
        "academic_term",
        "academic_year",
    )
    list_filter = ("academic_year", "academic_term")
    search_fields = (
        "curriculum_course__curriculum__program__department__title",
        "curriculum_course__curriculum__program__title",
        "curriculum_course__course__code",
        "curriculum_course__course__title",
        "advisor__user__first_name",
        "advisor__user__middle_name",
        "advisor__user__last_name",
        "advisor__user__name_suffix",
        "section__name",
    )
    ordering = (
        "-academic_year",
        "-academic_term",
        "curriculum_course__curriculum__program__department__title",
        "curriculum_course__curriculum__program__title",
        "curriculum_course__course__title",
        "advisor",
        "section",
    )


class StudentRecordAdmin(admin.ModelAdmin):
    list_display = ("student", "record", "rating", "remark")
    list_filter = ("record__academic_year", "record__academic_term")
    search_fields = (
        "student__user__first_name",
        "student__user__middle_name",
        "student__user__last_name",
        "student__user__name_suffix",
        "record__advisor__user__first_name",
        "record__advisor__user__middle_name",
        "record__advisor__user__last_name",
        "record__advisor__user__name_suffix",
        "record__curriculum_course__curriculum__program__department__title",
        "record__curriculum_course__curriculum__program__title",
        "record__curriculum_course__course__code",
        "record__curriculum_course__course__title",
        "record__section__name",
    )
    ordering = (
        "student",
        "-record__academic_year",
        "-record__academic_term",
        "record__curriculum_course__course__title",
    )


admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(CurriculumCourse, CurriculumCourseAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(StudentRecord, StudentRecordAdmin)
