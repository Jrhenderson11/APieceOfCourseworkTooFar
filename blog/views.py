from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, CV
from .forms import CVForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def cv(request):
    cv = None
    if len(CV.objects.all()) > 0:
        cv = CV.objects.all()[0]
    return render(request, 'blog/cv.html', {'cv':cv})

def cv_edit(request):
    if request.user.is_authenticated:
        cv = None
        if len(CV.objects.all()) > 0:
            cv = CV.objects.all()[0]
        if request.method == "POST":
            form = CVForm(request.POST, instance=cv)
            if form.is_valid():
                cv = form.save(commit=False)
                cv.owner = request.user
                cv.save()
                return redirect('/cv')
        else:
            form = CVForm(instance=cv)
        return render(request, 'blog/cv_edit.html', {'form': form})
    else:
        return redirect('/cv')