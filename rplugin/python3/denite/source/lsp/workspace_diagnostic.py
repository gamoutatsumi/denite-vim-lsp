from denite.base.source import Base

import os

DIAGNOSTIC_KINDS = {
    "E": "Error",
    "W": "Warning",
    "I": "Information",
    "H": "Hint"
}


class Source(Base):
    def __init__(self, vim):
        super().__init__(vim)
        self.vim = vim
        self.name = 'lsp/workspace_diagnostic'
        self.kind = 'file'

        self.vim.vars['denite#source#vim_lsp#_results'] = []
        self.vim.vars['denite#source#vim_lsp#_request_completed'] = False

    def gather_candidates(self, context):
        return make_candidates(
            self.vim.call('denite_vim_lsp#workspace_diagnostics'))


def make_candidates(diagnostics):
    if not diagnostics:
        return []
    if not isinstance(diagnostics, list):
        return []
    candidates = [_parse_candidate(diagnostic) for diagnostic in diagnostics]
    return candidates


def _parse_candidate(diagnostic):
    candidate = {}
    fp = diagnostic['filename']

    candidate['word'] = '{} {}:{} [{}]  {}'.format(
        os.path.basename(fp),
        str(diagnostic['lnum']),
        str(diagnostic['col']),
        DIAGNOSTIC_KINDS[diagnostic['type']],
        diagnostic['text'],
    )

    candidate['action__path'] = fp
    candidate['action__line'] = diagnostic['lnum']
    candidate['action__col'] = diagnostic['col']
    return candidate
