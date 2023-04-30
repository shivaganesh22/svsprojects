from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.forms import inlineformset_factory,formset_factory,CheckboxInput
from app.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
# Create your views here.
def home(r):
    return render(r,'index.html')
def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username.title(),password=password)
        if user is not None:
            login(request,user)
            if lambda u:u.is_superuser:
                return redirect('/a')
            else:
                return redirect('home')
        else:
            messages.error(request,"Invalid login credentials")
    return render(request,'signin.html')
def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password1=request.POST['password1']
        if password!=password1 :
            messages.error(request,"Passwords not matches")
        elif User.objects.filter(username=username.title()):
            messages.error(request,"Username already exists...!")
        elif User.objects.filter(email=email):
            messages.error(request,"Email already taken...!")
        elif len(password)<8:
            messages.error(request,"Password must be eight characters")
        else:
            User.objects.create_user(username=username.title(),email=email,password=password)
            user=authenticate(username=username.title(),password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
    return render(request,'signup.html')
def signout(request):
    logout(request)
    return redirect('home')
@login_required
def usrvideos(r):
    videos=Video.objects.all()
    return render(r,'videos.html',{'videos':videos})

#writing Quiz
@login_required
def take_quiz(request, vid,id):
    quiz = Quizs.objects.get(id=id)
    l = Questions.objects.filter(quiz=quiz).count()
    questions = Questions.objects.filter(quiz=quiz)
    student = request.user

    if request.method == "POST":
        score = 0
        for question in questions:
            response = request.POST.get(f"question_{question.pk}")
            k=StudentResponse.objects.filter(student=student,question=question)
            k.delete()
            StudentResponse.objects.create(student=student, question=question, response=response)
            if response == question.answer:
                score += 1
        m=ExamResult.objects.filter(student=student,quiz=quiz)
        m.delete()
        ExamResult.objects.create(student=student, quiz=quiz,total=l, score=score)
        return player(request,vid)

    context = {'quiz': quiz, 'questions': questions}
    return render(request, 'quiz.html', context)

@login_required
def allquizes(r):
    res=Subquery(ExamResult.objects.filter(quiz=OuterRef('pk')).values('quiz').annotate(count=Count('id')).values('count'))
    num_q=Subquery(Questions.objects.filter(quiz=OuterRef('pk')).values('quiz').annotate(count=Count('id')).values('count'))
    videos=Video.objects.filter(quiz=OuterRef('pk'))
    results=ExamResult.objects.filter(quiz=OuterRef('pk'),student=r.user)
    vid_ids=Subquery(videos.values('id')[:1])
    scores=Subquery(results.values('score')[:1])
    k=Quizs.objects.annotate(num_q=num_q,res=res,vid_id=vid_ids,score=scores)
    return render(r,'quizes.html',{'quizes':k})



import re
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build

# def get_video_url(request,file_id):
#     credentials = Credentials.from_authorized_user_info(info=request.session['AIzaSyDd4Rg4lQ2hTe4EFM5UMlUBxEooP1ShB0c'])
#     service = build('drive', 'v3', credentials=credentials)
#     file = service.files().get(fileId=file_id, fields='webContentLink').execute()
#     return file.get('webContentLink')
def get_drive_file_id(drive_link):
    match = re.search(r'([\w-]{25,})', drive_link)
    if match:
        return f"https://drive.google.com/uc?id={match.group(1)}&export=download"
    return drive_link
@login_required
def player(r,id):
    video=Video.objects.get(id=id)
    
    if ExamResult.objects.filter(student=r.user,quiz=video.quiz):
        res=ExamResult.objects.get(student=r.user,quiz=video.quiz)
        
        if res.total==res.score:
            file_id = get_drive_file_id(video.video_url)
            linktype="0"
        else:
            file_id = get_drive_file_id(video.hidden_video_url)
            linktype="hide"
    else:
        file_id = get_drive_file_id(video.hidden_video_url)
        linktype="hide"
    
    return render(r,'player.html',{'video':video,"video_url":file_id,"linktype":linktype})
@login_required
def replayer(r,id):
    video=Video.objects.get(id=id)
    ExamResult.objects.get(student=r.user,quiz=video.quiz).delete()
    if ExamResult.objects.filter(student=r.user,quiz=video.quiz):
        res=ExamResult.objects.get(student=r.user,quiz=video.quiz)
        
        if res.total==res.score:
            file_id = get_drive_file_id(video.video_url)
            linktype="0"
        else:
            file_id = get_drive_file_id(video.hidden_video_url)
            linktype="hide"
    else:
        file_id = get_drive_file_id(video.hidden_video_url)
        linktype="hide"
    
    return render(r,'player.html',{'video':video,"video_url":file_id,"linktype":linktype})

@login_required
def results(r):
    res = ExamResult.objects.filter(student=r.user)
    return render(r,'result.html',{"results":res})





#admin views
@user_passes_test(lambda u:u.is_superuser)
def dashboard(r):
    return render(r,'admin/home.html')

#videos
@user_passes_test(lambda u:u.is_superuser)
def videos(r):
    videos=Video.objects.all()
    return render(r,'admin/videos.html',{'videos':videos})
@user_passes_test(lambda u:u.is_superuser)
def addvideos(r):
    form=VideoForm()
    if r.method=="POST":
        form=VideoForm(data=r.POST,files=r.FILES)
        if form.is_valid():
            form.save()
            if r.POST['quiz']=='':
                return redirect('/a/quiz/add')
            else:
                return redirect('/a/videos')
    return render(r,"admin/addvideos.html",{'form':form})
@user_passes_test(lambda u:u.is_superuser)
def updatevideo(r,id):
    k=Video.objects.get(id=id)
    form=VideoForm(instance=k)
    if r.method=="POST":
        form=VideoForm(data=r.POST,files=r.FILES,instance=k)
        if form.is_valid():
            form.save()
            return redirect('/a/videos')
    return render(r,'admin/editvideo.html',{"form":form})
@user_passes_test(lambda u:u.is_superuser)
def adminplayer(r,id):
    video=Video.objects.get(id=id)
    org = get_drive_file_id(video.video_url)
    hide=get_drive_file_id(video.hidden_video_url)
    
    return render(r,'admin/player.html',{'video':video,"org":org,"hide":hide})

@user_passes_test(lambda u:u.is_superuser)
def deletevideo(r,id):
    k=Video.objects.get(id=id)
    k.delete()
    return redirect('/a/videos')
#quizes
from django.db.models import OuterRef,Count,Subquery

n=10
@user_passes_test(lambda u:u.is_superuser)
def quizes(r):
    global n
    res=Subquery(ExamResult.objects.filter(quiz=OuterRef('pk')).values('quiz').annotate(count=Count('id')).values('count'))
    num_q=Subquery(Questions.objects.filter(quiz=OuterRef('pk')).values('quiz').annotate(count=Count('id')).values('count'))
    k=Quizs.objects.annotate(num_q=num_q,res=res)

    if r.method=="POST":
        n=int(r.POST['num_questions'])
        return redirect('/a/quiz/add')
    return render(r,'admin/quizes.html',{'quizes':k})
@user_passes_test(lambda u:u.is_superuser)
def addquiz(request):
    global n
    quiz_form = QuizForm(request.POST or None)
    questions_formset = inlineformset_factory(Quizs, Questions, fields=('question', 'option1', 'option2', 'option3', 'option4', 'answer'), extra=n,can_delete=True)(request.POST or None, instance=Quizs()) 
    for form in questions_formset:
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
    if request.method == 'POST':
        if quiz_form.is_valid() and questions_formset.is_valid():
            quiz = quiz_form.save()
            questions_formset.instance = quiz
            questions_formset.save()
        return redirect('/a/quizes')
    return render(request,'admin/addquiz.html',{'quiz_form':quiz_form,'questions_formset':questions_formset})
@user_passes_test(lambda u:u.is_superuser)
def updatequiz(r,id):
    quiz = Quizs.objects.get(id=id)
    quiz_form = QuizForm(instance=quiz)
    questions_formset = inlineformset_factory(
        Quizs, Questions, fields=('question', 'option1', 'option2', 'option3', 'option4', 'answer'), extra=5, can_delete=True)(r.POST or None, instance=quiz)
    for form in questions_formset:
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            if isinstance(field.widget, CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
    if r.method == 'POST':
        quiz_form = QuizForm(r.POST, instance=quiz)
        if quiz_form.is_valid() and questions_formset.is_valid():
            quiz_form.save()
            # print(questions_formset)
            questions_formset.save()
            l = Questions.objects.filter(quiz=id).count()
            ExamResult.objects.filter(quiz=id).update(total=l)
            # print(questions_formset)
            return redirect('/a/quizes')
    return render(r,'admin/editquiz.html',{'quiz_form':quiz_form,'questions_formset':questions_formset})
@user_passes_test(lambda u:u.is_superuser)
def deletequiz(r,id):
    k=Quizs.objects.get(id=id)
    s=Questions.objects.filter(quiz_id=id)
    s.delete()
    k.delete()
    return redirect('/a/quizes')
@user_passes_test(lambda u:u.is_superuser)
def exam_results(request, id):
    quiz = Quizs.objects.get(id=id)
    result = ExamResult.objects.filter( quiz=quiz)
    ExamResult.objects.annotate()
    return render(request, 'admin/result.html',{'result':result})
@user_passes_test(lambda u:u.is_superuser)
def responses(request, id):
    exam = ExamResult.objects.get(id=id)
    quiz=Quizs.objects.get(id=exam.quiz.id)
    student = User.objects.get(id=exam.student.id)
    result = ExamResult.objects.get(student=student, quiz=quiz)
    responses = StudentResponse.objects.filter(student=student, question__quiz=quiz)

    context = {'quiz': quiz, 'result': result, 'responses': responses}
    return render(request, 'admin/responses.html', context)

def noquiz(r):
    return redirect('/a/videos')
    
    
