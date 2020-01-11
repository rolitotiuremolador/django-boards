from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse, Http404
from boards.models import Board, Topic, Post
from django.contrib.auth.models import User
from .forms import NewTopicForm

# Create your views here.
def home(req):
    # return HttpResponse("Hello World!")
    boards = Board.objects.all()
    # boards_names = list()
    # for board in boards:
    #     boards_names.append(board.name)
    # res = '<br>'.join(boards_names)
    # return HttpResponse(res)
    return render(req, "home.html", {'boards':boards})

def board_topics(req, pk):
    board = get_object_or_404(Board, pk=pk)
    # try:
    #     board = Board.objects.get(pk=pk)
    # except Board.DoesNotExist:
    #     raise Http404
    return render(req, 'topics.html', {'board':board})

def new_topic(req, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first() #TODO: get the currently logged in user

    if req.method == 'POST':
        form = NewTopicForm(req.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = user
            )
            # subject = req.POST['subject']
            # message = req.POST['message']

            # user = User.objects.first() #TODO: get the currently loggedin user

            # topic = Topic.objects.create(
            #     subject = subject,
            #     board = board,
            #     starter=user
            # )

            # post = Post.objects.create(
            #     message = message,
            #     topic = topic,
            #     created_by =user
            # )
            
            return redirect('board_topics', pk=board.pk) #TODO: to redirect the created topic page
    else:
        form = NewTopicForm()
    return render(req, 'new_topic.html', {'board': board, 'form':form})
