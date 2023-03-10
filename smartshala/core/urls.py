from django.urls import include, path

urlpatterns = [
    path("grader/", include("smartshala.grader_app.urls")),
    path("test/", include("smartshala.test_app.urls")),
    path("school/", include("smartshala.school_app.urls")),
]
