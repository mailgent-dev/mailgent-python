import httpx
import pytest
import respx
from mailgent import Mailgent
from mailgent.types import CalendarEvent


class TestCalendarResource:
    @respx.mock
    def test_create(self):
        respx.post("https://api.mailgent.dev/v0/calendar").mock(
            return_value=httpx.Response(201, json={
                "eventId": "evt-1", "title": "Meeting", "description": None,
                "startAt": "2026-04-10T10:00:00Z", "endAt": "2026-04-10T11:00:00Z",
                "isAllDay": False, "location": "Zoom", "metadata": None,
                "createdAt": "2026-04-03T00:00:00Z", "updatedAt": "2026-04-03T00:00:00Z",
            }))
        client = Mailgent(api_key="mgent-test")
        result = client.calendar.create("Meeting", "2026-04-10T10:00:00Z", end_at="2026-04-10T11:00:00Z", location="Zoom")
        assert isinstance(result, CalendarEvent)
        assert result.event_id == "evt-1"
        assert result.title == "Meeting"
        assert result.location == "Zoom"
        client.close()

    @respx.mock
    def test_list(self):
        respx.get("https://api.mailgent.dev/v0/calendar").mock(
            return_value=httpx.Response(200, json={
                "events": [{"eventId": "evt-1", "title": "Meeting", "description": None,
                            "startAt": "2026-04-10T10:00:00Z", "endAt": None,
                            "isAllDay": False, "location": None, "metadata": None,
                            "createdAt": "2026-04-03T00:00:00Z", "updatedAt": "2026-04-03T00:00:00Z"}],
                "count": 1,
            }))
        client = Mailgent(api_key="mgent-test")
        result = client.calendar.list()
        assert result["count"] == 1
        assert isinstance(result["events"][0], CalendarEvent)
        client.close()

    @respx.mock
    def test_get(self):
        respx.get("https://api.mailgent.dev/v0/calendar/evt-1").mock(
            return_value=httpx.Response(200, json={
                "eventId": "evt-1", "title": "Meeting", "description": "Team sync",
                "startAt": "2026-04-10T10:00:00Z", "endAt": None,
                "isAllDay": False, "location": None, "metadata": None,
                "createdAt": "2026-04-03T00:00:00Z", "updatedAt": "2026-04-03T00:00:00Z",
            }))
        client = Mailgent(api_key="mgent-test")
        result = client.calendar.get("evt-1")
        assert result.description == "Team sync"
        client.close()

    @respx.mock
    def test_update(self):
        respx.patch("https://api.mailgent.dev/v0/calendar/evt-1").mock(
            return_value=httpx.Response(200, json={
                "eventId": "evt-1", "title": "Updated Meeting", "description": None,
                "startAt": "2026-04-10T10:00:00Z", "endAt": None,
                "isAllDay": False, "location": "Office", "metadata": None,
                "createdAt": "2026-04-03T00:00:00Z", "updatedAt": "2026-04-03T01:00:00Z",
            }))
        client = Mailgent(api_key="mgent-test")
        result = client.calendar.update("evt-1", title="Updated Meeting", location="Office")
        assert result.title == "Updated Meeting"
        assert result.location == "Office"
        client.close()

    @respx.mock
    def test_delete(self):
        respx.delete("https://api.mailgent.dev/v0/calendar/evt-1").mock(
            return_value=httpx.Response(204))
        client = Mailgent(api_key="mgent-test")
        assert client.calendar.delete("evt-1") is None
        client.close()

    @respx.mock
    def test_set_public(self):
        respx.post("https://api.mailgent.dev/v0/calendar/public").mock(
            return_value=httpx.Response(200, json={"calendarPublic": True}))
        client = Mailgent(api_key="mgent-test")
        result = client.calendar.set_public(True)
        assert result["calendarPublic"] is True
        client.close()

    def test_client_has_calendar(self):
        client = Mailgent(api_key="mgent-test")
        assert client.calendar is not None
        client.close()
