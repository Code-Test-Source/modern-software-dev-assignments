from django.urls import include, path

urlpatterns = [
    path("api/notes/", include("notes.urls")),
    path("api/action-items/", include("actionitems.urls")),
]
