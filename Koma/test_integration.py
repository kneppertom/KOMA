from django.test import TestCase, Client
from django.contrib.auth.models import User
from Koma.models import Ticket, TicketHistory, Module
from django.urls import reverse


class TicketIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.module = Module.objects.create(name="Test Modul", short_name="TM")

    # def test_ticket_creation_and_history(self):
    #     # Login
    #     self.client.login(username='testuser', password='testpassword')
    #
    #     # Ticket erstellen
    #     response = self.client.post(reverse('create_ticket'), {
    #         'title': 'Integration Ticket',
    #         'description': 'Integration Test',
    #         'priority': 1,
    #         'status': 'Received',
    #         'module': self.module.id,
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     ticket = Ticket.objects.get(title="Integration Ticket")
    #     self.assertIsNotNone(ticket)
    #
    #     # Ticket-Historie hinzufügen
    #     response = self.client.post(reverse('add_remark', args=[ticket.id]), {
    #         'text': 'Erster Kommentar',
    #         'status': 'IN_PROGRESS',
    #     })
    #     self.assertEqual(response.status_code, 200)
    #     history = TicketHistory.objects.filter(ticket=ticket)
    #     self.assertEqual(history.count(), 1)
    #     self.assertEqual(history.first().status, 'IN_PROGRESS')
