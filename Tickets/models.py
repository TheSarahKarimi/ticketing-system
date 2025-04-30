from django.utils import timezone
from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Ticket (models.Model):
    PRIORITY_CRITICAL = 'P1'
    PRIORITY_HIGH = 'P2'
    PRIORITY_MEDIUM = 'P3'
    PRIORITY_LOW = 'P4'

    STATUS_OPEN = 'open'
    STATUS_IN_PROGRESS = 'progress'
    STATUS_CLOSED = 'closed'

    PRIORITY_CHOICES = [
        (PRIORITY_CRITICAL,'Critical'),
        (PRIORITY_HIGH,'High'),
        (PRIORITY_MEDIUM,'Medium'),
        (PRIORITY_LOW,'Low'),
    ]

    STATUS_CHOICES = [
        (STATUS_OPEN,'Open'),
        (STATUS_IN_PROGRESS,'In Progress'),
        (STATUS_CLOSED,'Closed'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey (settings.AUTH_USER_MODEL, null=False, on_delete=models.CASCADE) 
    title = models.CharField (max_length=255)
    priority = models.CharField (
        max_length=2 , choices=PRIORITY_CHOICES , default=PRIORITY_LOW
        )
    status = models.CharField (
        max_length= 20 , choices=STATUS_CHOICES , default=STATUS_OPEN
        )
    desc = models.TextField()
    is_admin= models.BooleanField(default=False)
    slug = models.SlugField()
    updated_at = models.DateTimeField (auto_now=True)
    created_at = models.DateTimeField (auto_now_add=True)
    completed_at = models.DateTimeField (null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        if self.status == self.STATUS_CLOSED and self.completed_at is None:
            self.completed_at = timezone.now()
        elif self.status != self.STATUS_CLOSED:
            self.completed_at = None
                
        super().save(*args, **kwargs)

    @property
    def name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return self.title

    class Meta():
        unique_together = ('user','title',)
        ordering = ['created_at']


class Comment (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey (settings.AUTH_USER_MODEL,null=False, on_delete=models.CASCADE )
    ticket = models.ForeignKey (Ticket, null=False, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    published_at = models.DateTimeField (auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.ticket.status == Ticket.STATUS_OPEN and self.user.is_staff:
            self.ticket.status = Ticket.STATUS_IN_PROGRESS
            self.ticket.save()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.ticket.title}'

    class Meta:
        ordering = ['published_at']