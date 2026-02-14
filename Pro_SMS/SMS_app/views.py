from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Student, Teacher, Parent, Department
from django.contrib.auth.hashers import make_password
from django.db.models import Q

def home(request):
    return render(request, 'home.html')

# ==================== STUDENT VIEWS ====================

def student_dashboard(request):
    return render(request, 'student/dashboard.html')

def student_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        try:
            student = Student.objects.get(phone=phone)
            if student.check_password(password):
                # Store in session
                request.session['student_id'] = student.id
                request.session['user_type'] = 'student'
                messages.success(request, f'Welcome {student.name}!')
                # Redirect to profile page with student ID
                return redirect('student_profile', student_id=student.id)
            else:
                messages.error(request, 'Wrong password! Please try again.')
        except Student.DoesNotExist:
            messages.error(request, 'Phone number not found! Please register as a new student.')
            return redirect('student_register')
    
    return render(request, 'student/login.html')

def student_register(request):
    if request.method == 'POST':
        # Get all form data
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        father_name = request.POST.get('father_name')
        mother_name = request.POST.get('mother_name')
        grand_father_name = request.POST.get('grand_father_name')
        department_id = request.POST.get('department')
        image = request.FILES.get('image')
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('student_register')
        
        if Student.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already registered!')
            return redirect('student_register')
        
        if Student.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('student_register')
        
        # Create student
        student = Student(
            name=name, 
            dob=dob, 
            gender=gender, 
            address=address,
            phone=phone, 
            email=email, 
            father_name=father_name,
            mother_name=mother_name, 
            grand_father_name=grand_father_name,
            department_id=department_id, 
            image=image
        )
        student.set_password(password)
        student.save()
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('student_login')
    
    departments = Department.objects.all()
    return render(request, 'student/register.html', {'departments': departments})

def student_profile(request, student_id):
    # Check if logged in student is accessing their own profile
    if 'student_id' not in request.session or request.session['student_id'] != student_id:
        messages.error(request, 'Please login first!')
        return redirect('student_login')
    
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'student/profile.html', {'student': student})

# ==================== TEACHER VIEWS ====================

def teacher_dashboard(request):
    return render(request, 'teacher/dashboard.html')

def teacher_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        try:
            teacher = Teacher.objects.get(phone=phone)
            if teacher.check_password(password):
                request.session['teacher_id'] = teacher.id
                request.session['user_type'] = 'teacher'
                messages.success(request, f'Welcome {teacher.name}!')
                return redirect('teacher_profile', teacher_id=teacher.id)
            else:
                messages.error(request, 'Wrong password!')
        except Teacher.DoesNotExist:
            messages.error(request, 'Phone number not found! Please register.')
            return redirect('teacher_register')
    
    return render(request, 'teacher/login.html')

def teacher_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        qualification = request.POST.get('qualification')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        image = request.FILES.get('image')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('teacher_register')
        
        if Teacher.objects.filter(phone=phone).exists():
            messages.error(request, 'Phone number already registered!')
            return redirect('teacher_register')
        
        if Teacher.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('teacher_register')
        
        teacher = Teacher(
            name=name, 
            qualification=qualification, 
            phone=phone,
            address=address, 
            email=email, 
            image=image
        )
        teacher.set_password(password)
        teacher.save()
        
        messages.success(request, 'Registration successful! Please login.')
        return redirect('teacher_login')
    
    return render(request, 'teacher/register.html')

def teacher_profile(request, teacher_id):
    if 'teacher_id' not in request.session or request.session['teacher_id'] != teacher_id:
        messages.error(request, 'Please login first!')
        return redirect('teacher_login')
    
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'teacher/profile.html', {'teacher': teacher})

# ==================== PARENT VIEWS ====================

def parent_dashboard(request):
    return render(request, 'parent/dashboard.html')

def parent_login(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        student_phone = request.POST.get('student_phone')
        student_email = request.POST.get('student_email')
        
        # Search for student with these details
        try:
            student = Student.objects.get(
                Q(name__icontains=student_name) & 
                Q(phone=student_phone) & 
                Q(email=student_email)
            )
            
            # Store parent session (using student's ID)
            request.session['parent_access_student_id'] = student.id
            request.session['user_type'] = 'parent'
            messages.success(request, f'Welcome! You are viewing {student.name}\'s profile')
            return redirect('parent_view_child', student_id=student.id)
            
        except Student.DoesNotExist:
            messages.error(request, 'No student found with these details! Please check and try again.')
        except Student.MultipleObjectsReturned:
            messages.error(request, 'Multiple students found! Please contact school administration.')
    
    return render(request, 'parent/dashboard.html')

def parent_view_child(request, student_id):
    # Check if parent has access to this student
    if 'parent_access_student_id' not in request.session or request.session['parent_access_student_id'] != student_id:
        messages.error(request, 'Please login first!')
        return redirect('parent_dashboard')
    
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'parent/child_profile.html', {'student': student})


def logout_view(request):
    request.session.flush()  # Saare session data delete kar deta hai
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')

from .models import HomeImage

def home(request):
    home_images = HomeImage.objects.filter(is_active=True).order_by('order')
    return render(request, 'home.html', {'home_images': home_images})