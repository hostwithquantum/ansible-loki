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
    version_output = host.check_output("docker images grafana/promtail")
    assert "1.6.1" in version_output


def test_promtail_port_binding(host):
    metrics_output = host.check_output("curl http://127.0.0.1:9080/metrics")
    assert len(metrics_output) > 0
    assert "cortex_deprecated_flags_inuse_total 0" in metrics_output
