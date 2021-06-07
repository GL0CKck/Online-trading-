from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render,redirect
from rest_framework.decorators import api_view

from .models import Bb,Rubric
from django.urls import reverse
from django.template import loader
from django.views.generic.edit import CreateView
from .forms import BbForm,RubricForm
from django.urls import reverse_lazy
from django.forms import modelformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
from django.contrib.messages.views import SuccessMessageMixin
from .serializers import RubricSerializer, BbSerializer
from rest_framework.response import Response
from rest_framework import status

# def add_rubrics(request):
#     if request.method == "POST":
#         rubrics = RubricForm(request.POST)
#         if rubrics.is_valid():
#             rubrics.save()
#             return redirect('by_rubric', rubric_id=rubrics.cleaned_data['rubric'].pk)
#         else:
#             context={'rub':rubrics}
#             return render(request,'bboard/add_rubrics.html',context)
#     else:
#         rubrics=RubricForm()
#         context={'rub':rubrics}
#         return render(request,'bboard/add_rubrics.html',context)




def home(request):
    return redirect(index)


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs':bbs,'rubrics':rubrics}
    return render(request,'bboard/index.html',context)

def by_rubric(request,rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric=Rubric.objects.get(pk=rubric_id) # читаем текущий айди нашей рубрики
    context = {'bbs':bbs,'rubrics':rubrics,'current_rubric':current_rubric}
    return render(request,'bboard/by_rubric.html',context)

class BbCreateView(SuccessMessageMixin,CreateView):
    template_name = 'bboard/add_rubrics.html' #путь к юрл файлу
    form_class = RubricForm
    success_url = reverse_lazy('index') #url для перехода при правельном вводе данных
    success_massage = 'Рубрика  успешно создана'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics']=Rubric.objects.all()
        return context


def add_and_save(request):
    if request.method == "POST":
        bbs = BbForm(request.POST)
        if bbs.is_valid():
            bbs.save()
            return redirect('by_rubric',rubric_id=bbs.cleaned_data['rubric'].pk)


        else:
            context = {'bbs': bbs}
            return render(request,'bboard/create.html',context)
    else:
        bbs=BbForm()
        context={'form': bbs}
        return render(request,'bboard/create.html',context)



def bb_delete(request,pk):
    bb=Bb.objects.get(pk=pk)
    if request.method=="POST":
        bb.delete()
        return HttpResponseRedirect(reverse('by_rubric',kwargs={'rubric_id':bb.rubric.pk}))
    else:
        context={'bb':bb}
        return render(request,'bboard/bb_delete.html',context)

def rubrics(request):
    RubricFormSet=modelformset_factory(Rubric,fields=('name',),can_order=True,can_delete=True)

    if request.method=="POST":
        formset=RubricFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    rubric = form.save(commit=False)
                    rubric.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    rubric.delete()
                return redirect('index')
    else:
        formset=RubricFormSet()
        context={'formset':formset}
        return render(request,'bboard/delete_rub.html',context)

@api_view(['GET','POST'])
def api_rubrics(request):
    if request.method=='GET':
        rubrics=Rubric.objects.all()
        serializer=RubricSerializer(rubrics,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer=RubricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def api_bb(request):
    if request.method=='GET':
        bb=Bb.objects.all()
        serializer=BbSerializer(bb,many=True) # many  со значением тrue,  говоря тем самым, что сериализовать  нужно именно набор записей, а не единичную запись.
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer=BbSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','PATCH','DELETE'])
def api_rubric_detail(request,pk):
    rubric = Rubric.objects.get(pk=pk)
    if request.method=='GET':
        serializer=RubricSerializer(rubric)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer=RubricSerializer(rubric,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        rubric.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','PUT','PATCH','DELETE'])
def api_bb_detail(request,pk):
    bb=Bb.objects.get(pk=pk)
    if request.method == 'GET':
        serializer=BbSerializer(bb)
        return Response(serializer.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer=BbSerializer(bb,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        bb.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



















