## What is API?

An application programming interface is a connection between computers or between computer programs. 

It is a type of software interface, offering a service to other pieces of software. 

A document or standard that describes how to build such a connection or interface is called an API specification.

API is **the messenger that delivers your request to the provider that you're requesting it from and then delivers the response back to you**.

What is REST API?

An API, or *application programming interface*, is a set of rules that define how applications or devices can connect to and communicate with each other. A REST API is an API that conforms to the design principles of the REST, or *representational state transfer* architectural style. For this reason, REST APIs are sometimes referred to RESTful APIs*.*

First defined in 2000 by computer scientist Dr. Roy Fielding in his doctoral dissertation, REST provides a relatively high level of flexibility and freedom for developers. This flexibility is just one reason why REST APIs have emerged as a common method for connecting components and applications in a [microservices](https://www.ibm.com/cloud/learn/microservices) architecture.

At the most basic level, an [API](https://www.ibm.com/cloud/learn/api) is a mechanism that enables an application or service to access a resource within another application or service. The application or service doing the accessing is called the client, and the application or service containing the resource is called the server.

Some APIs, such as SOAP or XML-RPC, impose a strict framework on developers. But REST APIs can be developed using virtually any programming language and support a variety of data formats. The only requirement is that they align to the following six REST design principles - also known as architectural constraints:

1. **Uniform interface**. All API requests for the same resource should look the same, no matter where the request comes from. The REST API should ensure that the same piece of data, such as the name or email address of a user, belongs to only one uniform resource identifier (URI). Resources shouldn’t be too large but should contain every piece of information that the client might need.
2. **Client-server decoupling**. In REST API design, client and server applications must be completely independent of each other. The only information the client application should know is the URI of the requested resource; it can't interact with the server application in any other ways. Similarly, a server application shouldn't modify the client application other than passing it to the requested data via HTTP.
3. **Statelessness**. REST APIs are stateless, meaning that each request needs to include all the information necessary for processing it. In other words, REST APIs do not require any server-side sessions. Server applications aren’t allowed to store any data related to a client request.
4. **Cacheability**. When possible, resources should be cacheable on the client or server side. Server responses also need to contain information about whether caching is allowed for the delivered resource. The goal is to improve performance on the client side, while increasing scalability on the server side.
5. **Layered system architecture**. In REST APIs, the calls and responses go through different layers. As a rule of thumb, don’t assume that the client and server applications connect directly to each other. There may be a number of different intermediaries in the communication loop. REST APIs need to be designed so that neither the client nor the server can tell whether it communicates with the end application or an intermediary.
6. **Code on demand (optional)**. REST APIs usually send static resources, but in certain cases, responses can also contain executable code (such as Java applets). In these cases, the code should only run on-demand.

# HANDS-ON PART

```bash
py -m venv env
.\env\Scripts\activate
pip install django
pip install python-decouple
django-admin --version
django-admin startproject drf
```

rename folder as src

create a new file and name as .env at same level as src

copy your SECRET_KEY from src/drf/settings.py into this .env file. Don't forget to remove quotation marks from SECRET_KEY

```
SECRET_KEY = django-insecure-)=b-%-w+0_^slb(exmy*mfiaj&wz6_fb4m&s=az-zs!#1^ui7j
```

go to src/drf/settings.py, make amendments below

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
```

 cd src

```bash
py manage.py migrate
py manage.py runserver
```

click the link with CTRL key pressed in the terminal and see django rocket.

new terminal and cd src

```
py manage.py startapp student_api
```

go to settings.py and add 'student_api' app to installed apps

go to student_api.models.py

```python
from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

```

create serializers.py under api_student

```python
from rest_framework import serializers
from fscohort.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name", "number"]
```

go to terminal

```bash
pip install djangorestframework
```

go to settings.py and add 'rest_framework' app to installed apps

go to student_api.views.py

```python

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

```

go to drf.urls.py

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('student_api.urls')),
]
```

go to student_api.urls.py

```python
from django.urls import path
from .views import home, manual_api, student_list_api, student_list_api2, student_add_api, student_api, student_api_get_update_delete

urlpatterns = [
    path('', home),
    path('manual/', manual_api),
    path('list/', student_list_api2),
    path('add/', student_add_api),
    path('student/', student_api),
    path('student/<int:id>/', student_api_get_update_delete)
]
```

```bash
py .\manage.py createsuperuser
py manage.py makemigrations
py manage.py migrate
pip freeze > requirements.txt
py .\manage.py runserver
```

CORS SETUP

```bash
pip install django-cors-headers
```

settings.py

```python
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    # ...
    'corsheaders',
]
MIDDLEWARE = [
    # ...
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ...
]
CORS_ORIGIN_ALLOW_ALL = True
```

index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <title>Document</title>
  </head>
  <body>
    <div id="message"></div>

    <form action="" method="POST" id="form">
      <label for="name">First Name</label>
      <input type="text" name="name" id="name" />
      <br />
      <label for="lastname">Last Name</label>
      <input type="text" name="lastname" id="lastname" />
      <br />
      <label for="number">Number</label>
      <input type="number" name="number" id="number" />
      <br />
      <input type="submit" value="Add" />
    </form>
    <br />
    <br />
    <div id="container"></div>
    <script src="app.js"></script>
  </body>
</html>

```

app.js

```js
const apiGet = async (url) => {
  //   let headers = new Headers();

  //   headers.append('Content-Type', 'application/json');
  //   headers.append('Accept', 'application/json');
  //   headers.append('Origin', 'http://localhost:8000');
  try {
    const response = await axios.get(url);
    // , {
    //   headers: headers,
    // });
    body = document.querySelector('#container');
    html = `<table style="width:50%">
    <tr>
      <th>Firstname</th>
      <th>Lastname</th>
      <th>Number</th>
    </tr>
    `;
    response.data.forEach((element) => {
      line = `      
        <tr>
            <td>${element.first_name}</td>
            <td>${element.last_name}</td>
            <td>${element.number}</td>
        </tr>`;
      html += line;
    });
    html += '</table>';
    body.innerHTML = html;
  } catch (err) {
    console.log(err.message);
  }
};

const apiPost = async (url, data) => {
  try {
    const response = await axios.post(url, data);
    // , {
    //   headers: headers,
    // });
    body = document.querySelector('#message');

    body.innerHTML = response.data.message;
  } catch (err) {
    console.log(err.message);
  }
};

apiGet('http://localhost:8000/api/student/');
// apiPost('http://localhost:8000/api/student/', {
//   first_name: 'veysel',
//   last_name: 'veysel',
//   number: 1002,
// });

let form = document.getElementById('form'); // selecting the form

form.addEventListener('submit', async function (event) {
  // 1
  event.preventDefault();
  console.log('form submit');

  let data = new FormData(); // 2

  data.append('first_name', document.getElementById('name').value);
  data.append('last_name', document.getElementById('lastname').value);
  data.append('number', document.getElementById('number').value); // 3

  try {
    const response = await axios.post(
      'http://localhost:8000/api/student/',
      data
    );

    body = document.querySelector('#message');

    body.innerHTML = response.data.message;
    apiGet('http://localhost:8000/api/student/');
  } catch (err) {
    console.log(err.message);
  }

  //   axios
  //     .post('http://localhost:8000/api/student/', data) // 4
  //     .then((res) => alert('Form Submitted')) // 5
  //     .catch((errors) => console.log(errors)); // 6
});

```

