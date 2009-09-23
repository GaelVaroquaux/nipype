"""Grab documentation from spm."""

import os

from nipype.interfaces import matlab

spm_doc_names = {'spm_realign' : 'Realign: Estimate & Reslice',
                 'spm_coreg' : 'Coreg: Estimate & Reslice',
                 'spm_normalise' : 'Normalise: Estimate & Write',
                 'spm_segment' : 'Segment',
                 'spm_smooth' : 'Smooth',
                 'spm_fmri_design' : 'fMRI model specification (design only)',
                 }

def grab_doc(funcname):
    """Grab the SPM documentation for the given function name `funcname`.
    
    Parameters
    ----------
    funcname : {'spm_realign', 'coreg'}
        Function for which we are grabbing documentation.

    """

    cmd = matlab.MatlabCommandLine()
    # We need to tell Matlab where to find our spm_get_doc.m file.
    cwd = os.path.dirname(__file__)
    cmd.inputs.cwd = cwd
    try:
        name = spm_doc_names[funcname]
        mcmd = "spm_get_doc('%s')" % name
        #print 'matlab command:\n', mcmd
        cmd.inputs.script_lines = mcmd
    except KeyError:
        raise KeyError('funcname must match one of the options listed')
    
    out = cmd.run()
    #doc = out.runtime.stdout
    return _strip_header(out.runtime.stdout)


def _strip_header(doc):
    """Strip Matlab header and splash info off doc.

    Searches for the tag 'NIPYPE' in the doc and returns everyting after that.

    """
    hdr = 'NIPYPE'
    cruft = '\x1b' # There's some weird cruft at the end of the
                   # docstring, almost looks like the hex for the
                   # escape character 0x1b.
    try:
        index = doc.index(hdr)
        index += len(hdr)
        index += 2
        doc = doc[index:]
        index = doc.index(cruft)
        return doc[:index]
    except KeyError:
        raise IOError('This docstring was not generated by Nipype!\n')
