from ._base import (
    INSTALLED_APPS,
    GEN_DOC,
)
if GEN_DOC:
    INSTALLED_APPS.append("drf_yasg")

