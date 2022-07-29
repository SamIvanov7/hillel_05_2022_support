from django.http import JsonResponse


class TicketsService:
    def get_all_tickets(self) -> dict:
        return {}


def get_all_tickets(request):
    ticket_service = TicketsService()
    data = ticket_service.get_all_tickets()

    return JsonResponse(data)
