from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        # fields = ['id','username', 'password', 'name', 'phone_number', 'email']
        fields = ['id','username', 'password','email']



class CustomUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    
    def __init__(self, *args, **kwargs):
        # Check if the serializer is being used for an update
        is_update = kwargs.get('context', {}).get('request') and kwargs['context']['request'].method == 'PUT'

        # Conditionally set required=False for password during updates
        if is_update:
            self.fields['password'].required = False

        super().__init__(*args, **kwargs)
    
    def create(self, validated_data):
        # Extract the password from validated_data
        password = validated_data.pop('password', None)
        # Create the user instance
        user = super().create(validated_data)
        # Hash the password and save the user
        if password is not None:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
    # Remove the 'password' key from the validated_data before updating
        password = validated_data.pop('password', None)

        # Call the parent class's update method
        instance = super().update(instance, validated_data)

        # If a new password is provided, update it separately
        if password is not None:
            instance.set_password(password)
            instance.save()

        return instance
