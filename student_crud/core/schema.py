# Copyright 2024 ritik
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import graphene
import graphene_django
from .models import Student

class StudentType(graphene_django.DjangoObjectType):
    class Meta:
        model = Student
        fields = '__all__'

class Query(graphene.ObjectType):
    students = graphene.List(StudentType)

    def resolve_students(self,info):
        return Student.objects.all()


class CreateStudent(graphene.Mutation):

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        gender = graphene.String()
        grade = graphene.String()
        age = graphene.Int()

    student = graphene.Field(StudentType)

    def mutate(self, info, first_name, last_name, gender, grade, age):
        student = Student(first_name=first_name, last_name=last_name, gender=gender, grade=grade, age=age)
        student.save()
        return CreateStudent(student=student)

class UpdateStudent(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        first_name = graphene.String()
        last_name = graphene.String()
        gender = graphene.String()
        grade = graphene.String()
        age = graphene.Int()

    success = graphene.Boolean()
    student = graphene.Field(StudentType)

    def mutate(self, info, id, first_name, last_name, gender, grade, age):
        student = Student.objects.get(pk=id)
        student.first_name = first_name
        student.last_name = last_name
        student.gender = gender
        student.grade = grade
        student.age = age
        student.save()
        return UpdateStudent(success=True, student=student)

class DeleteStudent(graphene.Mutation):

    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()
    student = graphene.Field(StudentType)

    def mutate(self, info, id):
        try:
            student_instance = Student.objects.get(id=id)
            student_instance.delete()
            return DeleteStudent(success=True, student=student_instance)
        except Student.DoesNotExist:
            return DeleteStudent(success=False, student=None)


class Mutation(graphene.ObjectType):
    create_student = CreateStudent.Field()
    update_student = UpdateStudent.Field()
    delete_student = DeleteStudent.Field()
