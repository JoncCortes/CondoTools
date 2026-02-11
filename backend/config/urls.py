from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.accounts.views import UserViewSet
from apps.announcements.views import AnnouncementViewSet
from apps.audit.views import AuditLogViewSet
from apps.common.dashboard import DashboardSummaryView
from apps.common_areas.views import CommonAreaViewSet
from apps.condominiums.views import CondominiumViewSet
from apps.incidents.views import IncidentViewSet
from apps.packages.views import PackageViewSet
from apps.reservations.views import ReservationViewSet
from apps.residents.views import ResidentViewSet
from apps.settings_menu.views import (
    CustomPageViewSet,
    MenuCategoryViewSet,
    MenuItemViewSet,
    PublicCustomPageViewSet,
    PublicMenuViewSet,
)
from apps.staff.views import StaffViewSet
from apps.units.views import UnitViewSet
from apps.visit_logs.views import VisitLogViewSet
from apps.visitors.views import VisitorViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("condominiums", CondominiumViewSet, basename="condominiums")
router.register("units", UnitViewSet, basename="units")
router.register("residents", ResidentViewSet, basename="residents")
router.register("staff", StaffViewSet, basename="staff")
router.register("visitors", VisitorViewSet, basename="visitors")
router.register("visit-logs", VisitLogViewSet, basename="visit-logs")
router.register("packages", PackageViewSet, basename="packages")
router.register("announcements", AnnouncementViewSet, basename="announcements")
router.register("incidents", IncidentViewSet, basename="incidents")
router.register("common-areas", CommonAreaViewSet, basename="common-areas")
router.register("reservations", ReservationViewSet, basename="reservations")
router.register("audit-logs", AuditLogViewSet, basename="audit-logs")
router.register("settings/menu-categories", MenuCategoryViewSet, basename="menu-categories")
router.register("settings/menu-items", MenuItemViewSet, basename="menu-items")
router.register("settings/custom-pages", CustomPageViewSet, basename="custom-pages")
router.register("menu", PublicMenuViewSet, basename="public-menu")
router.register("pages", PublicCustomPageViewSet, basename="public-pages")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/dashboard/summary/", DashboardSummaryView.as_view(), name="dashboard-summary"),
    path("api/", include(router.urls)),
]
