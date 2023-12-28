from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat')  
    else:
        form = AuthenticationForm()
    return render(request, 'reg/login.html', {'form': form})
@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat') 
    else:
        form = UserCreationForm()
    return render(request, 'reg/signup.html', {'form': form})

@csrf_exempt
@login_required
def chat(request):
    alpha =[]
    timeout = 30
    for i in range(97,97+26,1):                      
            alpha.append(chr(i))
    if request.method == 'POST':
        user = request.user
        user_message = request.POST.get('user_message')
        messages = Message.objects.filter(user=user).order_by('-time')
        previous_message_time = messages.first().time if messages.exists() else None
        words = transform1('myapp/templates/reg/words.txt',alpha)
        user_score =0
        com_score =0
        if previous_message_time:
            user_score=messages.first().user_score
            com_score = messages.first().computer_score
            
        user_content = Message.objects.filter(user=user).values_list('content', flat=True)
        user_computer_response = Message.objects.filter(user=user).values_list('computer_response', flat=True)    
        com_word = transform2(user_message.lower(), words,alpha,user_content,user_computer_response)
        if com_word == " ":
            computer_response = f"You lose.<br>Because of illegal word <q>{user_message}</q>"
            return JsonResponse({'status': 'fail', 'message': user_message, 'term_message': computer_response,'compliment': "Computer has won the game"})
        
        if com_word is None:
            return JsonResponse({'status': 'fail', 'message': user_message, 'term_message': computer_response,'compliment': f"{user.username}won the game"})
        existing_content = Message.objects.filter(user=request.user,content=user_message.lower()).exists()
        existing_computer_response = Message.objects.filter(user=request.user,computer_response=user_message.lower()).exists()
        
        if previous_message_time:
            current_time = timezone.now()
            time_difference = current_time - previous_message_time
            if time_difference.total_seconds() > timeout:
                computer_response = f"You lose.<br>Because you took {time_difference.total_seconds()} s extra time"
                return JsonResponse({'status': 'fail', 'message': user_message, 'term_message': computer_response,'compliment': "Computer has won the game By Default"})
            
        if previous_message_time:
            if not messages.first().computer_response[-1].lower() == user_message[0].lower():
                computer_response = f"You lose.<br>Because Starting letter of <q>{user_message}</q> and last letter of <q>{messages.first().computer_response}</q> is different"
                return JsonResponse({'status': 'fail', 'message': user_message, 'term_message': computer_response, 'compliment': "Computer has won the game By Default"})
        
        if existing_content or existing_computer_response:
            computer_response = f"You lose.<br>Because <q>{user_message}</q> already used"
            return JsonResponse({'status': 'fail', 'message': user_message, 'term_message': computer_response,'compliment': "Computer has won the game By Default"})
        computer_response = f"{com_word}"

        Message.objects.create(user=user, content=user_message.lower(), computer_response=computer_response.lower(),computer_score=com_score+len(com_word),user_score=user_score+len(user_message))
        return JsonResponse({'status': 'success', 'message': user_message, 'computer_response': computer_response,'comp':com_score+len(com_word),'usr':user_score+len(user_message)})
    messages = Message.objects.filter(user=request.user).delete()
    return render(request, 'reg/chat.html', {'messages': messages,'valid':True})

def transform1(file,alpha):                           
        f1 = open(file,'r')
        list1 = f1.read().split('\n')
        list2 = []
        for j in range(0,26,1):
            temp_list = []
            for i in range(0,len(list1),1):
                if list1[i][0] == alpha[j]:
                    temp_list.append (list1[i])
            list2.append(temp_list) 
        return list2

def transform2(word, list1,alpha,user_content,user_computer_response):
        lastchar = word[-1]
        if word.isalpha():
            pos = alpha.index(lastchar)
            templist = list1[pos]
            content =user_content
            computer_response =user_computer_response
            max_size_word = " "
            for new_word in templist:
                if new_word not in content and new_word not in computer_response:
                    if len(new_word) > len(max_size_word):  #this is for best case
                        max_size_word = new_word
            if max_size_word == " ":
                return None        
        else:
            return " "
        return max_size_word 
        