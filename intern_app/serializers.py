from email.policy import default
from rest_framework import serializers, status
from rest_framework.validators import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User, Task, Attendance

from validate_email import validate_email

import re                                                  
from django.utils.text import slugify




class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)                      

    default_error_messages = {'username': 'The username should only contain alphanumeric characters'}
    email_error_messages = {'email': 'Enter a valid and real email address.'}

    class Meta:
        model = User                                                                                    
        fields = ['email', 'username', 'password']                                                      


    def validate(self, attrs):                                                                          
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():                                               
            raise serializers.ValidationError(self.default_error_messages)

        is_valid = validate_email(email_address= email, check_format= True, check_blacklist= True, check_dns= True, dns_timeout= 10, check_smtp= True, smtp_timeout= 10, smtp_helo_host='my.host.name', smtp_from_address='my@from.addr.ess')
        if is_valid == False:
            raise serializers.ValidationError(self.email_error_messages)

        return attrs                                                                                    

    def create(self, validated_data):                                                                   
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)                                                                           
        if password is not None:
            instance.set_password(password)                                                        
        instance.save()
        return instance




class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only = True)
    email = serializers.EmailField(read_only = True)
    isSupervisor = serializers.SerializerMethodField(read_only = True)
    isIntern = serializers.SerializerMethodField(read_only = True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'isSupervisor', 'isIntern', 'created_at', 'updated_at']

    def get_isSupervisor(self, obj):                            
        return obj.is_staff
    
    def get_isIntern(self, obj):                            
        return obj.is_intern
    


class UserSerializerWithToken(UserSerializer):
    tokens = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'isSupervisor', 'isIntern', 'created_at', 'updated_at', 'tokens']

    def get_tokens(self, obj):
        refresh = RefreshToken.for_user(obj)
        access = RefreshToken.for_user(obj).access_token

        tokens = {
            "refresh": str(refresh),
            "access": str(access)
        }

        return tokens



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {'bad_token': ('Token expired or not valid') }

    def validate(self, attrs):
        self.token = attrs['refresh']                                      
        return attrs                                                        

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()                            
        except TokenError:
            raise serializers.ValidationError('Token expired or not valid')






class TaskSerializer(serializers.ModelSerializer):
    slug = serializers.SerializerMethodField(read_only=True)              # SerializerMethodField() ko help batw model ma nai navako data lai serialize garera frontend ma pathauna cha vani yesari pathauna sakincha
    is_completed = serializers.BooleanField(default=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task
        fields = ['tasktitle', 'assignee', 'assignor', 'slug', 'is_completed', 'created_at', 'updated_at']
        # fields = '__all__'


    def get_slug(self, obj):                    # custom function for SerializerMethodField()
        return slugify(obj.tasktitle)


    def validate(self, validated_data):         # validate() is serializers inbuilt method for validating data before saving into models or tables
        if validated_data.get('tasktitle'):
            tasktitle = validated_data.get('tasktitle')
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

            if len(tasktitle) < 3:
                raise ValidationError(detail="Task Title must be more than 3 characters", code=status.HTTP_406_NOT_ACCEPTABLE) 

            if not regex.search(tasktitle) == None:
                raise ValidationError(detail="Task Title should not contain special characters", code=status.HTTP_406_NOT_ACCEPTABLE)
            
        return validated_data





class AttendanceSerializer(serializers.ModelSerializer):
    date = serializers.DateField(read_only=True)
    status = serializers.BooleanField(read_only=True)
    attendant = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Attendance
        fields = ['user', 'status', 'date', 'work_start_time', 'work_end_time', 'attendant']
        # fields = '__all__'


    def get_attendant(self, obj):                    
        user = obj.user                                         
        serializer = UserSerializer(user, many=False)           
        return serializer.data


    def validate(self, data):
        if data.get('user') == None:
            raise ValidationError(detail="User is required for attendance", code=status.HTTP_406_NOT_ACCEPTABLE)

        if data.get('work_start_time') and data.get('work_end_time'):
            if data['work_start_time'] <= data['work_end_time']:
                raise serializers.ValidationError(detail="Working time does not seems realistic/correct. Re-input it.", code=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            data['work_start_time'] = "11:00:00"
            data['work_end_time'] = "05:00:00"

        return data





    