from django.test import TestCase
from django.contrib.auth.models import User
from Koma.models import Ticket, TicketHistory, Module


class TicketModelTest(TestCase):
    def setUp(self):
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

    def test_ticket_creation(self):
        self.assertEqual(self.ticket.title, "Test Ticket")
        self.assertEqual(self.ticket.status, "Received")
        self.assertEqual(self.ticket.module.name, "Test Modul")

    def test_ticket_history_creation(self):
        history = TicketHistory.objects.create(
            ticket=self.ticket,
            text="Test Änderung",
            status="IN_PROGRESS",
            user=self.user
        )
        self.assertEqual(history.ticket, self.ticket)
        self.assertEqual(history.status, "IN_PROGRESS")
        self.assertEqual(history.user.username, "testuser")
