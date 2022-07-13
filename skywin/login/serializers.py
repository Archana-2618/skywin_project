from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from django.core.exceptions import ValidationError
from uuid import uuid4


class UserSerializer(serializers.ModelSerializer):
    # mobile = serializers.CharField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    #     )
    # user_type =serializers.CharField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    #     )
    # username = serializers.CharField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    #     )
    # password = serializers.CharField(max_length=8)

    class Meta:
        model = User
        fields = ['username','user_type','mobile','password','confirm_password','created_date','updated_date']


class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    mobile = serializers.IntegerField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        mobile = data.get("mobile", None)
        password = data.get("password", None)
        if not mobile and not password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if mobile:
            user = User.objects.filter(
                Q(mobile=mobile) &
                Q(password=password)
                ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(mobile=mobile)
        else:
            user = User.objects.filter(
                Q(mobile=mobile) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(mobile=mobile)
        if user.ifLogged:
            raise ValidationError("User already logged in.")
        user.ifLogged = True
        data['token'] = uuid4()
        user.token = data['token']
        user.save()
        return data

    class Meta:
        model = User
        fields = (
            'mobile',
            'password',
            'token',
        )

        read_only_fields = (
            'token',
        )

class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        user = None
        try:
            user = User.objects.get(token=token)
            if not user.ifLogged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.ifLogged = False
        user.token = ""
        user.save()
        data['status'] = "User is logged out."
        return data

    class Meta:
        model = User
        fields = (
            'token',
            'status',
        )