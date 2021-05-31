import xml.etree.ElementTree as ET
from clarity_ext.domain import UdfMapping, Project
from clarity_ext.domain.aliquot import Sample
from clarity_ext.inversion_of_control.ioc import ioc
from clarity_ext.service.application import ApplicationService
from genologics.entities import Sample as GenologicsSample, Artifact, Container, Containertype
from genologics.entities import Project as GenologicsProject
from genologics.lims import Lims
from test.unit.resources.resource_bag import get_single_sample, get_container_from, get_single_project


class TestBase(object):
    def init_cache_with(self, lims, xml_string, entity_class):
        root = ET.fromstring(xml_string)
        uri = root.attrib['uri']
        split_uri = uri.split('?state')
        stateless_uri = split_uri[0]
        fetched_entity = entity_class(lims, uri=stateless_uri)
        fetched_entity.root = root
        lims.cache[stateless_uri] = fetched_entity
        return stateless_uri

    def setup_single_project(self, lims=None):
        if lims is None:
            lims = Lims('', '', '')
        xml = get_single_project()
        uri = self.init_cache_with(lims, xml, GenologicsProject)
        resource = lims.cache[uri]
        udf_map = UdfMapping(resource.udf)
        project = Project(resource.name)
        return project, lims

    def setup_single_sample(self):
        lims = Lims('', '', '')
        project, _ = self.setup_single_project(lims)
        xml = get_single_sample()
        uri = self.init_cache_with(lims, xml, GenologicsSample)
        resource = lims.cache[uri]
        udf_map = UdfMapping(resource.udf)
        sample = Sample(resource.id,
                        resource.name,
                        project,
                        udf_map,
                        mapper=None)
        sample.api_resource = resource
        return sample, lims

    def setup_flowcell(self):
        lims = Lims('', '', '')
        xml_contents = get_container_from('flowcell_w_3_artifacts')
        for s in xml_contents.samples:
            self.init_cache_with(lims, s, GenologicsSample)

        for a in xml_contents.artifacts:
            self.init_cache_with(lims, a, Artifact)

        self.init_cache_with(lims, xml_contents.project, GenologicsProject)
        uri = self.init_cache_with(lims, xml_contents.container, Container)
        self.init_cache_with(lims, xml_contents.container_type, Containertype)
        return lims, uri


class FakeSession(object):
    def __init__(self, lims, container_uri):
        lims.get_containers = self.get_containers
        lims.get_batch = self.get_batch
        self.api = lims
        self.container_uri = container_uri
        ioc.set_application(ApplicationService(self))

    def get_containers(self, name=None, type=None,
                       state=None, last_modified=None,
                       udf=dict(), udtname=None, udt=dict(), start_index=None,
                       add_info=False):
        return [Container(self.api, uri=self.container_uri)]

    def get_batch(self, instances, force=False):
        entities = list()
        clazz = self._get_class_for(instances)
        for i in instances:
            entities.append(clazz(self.api, uri=i.uri))
        return entities

    def _get_class_for(self, instances):
        if len(instances) == 0:
            return None

        if isinstance(instances[0], Artifact):
            return Artifact

        if isinstance(instances[0], GenologicsSample):
            return GenologicsSample

        return None
