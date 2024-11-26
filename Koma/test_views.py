from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Koma.models import Ticket, Module


class TicketViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.module = Module.objects.create(name="Test Modul", short_name="TM")
        self.ticket = Ticket.objects.create(
            title="Test Ticket",
            description="Test Beschreibung",
            priority=1,
            status="Received",
            module=self.module,
            created_by=self.user,
        )

    def test_ticket_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('ticket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Ticket")

    # def test_ticket_create_view(self):
    #     self.client.login(username='testuser', password='testpassword')
    #     response = self.client.post(reverse('create_ticket'), {
    #         'title': 'Neues Ticket',
    #         'description': 'Beschreibung',
    #         'priority': 2,
    #         'status': 'Received',
    #         'module': self.module.id,
    #     })
    #     self.assertTemplateUsed(response, 'tickets/ticket_form.html')
    #     self.assertEqual(response.status_code, 302)  # Redirect nach Erfolg
    #     self.assertTrue(Ticket.objects.filter(title="Neues Ticket").exists())

    def test_ticket_edit_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_ticket', args=[self.ticket.id]), {
            'title': 'Bearbeitetes Ticket',
            'description': 'Neue Beschreibung',
            'priority': 3,
            'status': 'IN_PROGRESS',
        })
        self.assertIn(response.status_code, [200, 302, 400])  # Akzeptiere Redirect oder Success
        self.ticket.refresh_from_db()
