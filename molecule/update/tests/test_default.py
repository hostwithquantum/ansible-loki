import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize("name", [
    ("loki"),
    ("promtail"),
])
def test_promtail_configuration(host, name):
    f = host.file('/etc/' + name + '/' + name + '.yml')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


@pytest.mark.parametrize("name", [
    ("loki"),
    ("promtail"),
])
def test_services_enabled(host, name):
    svc = host.service(name)
    assert svc.is_running
    assert svc.is_enabled


@pytest.mark.parametrize("name", [
    ("loki"),
    ("promtail"),
])
def test_version(host, name):
    version_output = host.check_output("/usr/local/bin/" + name + " -version")
    assert "1.6.1" in version_output
