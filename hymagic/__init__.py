# Copyright (c) 2013 Paul Tagliamonte <paultag@debian.org>
# Copyright (c) 2013 Gergely Nagy <algernon@madhouse-project.org>
# Copyright (c) 2013 James King <james@agentultra.com>
# Copyright (c) 2013 Julien Danjou <julien@danjou.info>
# Copyright (c) 2013 Konrad Hinsen <konrad.hinsen@fastmail.net>
# Copyright (c) 2013 Thom Neale <twneale@gmail.com>
# Copyright (c) 2013 Will Kahn-Greene <willg@bluesock.org>
# Copyright (c) 2013 Bob Tolbert <bob@tolbert.org>
#
# hymagic is an adaptation of the HyRepl to allow ipython iteration
# hymagic author - Todd Iverson
# Available as github.com/yardsale8/hymagic
#
# Copyright (c) 2018 Greg Werbin <outthere@me.gregwerbin.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import ast
import sys

import hy
from hy.lex import LexException, PrematureEndOfInput, tokenize
from hy.compiler import hy_compile, HyTypeError
from hy.importer import ast_compile
from IPython.core.magic import Magics, magics_class, line_cell_magic

SIMPLE_TRACEBACKS = True

@magics_class
class HyMagics(Magics):
    """ IPython magic for Hy """
    def __init__(self, shell):
        """
        Parameters
        ----------
        shell : IPython shell
        """
        super(HyMagics, self).__init__(shell)

    @line_cell_magic
    def hy(self, line, cell=None, filename='<input>', symbol='single'):
        """ Ipython magic function for running hylang code in ipython

        Note that we pass the AST directly to IPython.
        """
        global SIMPLE_TRACEBACKS
        source = cell if cell else line

        try:
            tokens = tokenize(source)
        except PrematureEndOfInput:
            print("Premature End of Input")
        except LexException as e:
            if e.source is None:
                e.source = source
                e.filename = filename
            print(str(e))

        try:
            _ast = hy_compile(tokens, "__console__", root=ast.Interactive)
            self.shell.run_ast_nodes(_ast.body,'<input>',compiler=ast_compile)
        except HyTypeError as e:
            if e.source is None:
                e.source = source
                e.filename = filename
            if SIMPLE_TRACEBACKS:
                print(str(e))
            else:
                self.shell.showtraceback()
        except Exception:
            self.shell.showtraceback()

    @line_cell_magic
    def hylang(self, line, cell=None, filename='<input>', symbol='single'):
        """ Legacy alias for %hy / %%hy """
        return self.hy(line, cell=cell, filename=filename, symbol=symbol)


def load_ipython_extension(ipython):
    """ Load the extension in IPython """
    ipython.register_magics(HyMagics)
