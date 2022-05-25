from .views import PostView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("", PostView)

urlpatterns = router.urls
