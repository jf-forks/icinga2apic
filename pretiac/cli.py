from typing import Any, Optional

import click
from rich import print

from pretiac import get_default_client
from pretiac.check_executor import check as execute_check
from pretiac.config import load_config_file
from pretiac.log import logger
from pretiac.object_types import (
    normalize_to_plural_snake_object_type_name,
)


@click.group()
@click.option(
    "-d",
    "--debug",
    count=True,
    help="Increase debug verbosity (use up to 3 times): -d: info -dd: debug -ddd: verbose.",
)
def main(debug: int) -> None:
    """Command line interface for the Icinga2 API."""
    logger.set_level(debug)
    logger.show_levels()


# v1/objects ###########################################################################


@click.group()
def objects() -> None:
    """Manage configuration objects."""
    pass


@click.command
@click.argument("object_type")
def list_objects(object_type: str) -> None:
    """List the different configuration object types."""
    client = get_default_client()
    print(
        getattr(
            client,
            f"get_{normalize_to_plural_snake_object_type_name(object_type)}",
        )()
    )


@click.command
@click.argument("host")
@click.argument("service")
def delete_service(host: str, service: str) -> None:
    """Delete a service."""
    get_default_client().delete_service(host=host, service=service)


objects.add_command(list_objects, "list")
objects.add_command(delete_service, "delete-service")


# v1/actions ###########################################################################


@click.group(invoke_without_command=True)
def actions() -> None:
    """There are several actions available for Icinga 2 provided by the
    ``/v1/actions`` URL endpoint."""


@click.command
@click.option(
    "--plugin-output",
    help="The plugin main output. Does **not** contain the performance data.",
)
@click.option("--performance-data", help="The performance data.")
@click.option(
    "--exit-status",
    help="For services: ``0=OK``, ``1=WARNING``, ``2=CRITICAL``, ``3=UNKNOWN``, "
    "for hosts: ``0=UP``, ``1=DOWN``.",
)
@click.option("--host", help="The name of the host.")
@click.argument("service")
def send_service_check_result(
    service: str,
    host: Optional[str] = None,
    exit_status: Optional[Any] = None,
    performance_data: Optional[str] = None,
    plugin_output: Optional[str] = None,
) -> None:
    """Send a check result for a service and create the host or the service if necessary."""
    print(
        get_default_client().send_service_check_result(
            service=service,
            host=host,
            exit_status=exit_status,
            plugin_output=performance_data,
            performance_data=plugin_output,
        )
    )


actions.add_command(send_service_check_result)


# v1/events ############################################################################


@click.command()
def events() -> None:
    """Subscribe to an event stream."""
    for event in get_default_client().subscribe_events(["CheckResult"], "cli"):
        print(event)


# v1/status ############################################################################


@click.command()
def status() -> None:
    """Retrieve status information and statistics for Icinga 2."""
    print(get_default_client().get_status())


# v1/config ############################################################################


@click.group(invoke_without_command=True)
@click.pass_context
def config(ctx: click.Context) -> None:
    """Manage configuration packages and stages.

    Manage configuration packages and stages based on configuration files and
    directory trees.
    """
    if ctx.invoked_subcommand is None:
        print(get_default_client().list_all_config_stage_files())
        click.echo("Use a subcommand")


@click.command()
def config_show() -> None:
    print(get_default_client().list_all_config_stage_files())


@click.argument("stage", required=False)
@click.argument("package")
@click.command()
def config_delete(package: str, stage: Optional[str] = None) -> None:
    """Delete a configuration package or a configuration stage entirely."""
    print(get_default_client().delete_config(package, stage))


config.add_command(config_delete, "delete")
config.add_command(config_show, "show")


# v1/types #############################################################################


@click.command()
def types() -> None:
    """Retrieve the configuration object types."""
    print(get_default_client().get_types())


# v1/variables #########################################################################


@click.command()
def variables() -> None:
    """Request information about global variables."""
    print(get_default_client().get_variables())


# other ################################################################################


@click.command()
@click.argument("file")
def check(file: str) -> None:
    """Execute checks and send it to the monitoring server."""
    execute_check(file)


@click.command()
def dump_config() -> None:
    """Dump the configuration of the pretiac client."""
    print(load_config_file())


main.add_command(objects)
main.add_command(actions)
main.add_command(events)
main.add_command(status)
main.add_command(config)
main.add_command(types)
main.add_command(variables)
main.add_command(check)
main.add_command(dump_config)
