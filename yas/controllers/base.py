from cement import Controller, ex
from ..core.version import get_version
from time import strftime
import os
import sys
from tabulate import tabulate

VERSION_BANNER = """
Yas - An aliasing manager for your terminal commands! v.%s
""" % (get_version())


class Base(Controller):
    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Yas - An aliasing manager for your terminal commands!'

        # text displayed at the bottom of --help output
        epilog = '''Usage:
         yas add <ALIAS> <COMMAND>
         yas run <ALIAS>
         yas get <ALIAS>
         yas list
        '''

        # controller level arguments. ex: 'yas --version'
        arguments = [
            (['-v', '--version', '--ver'],
             {
                 'action': 'version',
                 'version': VERSION_BANNER
             })
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(

        help='Add new alias to a command',

        arguments=[
            (
                    [],
                    {
                        'help': 'alias name',
                        'action': 'store',
                        'dest': 'alias'
                    }
            ),
            (
                    [],
                    {
                        'help': 'Full command that will be aliased',
                        'action': 'store',
                        'dest': 'command'
                    }
            )
        ]
    )
    def add(self):
        """adds a new alias to a command"""

        ## check if the alias or the command is not there
        if self.app.pargs.alias is None:
            self.app.log.error('Need to add an alias to the command')
            self.app.log.error('Ex: yas add <ALIAS> <COMMAND>')
        elif self.app.pargs.command is None:
            self.app.log.error('Need to add an command to be aliased')
            self.app.log.error('Ex: yas add <ALIAS> <COMMAND>')
        else:
            message = "Added an alias ({}) for the command => ({})".format(self.app.pargs.alias,
                                                                           self.app.pargs.command)
            now = strftime("%Y-%m-%d %H:%M:%S")
            record = {
                'timestamp': now,
                'command': self.app.pargs.command,
                'alias': self.app.pargs.alias,
                'active': True
            }

            self.app.db.insert(record)
            self.app.log.info(message)

    @ex(

        help='Runs an alias command',

        arguments=[
            (
                    [],
                    {
                        'help': 'alias name',
                        'action': 'store',
                        'dest': 'alias'
                    }
            )
        ]
    )
    def run(self):
        """Runs an alias command"""

        if self.app.pargs.alias is None:
            self.app.log.error('Need to add an alias to run')
            self.app.log.error('Hint: yas run <ALIAS> ')
        else:
            matched_record = self.app.db.search(self.app.db_search('alias') == self.app.pargs.alias)
            if not matched_record:
                # we don't have this alias
                self.app.log.error('Alias ({}) not added before'.format(self.app.pargs.alias))
                self.app.log.error('Hint: yas add <ALIAS> <COMMAND> ')
            else:
                command = matched_record[0]['command']
                self.app.log.info('{}'.format(command))
                result = os.system(command)
                if result != 0:
                    print(result)

    @ex(

        help='List Saved Commands'
    )
    def list(self):
        '''Give a list of all aliases'''
        data = self.app.db.all()
        headers = ["Alias", "Command"]
        rows = map(lambda l: [l["alias"], l["command"]], data)
        table = tabulate(tabular_data=rows,
                         headers=headers,
                         showindex=True)
        print(table)

    @ex(

        help='Gets an aliased command',

        arguments=[
            (
                    [],
                    {
                        'help': 'alias name',
                        'action': 'store',
                        'dest': 'alias'
                    }
            )
        ]
    )
    def get(self):
        """Gets a command by its alias"""

        if self.app.pargs.alias is None:
            self.app.log.error('Need to add an alias to get')
            self.app.log.error('Hint: yas get <ALIAS> ')
        else:
            matched_record = self.app.db.search(self.app.db_search('alias') == self.app.pargs.alias)
            # print(matched_record)
            if not matched_record:
                # we don't have this alias
                self.app.log.error('Alias ({}) not added before'.format(self.app.pargs.alias))
                self.app.log.error('Hint: yas add <ALIAS> <COMMAND> ')
            else:
                command = matched_record[0]['command']
                print(command)

    @ex(

        help='Remove an aliased Command',

        arguments=[
            (
                    [],
                    {
                        'help': 'alias name',
                        'action': 'store',
                        'dest': 'alias'
                    }
            )
        ]
    )
    def remove(self):
        """Remove a command by its alias"""
        if self.app.pargs.alias is None:
            self.app.log.error('No Alias Found!')
            self.app.log.error('Hint: yas remove <ALIAS> ')
        else:
            matched_record = self.app.db.search(self.app.db_search('alias') == self.app.pargs.alias)
            if not matched_record:
                # we don't have this alias
                self.app.log.error('Alias ({}) not added before'.format(self.app.pargs.alias))
                self.app.log.error('Hint: yas add <ALIAS> <COMMAND> ')
            else:
                self.app.db.remove(self.app.db_search('alias') == matched_record[0]['alias'])
                self.app.log.info('Alias ({}) deleted'.format(self.app.pargs.alias))


    @ex(
        help='Clean all aliases',
    )

    def drop(self):
        """Remove a command by its alias"""
        self.app.db.purge()