from django.conf import settings
from django.db import models
from django.utils import timezone

from users.models.users import User


class ContactMessageChoices(models.TextChoices):
    NEW = "new", "New"
    IN_PROGRESS = "in_progress", "In Progress"
    RESOLVED = "resolved", "Resolved"
    CLOSED = "closed", "Closed"


class ContactMessage(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(max_length=64, null=False, blank=False)
    message = models.TextField(max_length=2000, null=False, blank=False)
    status = models.CharField(
        max_length=20,
        choices=ContactMessageChoices.choices,
        default=ContactMessageChoices.NEW,
    )
    response = models.TextField(blank=True)
    answered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="answered_messages",
    )
    answered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Contact Messages"
        verbose_name = "Contact Message"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.name} - {self.email} - {self.status}"

    @property
    def is_new(self):
        return self.status == ContactMessageChoices.NEW

    @property
    def is_in_progress(self):
        return self.status == ContactMessageChoices.IN_PROGRESS

    @property
    def is_resolved(self):
        return self.status == ContactMessageChoices.RESOLVED

    @property
    def is_closed(self):
        return self.status == ContactMessageChoices.CLOSED

    def mark_as_answered(self, response_text: str, user: User) -> None:
        if not response_text.strip():
            raise ValueError("Response text cannot be empty.")

        if not user.is_authenticated:
            raise ValueError("User is not authenticated.")

        if not user.is_staff:
            raise PermissionError("User does not have permission to answer messages.")

        self.response = response_text
        self.answered_at = timezone.now()
        self.answered_by = user
        self.status = ContactMessageChoices.RESOLVED
        self.save()
