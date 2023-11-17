from django.shortcuts import render, redirect
from partnership.forms import FeedbackJobForm, PhotoFormSet
from partnership.models import InfoChairman, FeedbackJob
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def info(request):
    """Главная старница"""
    try:
        info_chairman = InfoChairman.objects.get()
    except InfoChairman.DoesNotExist:
        info_chairman = None
    in_work = FeedbackJob.objects.filter(status='В работе')
    total_in_work = in_work.count()
    status_completed = FeedbackJob.objects.filter(status='Выполнен')
    total_completed = status_completed.count()
    return render(request, 'info.html', {'info_chairman': info_chairman, 'total_in_work': total_in_work, 'total_completed': total_completed, })


def feedback_job_create(request):
    """Создать заявку"""
    info_chairman = InfoChairman.objects.get()
    feedback_limit = info_chairman.feedback_limit
    in_work = FeedbackJob.objects.filter(status='В работе')
    total_in_work = in_work.count()
    status_completed = FeedbackJob.objects.filter(status='Выполнен')
    total_completed = status_completed.count()
    feedback_count_key = 'feedback_count'
    feedback_count = request.session.get(feedback_count_key, 0)
    if request.method == 'POST':
        feedback_job_create_form = FeedbackJobForm(request.POST, request.FILES)
        photo_formset = PhotoFormSet(request.POST, request.FILES, instance=FeedbackJob())
        if feedback_job_create_form.is_valid() and photo_formset.is_valid():
            if feedback_count < feedback_limit:
                feedback_job = feedback_job_create_form.save()
                photo_formset.instance = feedback_job
                photo_formset.save()
                request.session[feedback_count_key] = feedback_count + 1
            else:
                return redirect('feedback_send_limit')
            return redirect('feedback_send')
    else:
        feedback_job_create_form = FeedbackJobForm()
        photo_formset = PhotoFormSet(instance=FeedbackJob())
    context = {
        'feedback_job_create_form': feedback_job_create_form,
        'photo_formset': photo_formset,
        'info_chairman': info_chairman,
        'total_in_work': total_in_work,
        'total_completed': total_completed,
    }
    return render(request, 'feedback_job_create.html', context)


def feedback_send_limit(request):
    """Заявка отправлена"""
    info_chairman = InfoChairman.objects.get()
    in_work = FeedbackJob.objects.filter(status='В работе')
    total_in_work = in_work.count()
    status_completed = FeedbackJob.objects.filter(status='Выполнен')
    total_completed = status_completed.count()
    return render(request, 'feedback_send_limit.html', {'info_chairman': info_chairman, 'total_in_work': total_in_work, 'total_completed': total_completed, })


def feedback_send(request):
    """Заявка отправлена"""
    info_chairman = InfoChairman.objects.get()
    in_work = FeedbackJob.objects.filter(status='В работе')
    total_in_work = in_work.count()
    status_completed = FeedbackJob.objects.filter(status='Выполнен')
    total_completed = status_completed.count()
    return render(request, 'feedback_send.html', {'info_chairman': info_chairman, 'total_in_work': total_in_work, 'total_completed': total_completed, })


def feedback_jobs_status_in_work(request):
    """Заявки в работе"""
    info_chairman = InfoChairman.objects.get()
    in_work = FeedbackJob.objects.filter(status='В работе')
    total_in_work = in_work.count()
    status_completed = FeedbackJob.objects.filter(status='Выполнен')
    total_completed = status_completed.count()
    items_per_page = 5
    paginator = Paginator(in_work, items_per_page)
    page = request.GET.get('page')
    try:
        in_work = paginator.page(page)
    except PageNotAnInteger:
        in_work = paginator.page(1)
    except EmptyPage:
        in_work = paginator.page(paginator.num_pages)
    return render(request, 'feedback_jobs_status_in_work.html', {'info_chairman': info_chairman, 'in_work': in_work, 'total_in_work': total_in_work, 'total_completed': total_completed, })


def feedback_jobs_status_completed(request):
    """Выполненные заявки"""
    info_chairman = InfoChairman.objects.get()
    in_work = FeedbackJob.objects.filter(status='В работе')
    total_in_work = in_work.count()
    status_completed = FeedbackJob.objects.filter(status='Выполнен')
    total_completed = status_completed.count()
    items_per_page = 5
    paginator = Paginator(status_completed, items_per_page)
    page = request.GET.get('page')
    try:
        status_completed = paginator.page(page)
    except PageNotAnInteger:
        status_completed = paginator.page(1)
    except EmptyPage:
        status_completed = paginator.page(paginator.num_pages)

    return render(request, 'feedback_jobs_status_completed.html', {'info_chairman': info_chairman, 'status_completed': status_completed, 'total_in_work': total_in_work, 'total_completed': total_completed, })
