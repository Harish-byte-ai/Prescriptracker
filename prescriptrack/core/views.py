import hashlib, qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from .models import AccessLog, Prescription, Patient, Doctor
from django.shortcuts import render, redirect
from django.utils import timezone
from django.shortcuts import render
from .utils import extract_qr_hash
from .models import Prescription
from django.utils import timezone
from datetime import timedelta
from .utils import check_for_fraud

import hashlib, qrcode, time
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Doctor, Patient, Prescription

def generate_prescription(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        patient_id = request.POST.get('patient_id')
        medicine = request.POST.get('medicine_details')
        timestamp = timezone.now().isoformat()

        # 🔎 Get selected doctor and patient objects
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            patient = Patient.objects.get(id=patient_id)
        except (Doctor.DoesNotExist, Patient.DoesNotExist):
            return render(request, 'index.html', {
                'doctors': Doctor.objects.all(),
                'patients': Patient.objects.all(),
                'error': "Invalid doctor or patient selection."
            })

        # 🔐 Create prescription hash
        raw_data = f"{doctor_id}{patient_id}{medicine}{timestamp}"
        hash_value = hashlib.sha256(raw_data.encode()).hexdigest()

        # 🧾 Generate QR code
        qr = qrcode.make(hash_value)
        stream = BytesIO()
        qr.save(stream, format='PNG')
        qr_image = ContentFile(stream.getvalue(), f'RX-{patient_id}-{int(time.time())}.png')

        # 🗃️ Save prescription
        Prescription.objects.create(
            prescription_id=f"RX-{patient_id}-{int(time.time())}",
            patient=patient,
            doctor=doctor,
            medicine_details=medicine,
            hash=hash_value,
            qr_code_image=qr_image
        )

        return redirect('success_page')  # Make sure this view exists and handles QR display

    # GET request → render form with dropdowns
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    return render(request, 'index.html', {
        'doctors': doctors,
        'patients': patients
    })



def verify_prescription(request):
    result = None
    fraud_flag = None
    
    if request.method == 'POST' and request.FILES.get('qr_image'):
        uploaded_image = request.FILES['qr_image']
        hash_value = extract_qr_hash(uploaded_image)
        result = Prescription.objects.filter(hash=hash_value).first()

        if result:
            fraud_flag = check_for_fraud(result)

            AccessLog.objects.create (
                pharmacist_name="Hari",  
                prescription=result,
                is_valid=True
            )
        else:
            fraud_flag = "❌ Invalid Prescription"

    return render(request, 'verify_prescription.html', {
        'result': result,
        'fraud_flag': fraud_flag
    })

from django.shortcuts import redirect

def redirect_to_create(request):
    return redirect('index')


from django.shortcuts import render
def success_page(request):
    latest = Prescription.objects.latest('id')
    return render(request, 'success.html', {'prescription': latest})
