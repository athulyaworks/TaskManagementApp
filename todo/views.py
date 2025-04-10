from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Task, Category
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# Create your views here.
def home(request):
    if 'id' in request.session:
        user_id = request.session['id']
        tasks = Task.objects.filter(user_id=user_id).order_by('completed', '-priority', 'due_date')
        categories = Category.objects.filter(user_id=user_id)
        return render(request, 'dashboard.html', {'tasks': tasks, 'categories': categories})
    return render(request, 'home.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        nm = request.POST['name']
        pw = request.POST['password']
        
        user = User.objects.filter(name=nm, password=pw)
        
        if user:
            for i in user:
                id_no = i.id
                nm = i.name
                email = i.email
            
            request.session['id'] = id_no
            request.session['name'] = nm
            request.session['email'] = email
            return redirect('dashboard')
        else:
            messages.error(request, "Username or Password is incorrect. Please try again.")
            return redirect('login')
    
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        nm = request.POST['name']
        email = request.POST['email']
        pw = request.POST['password']
        
        if User.objects.filter(name=nm).exists():
            messages.error(request, "Username already exists. Please choose another one.")
            return redirect('register')
        
        # Create new user
        new_user = User(name=nm, email=email, password=pw)
        new_user.save()
        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')
    
    return render(request, 'register.html')

def dashboard(request):
    if 'id' not in request.session:
        return redirect('login')
    
    user_id = request.session['id']
    tasks = Task.objects.filter(user_id=user_id).order_by('completed', '-priority', 'due_date')
    categories = Category.objects.filter(user_id=user_id)
    
    # Count incomplete tasks
    incomplete_tasks_count = Task.objects.filter(user_id=user_id, completed=False).count()
    
    return render(request, 'dashboard.html', {
        'tasks': tasks, 
        'categories': categories,
        'incomplete_tasks_count': incomplete_tasks_count
    })

def add_task(request):
    if 'id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST.get('description', '')
        priority = request.POST['priority']
        due_date_str = request.POST.get('due_date', '')
        category_id = request.POST.get('category', '')
        
        user_id = request.session['id']
        
        # Handle due date
        due_date = None
        if due_date_str:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        
        # Handle category
        category = None
        if category_id:
            category = get_object_or_404(Category, id=category_id, user_id=user_id)
        
        # Create task
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            user_id=user_id,
            category=category
        )
        task.save()
        
        messages.success(request, "Task added successfully!")
        return redirect('dashboard')
    
    categories = Category.objects.filter(user_id=request.session['id'])
    return render(request, 'add_task.html', {'categories': categories})

def edit_task(request, task_id):
    if 'id' not in request.session:
        return redirect('login')
    
    user_id = request.session['id']
    task = get_object_or_404(Task, id=task_id, user_id=user_id)
    
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST.get('description', '')
        task.priority = request.POST['priority']
        
        due_date_str = request.POST.get('due_date', '')
        if due_date_str:
            task.due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        else:
            task.due_date = None
        
        category_id = request.POST.get('category', '')
        if category_id:
            task.category = get_object_or_404(Category, id=category_id, user_id=user_id)
        else:
            task.category = None
        
        task.save()
        messages.success(request, "Task updated successfully!")
        return redirect('dashboard')
    
    categories = Category.objects.filter(user_id=user_id)
    return render(request, 'edit_task.html', {'task': task, 'categories': categories})

def delete_task(request, task_id):
    if 'id' not in request.session:
        return redirect('login')
    
    task = get_object_or_404(Task, id=task_id, user_id=request.session['id'])
    task.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect('dashboard')

def complete_task(request, task_id):
    if 'id' not in request.session:
        return redirect('login')
    
    task = get_object_or_404(Task, id=task_id, user_id=request.session['id'])
    task.completed = not task.completed
    task.save()
    
    status = "completed" if task.completed else "marked as incomplete"
    messages.success(request, f"Task {status} successfully!")
    return redirect('dashboard')

def add_category(request):
    if 'id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        name = request.POST['name']
        user_id = request.session['id']
        
        # Check if category exists
        if Category.objects.filter(name=name, user_id=user_id).exists():
            messages.error(request, "Category already exists!")
            return redirect('add_category')
        
        category = Category(name=name, user_id=user_id)
        category.save()
        messages.success(request, "Category added successfully!")
        return redirect('dashboard')
    
    return render(request, 'add_category.html')

def logout(request):
    if 'id' in request.session:
        del request.session['id']
        del request.session['name']
        del request.session['email']
    return redirect('home')