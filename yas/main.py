import os
# from tinydb import TinyDB, where
from tinydb import *
from cement.utils import fs
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import YasError
from .controllers.base import Base

# configuration defaults
CONFIG = init_defaults('yas')
CONFIG['yas']['foo'] = 'bar'
CONFIG['yas']['db_file'] = '~/.yas/db.json'


def extend_tinydb(app):
    db_file = app.config.get('yas', 'db_file')

    # ensure that we expand the full path
    db_file = fs.abspath(db_file)

    # ensure our parent directory exists
    db_dir = os.path.dirname(db_file)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    app.extend('db', TinyDB(db_file))
    app.extend('db_search',where)

class Yas(App):
    """Yas primary application."""

    class Meta:
        label = 'yas'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        close_on_exit = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        # register handlers
        handlers = [
            Base
        ]

        ## hooking application
        hooks = [
            ('post_setup', extend_tinydb)
        ]


class YasTest(TestApp,Yas):
    """A sub-class of Yas that is better suited for testing."""

    class Meta:
        label = 'yas'


def main():
    with Yas() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except YasError:
            print('YasError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
