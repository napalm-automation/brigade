from brigade.core.exceptions import CommandError
from brigade.plugins.tasks import commands


class Test(object):

    def test_command(self, brigade):
        result = brigade.run(commands.command, command="echo {host.name}")
        assert result
        for h, r in result.items():
            assert h == r.stdout.strip()

    def test_command_error(self, brigade):
        result = brigade.run(commands.command, command="ech")
        processed = False
        for r in result.values():
            processed = True
            assert isinstance(r.exception, OSError)
        assert processed
        brigade.data.reset_failed_hosts()

    def test_command_error_generic(self, brigade):
        result = brigade.run(commands.command, command="ls /asdadsd")
        processed = False
        for r in result.values():
            processed = True
            assert isinstance(r.exception, CommandError)
        assert processed
        brigade.data.reset_failed_hosts()
