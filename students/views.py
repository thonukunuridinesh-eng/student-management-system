from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm

def student_list(request):
    students = Student.objects.all()
    # Updated template path to look inside the application subfolder
    return render(request, "students/student_list.html", {"students": students})

def add_student(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("student_list")
    # Updated template path to look inside the application subfolder
    return render(request, "students/student_form.html", {"form": form})

def update_student(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect("student_list")
    # Updated template path to look inside the application subfolder
    return render(request, "students/student_form.html", {"form": form})

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect("student_list")
