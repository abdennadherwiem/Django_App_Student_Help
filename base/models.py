from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.db.models import Count
from django.template import loader
from django.shortcuts import render
from django.utils import timezone
from datetime import date
User = get_user_model()

# Create your models here.
class Profile(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user=models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    fname = models.TextField(blank=True)
    lname = models.TextField(blank=True)
    username=models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')

    def __str__(self):
        return(str(self.user)) 
    
    def total_likes_received(self):
        user_posts = Post.objects.filter(author=self)
        total_likes = 0
        for post in user_posts:
            total_likes += post.no_of_likes

        return total_likes



   
    def get_absolute_url(self):
        return reverse('home')

class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
         return f'{self.follower} follows {self.user}'






class Post(models.Model):
    title=models.CharField(max_length=255)
    image=models.ImageField(null=True,blank=True,upload_to="images/")
    title_tag=models.CharField(max_length=255,default="")
    author=models.ForeignKey(Profile,on_delete=models.CASCADE)
    caption=RichTextField(blank=True,null=True)
    post_date=models.DateField(auto_now_add=True)
    reserved_seats = models.IntegerField(default=0)
    
    TYPEPOSTCHOICES = [
        ('offre', 'Offre'),  # Mapping de la valeur numérique 0 à la chaîne 'Offre'
        ('Demande', 'Demande')  # Mapping de la valeur numérique 1 à la chaîne 'Demande'
    ]
    type=models.CharField(max_length=255,choices=TYPEPOSTCHOICES,default="")
     

    no_of_likes=models.IntegerField(default=0)

    def __str__(self):
      return f"{self.title} | {self.author} |{self.type}"


    def get_absolute_url(self):
        return reverse('home')

    def get_owner_pp(self):
        return self.author.profileimg.url

    def profileid(self):
        return self.author.user.id
    




    def get_stage_details(self):
        # Vérifiez d'abord si un stage est lié à ce post
        if hasattr(self, 'stage'):
            stage = self.stage
            stage_details = {
                'societe': stage.societe,
               'type_stage': stage.type_stage,
                'sujet': stage.sujet,
                'contact_info': stage.contact_info,
                'specialiste': stage.specialiste
            }
            return stage_details
        else:
            return None
        
    def get_transport_details(self):
        if hasattr(self, 'transport'):
            transport = self.transport
            transport_details = {
                'depart': transport.depart,
                'destination': transport.destination,
                'heure_depart': transport.heure_depart,
                'nombre_sieges': transport.nombre_sieges,
                'contact_info': transport.contact_info,
                'capacity': transport.capacity,
                'reserved_seats': transport.reserved_seats,
                 'available_seats': transport.available_seats()
            }
            return transport_details
        else:
            return None
    
    def get_logement_details(self):
        if hasattr(self, 'logement'):
            logement = self.logement
            logement_details = {
                'localisation': logement.localisation,
                'description': logement.description,
                'contact_info': logement.contact_info,
                'capacity': logement.capacity,
                'reserved_seats': logement.reserved_seats,
                'available_seats': logement.available_seats()
            }
            return logement_details
        else:
            return None
    
    def get_evenement_details(self):
     if hasattr(self, 'evenement'):
        evenement = self.evenement
        evenement_details = {
            'intitule': evenement.intitule,
            'description': evenement.description,
            'lieu': evenement.lieu,
            'contact_info': evenement.contact_info,
            'capacity': evenement.capacity,
            'reserved_seats': evenement.reserved_seats,
            'available_seats': evenement.available_seats()
        }
        return evenement_details
     else:
        return None
     
from django.db.models.signals import pre_delete
from django.dispatch import receiver
@receiver(pre_delete, sender=Post)
def delete_posts_on_today(sender, instance, **kwargs):
    today = timezone.now().date()
    if instance.post_date == today:
        instance.delete()
    



class Stage(models.Model):
   
    societe = models.CharField(max_length=255)
    TYPESTAGECHOICES=[
        ('ouvrier','ouvrier'),
        ('technicien','technicien'),
        ('PFE','PFE')
    ]
    type_stage = models.CharField(max_length=255,default="")
    sujet = models.TextField()
    contact_info = models.CharField(max_length=255)
    specialiste = models.CharField(max_length=255)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0)
    reserved_seats = models.IntegerField(default=0)

    def available_seats(self):
        return self.capacity - self.reserved_seats

   
    
class Recommandation(models.Model):
    texte = RichTextField(blank=True,null=True)

    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    def __str__ (self):
        return "Text => "+self.texte+"| Post=>"+str(self.post)


class Transport(models.Model):
    depart = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    heure_depart = models.DateTimeField()
    nombre_sieges = models.IntegerField()
    contact_info = models.CharField(max_length=255)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0)
    reserved_seats = models.IntegerField(default=0)

    def available_seats(self):
        return self.capacity - self.reserved_seats
    
    def  __str__ (self):
        return f"Transport de {self.contact_info} partant de {self.depart} pour aller à {self.destination} à {self.heure_depart} avec nombre des sieges est {self.nombre_sieges}."

    
    
    def mark_as_deleted(self):
        """
        Marquer l'événement comme supprimé sans supprimer les réservations associées.
        """
        self.is_deleted = True
        self.save()


class Logement(models.Model):
    localisation = models.CharField(max_length=255)
    description = models.TextField()
    contact_info = models.CharField(max_length=255)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0)
    reserved_seats = models.IntegerField(default=0)
    nombre_sieges = models.IntegerField(null=True) 





    def available_seats(self):
        return self.capacity - self.reserved_seats
    
    def  __str__ (self):
        return "Logement à "+self.localisation+", Description => "+self.description[:30]+"..."
    
    def mark_as_deleted(self):
        """
        Marquer l'événement comme supprimé sans supprimer les réservations associées.
        """
        self.is_deleted = True
        self.save()
 




class Evenement(models.Model):
    intitule = models.CharField(max_length=255)
    description = models.TextField()
    lieu = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    capacity = models.IntegerField(default=0)
    reserved_seats = models.IntegerField(default=0)
    nombre_sieges = models.IntegerField(default=0) 

    def   __str__(self):
        return "Intitule : " + self.intitule + ", Lieu : " + self.lieu + ", Description : " + self.description[:4] 
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    def available_seats(self):
        return self.capacity - self.reserved_seats  # Calcul du nombre de places disponibles
    
    def mark_as_deleted(self):
        """
        Marquer l'événement comme supprimé sans supprimer les réservations associées.
        """
        self.is_deleted = True
        self.save()



class EventSocial(models.Model):
    prix = models.DecimalField(max_digits=8, decimal_places=2)
    evenement = models.OneToOneField(Evenement, on_delete=models.CASCADE)
    def __str__(self):
        return "Inscription pour l'événement : " + self.evenement.intitule + ', Prix : ' + str(self.prix)+'€'

class EventClub(models.Model):
    club = models.CharField(max_length=255)
    evenement = models.OneToOneField(Evenement, on_delete=models.CASCADE)
    def __str__(self):
        return "Adhésion au club de l'évenement : " + self.club + ", " + self.evenement.intitule



class Comment(models.Model):
    post=models.ForeignKey(Post,related_name="comments",on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
  
    body=RichTextField(blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title,self.name)

    def get_absolute_url(self):
        return reverse('home')

class LikePost(models.Model):
    post_id=models.CharField(max_length=500)
    username=models.CharField(max_length=100)

    def __str__(self):
        return self.username
    

class Reservation(models.Model):
  
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Lien vers le profil utilisateur
    date_reserved = models.DateTimeField(auto_now_add=True)
    nb_persons = models.IntegerField(default=1)
    event = models.ForeignKey(Evenement, on_delete=models.CASCADE, default=None, null=True)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, default=None, null=True)
    logement = models.ForeignKey(Logement, on_delete=models.CASCADE, default=None, null=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, default=None, null=True)


    def __str__(self):
        return f"Reservation for {self.nb_persons} persons for {self.post.title}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            if hasattr(self.post, 'evenement'):
                # Si l'objet post a un attribut 'evenement'
                self.post.evenement.reserved_seats += self.nb_persons
                self.post.evenement.save()
            elif hasattr(self.post, 'transport'):
                # Si l'objet post a un attribut 'transport'
                self.post.transport.reserved_seats += self.nb_persons
                self.post.transport.save()
            elif hasattr(self.post, 'logement'):
                # Si l'objet post a un attribut 'transport'
                self.post.logement.reserved_seats += self.nb_persons
                self.post.logement.save()
            elif hasattr(self.post, 'stage'):
                # Si l'objet post a un attribut 'transport'
                self.post.stage.reserved_seats += self.nb_persons
                self.post.stage.save()
        super().save(*args, **kwargs)








class ReservationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Evenement, on_delete=models.CASCADE)  # Importez le modèle Evenement
    reserved_seats = models.IntegerField()
    reservation_date = models.DateTimeField(auto_now_add=True)
    deleted_event = models.BooleanField(default=False)
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, default=None) 
    logement = models.ForeignKey(Logement, on_delete=models.CASCADE, default=None) 
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, default=None) 
    # Ajoutez la valeur par défaut
    def __str__(self):
        return f"Reservation for {self.event} by {self.user} on {self.reservation_date}"
    
    
    @staticmethod
    def get_user_reservation_history(user):
        """
        Méthode statique pour récupérer l'historique des réservations pour un utilisateur donné.
        :param user: L'utilisateur pour lequel récupérer l'historique des réservations.
        :return: Un queryset contenant les réservations de l'utilisateur.
        """
        return ReservationHistory.objects.filter(user=user)
    


class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
   
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} to {self.receiver}"