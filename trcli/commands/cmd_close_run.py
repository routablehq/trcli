import click

from trcli.api.project_based_client import ProjectBasedClient
from trcli.cli import pass_environment, CONTEXT_SETTINGS, Environment
from trcli.data_classes.dataclass_testrail import TestRailSuite


def print_config(env: Environment):
    env.log(f"Parser Results Execution Parameters"
            f"\n> TestRail instance: {env.host} (user: {env.username})"
            f"\n> Project: {env.project if env.project else env.project_id}"
            f"\n> Suite ID: {env.suite_id}"
            f"\n> Run ID: {env.run_id}")


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--suite-id",
    type=click.IntRange(min=1),
    metavar="",
    help="Suite ID of the test run.",
)
@click.option(
    "--run-id",
    type=click.IntRange(min=1),
    metavar="",
    help="Run ID for the run to be closed.",
)
@click.pass_context
@pass_environment
def cli(environment: Environment, context: click.Context, *args, **kwargs):
    environment.cmd = "close_run"
    environment.set_parameters(context)
    environment.check_for_required_parameters()
    print_config(environment)

    project_client = ProjectBasedClient(
        environment=environment,
        suite=TestRailSuite(name=environment.suite_name, suite_id=environment.suite_id),
    )
    project_client.resolve_project()
    project_client.resolve_suite()
    environment.log(f"Run: {project_client.get_test_run_url(environment.run_id)}")
    project_client.close_test_run(environment.run_id)
