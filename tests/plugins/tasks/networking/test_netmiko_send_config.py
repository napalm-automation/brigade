from nornir.plugins.tasks import connections, networking


class Test(object):
    def test_explicit_netmiko_connection(self, nornir):
        nornir.filter(name="dev4.group_2").run(task=connections.netmiko_connection)
        result = nornir.filter(name="dev4.group_2").run(
            networking.netmiko_send_config, config_commands="hostname"
        )
        assert result
        for h, r in result.items():
            assert h in r.result.strip()

    def test_netmiko_send_command(self, nornir):
        result = nornir.filter(name="dev4.group_2").run(
            networking.netmiko_send_config, config_commands="hostname"
        )
        assert result
        for h, r in result.items():
            assert h in r.result.strip()
