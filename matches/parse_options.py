"""Simple option parsing, for those for whom life is too short for argparse."""
import sys
from collections import OrderedDict


def decode_option(arg):
    """Decode an option in -foo or -foo=bar format, returning key and value.

    If no value is provided, gives None.

    >>> decode_option('-face')
    ('face', None)
    >>> decode_option('-face=eyes')
    ('face', 'eyes')
    >>> decode_option('bee')
    Traceback (most recent call last):
     ...
    ValueError: Argument does not begin with a '-'

    """
    if arg[0] != '-':
        raise ValueError("Argument does not begin with a '-'")
    components = arg[1:].split('=', 1)
    assert 1 <= len(components) <= 2, "unexpected component count"
    key = components[0]
    value = components[1] if len(components) == 2 else None
    return key, value

class OptionParser(object):
    """A handler for system options. Simpler than argparse or optparse.

    This implements argument parsing in -key=value format, doing little
    further interpretation.

    """
    def __init__(self):
        """Standard constructor, nothing wacky.

        >>> parser = OptionParser()
        >>> parser.options
        OrderedDict()
        >>> parser.arguments
        []
        >>> parser.parse_options
        True
        >>> parser.program_name is None
        True

        """
        self.options = OrderedDict()
        self.arguments = []
        self.parse_options = True
        self.program_name = None

    def handle_arg(self, arg):
        """Handle a single argument, doing whatever parsing necessary.

        >>> parser = OptionParser()
        >>> parser.handle_arg('bees')
        >>> parser.arguments
        ['bees']
        >>> parser.handle_arg('-eyes')
        >>> 'eyes' in parser.options
        True
        >>> parser.handle_arg('-kitten=face')
        >>> parser['kitten']
        'face'
        >>> parser.handle_arg('-kitten=eyes')
        >>> parser['kitten']
        'eyes'
        >>> parser.handle_arg('--')
        >>> parser.parse_options
        False
        >>> parser.handle_arg('-kitten=eyes')
        >>> parser.arguments
        ['bees', '-kitten=eyes']
        >>> parser.handle_arg('')
        Traceback (most recent call last):
         ...
        ValueError: cannot handle an empty argument

        """
        if not arg:
            raise ValueError('cannot handle an empty argument')
        if arg[0] == '-' and self.parse_options:
            if arg == '--':
                self.stop_handling_options()
            else:
                key, value = decode_option(arg)
                self.add_option(key, value)
        else:
            self.add_argument(arg)

    def handle_args(self, args):
        """Handle a sequence of arguments, calling handle_arg on each.

        >>> parser = OptionParser()
        >>> parser.handle_args(['-face', '-bees', 'eyes'])
        >>> parser.options
        OrderedDict([('face', None), ('bees', None)])
        >>> parser.arguments
        ['eyes']

        """
        for arg in args:
            self.handle_arg(arg)

    def handle_argv(self, argv):
        """Handle a sys.argv-style array of arguments, using the first to
        determine the program name and the rest being passed on to
        parser.handle_args.

        >>> parser = OptionParser()
        >>> parser.handle_argv(['rm', '-recursive', '-force', '/'])
        >>> parser.program_name
        'rm'
        >>> parser.arguments
        ['/']
        >>> parser.options.keys()
        ['recursive', 'force']

        """
        self.program_name = argv[0]
        self.handle_args(argv[1:])

    def handle_all(self):
        """Handle the arguments passed to the program in sys.argv.

        Just a wrapper around handle_argv.

        >>> parser = OptionParser()
        >>> parser.handle_all()
        >>> import sys
        >>> parser.program_name == sys.argv[0]
        True

        """
        import sys
        self.handle_argv(sys.argv)

    def auto_compute_program_name(self):
        """Attempt to automatically determine the program name from the system.

        This is guaranteed to produce a name as a string.

        >>> parser = OptionParser()
        >>> parser.auto_compute_program_name()
        >>> type(parser.program_name)
        <type 'str'>
        >>> import sys
        >>> sys.argv = []
        >>> parser.auto_compute_program_name()
        >>> parser.program_name
        '<script>'
        >>> sys.argv.append('faces.py')
        >>> parser.auto_compute_program_name()
        >>> parser.program_name
        'faces.py'

        """
        if sys.argv:
            self.program_name = sys.argv[0]
        else:
            self.program_name = '<script>'

    def stop_handling_options(self):
        """Stop handling any options, interpreting anything onwards as an
        argument.

        >>> parser = OptionParser()
        >>> parser.stop_handling_options()
        >>> parser.handle_arg('-eyes')
        >>> parser.arguments
        ['-eyes']
        >>> parser.options.keys()
        []

        """
        self.parse_options = False

    def add_option(self, key, value = None):
        """Add a single option to the list of options, with an optional value.

        >>> parser = OptionParser()
        >>> parser.add_option('eyes')
        >>> parser.add_option('bees', 'cheese')
        >>> parser.options
        OrderedDict([('eyes', None), ('bees', 'cheese')])

        """
        self.options[key] = value

    def add_argument(self, arg):
        """Add a single argument to the list of arguments.

        >>> parser = OptionParser()
        >>> parser.add_argument('kitten')
        >>> parser.arguments
        ['kitten']

        """
        self.arguments.append(arg)

    def __getitem__(self, name):
        """Get a single option from the options dict.

        >>> parser = OptionParser()
        >>> parser.add_option('eye', 'bacon')
        >>> parser['eye']
        'bacon'
        >>> parser.add_option('face')
        >>> parser['face'] is None
        True
        >>> parser['kitten']
        Traceback (most recent call last):
         ...
        KeyError: 'kitten'

        """
        if name not in self.options:
            raise KeyError(name)
        return self.options[name]

    def __contains__(self, name):
        """Check if an option is specified.

        >>> parser = OptionParser()
        >>> parser.add_option('pony')
        >>> 'pony' in parser
        True
        >>> 'death' in parser
        False

        """
        return name in self.options

def test():
    """Run the option parser unit tests."""
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    test()

