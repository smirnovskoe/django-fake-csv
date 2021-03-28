from django.urls import path

from . import views

app_name = 'csv_maker'

urlpatterns = [
    path('', views.SchemaListView.as_view(), name='schema-list'),
    path('<int:pk>/delete/', views.SchemaDeleteView.as_view(), name='schema-delete'),
    path('<int:pk>/update/', views.SchemaUpdateView.as_view(), name='schema-update'),
    path('create/', views.SchemaCreateView.as_view(), name='schema-create'),
    path('datasets/', views.DatasetListView.as_view(), name='schema-datasets'),

    # Celery path
    path('tasks/<row_number>/', views.start_tasks, name='run-tasks'),
    path('task_status/<task_id>/', views.task_status, name='task-status'),
]
