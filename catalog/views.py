from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Sum, Count, Max
from django.views import generic
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Add models here
from catalog.models import PlayerModel, Rd1HoleModel, Rd1SlotModel, Rd1ScoreModel, Rd1StablefordModel, Rd2HoleModel, Rd2SlotModel, Rd2ScoreModel, Rd2StablefordModel, Rd3HoleModel, Rd3SlotModel, Rd3ScoreModel, Rd3StablefordModel, Rd4HoleModel, Rd4SlotModel, Rd4ScoreModel, Rd4StablefordModel, EventEntryModel, LeaderBoardModel, SportsTippingModel,SportsTippingResultsModel, SportsTippingScoreModel, FridaySocialModel, TourAgendaModel, TopGolfModel, RacingModel
# Add forms here
from catalog.forms import Rd1ScoreForm, Rd2ScoreForm, Rd3ScoreForm, Rd4ScoreForm, SportsTippingForm, FridaySocialForm, SaturdaySocialForm

def login (request):
    """View function for login of site."""
    # Define views here
    context = {}
    return render(request, 'login.html', context=context)

def landingpage (request):
    """View function for login of site."""
    # Define views here
    context = {}
    return render(request, 'landingPage.html', context=context)

def fullleaderboard (request):
    """Define function for leaderboard view"""
    # Define views here
    score_submit = EventEntryModel.objects.exclude(winner__isnull=True).count()
    active_players = PlayerModel.objects.all()

    loaded_points = list(EventEntryModel.objects.aggregate(Sum('points')).values())[0]
    awarded_points = list(EventEntryModel.objects.exclude(winner__isnull=True).aggregate(Sum('points')).values())[0]

    context = {
    'score_submit': score_submit,
    'active_players': active_players,
    'loaded_points': loaded_points,
    'awarded_points': awarded_points,
    }

    return render(request, 'fullLeaderboard.html', context=context)

def scoringpage (request):
    """View function for login of site."""
    # Define views here
    context = {}
    return render(request, 'scoringPage.html', context=context)

def playerdetail (request,name):
    """View function showing individual player's results"""

    #Basic player details
    player_image = PlayerModel.objects.get(name=name).image
    player_HC = PlayerModel.objects.get(name=name).HC
    player_highfinish = PlayerModel.objects.get(name=name).highfinish
    player_tournum = PlayerModel.objects.get(name=name).tournum
    player_totalpoints = LeaderBoardModel.objects.get(player=name).overall_total
    player_totalrank = LeaderBoardModel.objects.filter(overall_total__gt=player_totalpoints).count() + 1


    target_holes = 1 #Change to 18 in production

    ##START ROUND 1 CALCULATIONS -->
    #Trigger to show score only when round finished
    rd1holes_played = Rd1SlotModel.objects.get(player_name__name=name).player_holesplayed

    #Rd1 Player golf score & rank
    if rd1holes_played >= target_holes:
        rd1golf_score = Rd1SlotModel.objects.get(player_name__name=name).player_score
        rd1golf_scoreRank = Rd1SlotModel.objects.filter(player_score__lt=rd1golf_score).count() + 1
        rd1golf_stbl = Rd1SlotModel.objects.get(player_name__name=name).player_stbl
        rd1golf_stblRank = Rd1SlotModel.objects.filter(player_stbl__gt=rd1golf_stbl).count() + 1
    else:
        rd1golf_score = "-"
        rd1golf_scoreRank= "n/a"
        rd1golf_stbl = "-"
        rd1golf_stblRank= "n/a"

    #Rd1PlayerPoints
    try:
        rd1golf_points = LeaderBoardModel.objects.get(player=name).rd1_golf
    except:
        rd1golf_points = "-"
    try:
        rd1golf_rank = LeaderBoardModel.objects.filter(rd1_golf__gt=rd1golf_points).count() + 1
    except:
        rd1golf_rank = "-"
    try:
        rd1ctpld_points = LeaderBoardModel.objects.get(player=name).rd1_ctpld
    except:
        rd1ctpld_points = "-"
    try:
        rd1ctpld_rank = LeaderBoardModel.objects.filter(rd1_ctpld__gt=rd1ctpld_points).count() + 1
    except:
        rd1ctpld_rank = "-"
    try:
        rd1bonus_points = LeaderBoardModel.objects.get(player=name).rd1_bonus
    except:
        rd1bonus_points = "-"
    try:
        rd1bonus_rank = LeaderBoardModel.objects.filter(rd1_bonus__gt=rd1bonus_points).count() + 1
    except:
        rd1bonus_rank = "-"
    try:
        rd1total_points = rd1golf_points + rd1ctpld_points + rd1bonus_points
    except:
        rd1total_points = "-"
    try:
        rd1total_rank = LeaderBoardModel.objects.filter(rd1_total__gt=rd1total_points).count() + 1
    except:
        rd1total_rank = "-"

    try:
        round1overall_points = list(LeaderBoardModel.objects.aggregate(Sum('rd1_total')).values())[0]
    except:
        round1overall_points = 0


    ##START ROUND 2 CALCULATIONS -->
    #Trigger to show score only when round finished
    try:
        rd2holes_played = Rd2SlotModel.objects.get(player_name__name=name).player_holesplayed
    except:
        rd2holes_played = 0

    #Rd2 Player golf score & rank
    if rd2holes_played >= target_holes:
        rd2golf_score = Rd2SlotModel.objects.get(player_name__name=name).player_score
        rd2golf_scoreRank = Rd2SlotModel.objects.filter(player_score__lt=rd2golf_score).count() + 1
        rd2golf_stbl = Rd1SlotModel.objects.get(player_name__name=name).player_stbl
        rd2golf_stblRank = Rd2SlotModel.objects.filter(player_stbl__gt=rd2golf_stbl).count() + 1
    else:
        rd2golf_score = "-"
        rd2golf_scoreRank= "n/a"
        rd2golf_stbl = "-"
        rd2golf_stblRank= "n/a"

    #Rd2PlayerPoints
    try:
        rd2golf_points = LeaderBoardModel.objects.get(player=name).rd2_golf
    except:
        rd2golf_points = "-"
    try:
        rd2golf_rank = LeaderBoardModel.objects.filter(rd2_golf__gt=rd2golf_points).count() + 1
    except:
        rd2golf_rank = "-"
    try:
        rd2ctpld_points = LeaderBoardModel.objects.get(player=name).rd2_ctpld
    except:
        rd2ctpld_points = "-"
    try:
        rd2ctpld_rank = LeaderBoardModel.objects.filter(rd2_ctpld__gt=rd2ctpld_points).count() + 1
    except:
        rd2ctpld_rank = "-"
    try:
        rd2bonus_points = LeaderBoardModel.objects.get(player=name).rd2_bonus
    except:
        rd2bonus_points = "-"
    try:
        rd2bonus_rank = LeaderBoardModel.objects.filter(rd2_bonus__gt=rd2bonus_points).count() + 1
    except:
        rd2bonus_rank = "-"
    try:
        rd2total_points = rd2golf_points + rd2ctpld_points + rd2bonus_points
    except:
        rd2total_points = "-"
    try:
        rd2total_rank = LeaderBoardModel.objects.filter(rd2_total__gt=rd2total_points).count() + 1
    except:
        rd2total_rank = "-"

    try:
        round2overall_points = list(LeaderBoardModel.objects.aggregate(Sum('rd2_total')).values())[0]
    except:
        round2overall_points = 0

    ##START ROUND 3 CALCULATIONS -->
    #Trigger to show score only when round finished
    try:
        rd3holes_played = Rd3SlotModel.objects.get(player_name__name=name).player_holesplayed
    except:
        rd3holes_played = 0

    #Rd3 Player golf score & rank
    if rd3holes_played >= target_holes:
        rd3golf_score = Rd3SlotModel.objects.get(player_name__name=name).player_score
        rd3golf_scoreRank = Rd3SlotModel.objects.filter(player_score__lt=rd2golf_score).count() + 1
        rd3golf_stbl = Rd3SlotModel.objects.get(player_name__name=name).player_stbl
        rd3golf_stblRank = Rd3SlotModel.objects.filter(player_stbl__gt=rd2golf_stbl).count() + 1
    else:
        rd3golf_score = "-"
        rd3golf_scoreRank= "n/a"
        rd3golf_stbl = "-"
        rd3golf_stblRank= "n/a"

    #Rd2PlayerPoints
    try:
        rd3golf_points = LeaderBoardModel.objects.get(player=name).rd3_golf
    except:
        rd3golf_points = "-"
    try:
        rd3golf_rank = LeaderBoardModel.objects.filter(rd3_golf__gt=rd3golf_points).count() + 1
    except:
        rd3golf_rank = "-"
    try:
        rd3ctpld_points = LeaderBoardModel.objects.get(player=name).rd3_ctpld
    except:
        rd3ctpld_points = "-"
    try:
        rd3ctpld_rank = LeaderBoardModel.objects.filter(rd3_ctpld__gt=rd3ctpld_points).count() + 1
    except:
        rd3ctpld_rank = "-"
    try:
        rd3bonus_points = LeaderBoardModel.objects.get(player=name).rd3_bonus
    except:
        rd3bonus_points = "-"
    try:
        rd3bonus_rank = LeaderBoardModel.objects.filter(rd3_bonus__gt=rd3bonus_points).count() + 1
    except:
        rd3bonus_rank = "-"
    try:
        rd3total_points = rd3golf_points + rd3ctpld_points + rd3bonus_points
    except:
        rd3total_points = "-"
    try:
        rd3total_rank = LeaderBoardModel.objects.filter(rd3_total__gt=rd3total_points).count() + 1
    except:
        rd3total_rank = "-"

    try:
        round3overall_points = list(LeaderBoardModel.objects.aggregate(Sum('rd3_total')).values())[0]
    except:
        round3overall_points = 0

    ##START OTHER_SCORES CALCULATIONS -->

    #Other Player Points
    try:
        social_points = LeaderBoardModel.objects.get(player=name).social
    except:
        social_points = "-"
    try:
        social_rank = LeaderBoardModel.objects.filter(social__gt=social_points).count() + 1
    except:
        social_rank = "-"
    try:
        bestdressed_points = LeaderBoardModel.objects.get(player=name).best_dressed
    except:
        bestdressed_points = "-"
    try:
        bestdressed_rank = LeaderBoardModel.objects.filter(best_dressed__gt=bestdressed_points).count() + 1
    except:
        bestdressed_rank = "-"
    try:
        tipping_points = LeaderBoardModel.objects.get(player=name).tipping
    except:
        tipping_points = "-"
    try:
        tipping_rank = LeaderBoardModel.objects.filter(tipping__gt=tipping_points).count() + 1
    except:
        tipping_rank = "-"
    try:
        othertotal_points = social_points + bestdressed_points + tipping_points
    except:
        othertotal_points = "-"
    try:
        othertotal_rank = LeaderBoardModel.objects.filter(other_total__gt=othertotal_points).count() + 1
    except:
        othertotal_rank = "-"

    try:
        otheroverall_points = list(LeaderBoardModel.objects.aggregate(Sum('other_total')).values())[0]
    except:
        otheroverall_points = 0

## == END SCORING CALCS ==

    context ={
    'name': name,
    'player_image': player_image,
    'player_HC': player_HC,
    'player_highfinish': player_highfinish,
    'player_tournum': player_tournum,
    'player_totalpoints': player_totalpoints,
    'player_totalrank': player_totalrank,
    'rd1golf_score': rd1golf_score,
    'rd1golf_stbl': rd1golf_stbl,
    'rd1golf_scoreRank': rd1golf_scoreRank,
    'rd1golf_stblRank': rd1golf_stblRank,
    'rd1golf_points': rd1golf_points,
    'rd1golf_rank': rd1golf_rank,
    'rd1ctpld_points': rd1ctpld_points,
    'rd1ctpld_rank': rd1ctpld_rank,
    'rd1bonus_points': rd1bonus_points,
    'rd1bonus_rank': rd1bonus_rank,
    'rd1total_points': rd1total_points,
    'rd1total_rank': rd1total_rank,
    'round1overall_points': round1overall_points,
    'rd2golf_score': rd2golf_score,
    'rd2golf_stbl': rd2golf_stbl,
    'rd2golf_scoreRank': rd2golf_scoreRank,
    'rd2golf_stblRank': rd2golf_stblRank,
    'rd2golf_points': rd2golf_points,
    'rd2golf_rank': rd2golf_rank,
    'rd2ctpld_points': rd2ctpld_points,
    'rd2ctpld_rank': rd2ctpld_rank,
    'rd2bonus_points': rd2bonus_points,
    'rd2bonus_rank': rd2bonus_rank,
    'rd2total_points': rd2total_points,
    'rd2total_rank': rd2total_rank,
    'round2overall_points': round2overall_points,
    'rd3golf_score': rd3golf_score,
    'rd3golf_stbl': rd3golf_stbl,
    'rd3golf_scoreRank': rd3golf_scoreRank,
    'rd3golf_stblRank': rd3golf_stblRank,
    'rd3golf_points': rd3golf_points,
    'rd3golf_rank': rd3golf_rank,
    'rd3ctpld_points': rd3ctpld_points,
    'rd3ctpld_rank': rd3ctpld_rank,
    'rd3bonus_points': rd3bonus_points,
    'rd3bonus_rank': rd3bonus_rank,
    'rd3total_points': rd3total_points,
    'rd3total_rank': rd3total_rank,
    'round3overall_points': round3overall_points,
    'social_points': social_points,
    'social_rank': social_rank,
    'bestdressed_points': bestdressed_points,
    'bestdressed_rank': bestdressed_rank,
    'tipping_points': tipping_points,
    'tipping_rank': tipping_rank,
    'othertotal_points': othertotal_points,
    'othertotal_rank': othertotal_rank,
    'otheroverall_points': otheroverall_points,

    }

    return render(request, 'playerDetail.html', context=context)

## -- START ROUND 1 -- ##

class rd1holelist (generic.ListView):
    """Create list of holes"""
    model = Rd1HoleModel
    template_name = 'rd1HoleList.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in additional querysets for context
        ctp_hole = Rd1HoleModel.objects.filter(CTP__gt=0)
        ld_hole = Rd1HoleModel.objects.filter(LD__gt=0)
        tussle_hole = Rd1HoleModel.objects.filter(tussle__isnull=False)

        context['ctp_hole'] = ctp_hole
        context['ld_hole'] = ld_hole
        return context

def rd1holedetail(request,pk):
    """Create hole detail for score entry"""
    #Hole details
    hole_number = Rd1HoleModel.objects.get(pk=pk).number
    hole_index = Rd1HoleModel.objects.get(pk=pk).index
    hole_par = Rd1HoleModel.objects.get(pk=pk).par
    hole_ctp = Rd1HoleModel.objects.get(pk=pk).CTP
    hole_ld = Rd1HoleModel.objects.get(pk=pk).LD
    selected_hole = Rd1HoleModel.objects.get(number=pk)
    hole_tussle = Rd1HoleModel.objects.get(pk=pk).tussle


    #Count active players for dynamic loading
    active_players = Rd1SlotModel.objects.filter(player_name__isnull=False).count()

    #Assign players to slots
    def player_setup():
        try:
            player1 = Rd1SlotModel.objects.get(player_slot = 1)
        except:
            player1 = 'None'
        try:
            player2 = Rd1SlotModel.objects.get(player_slot = 2)
        except:
            player2 = 'None'
        try:
            player3 = Rd1SlotModel.objects.get(player_slot = 3)
        except:
            player3 = 'None'
        try:
            player4 = Rd1SlotModel.objects.get(player_slot = 4)
        except:
            player4 = 'None'
        try:
            player5 = Rd1SlotModel.objects.get(player_slot = 5)
        except:
            player5 = 'None'
        try:
            player6 = Rd1SlotModel.objects.get(player_slot = 6)
        except:
            player6 = 'None'
        try:
            player7 = Rd1SlotModel.objects.get(player_slot = 7)
        except:
            player7 = 'None'
        try:
            player8 = Rd1SlotModel.objects.get(player_slot = 8)
        except:
            player8 = 'None'
        try:
            player9 = Rd1SlotModel.objects.get(player_slot = 9)
        except:
            player9 = 'None'
        try:
            player10 = Rd1SlotModel.objects.get(player_slot = 10)
        except:
            player10 = 'None'
        try:
            player11 = Rd1SlotModel.objects.get(player_slot = 11)
        except:
            player11 = 'None'
        try:
            player12 = Rd1SlotModel.objects.get(player_slot = 12)
        except:
            player12 = 'None'

        return (player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12)

    player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12 = player_setup()

    #Accept form input (create, edit, display)
    if request.method == 'POST':
        form = Rd1ScoreForm(request.POST)
        try:
            instance = Rd1ScoreModel.objects.get(hole=selected_hole)
            instance.ctp = form.save(commit=False).ctp
            instance.ld = form.save(commit=False).ld
            instance.slot1_score = form.save(commit=False).slot1_score
            instance.slot2_score = form.save(commit=False).slot2_score
            instance.slot3_score = form.save(commit=False).slot3_score
            instance.slot4_score = form.save(commit=False).slot4_score
            instance.slot5_score = form.save(commit=False).slot5_score
            instance.slot6_score = form.save(commit=False).slot6_score
            instance.slot7_score = form.save(commit=False).slot7_score
            instance.slot8_score = form.save(commit=False).slot8_score
            instance.slot9_score = form.save(commit=False).slot9_score
            instance.slot10_score = form.save(commit=False).slot10_score
            instance.slot11_score = form.save(commit=False).slot11_score
            instance.slot12_score = form.save(commit=False).slot12_score
            instance.save()
            return redirect('rd1holelist')
        except:
            if form.is_valid():
                post = form.save(commit=False)
                post.hole = selected_hole
                post.save()
                return redirect('rd1holelist')
    else:
        try:
            form = Rd1ScoreForm(instance=get_object_or_404(Rd1ScoreModel,hole=selected_hole))
        except:
            form = Rd1ScoreForm()


    # Define HTML context
    context = {
        'hole_number': hole_number,
        'hole_index': hole_index,
        'hole_par': hole_par,
        'active_players': active_players,
        'player1': player1,
        'player2': player2,
        'player3': player3,
        'player4': player4,
        'player5': player5,
        'player6': player6,
        'player7': player7,
        'player8': player8,
        'player9': player9,
        'player10': player10,
        'player11': player11,
        'player12': player12,
        'form': form,
        'hole_ctp': hole_ctp,
        'hole_ld': hole_ld,
        'hole_tussle': hole_tussle,
        }

    return render(request, 'rd1HoleDetail.html', context=context)

def rd1leaderboard(request):
    """Create leaderboard view for Round1"""

    #Add views
    playing_players = Rd1SlotModel.objects.filter(player_name__isnull=False)

    endurance_leader = Rd1SlotModel.objects.aggregate(Max('endurance_score'))

    #Add context
    context = {
        'playing_players': playing_players,
        'endurance_leader': endurance_leader,
        }

    return render(request, 'rd1Leaderboard.html', context=context)

# ## -- END ROUND 1 -- ##

## -- START ROUND 2 -- ##
class rd2holelist (generic.ListView):
    """Create list of holes"""
    model = Rd2HoleModel
    template_name = 'rd2HoleList.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in additional querysets for context
        ctp_hole = Rd2HoleModel.objects.filter(CTP__gt=0)
        ld_hole = Rd2HoleModel.objects.filter(LD__gt=0)
        tussle_hole = Rd2HoleModel.objects.filter(tussle__isnull=False)

        context['ctp_hole'] = ctp_hole
        context['ld_hole'] = ld_hole
        return context

def rd2holedetail(request,pk):
    """Create hole detail for score entry"""
    #Hole details
    hole_number = Rd2HoleModel.objects.get(pk=pk).number
    hole_index = Rd2HoleModel.objects.get(pk=pk).index
    hole_par = Rd2HoleModel.objects.get(pk=pk).par
    hole_ctp = Rd2HoleModel.objects.get(pk=pk).CTP
    hole_ld = Rd2HoleModel.objects.get(pk=pk).LD
    selected_hole = Rd2HoleModel.objects.get(number=pk)
    hole_tussle = Rd1HoleModel.objects.get(pk=pk).tussle

    #Count active players for dynamic loading
    active_players = Rd2SlotModel.objects.filter(player_name__isnull=False).count()

    #Assign players to slots
    def player_setup():
        try:
            player1 = Rd2SlotModel.objects.get(player_slot = 1)
        except:
            player1 = 'None'
        try:
            player2 = Rd2SlotModel.objects.get(player_slot = 2)
        except:
            player2 = 'None'
        try:
            player3 = Rd2SlotModel.objects.get(player_slot = 3)
        except:
            player3 = 'None'
        try:
            player4 = Rd2SlotModel.objects.get(player_slot = 4)
        except:
            player4 = 'None'
        try:
            player5 = Rd2SlotModel.objects.get(player_slot = 5)
        except:
            player5 = 'None'
        try:
            player6 = Rd2SlotModel.objects.get(player_slot = 6)
        except:
            player6 = 'None'
        try:
            player7 = Rd2SlotModel.objects.get(player_slot = 7)
        except:
            player7 = 'None'
        try:
            player8 = Rd2SlotModel.objects.get(player_slot = 8)
        except:
            player8 = 'None'
        try:
            player9 = Rd2SlotModel.objects.get(player_slot = 9)
        except:
            player9 = 'None'
        try:
            player10 = Rd2SlotModel.objects.get(player_slot = 10)
        except:
            player10 = 'None'
        try:
            player11 = Rd2SlotModel.objects.get(player_slot = 11)
        except:
            player11 = 'None'
        try:
            player12 = Rd2SlotModel.objects.get(player_slot = 12)
        except:
            player12 = 'None'

        return (player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12)

    player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12 = player_setup()

    #Accept form input (create, edit, display)
    if request.method == 'POST':
        form = Rd2ScoreForm(request.POST)
        try:
            instance = Rd2ScoreModel.objects.get(hole=selected_hole)
            instance.ctp = form.save(commit=False).ctp
            instance.ld = form.save(commit=False).ld
            instance.slot1_score = form.save(commit=False).slot1_score
            instance.slot2_score = form.save(commit=False).slot2_score
            instance.slot3_score = form.save(commit=False).slot3_score
            instance.slot4_score = form.save(commit=False).slot4_score
            instance.slot5_score = form.save(commit=False).slot5_score
            instance.slot6_score = form.save(commit=False).slot6_score
            instance.slot7_score = form.save(commit=False).slot7_score
            instance.slot8_score = form.save(commit=False).slot8_score
            instance.slot9_score = form.save(commit=False).slot9_score
            instance.slot10_score = form.save(commit=False).slot10_score
            instance.slot11_score = form.save(commit=False).slot11_score
            instance.slot12_score = form.save(commit=False).slot12_score
            instance.save()
            return redirect('rd2holelist')
        except:
            if form.is_valid():
                post = form.save(commit=False)
                post.hole = selected_hole
                post.save()
                return redirect('rd2holelist')
    else:
        try:
            form = Rd2ScoreForm(instance=get_object_or_404(Rd2ScoreModel,hole=selected_hole))
        except:
            form = Rd2ScoreForm()


    # Define HTML context
    context = {
        'hole_number': hole_number,
        'hole_index': hole_index,
        'hole_par': hole_par,
        'active_players': active_players,
        'player1': player1,
        'player2': player2,
        'player3': player3,
        'player4': player4,
        'player5': player5,
        'player6': player6,
        'player7': player7,
        'player8': player8,
        'player9': player9,
        'player10': player10,
        'player11': player11,
        'player12': player12,
        'form': form,
        'hole_ctp': hole_ctp,
        'hole_ld': hole_ld,
        'hole_tussle': hole_tussle,
        }

    return render(request, 'rd2HoleDetail.html', context=context)

def rd2leaderboard(request):
    """Create leaderboard view for Round2"""

    #Add views
    playing_players = Rd2SlotModel.objects.filter(player_name__isnull=False)

    #Add context
    context = {
        'playing_players': playing_players,
        }

    return render(request, 'rd2Leaderboard.html', context=context)

## --END ROUND 2 -- ##
#
## START ROUND 3 -- ##
class rd3holelist (generic.ListView):
    """Create list of holes"""
    model = Rd3HoleModel
    template_name = 'rd3HoleList.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in additional querysets for context
        ctp_hole = Rd3HoleModel.objects.filter(CTP__gt=0)
        ld_hole = Rd3HoleModel.objects.filter(LD__gt=0)
        tussle_hole = Rd3HoleModel.objects.filter(tussle__isnull=False)

        context['ctp_hole'] = ctp_hole
        context['ld_hole'] = ld_hole
        return context

def rd3holedetail(request,pk):
    """Create hole detail for score entry"""
    #Hole details
    hole_number = Rd3HoleModel.objects.get(pk=pk).number
    hole_index = Rd3HoleModel.objects.get(pk=pk).index
    hole_par = Rd3HoleModel.objects.get(pk=pk).par
    hole_ctp = Rd3HoleModel.objects.get(pk=pk).CTP
    hole_ld = Rd3HoleModel.objects.get(pk=pk).LD
    selected_hole = Rd3HoleModel.objects.get(number=pk)
    hole_tussle = Rd1HoleModel.objects.get(pk=pk).tussle


    #Count active players for dynamic loading
    active_players = Rd3SlotModel.objects.filter(player_name__isnull=False).count()

    #Assign players to slots
    def player_setup():
        try:
            player1 = Rd3SlotModel.objects.get(player_slot = 1)
        except:
            player1 = 'None'
        try:
            player2 = Rd3SlotModel.objects.get(player_slot = 2)
        except:
            player2 = 'None'
        try:
            player3 = Rd3SlotModel.objects.get(player_slot = 3)
        except:
            player3 = 'None'
        try:
            player4 = Rd3SlotModel.objects.get(player_slot = 4)
        except:
            player4 = 'None'
        try:
            player5 = Rd3SlotModel.objects.get(player_slot = 5)
        except:
            player5 = 'None'
        try:
            player6 = Rd3SlotModel.objects.get(player_slot = 6)
        except:
            player6 = 'None'
        try:
            player7 = Rd3SlotModel.objects.get(player_slot = 7)
        except:
            player7 = 'None'
        try:
            player8 = Rd3SlotModel.objects.get(player_slot = 8)
        except:
            player8 = 'None'
        try:
            player9 = Rd3SlotModel.objects.get(player_slot = 9)
        except:
            player9 = 'None'
        try:
            player10 = Rd3SlotModel.objects.get(player_slot = 10)
        except:
            player10 = 'None'
        try:
            player11 = Rd3SlotModel.objects.get(player_slot = 11)
        except:
            player11 = 'None'
        try:
            player12 = Rd3SlotModel.objects.get(player_slot = 12)
        except:
            player12 = 'None'

        return (player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12)

    player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12 = player_setup()

    #Accept form input (create, edit, display)
    if request.method == 'POST':
        form = Rd3ScoreForm(request.POST)
        try:
            instance = Rd3ScoreModel.objects.get(hole=selected_hole)
            instance.ctp = form.save(commit=False).ctp
            instance.ld = form.save(commit=False).ld
            instance.slot1_score = form.save(commit=False).slot1_score
            instance.slot2_score = form.save(commit=False).slot2_score
            instance.slot3_score = form.save(commit=False).slot3_score
            instance.slot4_score = form.save(commit=False).slot4_score
            instance.slot5_score = form.save(commit=False).slot5_score
            instance.slot6_score = form.save(commit=False).slot6_score
            instance.slot7_score = form.save(commit=False).slot7_score
            instance.slot8_score = form.save(commit=False).slot8_score
            instance.slot9_score = form.save(commit=False).slot9_score
            instance.slot10_score = form.save(commit=False).slot10_score
            instance.slot11_score = form.save(commit=False).slot11_score
            instance.slot12_score = form.save(commit=False).slot12_score
            instance.save()
            return redirect('rd3holelist')
        except:
            if form.is_valid():
                post = form.save(commit=False)
                post.hole = selected_hole
                post.save()
                return redirect('rd3holelist')
    else:
        try:
            form = Rd3ScoreForm(instance=get_object_or_404(Rd3ScoreModel,hole=selected_hole))
        except:
            form = Rd3ScoreForm()


    # Define HTML context
    context = {
        'hole_number': hole_number,
        'hole_index': hole_index,
        'hole_par': hole_par,
        'active_players': active_players,
        'player1': player1,
        'player2': player2,
        'player3': player3,
        'player4': player4,
        'player5': player5,
        'player6': player6,
        'player7': player7,
        'player8': player8,
        'player9': player9,
        'player10': player10,
        'player11': player11,
        'player12': player12,
        'form': form,
        'hole_ctp': hole_ctp,
        'hole_ld': hole_ld,
        'hole_tussle': hole_tussle,
        }

    return render(request, 'rd3HoleDetail.html', context=context)

def rd3leaderboard(request):
    """Create leaderboard view for Round3"""

    #Add views
    playing_players = Rd3SlotModel.objects.filter(player_name__isnull=False)

    #Add context
    context = {
        'playing_players': playing_players,
        }

    return render(request, 'rd3Leaderboard.html', context=context)

## -- END ROUND 3 -- ##

## -- START ROUND 4 -- ##

class rd4holelist (generic.ListView):
    """Create list of holes"""
    model = Rd4HoleModel
    template_name = 'rd4HoleList.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in additional querysets for context
        ctp_hole = Rd4HoleModel.objects.filter(CTP__gt=0)
        ld_hole = Rd4HoleModel.objects.filter(LD__gt=0)
        tussle_hole = Rd4HoleModel.objects.filter(tussle__isnull=False)

        context['ctp_hole'] = ctp_hole
        context['ld_hole'] = ld_hole
        return context

def rd4holedetail(request,pk):
    """Create hole detail for score entry"""
    #Hole details
    hole_number = Rd4HoleModel.objects.get(pk=pk).number
    hole_index = Rd4HoleModel.objects.get(pk=pk).index
    hole_par = Rd4HoleModel.objects.get(pk=pk).par
    hole_ctp = Rd4HoleModel.objects.get(pk=pk).CTP
    hole_ld = Rd4HoleModel.objects.get(pk=pk).LD
    selected_hole = Rd4HoleModel.objects.get(number=pk)
    hole_tussle = Rd4HoleModel.objects.get(pk=pk).tussle


    #Count active players for dynamic loading
    active_players = Rd4SlotModel.objects.filter(player_name__isnull=False).count()

    #Assign players to slots
    def player_setup():
        try:
            player1 = Rd4SlotModel.objects.get(player_slot = 1)
        except:
            player1 = 'None'
        try:
            player2 = Rd4SlotModel.objects.get(player_slot = 2)
        except:
            player2 = 'None'
        try:
            player3 = Rd4SlotModel.objects.get(player_slot = 3)
        except:
            player3 = 'None'
        try:
            player4 = Rd4SlotModel.objects.get(player_slot = 4)
        except:
            player4 = 'None'
        try:
            player5 = Rd4SlotModel.objects.get(player_slot = 5)
        except:
            player5 = 'None'
        try:
            player6 = Rd4SlotModel.objects.get(player_slot = 6)
        except:
            player6 = 'None'
        try:
            player7 = Rd4SlotModel.objects.get(player_slot = 7)
        except:
            player7 = 'None'
        try:
            player8 = Rd4SlotModel.objects.get(player_slot = 8)
        except:
            player8 = 'None'
        try:
            player9 = Rd4SlotModel.objects.get(player_slot = 9)
        except:
            player9 = 'None'
        try:
            player10 = Rd4SlotModel.objects.get(player_slot = 10)
        except:
            player10 = 'None'
        try:
            player11 = Rd4SlotModel.objects.get(player_slot = 11)
        except:
            player11 = 'None'
        try:
            player12 = Rd4SlotModel.objects.get(player_slot = 12)
        except:
            player12 = 'None'

        return (player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12)

    player1, player2, player3, player4, player5, player6, player7, player8, player9, player10, player11, player12 = player_setup()

    #Accept form input (create, edit, display)
    if request.method == 'POST':
        form = Rd4ScoreForm(request.POST)
        try:
            instance = Rd4ScoreModel.objects.get(hole=selected_hole)
            instance.ctp = form.save(commit=False).ctp
            instance.ld = form.save(commit=False).ld
            instance.slot1_score = form.save(commit=False).slot1_score
            instance.slot2_score = form.save(commit=False).slot2_score
            instance.slot3_score = form.save(commit=False).slot3_score
            instance.slot4_score = form.save(commit=False).slot4_score
            instance.slot5_score = form.save(commit=False).slot5_score
            instance.slot6_score = form.save(commit=False).slot6_score
            instance.slot7_score = form.save(commit=False).slot7_score
            instance.slot8_score = form.save(commit=False).slot8_score
            instance.slot9_score = form.save(commit=False).slot9_score
            instance.slot10_score = form.save(commit=False).slot10_score
            instance.slot11_score = form.save(commit=False).slot11_score
            instance.slot12_score = form.save(commit=False).slot12_score
            instance.save()
            return redirect('Rd4holelist')
        except:
            if form.is_valid():
                post = form.save(commit=False)
                post.hole = selected_hole
                post.save()
                return redirect('rd4holelist')
    else:
        try:
            form = Rd4ScoreForm(instance=get_object_or_404(Rd4ScoreModel,hole=selected_hole))
        except:
            form = Rd4ScoreForm()


    # Define HTML context
    context = {
        'hole_number': hole_number,
        'hole_index': hole_index,
        'hole_par': hole_par,
        'active_players': active_players,
        'player1': player1,
        'player2': player2,
        'player3': player3,
        'player4': player4,
        'player5': player5,
        'player6': player6,
        'player7': player7,
        'player8': player8,
        'player9': player9,
        'player10': player10,
        'player11': player11,
        'player12': player12,
        'form': form,
        'hole_ctp': hole_ctp,
        'hole_ld': hole_ld,
        'hole_tussle': hole_tussle,
        }

    return render(request, 'rd4HoleDetail.html', context=context)

def rd4leaderboard(request):
    """Create leaderboard view for Round1"""

    #Add views
    playing_players = Rd4SlotModel.objects.filter(player_name__isnull=False)

    #Add context
    context = {
        'playing_players': playing_players,
        }

    return render(request, 'rd4Leaderboard.html', context=context)

# ## -- END ROUND 4 -- ##

def entertips(request):
    """Create view for tips entry view"""

    #Add views
    if request.method == 'POST':
        form = SportsTippingForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('tipresults')

    else:
        form = SportsTippingForm()

    context = {
        'form': form,
        }

    return render(request, 'enterSportsTips.html', context=context)

def tipresults(request):
    """Redirect page for input and show results"""
    #Basic counts and definitions
    recordedtips = SportsTippingScoreModel.objects.all()

    try:
        results = SportsTippingResultsModel.objects.get(name="result")

        if results:
            if results.result1 == "NOT_COMPLETE":
                num_games1 = 0
            else:
                num_games1 = 1
            if results.result2 == "NOT_COMPLETE":
                num_games2 = 0
            else:
                num_games2 = 1
            if results.result3 == "NOT_COMPLETE":
                num_games3 = 0
            else:
                num_games3 = 1
            if results.result4 == "NOT_COMPLETE":
                num_games4 = 0
            else:
                num_games4 = 1
            if results.result5 == "NOT_COMPLETE":
                num_games5 = 0
            else:
                num_games5 = 1
            if results.result6 == "NOT_COMPLETE":
                num_games6 = 0
            else:
                num_games6 = 1
            if results.result7 == "NOT_COMPLETE":
                num_games7 = 0
            else:
                num_games7 = 1
            if results.result8 == "NOT_COMPLETE":
                num_games8 = 0
            else:
                num_games8 = 1
            if results.result9 == "NOT_COMPLETE":
                num_games9 = 0
            else:
                num_games9 = 1
            if results.result10 == "NOT_COMPLETE":
                num_games10 = 0
            else:
                num_games10 = 1

            num_games = num_games1 +num_games2 +num_games3 +num_games4 +num_games5 +num_games6 +num_games7 +num_games8 +num_games9 +num_games10

        else:
            num_games = 0

    except:
        num_games = 0

    context = {
        'recordedtips': recordedtips,
        'num_games': num_games,
        }

    return render(request, 'tipResults.html', context=context)

def entersocial(request):
    """Create view for social entry view"""

    if request.method == 'POST':
        if 'friday' in request.POST:
            fridayform = FridaySocialForm(request.POST, prefix='friday')
            if fridayform.is_valid():
                post = fridayform.save(commit=False)
                post.save()
                return redirect('landingpage')
                saturdayform = SaturdaySocialForm(prefix='saturday')

        elif 'saturday' in request.POST:
            saturdayform = SaturdaySocialForm(request.POST, prefix='saturday')
            if saturdayform.is_valid():
                post = saturdayform.save(commit=False)
                post.save()
                return redirect('landingpage')
                fridayform = FridaySocialForm(prefix='friday')
    else:
        fridayform = FridaySocialForm(prefix='friday')
        saturdayform = SaturdaySocialForm(prefix='saturday')

    context = {
#        'fridayform': fridayform,
        'saturdayform': saturdayform,
        'fridayform': fridayform,
        }

    return render(request, 'enterSocial.html', context=context)

def tourdetails(request):
    """Landing page for tour details"""

    context = {}

    return render(request, 'tourDetails.html', context=context)

def touragenda(request):
    """Landing page for tour details"""
    active_events = TourAgendaModel.objects.order_by('number')
    friday_events = TourAgendaModel.objects.all().filter(day='FRIDAY')
    saturday_events = TourAgendaModel.objects.all().filter(day='SATURDAY')
    sunday_events = TourAgendaModel.objects.all().filter(day='SUNDAY')

    context = {
        'active_events': active_events,
        'friday_events': friday_events,
        'saturday_events': saturday_events,
        'sunday_events': sunday_events,
        }

    return render(request, 'tourAgenda.html', context=context)

def tourmap(request):
    """Landing page for tour details"""

    context = {}

    return render(request, 'tourMap.html', context=context)

def tourplayers(request):
    """Landing page for tour details"""
    active_players = PlayerModel.objects.order_by('number')

    context = {
        'active_players': active_players,
        }

    return render(request, 'tourPlayers.html', context=context)
#
def topgolf(request):
    """display top golf results"""

    try:
        entry = TopGolfModel.objects.all()
        reference_entry = TopGolfModel.objects.get(reference="reference")
        topgolf1 = reference_entry.first
        topgolf2 = reference_entry.second
        topgolf3 = reference_entry.third
        topgolf4 = reference_entry.fourth
        topgolf5= reference_entry.fifth
        topgolf6 = reference_entry.sixth

    except:
        topgolf1 = "Not decided yet"
        topgolf2 = "Not decided yet"
        topgolf3 = "Not decided yet"
        topgolf4 = "Not decided yet"
        topgolf5 = "Not decided yet"
        topgolf6 = "Not decided yet"

    context = {
        'topgolf1': topgolf1,
        'topgolf2': topgolf2,
        'topgolf3': topgolf3,
        'topgolf4': topgolf4,
        'topgolf5': topgolf5,
        'topgolf6': topgolf6,
        }

    return render(request, 'topgolf.html', context=context)

def racing(request):
    """display racing results"""

    try:
        entry = RacingModel.objects.all()
        reference_entry = RacingModel.objects.get(reference="reference")
        racing1 = reference_entry.first
        racing2 = reference_entry.second
        racing3 = reference_entry.third
        racing4 = reference_entry.fourth
        racing5= reference_entry.fifth
        racing6 = reference_entry.sixth
    except:
        racing1 = "Not started"
        racing2 = "Not started"
        racing3 = "Not started"
        racing4 = "Not started"
        racing5 = "Not started"
        racing6 = "Not started"

    context = {
        'racing1': racing1,
       'racing2': racing2,
        'racing3': racing3,
        'racing4': racing4,
        'racing5': racing5,
        'racing6': racing6,
        }

    return render(request, 'racing.html', context=context)




#############testview - DELETE ONCE RUNNING
def testpage(request):

    context={}

    return render(request, 'testpage.html', context=context)
