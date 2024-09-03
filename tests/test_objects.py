import re

import pytest

from pretiac.exceptions import PretiacRequestException
from pretiac.raw_client import RawClient


class TestList:
    def test_hosts(self, raw_client: RawClient) -> None:
        results = raw_client.objects.list("Host")
        host = results[0]
        assert host["attrs"]["address"] == "127.0.0.1"
        assert set(host["attrs"].keys()) == set(
            [
                "__name",
                "acknowledgement",
                "acknowledgement_expiry",
                "acknowledgement_last_change",
                "action_url",
                "active",
                "address",
                "address6",
                "check_attempt",
                "check_command",
                "check_interval",
                "check_period",
                "check_timeout",
                "command_endpoint",
                "display_name",
                "downtime_depth",
                "enable_active_checks",
                "enable_event_handler",
                "enable_flapping",
                "enable_notifications",
                "enable_passive_checks",
                "enable_perfdata",
                "event_command",
                "executions",
                "flapping",
                "flapping_current",
                "flapping_ignore_states",
                "flapping_last_change",
                "flapping_threshold",
                "flapping_threshold_high",
                "flapping_threshold_low",
                "force_next_check",
                "force_next_notification",
                "groups",
                "ha_mode",
                "handled",
                "icon_image",
                "icon_image_alt",
                "last_check",
                "last_check_result",
                "last_hard_state",
                "last_hard_state_change",
                "last_reachable",
                "last_state",
                "last_state_change",
                "last_state_down",
                "last_state_type",
                "last_state_unreachable",
                "last_state_up",
                "max_check_attempts",
                "name",
                "next_check",
                "next_update",
                "notes",
                "notes_url",
                "original_attributes",
                "package",
                "paused",
                "previous_state_change",
                "problem",
                "retry_interval",
                "severity",
                "source_location",
                "state",
                "state_type",
                "templates",
                "type",
                "vars",
                "version",
                "volatile",
                "zone",
            ]
        )

    def test_attrs(self, raw_client: RawClient) -> None:
        results = raw_client.objects.list("Host", attrs=("address", "notes"))
        host = results[0]
        assert host["attrs"]["address"] == "127.0.0.1"
        assert set(host["attrs"].keys()) == set(
            [
                "address",
                "notes",
            ]
        )

    def test_commands(self, raw_client: RawClient) -> None:
        results = raw_client.objects.list("CheckCommand")
        command = results[0]
        assert isinstance(command["attrs"]["name"], str)

    def test_exception(self, raw_client: RawClient) -> None:
        with pytest.raises(PretiacRequestException, match="No objects found."):
            raw_client.objects.list("Host", "XXX")

    def test_suppress_exception(self, raw_client: RawClient) -> None:
        result = raw_client.objects.list("Host", "XXX", suppress_exception=True)
        assert result["error"] == 404
        assert result["status"] == "No objects found."


class TestGet:
    def test_host(self, raw_client: RawClient) -> None:
        host = raw_client.objects.get("Host", "Host1")
        assert host["attrs"]["name"] == "Host1"
        assert host["attrs"]["address"] == "127.0.0.1"


class TestCreate:
    def test_create(self, raw_client: RawClient) -> None:
        raw_client.objects.delete(
            "Service", "Host1!custom-load", suppress_exception=True
        )
        result = raw_client.objects.create(
            "Service",
            "Host1!custom-load",
            templates=["generic-service"],
            attrs={"check_command": "load", "check_interval": 1, "retry_interval": 1},
        )
        assert result["results"][0]["code"] == 200
        assert result["results"][0]["status"] == "Object was created"

    def test_create_minimal_service(self, raw_client: RawClient) -> None:
        """Create a service with minimal arguments"""
        raw_client.objects.delete(
            "Service", "Host1!custom-load", suppress_exception=True
        )
        result = raw_client.objects.create(
            "Service",
            "Host1!custom-load",
            attrs={"check_command": "load"},
        )
        assert result["results"][0]["code"] == 200
        assert result["results"][0]["status"] == "Object was created"

    def test_create_minimal_host(self, raw_client: RawClient) -> None:
        """Create a host with minimal arguments"""
        raw_client.objects.delete("Host", "NewHost", suppress_exception=True)
        result = raw_client.objects.create(
            "Host", "NewHost", attrs={"check_command": "load"}, suppress_exception=True
        )
        assert result["results"][0]["code"] == 200
        assert result["results"][0]["status"] == "Object was created"

    def test_create_minimal_host2(self, raw_client: RawClient) -> None:
        """Create a host with minimal arguments (only templates)"""
        raw_client.objects.delete("Host", "NewHost", suppress_exception=True)
        result = raw_client.objects.create(
            "Host", "NewHost", templates=["passive-host"], suppress_exception=True
        )
        assert result["results"][0]["code"] == 200
        assert result["results"][0]["status"] == "Object was created"

    def test_error_attribute_not_empty(self, raw_client: RawClient) -> None:
        result = raw_client.objects.create(
            "Service",
            "Host1!xxx",
            suppress_exception=True,
        )
        error = result["results"][0]
        assert error["code"] == 500
        assert re.match(
            r"Error: Validation failed for object 'Host1!xxx' of type 'Service'; Attribute 'check_command': Attribute must not be empty.\nLocation: in /var/lib/icinga2/api/packages/_api/.*/conf.d/services/Host1!xxx.conf:",
            error["errors"][0],
        )
        assert error["status"] == "Object could not be created."

    def test_error_unknown_attr(self, raw_client: RawClient) -> None:
        result = raw_client.objects.create(
            "Service",
            "Host1!xxx",
            attrs={"unknown": "unknown"},
            suppress_exception=True,
        )
        assert (
            result["results"][0]["errors"][0]
            == "Error: Invalid attribute specified: unknown\n"
        )
