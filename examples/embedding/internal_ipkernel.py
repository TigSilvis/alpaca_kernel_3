"""An internal alpaca_kernel example."""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import sys

from IPython.lib.kernel import connect_qtconsole

from alpaca_kernel.kernelapp import IPKernelApp


# -----------------------------------------------------------------------------
# Functions and classes
# -----------------------------------------------------------------------------
def mpl_kernel(gui):
    """Launch and return an IPython kernel with matplotlib support for the desired gui"""
    kernel = IPKernelApp.instance()
    kernel.initialize(
        [
            "python",
            "--matplotlib=%s" % gui,
            #'--log-level=10'
        ]
    )
    return kernel


class InternalIPKernel:
    """An internal alpaca_kernel class."""

    def init_ipkernel(self, backend):
        """Start IPython kernel with GUI event loop and mpl support."""
        self.ipkernel = mpl_kernel(backend)
        # To create and track active qt consoles
        self.consoles = []

        # This application will also act on the shell user namespace
        self.namespace = self.ipkernel.shell.user_ns

        # Example: a variable that will be seen by the user in the shell, and
        # that the GUI modifies (the 'Counter++' button increments it):
        self.namespace["app_counter"] = 0
        # self.namespace['ipkernel'] = self.ipkernel  # dbg

    def print_namespace(self, evt=None):
        """Print the namespace."""
        print("\n***Variables in User namespace***")
        for k, v in self.namespace.items():
            if not k.startswith("_"):
                print(f"{k} -> {v!r}")
        sys.stdout.flush()

    def new_qt_console(self, evt=None):
        """start a new qtconsole connected to our kernel"""
        return connect_qtconsole(self.ipkernel.abs_connection_file, profile=self.ipkernel.profile)

    def count(self, evt=None):
        """Get the app counter value."""
        self.namespace["app_counter"] += 1

    def cleanup_consoles(self, evt=None):
        """Clean up the consoles."""
        for c in self.consoles:
            c.kill()
