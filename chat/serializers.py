from rest_framework.serializers import ModelSerializer
from .models import Message


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ('author', 'message')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.author:
            ret['author'] = {"id": instance.author.id,
                             "username": instance.author.username}
        return ret
