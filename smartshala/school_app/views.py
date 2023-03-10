# from django_filters import *
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAdminUser

import smartshala.core.exceptions as http_exc

from .models import School, SchoolTeacher
from .serializers import SchoolSerializer, TeacherSerializer

# School Related APIS
# Requires Auth : Only admin users


class CreateSchool(generics.ListCreateAPIView):
    """Hello world"""

    permission_classes = [IsAdminUser]
    serializer_class = SchoolSerializer

    def get_queryset(self):
        return School.objects.filter(
            deleted=False,
            created_by=self.request.user,
        ).order_by("created_at")


class UpdateDeleteSchool(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAdminUser]

    serializer_class = SchoolSerializer

    def get_object(self):
        try:
            return School.objects.get(
                id=self.kwargs["school_id"], deleted=False
            )
        except School.DoesNotExist or School.MultipleObjectsReturned:
            raise http_exc.Http404(
                "Invalid School ID Provided/No School Found!"
            )
        except KeyError:
            raise http_exc.Http400("Please Provide School ID")

    def delete(self):
        school = self.get_object()
        school.delete = True
        school.save()
        raise http_exc.Http200("Deleted Successfully")


class AddGetTeachers(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = TeacherSerializer
    filter_backends = [SearchFilter]

    def get_queryset(self):
        try:
            return (
                SchoolTeacher.objects.filter(
                    school=self.kwargs["school_id"],
                    school__deleted=False,
                )
                .prefetch_related(
                    "school_teacher_subjects", "school_teacher_standards"
                )
                .select_related("school_teacher_teacher")
                .order_by("updated_at")
            )
        except KeyError:
            raise http_exc.Http400("Please Provide School ID")


class UpdateDeleteTeachers(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = TeacherSerializer

    def get_object(self):
        try:
            return SchoolTeacher.objects.get(
                id=self.kwargs["teacher_id"],
                school_id=self.kwargs["school_id"],
                school__deleted=False,
            )
        except (
            SchoolTeacher.DoesNotExist or SchoolTeacher.MultipleObjectsReturned
        ):
            raise http_exc.Http404(
                "Invalid Teacher ID Provided/No Teacher Found!"
            )
        except KeyError:
            raise http_exc.Http400("Please Provide School/Teacher ID")
