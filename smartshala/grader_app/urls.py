from django.urls import path
from grader_app.views import AnsweredQuestionListView, uploadTestPaperView

app_name = "Grader"

urlpatterns = [
    path(
        "<int:test_id>/",
        uploadTestPaperView.as_view(),
        name="view_upload_answersheets",
    ),  # GET # POST
    path(
        "answers/<int:ans_sheet_id>/",
        AnsweredQuestionListView.as_view(),
        name="view_answersheet",
    ),  # GET
]
