from peewee_migrate import Router
from db import models

router = Router(models.db)
router.create(auto=models)
router.run()
