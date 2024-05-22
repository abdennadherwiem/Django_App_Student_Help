from .models import Profile,Post,Comment,Recommandation,Transport,Logement,Evenement,EventSocial,EventClub,Stage,Reservation,PrivateMessage
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class EditProfileNewForm(forms.ModelForm):
     class Meta:
       model=Profile
       fields = ('username','fname','lname','description','profileimg')

       widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'fname':forms.TextInput(attrs={'class':'form-control'}),
            'lname':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
        }

class ProfilePageForm(forms.ModelForm):
    class Meta:
       model=Profile
       fields = ('username','fname','lname','description','profileimg')

       widgets={
          'username':forms.TextInput(attrs={'class':'form-control'}),
          'fname':forms.TextInput(attrs={'class':'form-control'}),
          'lname':forms.TextInput(attrs={'class':'form-control'}),
          'description':forms.Textarea(attrs={'class':'form-control'}), 
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author','type','image','title','caption')

        widgets={
            
            'author':forms.Select(attrs={'class':'form-control'}),
           
             'type': forms.Select(choices=[('offre', 'Offre'), ('Demande', 'Demande')],
                     attrs={'class': 'form-control'}),

             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
              'caption':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content'}),
               
        }





class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['receiver', 'message']

        
class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['societe', 'type_stage', 'sujet', 'specialiste', 'contact_info','capacity']
        widgets = {
            'type_stage': forms.Select(choices=[
                ('ouvrier', 'ouvrier'),
                ('technicien', 'technicien'),
                ('PFE', 'PFE')
            ], attrs={'class': 'form-control'}),
        }


class RecommandationForm(forms.ModelForm):
    class Meta:
        model = Recommandation
        fields = ('texte', 'post')
        widgets={
            
            

              'texte':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content'}),
        }
        
class TransportForm(forms.ModelForm):
    class Meta:
        model = Transport
        fields = ['depart', 'destination', 'heure_depart', 'nombre_sieges', 'contact_info','capacity']
       

        
class LogementForm(forms.ModelForm):
    class Meta:
        model = Logement
        fields = ['localisation', 'description', 'contact_info','capacity','nombre_sieges']


        

class EvenementForm(forms.ModelForm):
    class Meta:
        model = Evenement
        fields = ['intitule', 'description','lieu','contact_info','capacity']


class EventSocialForm(forms.ModelForm):
    class Meta:
        model = EventSocial
        fields = ['prix','evenement']


class EventClubForm(forms.ModelForm):
    class Meta:
        model = EventClub
        fields = ['club','evenement']

class PasswordChangingForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control', 'type':'password'}))
    new_password1=forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))
    new_password2=forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type':'password'}))

    class Meta:
        model= User
        fields = ('old_password','new_password1','new_password2')

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','body')

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'body':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content'}),
            
       }

class EditForm(forms.ModelForm):
    class Meta:
        model=Post
        fields = ('author','type','image','caption')

        widgets={
           
            'author':forms.Select(attrs={'class':'form-control','placeholder':'username'}),
            
           'type': forms.Select(choices=[(1, 'Offre'), (2, 'Demande')],
                                     attrs={'class': 'form-control'}),

            'caption':forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content'}),
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['post', 'author', 'nb_persons']

        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'nb_persons': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
   