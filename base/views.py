from multiprocessing import context
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.generic import DetailView,CreateView
from django.contrib.auth.views import PasswordChangeView
from .models import *
from django.urls import reverse_lazy,reverse
from django.views import generic
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from .forms import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EditForm
from django.shortcuts import get_object_or_404

from django.db.models import Q


# Create your views here.
@login_required(login_url='signup')
def home(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    all_users = User.objects.all()
    all_posts=Post.objects.all()
    all_profile=Profile.objects.all()


    # Filtrer les posts par titre et légende
    query = request.GET.get('q')
    if query:
        all_posts = Post.objects.filter(Q(title__icontains=query) | Q(caption__icontains=query))
    else:
        all_posts = Post.objects.all()
        
    count_posts=len(all_posts)

    my_user=[user_profile]
    suggestion_users=[]

    for user in all_profile:
        if user not in my_user:
            suggestion_users.append(user)

    random.shuffle(suggestion_users)


    

# Récupérer les messages privés de l'utilisateur connecté
    messages_received = PrivateMessage.objects.filter(receiver=request.user).order_by('-timestamp')
    # Traiter le formulaire d'envoi de message
    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            recipient_username = form.cleaned_data['receiver']
            try:
                recipient = User.objects.get(username=recipient_username)
                # Check if the sender is following the recipient
                if FollowersCount.objects.filter(follower=request.user.username, user=recipient_username).exists():
                    message.receiver = recipient
                    message.save()
                    return redirect('home')  # Redirect to home after sending the message
                else:
                    messages.error(request, 'You can only send messages to users you are following.')
            except User.DoesNotExist:
                messages.error(request, 'Recipient does not exist.')
    else:
        form = PrivateMessageForm()
    

    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'all_users':all_users,
        'all_posts':all_posts,
        'all_profile':all_profile,
        'count_posts':count_posts,
        'suggestion_users':suggestion_users,

          'messages': messages_received,
        'form': form,
        
    }
    return render(request,"base/home.html",context)

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'base/Otherprofile.html'

    def get_context_data(self,*args,**kwargs):
        context=super(ShowProfilePageView,self).get_context_data(*args,**kwargs)
        page_user=get_object_or_404(Profile,id=self.kwargs['pk'])
        logged_in_user_posts = Post.objects.filter(author=page_user)

    
     


  
    #dd
    

        if FollowersCount.objects.filter(user=page_user).first():
            button_text='UnFollow'
        else:
            button_text='Follow'

        user_followers=len(FollowersCount.objects.filter(user=page_user))
        user_following=len(FollowersCount.objects.filter(follower=page_user))

        num_posts=len(logged_in_user_posts)


     
        context["page_user"]=page_user
        context['logged_in_user_posts']=logged_in_user_posts
        context['num_posts']=num_posts
        context['button_text']=button_text
        context['user_followers']=user_followers
        context['user_following']=user_following

        # Ajouter l'historique des réservations à context
        
        author = self.get_object()
        reservations = author.reservation_set.all()  # Récupérer toutes les réservations de l'auteur
        context['reservations'] = reservations





        return context
    



       
        
    
def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        login_username=request.POST.get('username', None)
        user_password=request.POST["password"]
        user = authenticate(request,username=login_username, password = user_password)
        if user is not None:
            auth_login(request, user)
            messages.add_message(request, messages.INFO, 'You have successfully logged in.')
            return redirect('/')

        else:
            messages.add_message(request, messages.INFO, 'Invalid username or password.')
            return render(request,"base/login.html")

    return render(request,"base/login.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST': 
        email=request.POST['email']
        password=request.POST['password']
        username=request.POST['username']
        email=email.rstrip()

        if email == '' or password == '' or username == '':
            messages.error(request,"Please fill all the fields.")
            return render(request,"base/signup.html")
        
        elif User.objects.filter(username=username).exists(): 
            messages.add_message(request, messages.INFO, 'Username already exists.')
            return render(request,"base/signup.html")
        
        elif User.objects.filter(email=email).exists():
            messages.add_message(request, messages.INFO, 'Email already exists.')
            return render(request,"base/signup.html")

        else :
            user = User.objects.create(email=email, username=username, password=make_password(password))
            user.save() 
            auth_login(request, user)    
            messages.add_message(request, messages.INFO, 'You have successfully signed up.')
            return redirect('/create_profile_page')
    else:
        return render(request,"base/signup.html")
    

def logout(request):
    auth_logout(request)
    return redirect('/')

class FriendView(ListView):
    model = Profile
    template_name = 'base/friends.html'
    profiles=Profile.objects.all()
    ordering = ['-id']

    def get_context_data(self,*args,**kwargs):
        context=super(FriendView,self).get_context_data(*args,**kwargs)
        page_user=get_object_or_404(Profile)
        context["page_user"]=page_user
        return context
    
class AddPostView(CreateView):
      model = Post  # Remplacez YourModel par le nom de votre modèle
      template_name = 'base/add_post.html'  # Remplacez 'base/ajout.html' par le chemin de votre modèle
      form_class = PostForm  # Remplacez PostForm par votre formulaire de création de post
      

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('home')
          

def create_post_and_stage(request):
    
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES)
        stage_form = StageForm(request.POST)
        transport_form = TransportForm(request.POST)
        logement_form = LogementForm(request.POST)
        evenement_form = EvenementForm(request.POST)
        EventClub_form =EventClubForm(request.POST)
        EventSocial_form =EventSocial(request.POST)

        submit_type = request.POST.get('submit_type', None)
        if submit_type == 'post_only':
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user.profile
                post.save()
                return redirect('home')
        elif submit_type == 'post_and_stage':
            if post_form.is_valid() and stage_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user.profile
                post.save()
                stage = stage_form.save(commit=False)
                stage.post = post
                stage.save()
                return redirect('home')
        elif submit_type == 'post_and_transport':
            if post_form.is_valid() and transport_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user.profile
                post.save()
                transport = transport_form.save(commit=False)
                transport.post = post
                transport.save()
                return redirect('home')
        elif submit_type == 'post_and_logement':
            if post_form.is_valid() and logement_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user.profile
                post.save()
                logement = logement_form.save(commit=False)
                logement.post = post
                logement.save()
                return redirect('home')
        
        elif submit_type == 'post_and_evenement':
            if post_form.is_valid() and evenement_form.is_valid():
                post = post_form.save(commit=False)
                post.author = request.user.profile
                post.save()
                evenement = evenement_form.save(commit=False)
                evenement.post = post
                evenement.save()
                return redirect('home')
        elif submit_type == 'post_and_EventClub':
            if evenement_form.is_valid() and EventClub_form.is_valid():
                evenement = evenement_form.save(commit=False)
                evenement.author = request.user.profile
                evenement.save()
                EventClub_form = EventClub_form.save(commit=False)
                EventClub_form.evenement = evenement
                EventClub_form.save()
                return redirect('home')
        elif submit_type == 'post_and_EventSocial':
            if evenement_form.is_valid() and EventSocial_form.is_valid():
                evenement = evenement_form.save(commit=False)
                evenement.author = request.user.profile
                evenement.save()
                EventSocial_form = EventClub_form.save(commit=False)
                EventSocial_form.evenement = evenement
                EventSocial_form.save()
                return redirect('home')
        
            



            
    else:
        post_form = PostForm()
        stage_form = StageForm()
        transport_form = TransportForm()
        logement_form = LogementForm()
        evenement_form = EvenementForm()
        EventClub_form =EventClubForm()
        EventSocial_form =EventSocialForm()
    return render(request, 'base/ajout.html', {'post_form': post_form, 'stage_form': stage_form, 
    'transport_form': transport_form , 'logement_form':logement_form ,'evenement_form':evenement_form, 'EventSocial_form':EventSocial_form,'EventClub_form':EventClub_form})




   

class RecommandationsListView(ListView):
    model = Recommandation
    template_name = 'base/recommandations_list.html'  # Assurez-vous que ce template existe
    context_object_name = 'recommandations'

    
class AddRecommondationView(CreateView):
    model = Recommandation
    form_class = RecommandationForm
    template_name = 'base/add_recommondation.html'

    def get_success_url(self):
        return reverse_lazy('home')
    


class AddTransportView(CreateView):
    model = Transport
    form_class = TransportForm
    template_name = 'base/add_transport.html'
    success_url = reverse_lazy('home')

class TransportListView(ListView):
    model = Transport
    template_name = 'base/transport_list.html'
    context_object_name = 'transports'

    def get_queryset(self):
        queryset = super().get_queryset()  # Obtenez le queryset de base

        # Récupérez la destination à partir des paramètres de requête GET
        destination = self.request.GET.get('destination')

        # Filtrer par destination si une valeur est spécifiée
        if destination:
            queryset = queryset.filter(destination__icontains=destination)

        return queryset

class AddLogementView(CreateView):
    model = Logement
    form_class = LogementForm
    template_name = 'base/add_post.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
class LogementListView(ListView):
    model = Logement
    template_name = 'base/logement_list.html'
    context_object_name = 'logements'  # Assurez-vous de rendre le nom du contexte pluriel

    def get_queryset(self):
        queryset = super().get_queryset()  # Obtenez le queryset de base

        # Récupérez la localisation à partir des paramètres de requête GET
        localisation = self.request.GET.get('localisation')

        # Filtrer par localisation si une valeur est spécifiée
        if localisation:
            queryset = queryset.filter(localisation__icontains=localisation)

        return queryset


#staegeee

class AddStageView(CreateView):
    model = Stage
    form_class = StageForm
    template_name = 'base/addstage.html'

    def get_success_url(self):
        return reverse_lazy('home')

 
class StageListView(ListView):
    model = Stage
    template_name = 'base/stage_list.html'  # Assurez-vous que ce template existe
    context_object_name = 'stages'


class AddEvenementView(CreateView):
    model = Evenement
    form_class = EvenementForm
    template_name = 'base/add_evenement.html'

    def get_success_url(self):
        return reverse_lazy('home')
    

class EvenementListView(ListView):
    model = Evenement
    template_name = 'base/evenement_list.html'
    context_object_name = 'evenements'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('z')
        if query:
            queryset = queryset.filter(Q(intitule__icontains=query) | Q(description__icontains=query) | Q(lieu__icontains=query))
        return queryset



class AddEventSocialView(CreateView):
    model = EventSocial
    form_class = EventSocialForm
    template_name = 'base/add_eventSocial.html'

    def get_success_url(self):
        return reverse_lazy('home')


class EventSocialListView(ListView):
    model = EventSocial
    template_name = 'base/eventSocial_list.html'
    context_object_name = 'eventSocials'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('w')
        prix_min = self.request.GET.get('prix_min')
        prix_max = self.request.GET.get('prix_max')
        if query:
            queryset = queryset.filter(Q(evenement__intitule__icontains=query) | Q(evenement__lieu__icontains=query))
        if prix_min:
            queryset = queryset.filter(prix__gte=prix_min)
        if prix_max:
            queryset = queryset.filter(prix__lte=prix_max)
        return queryset



class AddEventClubView(CreateView):
    model = EventClub
    form_class = EventClubForm
    template_name = 'base/add_eventClub.html'

    def get_success_url(self):
        return reverse_lazy('home')
    
class EventClubListView(ListView):
    model = EventClub
    template_name = 'base/eventClub_list.html'
    context_object_name = 'event_clubs'

    def get_queryset(self):
        queryset = super().get_queryset()
        club_name = self.request.GET.get('club_name')
        if club_name:
            queryset = queryset.filter(club__icontains=club_name)
        return queryset


class CreateProfilePageView(CreateView):
    model = Profile
    form_class=ProfilePageForm
    template_name="base/create_user_profile.html"

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super().form_valid(form)

class EditProfilePageView(generic.UpdateView):
    model = Profile
    form_class=EditProfileNewForm
    template_name='base/edit_profile_page.html'
    success_url=reverse_lazy('home')


def followers_list(request):
    # Retrieve the followers of the current user
    followers = FollowersCount.objects.filter(user=request.user.username)
    return render(request, 'base/home.html', {'followers': followers})


def user_profile(request, username):
    followers = FollowersCount.objects.filter(user=username)
    return render(request, 'base/Otherprofile.html', {'username': username, 'followers': followers})

@login_required
def private_messages(request):
    # Récupérer les messages privés de l'utilisateur connecté
    messages = PrivateMessage.objects.filter(receiver=request.user).order_by('-timestamp')
    return render(request, 'base/private_messages.html', {'messages': messages})


@login_required
def send_private_message(request):
    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            # 'receiver' corresponds to the field name in your form
            recipient_username = form.cleaned_data['receiver']
            recipient = User.objects.get(username=recipient_username)
            # Check if the sender is following the recipient
            if FollowersCount.objects.filter(follower=request.user.username, user=recipient_username).exists():
                message.receiver = recipient
                message.save()
                return redirect('home')  # Redirect to inbox after sending the message
            else:
                # Handle case where sender is not following the recipient
                messages.error(request, 'You can only send messages to users you are following.')
                return redirect('send_private_message')
    else:
        form = PrivateMessageForm()
    return render(request, 'base/send_private_message.html', {'form': form})



class PasswordsChangeView(PasswordChangeView):
       form_class= PasswordChangingForm
       success_url= reverse_lazy('password_success')

def password_success(request):
    return render(request, 'base/password_success.html', {})

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'base/add_comment.html'

    def form_valid(self,form):
        form.instance.post_id=self.kwargs['pk']
        return super().form_valid(form)

@login_required(login_url='signup')
def like_post(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    post=Post.objects.get(id=post_id)
    like_filter=LikePost.objects.filter(post_id=post_id,username=username).first()

    if like_filter==None:
        new_like=LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()

        post.no_of_likes=post.no_of_likes+1
        post.save()
        return redirect('/')

    else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        return redirect('/')

    
@login_required(login_url='signup')
def user_likes(request):
    user = request.user
    
    # Calculer le nombre total de likes reçus par l'utilisateur
    total_likes_received = LikePost.objects.filter(post__author=user).count()

    return render(request, 'Otherprofile.html', {'user': user, 'total_likes_received': total_likes_received})

@login_required(login_url='signup')
def user_profile(request):
    username = request.user.username
    user_likes = LikePost.objects.filter(username=username)
    return render(request, 'base/profile.html', {'user_likes': user_likes})


class DeletePostView(DeleteView):
    model = Post
    template_name = 'base/delete_post.html'
    success_url = reverse_lazy('home')

   

@login_required(login_url='signup')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = Profile.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'base/search.html', { 'user_profile':user_profile,'username_profile_list': username_profile_list,'username_profile':username_profile})


class UpdatePostView(UpdateView):
    model = Post
    form_class=EditForm
    template_name = 'base/update_post.html'

@login_required(login_url='signup')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/')
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/')
    else:
        return redirect('/')



def searchstage(request):
    if request.method == 'POST':
        type_stage = request.POST.get('type_stage', '')  # Récupérer le type de stage depuis le formulaire
        stages = Stage.objects.filter(type_stage=type_stage)  # Filtrer les stages par type
        if not stages:  # Si aucun stage n'est trouvé
            return render(request, 'base/search.html', {})  # Rediriger vers la page de recherche
        else:
            return render(request, 'base/stage_list.html', {'stages': stages})
    else:
        return render(request, 'base/search.html', {})


from django.shortcuts import get_object_or_404
def AddReservationView(request, event_id):
   event = get_object_or_404(Evenement, pk=event_id)
    
   if Reservation.objects.filter(post=event.post, author=request.user.profile).exists():
        return render(request, 'base/error_existing_reservation.html')
    
   if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            nb_persons = form.cleaned_data['nb_persons']
            if nb_persons <= event.capacity - event.reserved_seats + 1:
                reservation = form.save(commit=False)
                reservation.event = event
                reservation.author = request.user.profile  # Assigner l'utilisateur actuel
                reservation.save()
                
                event.reserved_seats += nb_persons
                event.save()
                
                messages.success(request, "Votre réservation a été effectuée avec succès !")
                
                # Ajouter une entrée dans l'historique des réservations
                
                return redirect('home')
            else:
                return render(request, 'base/error_capacity.html')
        else:
            return render(request, 'base/add_reservation.html', {'form': form})
   else:
        form = ReservationForm()
        return render(request, 'base/add_reservation.html', {'form': form})


def AddTransportReservationView(request, transport_id):
      transport = get_object_or_404(Transport, pk=transport_id)
    
      if Reservation.objects.filter(transport=transport, author=request.user.profile).exists():
        return render(request, 'base/error_existing_reservation.html')
    
      if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            nb_persons = form.cleaned_data['nb_persons']
            if  nb_persons <= transport.capacity - transport.reserved_seats + 1:    
                reservation = form.save(commit=False)
                reservation.transport = transport
                reservation.author = request.user.profile
                reservation.save()
                
                transport.reserved_seats += nb_persons
                transport.save()
                
                return redirect('home')
            else:
                return render(request, 'base/error_capacity.html')
        else:
            return render(request, 'base/add_reservation.html', {'form': form})
      else:
        form = ReservationForm()
      return render(request, 'base/add_reservation.html', {'form': form})



def AddStageReservationView(request, stage_id):
      stage = get_object_or_404(Stage, pk=stage_id)
    
      if Reservation.objects.filter(stage=stage, author=request.user.profile).exists():
        return render(request, 'base/error_existing_reservation.html')
    
      if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            nb_persons = form.cleaned_data['nb_persons']
            if  nb_persons <= stage.capacity - stage.reserved_seats + 1:    
                reservation = form.save(commit=False)
                reservation.stage = stage
                reservation.author = request.user.profile
                reservation.save()
                
                stage.reserved_seats += nb_persons
                stage.save()
                
                return redirect('home')
            else:
                return render(request, 'base/error_capacity.html')
        else:
            return render(request, 'base/add_reservations.html', {'form': form})
      else:
        form = ReservationForm()
      return render(request, 'base/add_reservations.html', {'form': form})

def AddLogementReservationView(request, logement_id):
    logement = get_object_or_404(Logement, pk=logement_id)
    
    # Vérifier si l'utilisateur a déjà une réservation pour ce logement
    if Reservation.objects.filter(post=logement.post, author=request.user.profile).exists():
        return render(request, 'base/error_existing_reservation.html')
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            nb_persons = form.cleaned_data['nb_persons']
            # Vérifier si le nombre de places disponibles est suffisant
            if nb_persons <= logement.capacity - logement.reserved_seats:
                reservation = form.save(commit=False)
                reservation.logement = logement
                reservation.author = request.user.profile
                reservation.save()
                
                # Mettre à jour le nombre de places réservées pour le logement
                logement.reserved_seats += nb_persons
                logement.save()
                
                # Vérifier si tous les sièges sont réservés
              
                
                return redirect('home')
            else:
                # Gérer le cas où le nombre de places est insuffisant
                return render(request, 'base/error_capacity.html')
        else:
            # Gérer le cas où le formulaire n'est pas valide
            return render(request, 'base/add_reservationl.html', {'form': form})
    else:
        form = ReservationForm()
    return render(request, 'base/add_reservationl.html', {'form': form})


from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation


def cancel_reservation(request, reservation_id):


    reservation = get_object_or_404(Reservation, pk=reservation_id)



    reservation.delete()
    if request.method == 'POST':
        # Annuler la réservation
       
        
        # Récupérer l'objet Evenement associé à la réservation annulée
        event = reservation.event
     
        # Réduire le nombre de sièges réservés dans l'événement
        if event:
            event.reserved_seats -= reservation.nb_persons
            event.save()
        
        # Récupérer l'objet Transport associé à la réservation annulée
        transport = reservation.transport
        if transport:
             transport.reserved_seats -= reservation.nb_persons
             transport.save()

        logement = reservation.logement
        if logement:
            logement.reserved_seats -= reservation.nb_persons
            logement.save()



        stage = reservation.stage
        if stage:
            stage.reserved_seats -= reservation.nb_persons
            stage.save()
            

        # Redirection vers une vue de confirmation ou autre
        return redirect('home')
        
def make_reservation(request, post_id):
    post = Post.objects.get(pk=post_id)
    # Logique pour vérifier la capacité restante
    if post.reserved_seats < post.capacity:
        # Effectuez la réservation et mettez à jour reserved_seats
        post.reserved_seats += 1
        post.save()