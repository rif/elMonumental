from scheduler.models import MatchDay, PlayerProfile, Team, GuestPlayer, Proposal, Sport
from django.contrib import admin

class MatchDayAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['start_date', 'location', 'sport_name']}),
        ('Participants', {'fields': ['participants', 'guest_stars'], 'classes': ['collapse']}),
    ]
    list_display = ('start_date', 'sport_name','location', 'isFuture')
    list_filter = ['start_date', 'sport_name']
    search_fields = ['location', 'sport_name']
    date_hierarchy = 'start_date'

class TeamAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'matchday']}),
        ('Participants', {'fields': ['participants', 'guest_stars'], 'classes': ['collapse']}),
    ]

class GuestPlayerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']

class TeamsInline(admin.TabularInline):
    model = Team
    max_num = 2
    raw_id_fields = ('participants', 'guest_stars')

class MatchDayAdminWithTeams(MatchDayAdmin):
    inlines = [TeamsInline]

admin.site.register(MatchDay, MatchDayAdmin)
admin.site.register(PlayerProfile)
admin.site.register(GuestPlayer, GuestPlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Proposal)
admin.site.register(Sport)
admin.site.unregister(MatchDay)
admin.site.register(MatchDay, MatchDayAdminWithTeams)

