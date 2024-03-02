from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Tawassut, Kafeel, Course, Class, Section, Student, Progress
from kifalat import models


def home(request):
    return render(request, 'home.html')

from django.db.models import Sum

def student_details(request, admission_number):
    student = Student.objects.get(admission_number=admission_number)
    progress = Progress.objects.filter(student=student)

    # Calculate total paid
    total_paid = student.progress_data.aggregate(Sum('amount_paid'))['amount_paid__sum__sum'] or 0.0


    # Calculate due amount
    total_fees = student.total_fees or 0
    due_amount = total_fees - total_paid

    context = {
        'student': student,
        'progress': progress,
        'total_paid': total_paid,
        'total_fees': total_fees,
        'due_amount': due_amount,
    }

    return render(request, 'student_details.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Kafeel, Student, Progress

def sponsor_dashboard(request, kafeel_id):
    if request.method == 'POST':
        entered_number = request.POST.get('kafeel_number')
        entered_phone = request.POST.get('kafeel_phone')

        try:
            entered_number = int(entered_number)
            entered_phone = int(entered_phone)
            kafeel = get_object_or_404(Kafeel, number=entered_number, phone=entered_phone)
            dashboard_data = Student.objects.filter(kafeel=kafeel, sponsoring_since__isnull=False)

            for student in dashboard_data:
                student.progress_data = Progress.objects.filter(student=student)
                # Calculate total paid
                total_paid = student.progress_data.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0.0
                # Fetch total fees for the student (replace 'total_fees' with the actual field name)
                total_fees = student.total_fees
                # Calculate due amount
                due_amount = total_fees - total_paid
                # Assign calculated values to the student object
                student.total_paid = total_paid
                student.total_fees = total_fees
                student.due_amount = due_amount

            context = {'kafeel': kafeel, 'dashboard_data': dashboard_data}
            return render(request, 'sponsor_dashboard.html', context)

        except (ValueError, Kafeel.DoesNotExist):
            return render(request, 'sponsor_dashboard_login.html', {'error_message': 'Invalid Kafeel credentials. Please try again.'})

    return render(request, 'sponsor_dashboard_login.html', {'kafeel_id': kafeel_id})

def student_details(request, admission_number):
    student = get_object_or_404(Student, admission_number=admission_number)
    progress = Progress.objects.filter(student=student)

    # Calculate total paid
    total_paid = progress.aggregate(models.Sum('amount_paid'))['amount_paid__sum'] or 0.0

    # Fetch total fees for the student (replace 'total_fees' with the actual field name)
    total_fees = student.total_fees or 0.0

    # Calculate due amount
    due_amount = total_fees - total_paid

    context = {'student': student, 'progress': progress, 'total_paid': total_paid, 'total_fees': total_fees, 'due_amount': due_amount}
    return render(request, 'student_details.html', context)



from .forms import ProgressForm  # Import your ProgressForm


def progress_form(request, kafeel_id, admission_number):
    kafeel = get_object_or_404(Kafeel, number=kafeel_id)
    student = get_object_or_404(Student, admission_number=admission_number)

    if request.method == 'POST':
        form = ProgressForm(request.POST)
        form.fields['student'].queryset = Student.objects.filter(kafeel=kafeel)  # Set the initial queryset
        if form.is_valid():
            # Handle form submission and save progress data
            # Access form.cleaned_data to get the cleaned data from the form
            # Add your form handling logic here
            return HttpResponse("Progress data saved successfully!")
    else:
        # If it's a GET request, initialize the form with the queryset for the 'student' field
        form = ProgressForm(initial={'kafeel': kafeel, 'student': student})
        form.fields['student'].queryset = Student.objects.filter(kafeel=kafeel)

    context = {'kafeel': kafeel, 'student': student, 'form': form}
    return render(request, 'progress_form.html', context)

