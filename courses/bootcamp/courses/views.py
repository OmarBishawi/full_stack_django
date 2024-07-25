from django.shortcuts import render, redirect
from .models import Course, Description, comment

def index(request):
    courses = Course.objects.all()
    return render(request, 'courses/index.html', {'courses': courses})

def add_course(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description_content = request.POST.get('description')
        
        # Validation
        errors = []
        if not name or len(name) <= 5:
            errors.append("Name must be more than 5 characters.")
        if not description_content or len(description_content) <= 15:
            errors.append("Description must be more than 15 characters.")
        
        if not errors:
            # Create the Description object first
            description = Description.objects.create(content=description_content)
            # Create the Course object with the associated Description object
            Course.objects.create(name=name, description=description)
            return redirect('index')
        
        # If there are errors, prepare context with errors, input values, and courses
        context = {
            'errors': errors,
            'name': name,
            'description': description_content,
            'courses': Course.objects.all()
        }
    else:
        # Prepare context for GET request
        context = {
            'courses': Course.objects.all()
        }
    
    # Render the template with context for both GET requests and POST requests with errors
    return render(request, 'courses/index.html', context)
def remove_course(request , course_id):
    try:
        course= Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return redirect('index')
    if request.method == 'POST':
        if 'confirm' in request.POST:
            course.delete()
        return redirect('index')
    return render(request, 'courses/delete.html', {'courses':course})

def course_comments(request, Course_id):
    try:
        course = Course.objects.get(pk=Course_id)
    except Course.DoesNotExist:
        return redirect('index')
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        if comment_text:
            comment.objects.create(course=course, text=comment_text)
    return render(request, 'courses/comments.html', {'course': course, 'comments': Course.comments.all()})