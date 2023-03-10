from django.db.models import Count, F, Sum
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from smartshala.school_app.models import SchoolTeacher
from smartshala.test_app.models import Question, Standard, Test
from smartshala.test_app.serializers import (
    QuestionSerializer,
    TestCreateSerializer,
    TestSerializer,
)


class TestView(generics.ListCreateAPIView):
    """Create and List Tests under a teacher"""

    serializer_class = TestSerializer

    def get_queryset(self):
        queryset = (
            Test.objects.filter(created_by=self.request.user)
            .annotate(
                question_count=Count("test_question"),
                total_score=Sum("test_question__marks"),
                topic_name=F("topic__name"),
                standard=F("topic__standard__name"),
                subject=F("topic__subject__name"),
                creator_name=F("created_by__name"),
            )
            .order_by("-updated_at")
        )
        _standard = self.request.query_params.get("standard")
        if _standard:
            queryset = queryset.filter(topic__standard_id=_standard)
        return queryset

    def get(self, request, *args, **kwargs):
        """
        List all tests under a teacher
        """
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Create a test"""
        serializer = TestCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateTestView(generics.RetrieveUpdateDestroyAPIView):
    """Update , retrieve and delete tests"""

    serializer_class = TestSerializer

    def get_object(self):
        try:
            return Test.objects.get(
                id=self.kwargs["test_id"], created_by=self.request.user
            )
        except Test.DoesNotExist:
            raise NotFound("Test not found")


class getTestFormData(APIView):
    def get_teacher(self):
        try:
            return SchoolTeacher.objects.get(teacher=self.request.user)
        except SchoolTeacher.DoesNotExist:
            raise NotFound("You are not assigned as a Teacher")

    def get(self, request, *args, **kwargs):
        teacher = self.get_teacher()
        data = {
            "standards": Standard.objects.filter(
                school_teacher_standards=teacher
            )
            .order_by("name")
            .values_list("id", "name"),
            "subjects": teacher.subjects.all()
            .order_by("name")
            .values_list("id", "name"),
        }
        return Response(data, status=status.HTTP_200_OK)


class AddQuestions(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        return Question.objects.filter(
            test_id=self.kwargs["test_id"], test__created_by=self.request.user
        ).order_by("id")

    def get_object(self):
        try:
            return Test.objects.get(
                id=self.kwargs["test_id"], created_by=self.request.user
            )
        except Test.DoesNotExist:
            raise NotFound("Test not found")

    def post(self, request, *args, **kwargs):
        test = self.get_object()
        qs = []
        for question in request.data:
            QuestionSerializer(data=question).is_valid(raise_exception=True)
            qs.append(Question(test=test, **question))
        response = Question.objects.bulk_create(qs)
        serializer = QuestionSerializer(response, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
