from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from models import GameTask

@permission_required('private_api.change_gametask')
def gametask_api(request, game_name, task_id, status):
    try:
        game = GameTask.objects.get(pk=task_id)
        if game.game.name != game_name:
            return HttpResponse('Name mismatch')
            # Naughty player. Log this.
            return
        
        if status not in [GameTask.START, GameTask.INPROGRESS, GameTask.SUCCESS, GameTask.FAIL]:
            return HttpResponse('Status mismatch')
            # Coding error? Log this.
            return
        
        game.status = status
        game.save()
    except GameTask.DoesNotExist:
        # Log this. Access to an object that does not exist?
        pass
    except GameTask.MultipleObjectsReturned:
        # Log this. Too many objects? Waaaat? By a key?
        pass
    
    return HttpResponse('Success')