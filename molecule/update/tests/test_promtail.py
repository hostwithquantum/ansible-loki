import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('promtail')


def test_external_labels(host):
    f = host.file('/etc/promtail/promtail.yml')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'

    assert f.contains("tenant_id: luzilla")
    assert f.contains("node: instance")
