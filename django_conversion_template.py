import os
import os.path
# app should be the main Django application
import app.settings
import shutil

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
  help = "One-off script to copy all of /friendlydb into new /friendlydb directory structure"

  def handle(self, **kwargs):
    # Or from wherever this is stored
    originalPath = app.settings.FRIENDLY_DB_PATH
    originalDirs = [o for o in os.listdir(originalPath) if os.path.isdir(os.path.join(originalPath, o))]

    backupPath = originalPath.replace('friendlydb', 'friendlydb_bak')
    try:
      os.rename(originalPath, backupPath)
    except Exception, e:
      print e.message;
      return

    newStructureDirs = [[os.sep.join([a[i:i+2] for i in range(0, len(a), 2)]), a] for a in originalDirs]

    os.mkdir(originalPath)
    for a in newStructureDirs:
      if not os.path.exists(os.path.join(originalPath, a[0])):
        os.makedirs(os.path.join(originalPath, a[0]))
        shutil.copy(os.path.join(backupPath, a[1], 'followers'), os.path.join(originalPath, a[0], 'followers'))
        shutil.copy(os.path.join(backupPath, a[1], 'following'), os.path.join(originalPath, a[0], 'following'))

    shutil.copy(os.path.join(backupPath, 'config.json'), os.path.join(originalPath, 'config.json'))
