from django.db.models import Q
from rest_framework.exceptions import ParseError
from rest_framework.permissions import BasePermission

from my_app.models import Interest


class HasInterestAccess(BasePermission):
    def __init__(
        self, interest_id_kwarg="interest_pk", sent_by=False, sent_to=False
    ) -> None:
        self.interest_id_kwarg = interest_id_kwarg
        self.sent_by = sent_by
        self.sent_to = sent_to

    def has_permission(self, request, view):
        interest_id = view.kwargs.get(self.interest_id_kwarg, None)
        if interest_id is None:
            raise ParseError("interest_id is required")
        if not interest_id.isdigit():
            raise ParseError("interest_id is must be a int")

        try:
            if self.sent_by:
                Interest.objects.get(sent_by=request.user, id=interest_id)
            elif self.sent_to:
                Interest.objects.get(sent_to=request.user, id=interest_id)
            else:
                Interest.objects.get(
                    Q(sent_by=request.user) | Q(sent_to=request.user), id=interest_id
                )
            return True
        except Interest.DoesNotExist:
            return False
