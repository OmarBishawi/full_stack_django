# books/views.py
from django.shortcuts import render, redirect
from .models import MyUser, Book
from django.http import HttpResponse

def validate_email(email):
    return "@" in email and "." in email

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        errors = []
        if not validate_email(email):
            errors.append('Invalid email format.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        if len(password) < 8:
            errors.append('Password must be at least 8 characters long.')
        if len(first_name) < 2 or len(last_name) < 2:
            errors.append('First name and last name must be at least 2 characters long.')

        if errors:
            return render(request, 'books/register.html', {'errors': errors})

        try:
            user = MyUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
            request.session['user_id'] = user.id  # Simple login by storing user ID in session
            return redirect('book_list')
        except ValueError as e:
            return render(request, 'books/register.html', {'errors': [str(e)]})

    return render(request, 'books/register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = MyUser.objects.get(email=email, password=password)
            request.session['user_id'] = user.id  # Simple login by storing user ID in session
            return redirect('book_list')
        except MyUser.DoesNotExist:
            return render(request, 'books/login.html', {'error': 'Invalid login credentials'})

    return render(request, 'books/login.html')

def book_list(request):
    if 'user_id' not in request.session:
        return redirect('user_login')
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})

def add_book(request):
    if 'user_id' not in request.session:
        return redirect('user_login')
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        user = MyUser.objects.get(id=request.session['user_id'])

        errors = []
        if not title:
            errors.append('Title is required.')
        if len(description) < 5:
            errors.append('Description must be at least 5 characters long.')

        if errors:
            return render(request, 'books/add_book.html', {'errors': errors})

        book = Book.objects.create(title=title, description=description, uploaded_by=user)
        book.favorited_by.add(user)
        return redirect('book_list')

    return render(request, 'books/add_book.html')

def book_detail(request, book_id):
    if 'user_id' not in request.session:
        return redirect('user_login')
    book = Book.objects.get(id=book_id)
    user = MyUser.objects.get(id=request.session['user_id'])
    is_favorited = user in book.favorited_by.all()
    return render(request, 'books/book_detail.html', {'book': book, 'is_favorited': is_favorited})

def edit_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('user_login')
    book = Book.objects.get(id=book_id)
    user = MyUser.objects.get(id=request.session['user_id'])
    if request.method == 'POST' and book.uploaded_by == user:
        title = request.POST['title']
        description = request.POST['description']

        errors = []
        if not title:
            errors.append('Title is required.')
        if len(description) < 5:
            errors.append('Description must be at least 5 characters long.')

        if errors:
            return render(request, 'books/edit_book.html', {'book': book, 'errors': errors})

        book.title = title
        book.description = description
        book.save()
        return redirect('book_detail', book_id=book.id)

    return render(request, 'books/edit_book.html', {'book': book})

def delete_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('user_login')
    book = Book.objects.get(id=book_id)
    user = MyUser.objects.get(id=request.session['user_id'])
    if request.method == 'POST' and book.uploaded_by == user:
        book.delete()
        return redirect('book_list')
    return render(request, 'books/delete_book.html', {'book': book})

def favorite_book(request, book_id):
    if 'user_id' not in request.session:
        return redirect('user_login')
    book = Book.objects.get(id=book_id)
    user = MyUser.objects.get(id=request.session['user_id'])
    if user in book.favorited_by.all():
        book.favorited_by.remove(user)
    else:
        book.favorited_by.add(user)
    return redirect('book_detail', book_id=book.id)

def user_logout(request):
    request.session.flush()  # Clear the session
    return redirect('user_login')
