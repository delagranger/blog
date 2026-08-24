from rest_framework.routers import DefaultRouter
from blog.api_views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = router.urls
