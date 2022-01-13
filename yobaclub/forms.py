from django import forms
from yobaclub.models import User, Thing
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth import authenticate, login
from yobaclub.logic.utils.vk_loader import VKLoader
from json import load, dumps


class SignUpForm(forms.Form):
    login = forms.CharField(label="User's login", max_length=25, required=True, min_length=3)
    mail = forms.EmailField(label="User's email", required=True)
    password = forms.CharField(label="User's password", required=True, max_length=200, min_length=8)
    password_confirm = forms.CharField(label="User's password second time", required=True, max_length=200, min_length=8)

    def is_valid(self) -> bool:
        return super().is_valid() and self.cleaned_data.get('password') == self.cleaned_data.get('password_confirm')

    def save_user(self) -> bool:
        try:
            hasher = PBKDF2PasswordHasher()
            login = self.cleaned_data.get("login")
            password = self.cleaned_data.get("password")
            password = hasher.encode(password, hasher.salt())
            email = self.cleaned_data.get("mail")
            user = User(login, password, email)
            user.save()
            return True
        except Exception as e:
            print(e.__repr__())
            return False

class SignInForm(forms.Form):
    login = forms.CharField(label="User's login or email", required=True, min_length=3)
    password = forms.CharField(label="User's password", required=True, max_length=200, min_length=8)
    remember = forms.BooleanField(required=False)

    def process_login(self) -> None:
        if "@" in self.cleaned_data.get("login"):
            self.login_type = "mail"
        else:
            self.login_type = "login"
    
    def login_user(self, request) -> bool:
        data = self.cleaned_data
        user = authenticate(request, login=data.get("login"), login_type=self.login_type, password=data.get("password"))
        if user is not None and request.user.is_anonymous:
            login(request, user)
            if not data.get("remember"):
                request.session.set_expiry(0)
            return True
        return False    

    def is_valid(self) -> bool:
        valid = super().is_valid()
        self.process_login()
        return valid

class PostThingForm(forms.Form):
    title = forms.CharField(label="Name of the thing", max_length=40, required=True)
    description = forms.CharField(label="Description of the thing", required=True)
    thing_files = forms.FileField(label="Files uploaded by poster",
                                  widget=forms.FileInput(attrs={'multiple': True}),
                                  required=False)
    
    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(PostThingForm, self).__init__(*args, **kwargs)

    def split_list(self, list_to_split: list, max_items: int, start_index=0):
        if start_index >= len(list_to_split):
            return []
        splited_list = []
        while True:
            if start_index+max_items >= len(list_to_split):
                splited_list.append(list_to_split[start_index:])
                break
            else:
                splited_list.append(list_to_split[start_index:start_index+max_items])
            start_index+=max_items
        return splited_list

    def process_files(self) -> list:
        saved_files = []
        if self.files.get("thing_files") is None:
            return saved_files
        #MAMU V ENV
        with open('secrets.json', 'r', encoding='utf-8') as f:
            vk_token = load(f).get('vk_save_thing_files_token')
        #MAMU V ENV
        loader = VKLoader(vk_token)
        uploaded_files = self.files.getlist("thing_files")
        uploaded_images = [uploaded_file for uploaded_file in uploaded_files 
                            if uploaded_file.name.split('.') is not None and 
                            len(uploaded_file.name.split('.')) > 1 and
                            uploaded_file.name.split('.')[-1] in ['jpg', 'png', 'jpeg']]
        for image in uploaded_images:
            saving_result = loader.upload_photos(197808880, 276735076, image)
            if saving_result is not None:
                saved_files.append(saving_result)
        uploaded_docs = [uploaded_file for uploaded_file in uploaded_files
                         if uploaded_file.name.split('.') is not None and
                         len(uploaded_file.name.split('.')) > 1 and
                         uploaded_file.name.split('.')[-1] in ['doc', 'docx', 'xls', 'xlsx', 'ppt',
                                                               'pptx', 'rtf', 'pdf', 'gif', 'psd', 
                                                               'djvu', 'fb2', 'ps', 'txt'
                                                               ]]
        for uploaded_doc in uploaded_docs:
            saving_result = loader.upload_file(uploaded_doc, 197808880, uploaded_doc.name)
            if saving_result is not None:
                saved_files.append(saving_result)
        self.saved_files = saved_files

    def save_thing(self) -> bool:
        try:
            title = self.cleaned_data.get('title')
            description = self.cleaned_data.get('description')
            files = dumps(self.saved_files, ensure_ascii=False)
            author = "Аноним" if self.user.is_anonymous else self.user.name
            thing = Thing(title, description, files, author)
            thing.save()
            return True
        except:
            return False

    def is_valid(self) -> bool:
        valid = super().is_valid()
        self.process_files()
        saved = self.save_thing()
        return valid and saved