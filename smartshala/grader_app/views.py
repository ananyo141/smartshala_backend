# from django.db.models import Count, Sum, F
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from smartshala.grader_app.models import AnsweredQuestion, AnswerSheet
from smartshala.grader_app.serializers import (
    AnsweredQuestionSerializer,
    AnswerSheetSerializer,
    AnswerSheetUploadSerializer,
)
from smartshala.test_app.models import Test

# Create your views here.


class uploadTestPaperView(generics.ListAPIView):
    """Upload Test Paper"""

    parser_classes = (MultiPartParser,)
    serializer_class = AnswerSheetSerializer

    def get_queryset(self):
        queryset = AnswerSheet.objects.filter(
            test__created_by=self.request.user,
            test=self.kwargs["test_id"],
        ).order_by("-updated_at")
        return queryset

    def get_object(self):
        try:
            print(self.kwargs["test_id"], self.request.user)
            return Test.objects.get(
                id=self.kwargs["test_id"], created_by=self.request.user
            )
        except Test.DoesNotExist:
            raise NotFound("Invalid Test ID")

    def get(self, request, *args, **kwargs):
        # Setting it here to avoid manual-schema to get overwritten
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        test_obj: Test = self.get_object()
        image = request.FILES.get("image")
        if not image:
            raise NotFound("Image not provided")
        serializer = AnswerSheetUploadSerializer(
            data={"test": test_obj.id, "image": image}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Test Paper Uploaded Successfully"}, status=201
            )
        else:
            return Response(serializer.errors, status=400)


class AnsweredQuestionListView(generics.ListAPIView):
    serializer_class = AnsweredQuestionSerializer

    def get_queryset(self):
        return (
            AnsweredQuestion.objects.filter(
                answer_sheet_id=self.kwargs.get("ans_sheet_id"),
                answer_sheet__test__created_by=self.request.user,
            )
            .prefetch_related("answered_question")
            .order_by("id")
        )
