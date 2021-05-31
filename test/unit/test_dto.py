import pytest
import json

from clarity_ext.utils import single

from snpseq_data.clarity.container_repository import ContainerRepository
from snpseq_data.clarity.serialization import SampleDTO, ContainerDTO
from test.unit.test_base import TestBase, FakeSession


class TestDto(TestBase):
    def test_serialize_sample_to_json(self):
        # Arrange
        sample, _ = self.setup_single_sample()
        sample_dto = SampleDTO(sample)

        # Act
        json_str_repr = sample_dto.toJSON()
        print(json_str_repr)

        # Assert
        json_as_dict = json.loads(json_str_repr)
        assert json_as_dict["name"] == "RB-1754-6774"
        assert json_as_dict["project"] == "RB-1754"
        assert json_as_dict["udf_conc_fc"] == "150 pM"

    def test_serialize_container_to_json(self):
        # Arrange
        lims, container_uri = self.setup_flowcell()
        session = FakeSession(lims, container_uri=container_uri)
        container_repo = ContainerRepository(session)
        container = container_repo.get('HKV5JCCXY')
        container_dto = ContainerDTO(container)

        # Act
        json_str_repr = container_dto.toJSON()
        # print(json_str_repr)

        # Assert
        json_as_dict = json.loads(json_str_repr)
        assert json_as_dict["name"] == "HKV5JCCXY"
        assert len(json_as_dict["samples"]) == 3
        # assert len(json_as_dict["projects"]) == 1
        samples = json_as_dict["samples"]
        sample1 = single([s for s in samples if s["name"] == "RB-1754-6774"])
        assert sample1["udf_conc_fc"] == "150 pM"
