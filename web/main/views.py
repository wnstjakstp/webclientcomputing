from django.shortcuts import render,get_object_or_404,redirect
from .models import Lecture, Comment, UserLecture
from django.core.paginator import Paginator
from django.db.models import Avg, Q
from .forms import CommentForm, LectureFilterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    recommended_lectures = None  # 추천 강의
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        # 사용자의 skill, level, language를 기반으로 강의 필터링
        user_skill = request.user.profile.skill
        user_level = request.user.profile.level
        user_language = request.user.profile.language
        
        # 조건에 맞는 강의를 최대 8개까지 가져옵니다.
        # 여기서는 Q 객체를 사용하여 skill, level, 또는 language 중 하나라도 일치하면 추천
        recommended_lectures = Lecture.objects.filter(
            Q(skill=user_skill) | Q(level=user_level) | Q(language=user_language)
        )[:6]
    
    lectures = Lecture.objects.all()
    paginator = Paginator(lectures, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/home.html', {'page_obj': page_obj, "recommended_lectures": recommended_lectures})


def detail(request, lecture_id):

    lecture = get_object_or_404(Lecture, pk=lecture_id)
    user_lecture = UserLecture.objects.filter(user=request.user, lecture=lecture).first()
    comments = Comment.objects.filter(lecture=lecture)
    # 뷰에서는 'lecture' 변수명을 사용하여 템플릿에 전달합니다.
    average_rating = calculate_average_rating(lecture)

    return render(request, 'main/detail.html', {'lecture': lecture,"comments":comments, 'average_rating': average_rating,'user_lecture': user_lecture} )

def calculate_average_rating(lecture):
    # 주어진 강의에 대한 모든 후기의 평균 평점 계산
    comments = lecture.comment_set.all()  # 해당 강의에 대한 모든 후기 가져오기
    average_rating = comments.aggregate(Avg('rating'))['rating__avg']  # 후기들의 평점의 평균 계산
    
    # 만약 후기가 없는 경우를 고려하여 None을 반환하거나 평균값을 소수 둘째 자리까지 반올림하여 반환합니다.
    return round(average_rating, 2) if average_rating is not None else None


def create_comment(request, lecture_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        rating = request.POST.get('rating')  # 평점 받아오기

        comment = Comment()
        comment.content = content
        comment.rating = rating
        comment.lecture = get_object_or_404(Lecture, pk=lecture_id)
        comment.user = request.user
        comment.save()

        return redirect('detail', lecture_id)
    else:
        return HttpResponseNotAllowed(['POST'])


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    lecture_id = comment.lecture.id
    comment.delete()
    return redirect('detail', lecture_id=lecture_id)




def update(request, comment_id):
    old_comment = get_object_or_404(Comment, pk=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=old_comment)
        if form.is_valid():
            form.save()
            return redirect('detail', old_comment.lecture_id)
    else:
        form = CommentForm(instance=old_comment)
    return render(request, 'main/edit.html', {'form': form, 'old_comment': old_comment, 'comment_id': comment_id,'lecture_id': old_comment.lecture_id})

def new_comment(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    return render(request, 'main/new_comment.html', {'lecture':lecture})

@login_required
def add_lecture(request, lecture_id):
    # 사용자가 해당 강의를 이미 듣고 있는지 확인
    if not UserLecture.objects.filter(user=request.user, lecture_id=lecture_id).exists():
        # 사용자가 해당 강의를 듣고 있지 않으면 추가
        UserLecture.objects.create(user=request.user, lecture_id=lecture_id)
        messages.success(request, '강의가 성공적으로 추가되었습니다.')
    else:
        messages.error(request, '이미 해당 강의를 듣고 있습니다.')

    return redirect('user_lectures')

@login_required
def user_lectures(request):
    # 현재 사용자의 강의 목록을 가져오는 로직
    user_lectures = UserLecture.objects.filter(user=request.user)
    return render(request, 'main/my_lecture.html', {'user_lectures': user_lectures})


@login_required
def delete_my_lecture(request, user_lecture_id):
    # UserLecture 객체의 pk로 객체를 가져옵니다. 인자 이름을 lecture_id에서 user_lecture_id로 변경했습니다.
    user_lecture = get_object_or_404(UserLecture, pk=user_lecture_id)

    # 현재 로그인한 사용자와 담은 강의의 사용자가 일치하는지 확인
    if user_lecture.user == request.user:
        lecture_id = user_lecture.lecture.id  # 강의의 ID를 정확히 참조합니다.
        user_lecture.delete()
        
        return redirect('user_lectures')
    



def lecture_list(request):
    form = LectureFilterForm(request.GET or None)
    filtered = False  # 검색이 이루어졌는지를 확인하는 변수

    lectures = Lecture.objects.all()  # 기본적으로 모든 강의를 가져옴

    if request.GET:  # 만약 GET 요청에 데이터가 있다면, 즉 검색이 이루어졌다면
        filtered = True  # 검색이 이루어졌다고 표시
        if form.is_valid():
            level = form.cleaned_data.get('level')
            skill = form.cleaned_data.get('skill')
            language = form.cleaned_data.get('language')

            if level and level != 'all':
                lectures = lectures.filter(level=level)
            if skill and skill != 'all':
                lectures = lectures.filter(skill=skill)
            if language and language != 'all':
                lectures = lectures.filter(language=language)

    context = {
        'form': form,
        'lectures': lectures,
        'filtered': filtered,  # 템플릿에서 검색이 이루어졌는지 여부를 확인하기 위해 context에 추가
    }
    return render(request, 'main/filter.html', context)

def ai(request):
    return render(request, 'main/ai.html')

def learn(request):
    return render(request, 'main/learn.html')
    