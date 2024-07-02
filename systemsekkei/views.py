from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.db.models import Q
import datetime

from systemsekkei.models import Employee
from systemsekkei.models import Shiiregyosha
from systemsekkei.models import Patient
from systemsekkei.models import Medicine



def index(request):
    return HttpResponse("ようこそ")

def login(request):
    return render(request, 'sekkei/login.html')

def homes(request):
    role = request.POST['role']
    if role == '管理者':
        return render(request, 'sekkei/home_kanrisya.html')
    elif role == '受付':
        return render(request, 'sekkei/home_uketuke.html')
    else:
        return render(request, 'sekkei/home_doctor.html')
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
    return render(request, 'sekkei/TBL.html')

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

        if user_id and new_password:
            try:
                employee = Employee.objects.get(empid=user_id)
                employee.emppasswd = new_password  # パスワードフィールドが `password` だと仮定します
                employee.save()
                return render(request, 'sekkei/update_password.html')
            except Employee.DoesNotExist:
                return render(request, 'sekkei/error2.html', {'message': 'ユーザーが見つかりません'})
        else:
            return render(request, 'sekkei/error2.html', {'message': 'ユーザーIDと新しいパスワードを入力してください'})

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
            # 文字列をdatetime.dateオブジェクトに変換
            hokenexp = datetime.strptime(hokenexp_str, '%Y-%m-%d')

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
def update_success(request):
    return render(request, 'sekkei/update_hoken.html')
def kanri(request):
    return render(request, 'sekkei/kanjakanri.html')

def search_name(request):
    query = request.GET.get('patient-name', '')
    if query:
        results = Patient.objects.filter(patfname__icontains=query, patlname__icontains=query)
        result_list = []
        print(results)
        for result in results:
            print(f'aaa={result.patid}')
            result_dict = {
                'patid': result.patid,
                'patfname': result.patfname,
                'patlname': result.patlname,
                'hokenmei': result.hokenmei,
                'hokenexp': result.hokenexp.strftime('%Y-%m-%d') if isinstance(result.hokenexp,
                                                                               datetime.date) else result.hokenexp
            }
            result_list.append(result_dict)
    else:
        results = Patient.objects.all()
        result_list = []
    print(result_list)
    return render(request, 'sekkei/search_name.html', {'results': results})
def kensaku(request):
    return render(request, 'sekkei/kanjameikensaku.html')

def home_doctor(request):
    return render(request, 'sekkei/home_doctor.html')
def kensaku2(request):
    return render(request, 'sekkei/kanjakensaku.html')

def shiji(request):
    return render(request, 'sekkei/kusurishiji.html')

def sakujo(request):
    return render(request, 'sekkei/kusurisakujo.html')

def kakutei(request):
    return render(request, 'sekkei/kakutei.html')

def rireki(request):
    return render(request, 'sekkei/rirekikakunin.html')