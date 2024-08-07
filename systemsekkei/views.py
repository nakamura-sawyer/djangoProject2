from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from datetime import datetime, date
from django.http import JsonResponse

from systemsekkei.models import Employee
from systemsekkei.models import Shiiregyosha
from systemsekkei.models import Patient
from systemsekkei.models import Prescription, Medicine


def index(request):
    return HttpResponse("ようこそ")


def login(request):
    if request.method == "POST":
        empid = request.POST['empid']
        password = request.POST['emppasswd']

        try:
            employee = Employee.objects.get(empid=empid)
            if employee.emppasswd == password:
                # ロールに基づいてリダイレクト
                if employee.emprole == 2:
                    return redirect('home_kanrisya')
                elif employee.emprole == 1:
                    return redirect('home_doctor')
                elif employee.emprole == 0:
                    return redirect('home_uketuke')
                else:
                    error_message = '無効な役割です。'
            else:
                error_message = 'パスワードが間違っています。'
        except Employee.DoesNotExist:
            error_message = '従業員IDが存在しません。'

        return render(request, 'sekkei/login.html', {'error_message': error_message})
    return render(request, 'sekkei/login.html')
def logout(request):
    return render(request, 'sekkei/logout.html')
def home_kanrisya(request):
    return render(request, 'sekkei/home_kanrisya.html')


def register_employee(request):
    if request.method == 'POST':
        empid = request.POST['empid']
        empfname = request.POST['empfname']
        emplname = request.POST['emplname']
        emppasswd = request.POST['emppasswd']
        emprole = request.POST['emprole']
        employee = Employee(
            empid=empid,
            empfname=empfname,
            emplname=emplname,
            emppasswd=emppasswd,
            emprole=emprole
        )

        employee.save()

        return redirect('register_success')
    else:
        return render(request, 'sekkei/jugyointouroku.html')


def register_success(request):
    return render(request, 'sekkei/jugyointouroku_success.html')


def juugyouin(request):
    return render(request, 'sekkei/jugyointouroku.html')


def TBL(request):
    shiiregyosha_list = Shiiregyosha.objects.all()
    return render(request, 'sekkei/TBL.html', {'shiiregyosha_list': shiiregyosha_list})

def register_vender(request):
    if request.method == 'POST':
        shiireid = request.POST['shiireid']
        shiiremei = request.POST['shiiremei']
        shiireaddress = request.POST['shiireaddress']
        shiiretel = request.POST['shiiretel']
        shihonkin = request.POST['shihonkin']
        nouki = request.POST['nouki']
        shiiregyosha = Shiiregyosha(
            shiireid=shiireid,
            shiiremei=shiiremei,
            shiireaddress=shiireaddress,
            shiiretel=shiiretel,
            shihonkin=shihonkin,
            nouki=nouki,
        )

        shiiregyosha.save()

        return redirect('vender_success')
    else:
        return render(request, 'sekkei/error.html')
def vender_success(request):
    return render(request,'sekkei/gyoshatuika_success.html')
def recode(request):
    return render(request, 'sekkei/recodetsuika.html')


def search_address(request):
    query = request.GET.get('address', '')
    if query:
        results = Shiiregyosha.objects.filter(shiireaddress__icontains=query)
    else:
        results = []

    return render(request, 'sekkei/search_address.html', {'results': results})


def jusyo(request):
    return render(request, 'sekkei/jusyokensaku.html')


def update_name(request):
    if request.method == 'POST':
        user_id = request.POST['userId']
        new_first_name = request.POST['newFirstName']
        new_last_name = request.POST['newLastName']

        try:
            employee = Employee.objects.get(empid=user_id)
            employee.empfname = new_first_name
            employee.emplname = new_last_name
            employee.save()
        except Employee.DoesNotExist:
            return render(request, 'sekkei/error.html', {'message': 'ユーザーが見つかりません'})

        return render(request, 'sekkei/update_name.html', {
            'userId': user_id,
            'newFirstName': new_first_name,
            'newLastName': new_last_name
        })
    else:
        return redirect('home_kanrisya')


def name(request):
    return render(request, 'sekkei/jugyoinnamehenkou.html')


def home_uketuke(request):
    return render(request, 'sekkei/home_uketuke.html')


def update_password(request):
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        new_password = request.POST.get('newPassword')
        confirm_password = request.POST.get('confirmPassword')

        if not user_id or not new_password or not confirm_password:
            return render(request, 'sekkei/error2.html', {'message': '全てのフィールドを入力してください'})

        if new_password != confirm_password:
            return render(request, 'sekkei/error2.html', {'message': 'パスワードが一致しません'})

        try:
            employee = Employee.objects.get(empid=user_id)
            employee.emppasswd = new_password  # パスワードを更新
            employee.save()
            return render(request, 'sekkei/update_password.html', {'message': 'パスワードが正常に変更されました'})
        except Employee.DoesNotExist:
            return render(request, 'sekkei/error2.html', {'message': 'ユーザーが見つかりません'})

    return redirect('home_uketuke')
def joho(request):
    return render(request, 'sekkei/jugyoinjohohenkou.html')


def register_patient(request):
    if request.method == 'POST':
        patid = request.POST['patid']
        patfname = request.POST['patfname']
        patlname = request.POST['patlname']
        hokenmei = request.POST['hokenmei']
        hokenexp = request.POST['hokenexp']
        patient = Patient(
            patid=patid,
            patfname=patfname,
            patlname=patlname,
            hokenmei=hokenmei,
            hokenexp=hokenexp
        )

        patient.save()

        return redirect('register_success2')
    else:
        return render(request, 'sekkei/kanjatouroku.html')


def register_success2(request):
    return render(request, 'sekkei/kanjatouroku_success.html')


def touroku(request):
    return render(request, 'sekkei/kanjatouroku.html')


def update_hoken(request):
    if request.method == 'POST':
        patid = request.POST.get('patid')
        hokenmei = request.POST.get('hokenmei')
        hokenexp_str = request.POST.get('hokenexp')

        try:
            hokenexp = datetime.strptime(hokenexp_str, '%Y-%m-%d').date()

            patient = Patient.objects.get(patid=patid)
            patient.hokenmei = hokenmei
            patient.hokenexp = hokenexp
            patient.save()
            return redirect('update_success')
        except Patient.DoesNotExist:
            return render(request, 'sekkei/error2.html', {'message': '患者IDが見つかりません'})
        except ValueError:
            return render(request, 'sekkei/error2.html', {'message': '有効な日付を入力してください'})

    return render(request, 'sekkei/update_hoken.html')
def get_hoken_details(request):
    patid = request.GET.get('patid')
    try:
        patient = Patient.objects.get(patid=patid)
        data = {
            'success': True,
            'hokenmei': patient.hokenmei,
            'hokenexp': patient.hokenexp
        }
    except Patient.DoesNotExist:
        data = {'success': False}
    return JsonResponse(data)
def update_success(request):
    return render(request, 'sekkei/update_hoken.html')


def kanri(request):
    return render(request, 'sekkei/kanjakanri.html')


def search_name(request):
    query = request.GET.get('patient-name', '')
    if query:
        results = Patient.objects.filter(patfname__icontains=query) | Patient.objects.filter(patlname__icontains=query)
        result_list = []
        for result in results:
            if isinstance(result.hokenexp, (datetime, date)):
                hokenexp_formatted = result.hokenexp.strftime('%Y-%m-%d')
            else:
                hokenexp_formatted = result.hokenexp
            result_dict = {
                'patid': result.patid,
                'patfname': result.patfname,
                'patlname': result.patlname,
                'hokenmei': result.hokenmei,
                'hokenexp': hokenexp_formatted
            }
            result_list.append(result_dict)
    else:
        result_list = []
    return render(request, 'sekkei/search_name.html', {'results': result_list})


def kensaku(request):
    return render(request, 'sekkei/kanjameikensaku.html')

def home_doctor(request):
    return render(request, 'sekkei/home_doctor.html')

def kensaku2(request):
    patients = Patient.objects.all()
    return render(request, 'sekkei/kanjakensaku.html', {'patients': patients})
def add(request):
    if request.method == "POST":
        patient_id = request.POST['patient_id']
        medicine_id = request.POST['medicine']
        dosage = request.POST['dosage']

        patient = Patient.objects.get(patid=patient_id)
        medicine = Medicine.objects.get(medicineid=medicine_id)

        prescription_data = {
            'patient_id': patient_id,
            'medicine_id': medicine_id,
            'dosage': dosage,
            'medicine_name': medicine.medicinename
        }
        request.session['prescription_data'] = prescription_data

        return redirect('kakutei')

    medicines = Medicine.objects.all()
    for medicine in medicines:
        print(medicine.medicineid)
    return render(request, 'sekkei/kusurishiji.html', {'medicines': medicines})
def shiji(request):
    medicines = Medicine.objects.all()
    return render(request, 'sekkei/kusurishiji.html', {'medicines': medicines})
def kakutei(request):
    try:
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'confirm':
                patient_id = request.POST.get('patient')
                medicine_id = request.POST.get('medicine')
                dosage = request.POST.get('dosage')
                if patient_id and medicine_id and dosage:
                    print(patient_id, medicine_id, dosage)
                    patient = Patient.objects.get(patid=patient_id)
                    medicine = Medicine.objects.get(medicineid=medicine_id)
                    prescription = Prescription(patient=patient, medicine=medicine, dosage=dosage)
                    prescription.save()

                    return redirect('confirm')
                else:
                    return render(request, 'sekkei/error3.html', {'message': '処方情報がありません。'})

            elif action == 'delete':
                if 'prescription_data' in request.session:
                    del request.session['prescription_data']
                return redirect('delete')

            else:
                patient_id = request.POST.get('patient_id')
                medicine_id = request.POST.get('medicine')
                dosage = request.POST.get('dosage')
                return render(request, 'sekkei/kakutei.html', {'patient': patient_id, 'medicine': medicine_id, 'dosage': dosage})
    except Exception as e:
        # 新たな例外が発生した場合にエラーメッセージをログに記録する
        print(f'エラーが発生しました: {str(e)}')
        return HttpResponse('エラーが発生しました。')

def confirm(request):
    return render(request, 'sekkei/confirm.html')
def delete(request):
    return render(request, 'sekkei/delete.html')
def history(request):
    if request.method == "POST":
        patient_id = request.POST['patient_id']

        try:
            patient = Patient.objects.get(patid=patient_id)  # 修正ポイント
            prescriptions = Prescription.objects.filter(patient=patient)

            return render(request, 'sekkei/history.html', {'patient': patient, 'prescriptions': prescriptions})
        except Patient.DoesNotExist:
            # 患者が見つからなかった場合のエラーハンドリング
            pass

    return render(request, 'sekkei/history.html')
def rireki(request):
    return render(request, 'sekkei/rirekikakunin.html')
