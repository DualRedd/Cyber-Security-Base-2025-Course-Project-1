from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Document
from .forms import DocumentForm


@login_required
def index(request):
    documents = Document.objects.order_by('-created_at')
    return render(request, 'docshare/pages/index.html', {'documents': documents})

@login_required
def mypage(request):
    documents = Document.objects.filter(owner=request.user).order_by('-created_at')
    return render(request, 'docshare/pages/my-page.html', {'documents': documents})

@login_required
def create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.owner = request.user
            doc.save()
            return redirect('mypage')
    else:
        form = DocumentForm()
    return render(request, 'docshare/pages/create-doc.html', {'form': form})


@login_required
def document_detail(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    back_url = request.META.get('HTTP_REFERER', reverse('index'))
    return render(request, 'docshare/pages/document-detail.html', {'document': document, 'back_url': back_url})

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'docshare/registration/register.html', {'form': form})


