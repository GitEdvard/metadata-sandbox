import os


def read_binary_file(path):
    with open(path, 'rb') as f:
        contents = f.read()
    return contents


def get_directory(sub_dir):
    this_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(this_dir, sub_dir)


def get_single_sample():
    dirr = get_directory('flowcell_w_3_artifacts')
    path = os.path.join(dirr, 'sample1.xml')
    return read_binary_file(path)


def get_single_project():
    dirr = get_directory('flowcell_w_3_artifacts')
    path = os.path.join(dirr, 'project.xml')
    return read_binary_file(path)


def get_container_from(subdir):
    xml_contents = ContainerXmlContents()
    ddir = get_directory(subdir)
    path = os.path.join(ddir, 'container1.xml')
    xml_contents.container = read_binary_file(path)
    path = os.path.join(ddir, 'project.xml')
    xml_contents.project = read_binary_file(path)

    for filename in os.listdir(ddir):
        path = os.path.join(ddir, filename)
        if filename.endswith('.xml') and filename.startswith('artifact'):
            xml_contents.artifacts.append(read_binary_file(path))

        if filename.endswith('.xml') and filename.startswith('sample'):
            xml_contents.samples.append(read_binary_file(path))

    path = os.path.join(ddir, 'container_type.xml')
    xml_contents.container_type = read_binary_file(path)
    return xml_contents


class ContainerXmlContents(object):
    def __init__(self):
        self.container = None
        self.artifacts = list()
        self.container_type = None
        self.samples = list()
        self.project = None
