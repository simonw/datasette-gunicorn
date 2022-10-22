import click
from datasette import hookimpl
import gunicorn.app.base


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self, app, options):
        self.app = app
        self.options = options
        super().__init__()

    def load_config(self):
        # Without this we get NotImplementedError
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)
        self.cfg.set("worker_class", "uvicorn.workers.UvicornWorker")

    def load(self):
        return self.app


def serve_with_gunicorn(**kwargs):
    from datasette import cli

    workers = kwargs.pop("workers")
    port = kwargs["port"]
    host = kwargs["host"]
    kwargs["return_instance"] = True
    ds = cli.serve.callback(**kwargs)
    asgi = StandaloneApplication(
        app=ds.app(),
        options={
            "bind": "{}:{}".format(host, port),
            "workers": workers,
        },
    )
    asgi.run()


@hookimpl
def register_commands(cli):
    serve_command = cli.commands["serve"]
    params = serve_command.params[:]
    params.append(
        click.Option(
            ["-w", "--workers"],
            type=int,
            default=1,
            help="Number of Gunicorn workers",
            show_default=True,
        )
    )
    gunicorn_command = click.Command(
        name="gunicorn",
        params=params,
        callback=serve_with_gunicorn,
        short_help="Serve Datasette using Gunicorn",
        help="Start a Gunicorn server running to serve Datasette",
    )
    cli.add_command(gunicorn_command, name="gunicorn")
