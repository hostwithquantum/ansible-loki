import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_only_promtail_is_present(host):
    promtail = host.service("promtail")
    assert promtail.is_running
    assert promtail.is_enabled


def test_promtail_version(host):
    version_output = host.check_output("/usr/local/bin/promtail -version")
    assert "1.6.1" in version_output


def test_loki_is_not_install(host):
    loki = host.service("loki")
    assert not loki.is_running
    assert not loki.is_enabled
    assert not host.file("/usr/local/bin/loki").exists
