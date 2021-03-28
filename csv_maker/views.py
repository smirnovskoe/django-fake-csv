from celery.result import AsyncResult
from django.contrib.auth import mixins
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from . import forms
from . import models
from . import tasks


class SchemaListView(mixins.LoginRequiredMixin, generic.ListView):
    model = models.Schema
    context_object_name = 'schemas'
    template_name = 'csv_maker/schema_list.html'

    def get_queryset(self):
        return models.Schema.objects.filter(creator=self.request.user)


class SchemaDeleteView(generic.DeleteView):
    model = models.Schema
    template_name = 'csv_maker/schema_delete.html'
    success_url = reverse_lazy('csv_maker:schema-list')


class SchemaCreateView(generic.CreateView):
    template_name = 'csv_maker/schema_create.html'
    form_class = forms.SchemaModelForm
    success_url = reverse_lazy('csv_maker:schema-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = forms.SchemaColumnFormSet(self.request.POST)
        else:
            context['formset'] = forms.SchemaColumnFormSet()

        return context

    def form_valid(self, form):
        if form.is_valid():
            new_schema = form.save(commit=False)
            new_schema.creator = self.request.user
            new_schema.save()

            context = self.get_context_data()
            formset = context.get('formset')

            if formset.is_valid():
                formset.instance = new_schema
                formset.save()

        return redirect('csv_maker:schema-list')


class SchemaUpdateView(generic.UpdateView):
    template_name = 'csv_maker/schema_update.html'
    form_class = forms.SchemaModelForm
    success_url = reverse_lazy('csv_maker:schema-list')

    def get_queryset(self):
        return models.Schema.objects.filter(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = forms.SchemaColumnFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = forms.SchemaColumnFormSet(instance=self.object)

        return context

    def form_valid(self, form):
        if form.is_valid():
            new_schema = form.save(commit=False)
            new_schema.creator = self.request.user
            new_schema.save()

            context = self.get_context_data()
            formset = context.get('formset')

            if formset.is_valid():
                formset.instance = new_schema
                # formset.queryset = new_schema.columns.order_by('order')
                formset.save()

        return redirect('csv_maker:schema-list')


class DatasetListView(generic.ListView):
    model = models.Dataset
    template_name = 'csv_maker/schema_datasets.html'
    context_object_name = 'datasets'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['path'] = self.request.META['HTTP_HOST']
        return context


@csrf_exempt
def task_status(request, task_id):
    """Check task status"""

    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)


@csrf_exempt
def start_tasks(request, row_number):
    """Run tasks"""

    print(row_number)
    all_task_id = list()
    schemas = models.Schema.objects.all()

    for schema in schemas:
        column_type = list()  # --> [(col_name, col_type,), ]

        columns = schema.columns.all()
        for column in columns:
            # prepare data for celery
            column_type.append((
                column.column_name,
                column.type,
                column.order,
            ))
        col_sep = schema.column_separator
        string_char = schema.string_character

        task = tasks.build_csv.delay(
            column_type,
            int(row_number),
            col_sep=col_sep,
            str_chr=string_char,
        )

        all_task_id.append(task.id)

    return JsonResponse({"tasks_id": all_task_id}, status=202)
