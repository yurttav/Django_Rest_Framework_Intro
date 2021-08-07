
from django.shortcuts import render, HttpResponse, get_object_or_404

from django.http import JsonResponse
from .models import Student

from django.core.serializers import serialize

from django.views.decorators.csrf import csrf_exempt
import json

from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Create your views here.


def home(request):
    return HttpResponse('<h1>API Page</h1>')


def manual_api(request):
    # from django.http import JsonResponse
    data = {
        "first_name": 'Barry',
        "last_name": 'Mitchell',
        'number': 5000
    }
    return JsonResponse(data)


def student_list_api(request):
    if request.method == 'GET':
        students = Student.objects.all()
        student_count = Student.objects.count()
        student_list = []
        for student in students:
            student_list.append({
                "first_name": student.first_name,
                "last_name": student.last_name,
                'number': student.number
            })
        data = {
            "students": student_list,
            "count": student_count
        }
        return JsonResponse(data)


def student_list_api2(request):
    # from django.core.serializers import serialize
    if request.method == 'GET':
        students = Student.objects.all()
        student_count = Student.objects.count()
        student_data = serialize("python", students)
        data = {
            "students": student_data,
            "count": student_count
        }
        return JsonResponse(data)


@csrf_exempt
def student_add_api(request):
    # import json
    # from django.views.decorators.csrf import csrf_exempt
    if request.method == 'POST':
        post_body = json.loads(request.body)
        student_data = {}
        student_data['first_name'] = post_body.get('first_name')
        student_data['last_name'] = post_body.get('last_name')
        student_data['number'] = post_body.get('number')
        student = Student.objects.create(**student_data)
        data = {
            "message": f"Student {student.last_name} added successfully"
        }
        return JsonResponse(data, status=201)


# @api_view()
@api_view(['GET', 'POST'])
def student_api(request):
    # from rest_framework.decorators import api_view
    # from rest_framework.response import Response
    # from rest_framework import status

    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        from pprint import pprint
        pprint(request)
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Student {serializer.validated_data.get('first_name')} saved successfully!"}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def student_api_get_update_delete(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                "message": f"Student {student.last_name} updated successfully"
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        student.delete()
        data = {
            "message": f"Student {student.last_name} deleted successfully"
        }
        return Response(data)
