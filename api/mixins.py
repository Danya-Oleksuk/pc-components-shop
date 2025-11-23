class ReadOnlySerializerMixin:
    def create(self, validated_data):
        raise NotImplementedError("This serializer is read-only.")

    def update(self, instance, validated_data):
        raise NotImplementedError("This serializer is read-only.")


class UpdateOnlySerializerMixin:
    def create(self, validated_data):
        raise NotImplementedError("This serializer is update-only.")


class CreateOnlySerializerMixin:
    def update(self, instance, validated_data):
        raise NotImplementedError("This serializer is create-only.")
