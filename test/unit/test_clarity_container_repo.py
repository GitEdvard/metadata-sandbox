import pytest
from snpseq_data.clarity.container_repository import ContainerRepository
from test.unit.test_base import TestBase, FakeSession


class TestClarityContainerRepo(TestBase):
    def test_container_repo_get__2_analytes_found(self):
        # Arrange
        lims, container_uri = self.setup_flowcell()
        session = FakeSession(lims, container_uri=container_uri)
        container_repo = ContainerRepository(session)

        # Act
        container = container_repo.get('HKV5JCCXY')

        # Assert
        contents = [well.artifact for well in container.occupied]
        # for a in contents:
        #     print(a.name, a.id)
        assert len(contents) == 2
        # assert False

    @pytest.mark.now
    def test_container_repo_get__3_samples_found(self):
        # Arrange
        lims, container_uri = self.setup_flowcell()
        session = FakeSession(lims, container_uri=container_uri)
        container_repo = ContainerRepository(session)

        # Act
        container = container_repo.get('HKV5JCCXY')

        # Assert
        assert len(container.samples) == 3
