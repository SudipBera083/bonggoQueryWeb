# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Collaboration, CodeSnippet
from .forms import ProjectForm, CodeSnippetForm

from django.contrib.auth.decorators import user_passes_test



def project_list(request):
    projects = Project.objects.all()
    user_collaborations = Collaboration.objects.filter(user=request.user).values_list('project_id', flat=True)
    
    return render(request, 'collaboration/project_list.html', {
        'projects': projects,
        'user_collaborations': user_collaborations,
    })


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    snippets = project.snippets.all()
    code_form = CodeSnippetForm()

    if request.method == 'POST':
        code_form = CodeSnippetForm(request.POST)
        if code_form.is_valid():
            code_snippet = code_form.save(commit=False)
            code_snippet.project = project
            code_snippet.user = request.user
            code_snippet.save()
            return redirect('Collaboration:project_detail', project_id=project.id)

    return render(request, 'collaboration/project_detail.html', {
        'project': project,
        'snippets': snippets,
        'code_form': code_form,
    })


@user_passes_test(lambda u: u.is_superuser)
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            return redirect('Collaboration:project_list')
    else:
        form = ProjectForm()
    return render(request, 'collaboration/create_project.html', {'form': form})



def join_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    collaboration, created = Collaboration.objects.get_or_create(project=project, user=request.user)
    return redirect('Collaboration:project_list')
