from rest_framework.routers import DefaultRouter
from blog.api_views import PostViewSet, CommentViewSet, TagViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"tags", TagViewSet)

urlpatterns = router.urls
