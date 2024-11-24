from django.db.models import Func
from django.db.models.expressions import RawSQL


class AllClients(Func):
    function = 'all_clients'
    template = '%(function)()'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def as_sql(self, compiler, connection):
        return RawSQL(self.template, [])
