from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Document
from .forms import DocumentForm


@login_required
def index(request):
    q = request.GET.get('q')
    if q:
        # Flaw 4: SQL injection vulnerability, directly using user input in raw SQL query
        #  -> The fix commented out below
        sql = f"SELECT * FROM docshare_document WHERE ispublic = 1 AND title LIKE '%{q}%' ORDER BY created_at DESC"
        documents = Document.objects.raw(sql)
        #documents = Document.objects.filter(ispublic=True, title__icontains=q).order_by('-created_at')
    else:
        documents = Document.objects.filter(ispublic=True).order_by('-created_at')

    return render(request, 'docshare/pages/index.html', {'documents': documents, 'q': q})

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


# Flaw 1: CSRF vulnerability, fixed by removing the @csrf_exempt decorator
# Flaw 2: Broken Access Control, missing @login_required decorator
@csrf_exempt
def edit(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)

    # Flaw 2: Broken Access Control, not checking if request.user is the owner of the document
    #  -> the fix commented out below
    """
    if document.owner != request.user:
        # redirect to referrer or index if no referrer
        return redirect(request.META.get('HTTP_REFERER', reverse('index')))
    """

    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            document = form.save()
            return redirect('viewdoc', doc_id=document.id)

        return redirect('viewdoc', doc_id=document.id)
    else:
        form = DocumentForm(instance=document)
    return render(request, 'docshare/pages/edit-doc.html', {'form': form})


@login_required
def document_detail(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    back_url = reverse('index')
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


