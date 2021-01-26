from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm
from django.views.generic import ListView,DetailView
from .models import Post,Comment

# Create your views here.
def signup(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=raw_password)
                
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse('registration failed')
                
    else:
        form=UserCreationForm()
    return render(request,'signup.html',{'form':form})




def logout(request):
    if request.method=='POST':
        logout(request)
        return HttpResponseRedirect('login')


def home(request):
    #return HttpResponse('this is HOME of {{request.user.username}} <p>Your Username is : {{request.user}} </p>')
    return render(request, 'index.html', {
        'user': request.user,
        })



def newpost(request):
    if request.method=='POST':
        form=PostForm(request.POST)
        if form.is_valid:
            p=form.save(commit=False)
            p.author=request.user
            form.save()
            return redirect('postsbyauthor')

    else:
        form=PostForm()
    return render(request,'createpost.html',{'form':form})



def newcomment(request,pk):
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid:
            c=form.save(commit=False)
            c.c_author=request.user
            c.post=Post.objects.get(pk=pk)
            #c.post=Post.objects.get(pk=self.kwargs.get('pk'))
            #c.post=get_object_or_404(Post,pk=self.kwrgs['pk'])
            form.save()
            return redirect('postdetail',pk=pk)

    else:
        form=CommentForm()
    return render(request,'createcomment.html',{'form':form})





class PostList(ListView):
    queryset=Post.objects.all().order_by('likes')
    template_name='blogpage.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['user_context'] = self.request.user
        return context


class PostDetail(DetailView):
    model=Post
    template_name='postpage.html'

class PostListbyAuthor(ListView):
    model=Post
    template_name='postsbyauthor.html'
    

    def get_queryset(self):
        """
        Return list of Blog objects created by BlogAuthor (author id specified in URL)
        """
        id = self.kwargs['pk']
        target_author=get_object_or_404(User, pk = id)
        return Post.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['author_context'] = get_object_or_404(User, pk = self.kwargs['pk'])
        return context

