from rest_framework import serializers

from .models import User

from validate_email import validate_email

from rest_framework_simplejwt.tokens import RefreshToken, TokenError



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
    username = serializers.CharField()
    email = serializers.EmailField(read_only = True)
    isSupervisor = serializers.SerializerMethodField(read_only = True)
    isIntern = serializers.SerializerMethodField(read_only = True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'isSupervisor', 'isIntern', 'created_at', 'updated_at']
        exclude = ['password']

    def get_isSupervisor(self, obj):                            
        return obj.is_staff
    
    def get_isIntern(self, obj):                            
        return obj.is_intern
    



class UserSerializerWithToken(UserSerializer):
    tokens = serializers.SerializerMethodField(read_only = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'isSupervisor', 'isIntern', 'created_at', 'updated_at', 'tokens']

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
