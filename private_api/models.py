from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Game(models.Model):
    name = models.CharField(max_length=16, unique=True)
    
    def __unicode__(self):
        return self.name
    
class GameTaskManager(models.Manager):
    def start_game(self, user, game_name):
        try:
            game = Game.objects.get(name=game_name)
            task = GameTask(user=user, game=game, status=GameTask.START)
            task.save()
        except Game.DoesNotExist:
            # Log this.
            pass
        except Game.MultipleObjectsReturned:
            # Log this. Should be completely impossible.
            pass

class GameTask(models.Model):
    START = 'S'
    INPROGRESS = 'I'
    SUCCESS = 'U'
    FAIL = 'F'
    
    STATUS_CHOICES = (
        (START, 'Start'),
        (INPROGRESS, 'In Progress'),
        (SUCCESS, 'Success'),
        (FAIL, 'Failed'),
    )
    
    objects = GameTaskManager()
    
    user = models.ForeignKey(User)
    game = models.ForeignKey(Game)
    
    start_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=START)
    
    def __unicode__(self):
        return str(self.id) + ": " + self.user.username + " playing: " + self.game.name
