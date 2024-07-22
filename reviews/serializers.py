from rest_framework import serializers
from .models import CustomerReportRecord
from .models import Comment


class CustomerReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerReportRecord

    def validate_title(self, value):
        # field-level validation
        if 'django' not in value.lower():
            raise serializers.ValidationError("error message")

        return value

    def validate(self, data):
        # object-level validation
        if data['start'] > data['finish']:
            raise serializers.ValidationError("finish must occur after start")
        return data

    def create(self, validated_data):
        # Overriding Serializer Methods : If we want to be able to return complete object instances
        # based on the validated data we need to implement one or both of the create() and update()
        # methods to our Serializer subclass.
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Overriding Serializer Methods : If we want to be able to return complete object instances
        # based on the validated data we need to implement one or both of the create() and update()
        # methods to our Serializer subclass.
        instance.email = validated_data.get('email', instance.email)
        instance.title = validated_data.get('content', instance.title)
        instance.save()
        return instance