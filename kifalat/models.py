from django.db import models
from django.shortcuts import render

class Tawassut(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    address = models.TextField()

class Kafeel(models.Model):
    number = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    tawassut = models.ForeignKey(Tawassut, on_delete=models.SET_NULL, null=True)
    
class Course(models.Model):
    name = models.CharField(max_length=255)

class Class(models.Model):
    name = models.CharField(max_length=255)

class Section(models.Model):
    name = models.CharField(max_length=255)


class Student(models.Model):
    # Change AutoField to CharField if you want a character-based admission number
    admission_number = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    address = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_field = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    kafeel = models.ForeignKey(Kafeel, on_delete=models.CASCADE)
    sponsoring_since = models.DateField(null=True)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        # Generate a unique admission number if it's not provided
        if not self.admission_number:
            # You can replace the following logic with your desired logic to generate admission numbers
            self.admission_number = self.generate_unique_admission_number()

        super().save(*args, **kwargs)

    def generate_unique_admission_number(self):
        # Replace this with your logic to generate a unique admission number
        # For example, you might want to use a combination of date and some random characters
        # Ensure that the generated number is unique in your system
        # Example: return some_logic_to_generate_unique_number()
        pass
  # Add this field

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Deactive', 'Deactive'),
        ('Dropped Out', 'Dropped Out'),
        ('Course Complete', 'Course Complete'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

class Progress(models.Model):
    kafeel = models.ForeignKey(Kafeel, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=255, unique=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    study_report = models.TextField()
    paid_date = models.DateTimeField()

from django.db.models import Sum

def student_details(request, admission_number):
    student = Student.objects.get(admission_number=admission_number)
    progress = Progress.objects.filter(student=student)
    
    # Calculate total paid
    total_paid = progress.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0.0

    # Calculate due amount
    total_fees = student.total_fees or 0.0
    due_amount = total_fees - total_paid

    context = {'student': student, 'progress': progress, 'total_paid': total_paid, 'total_fees': total_fees, 'due_amount': due_amount}
    return render(request, 'student_details.html', context)
