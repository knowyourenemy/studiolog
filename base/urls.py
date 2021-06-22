from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CustomLoginView, InstrumentCreate, InstrumentDelete, InstrumentDetail, InstrumentList, InstrumentUpdate, PieceCreate, PieceDelete, PieceDetail, PieceList, PieceUpdate, PracticeDelete, PracticeDetail, PracticeList, PracticeCreate, PracticeUpdate, RegisterView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', PracticeList.as_view(), name='practice list'),
    path('practice/<int:pk>/', PracticeDetail.as_view(), name='practice detail'),
    path('practice-create/', PracticeCreate.as_view(), name='practice create'),
    path('practice-update/<int:pk>/', PracticeUpdate.as_view(), name='practice update'),
    path('practice-delete/<int:pk>/', PracticeDelete.as_view(), name='practice delete'),
    path('instruments', InstrumentList.as_view(), name='instrument list'),
    path('instrument/<int:pk>/', InstrumentDetail.as_view(), name='instrument detail'),
    path('instrument-create/', InstrumentCreate.as_view(), name='instrument create'),
    path('instrument-update/<int:pk>/', InstrumentUpdate.as_view(), name='instrument update'),
    path('instrument-delete/<int:pk>/', InstrumentDelete.as_view(), name='instrument delete'),
    path('pieces', PieceList.as_view(), name='piece list'),
    path('piece/<int:pk>/', PieceDetail.as_view(), name='piece detail'),
    path('piece-create/', PieceCreate.as_view(), name='piece create'),
    path('piece-update/<int:pk>/', PieceUpdate.as_view(), name='piece update'),
    path('piece-delete/<int:pk>/', PieceDelete.as_view(), name='piece delete'),
]