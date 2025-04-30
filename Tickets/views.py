from django.shortcuts import render, redirect, get_object_or_404
from .models import Ticket
from .forms import TicketForm, CommentForm
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator

def home (request):
    return render (request, 'home.html')


def create_ticket (request):
    if request.method == 'POST':
        form = TicketForm (request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('dashboard')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})

User = get_user_model()

def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    comments = ticket.comments.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()

            # Admin commenting and updating the status to 'in_progress'
            if ticket.status == Ticket.STATUS_OPEN and request.user.is_staff:
                ticket.status = Ticket.STATUS_IN_PROGRESS  
                ticket.save() 
                
            # If admin comments, status should be 'in_progress'
            if ticket.status == Ticket.STATUS_IN_PROGRESS and ticket.completed_at:
                ticket.completed_at = None  # If somehow reopened
                ticket.save()

            return redirect('ticket_detail', pk=ticket.pk)
    
    else:
        form = CommentForm()

    return render(request, 'ticket_detail.html', {
        'ticket': ticket,
        'comments': comments,
        'form': form
    })

def ticket_edit(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    form = TicketForm(request.POST or None, instance=ticket)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'create_ticket.html', {'form': form})

def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.delete()
    return redirect('dashboard')

def dashboard(request):
    tickets = Ticket.objects.filter(user=request.user)
    status_filter = request.GET.get('status')
    priority_filter = request.GET.get('priority')

    # Apply filters
    status_filter = request.GET.get('status')
    if status_filter:
        tickets = tickets.filter(status=status_filter)

    priority_filter = request.GET.get('priority')
    if priority_filter:
        tickets = tickets.filter(priority=priority_filter)

    # Apply sorting
    sort = request.GET.get('sort')
    if sort == 'oldest':
        tickets = tickets.order_by('created_at')
    else:
        tickets = tickets.order_by('-created_at')

    # Paginate AFTER filtering & sorting
    paginator = Paginator(tickets, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard.html', {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'sort': sort,
    })