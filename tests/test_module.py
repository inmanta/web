from pytest_inmanta.plugin import Project


def test_module(project: Project) -> None:
    project.compile("import web")
