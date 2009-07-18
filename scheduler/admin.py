from elMonumental.scheduler.models import MatchDay, PlayerProfile, Team, GuestPlayer, Proposal
from django.contrib import admin

class MatchDayAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['start_date', 'location']}),
        ('Participants', {'fields': ['participants', 'guest_stars'], 'classes': ['collapse']}),
    ]
    list_display = ('start_date', 'location', 'isFuture')
    list_filter = ['start_date']
    search_fields = ['location']
    date_hierarchy = 'start_date'

class TeamsInline(admin.StackedInline):
    model = Team
    max_num = 2

class MatchDayAdminWithTeams(MatchDayAdmin):
    inlines = [TeamsInline]

admin.site.register(MatchDay, MatchDayAdmin)
admin.site.register(PlayerProfile)
admin.site.register(GuestPlayer)
admin.site.register(Team)
admin.site.register(Proposal)
admin.site.unregister(MatchDay)
admin.site.register(MatchDay, MatchDayAdminWithTeams)
