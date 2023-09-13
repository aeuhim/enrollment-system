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
    list_display = ("curriculum", "course", "year_level", "academic_term")
    search_fields = ("curriculum__title", "course__title")
    ordering = ("curriculum", "year_level", "academic_term", "course")


admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(CurriculumCourse, CurriculumCourseAdmin)
