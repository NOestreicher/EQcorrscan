"""EQcorrscan is a python module designed to run match filter routines for \
seismology, within it are routines for integration to seisan and obspy. \
With obspy integration (which is necessary) all main waveform formats can be \
read in and output.

This main section contains a script, LFE_search.py which demonstrates the usage
of the built in functions from template generation from picked waveforms
through detection by match filter of continuous data to the generation of lag
times to be used for relative locations.

The match-filter routine described here was used a previous Matlab code for the
Chamberlain et al. 2014 G-cubed publication.  The basis for the lag-time
generation section is outlined in Hardebeck & Shelly 2011, GRL.

Code generated by Calum John Chamberlain of Victoria University of Wellington,
2015.

All rights reserved.

Pre-requisites:
    gcc             - for the installation of the openCV correlation routine
    python-joblib   - used for parallel processing
    python-obspy    - used for lots of common seismological processing
                    - requires:
                        numpy
                        scipy
                        matplotlib
    python-pylab    - used for plotting
"""
import sys
import importlib
import warnings


__all__ = ['Sfile_util', 'pre_processing', 'findpeaks', 'plotting',
           'mag_calc', 'catalog_to_dd', 'clustering',
           'seismo_logs', 'stacking', 'synth_seis', 'timer']

# Cope with changes to name-space to remove most of the camel-case
_import_map = {
    "catalogue2DD": "catalog_to_dd",
    "EQcorrscan_plotting": "plotting"
}


class EQcorrscanDeprecationWarning(UserWarning):
    """
    Force pop-up of warnings.
    """
    pass


class EQcorrscanRestructureAndLoad(object):
    """
    Path finder and module loader for transitioning
    """
    def find_module(self, fullname, path=None):
        # Compatibility with namespace paths.
        if hasattr(path, "_path"):
            path = path._path

        if not path or not path[0].startswith(__path__[0]):
            return None

        for key in _import_map.keys():
            if fullname.startswith(key):
                break
        else:
            return None
        return self

    def load_module(self, name):
        # Use cached modules.
        if name in sys.modules:
            return sys.modules[name]
        # Otherwise check if the name is part of the import map.
        elif name in _import_map:
            new_name = _import_map[name]
        else:
            new_name = name
            for old, new in _import_map.items():
                if not new_name.startswith(old):
                    continue
                new_name = new_name.replace(old, new)
                break
            else:
                return None

        # Don't load again if already loaded.
        if new_name in sys.modules:
            module = sys.modules[new_name]
        else:
            module = importlib.import_module(new_name)

        # Warn here as at this point the module has already been imported.
        warnings.warn("Module '%s' is deprecated and will stop working "
                      "with the next EQcorrscan version. Please import module "
                      "'%s' instead." % (name, new_name),
                      EQcorrscanDeprecationWarning)
        sys.modules[new_name] = module
        sys.modules[name] = module
        return module


sys.meta_path.append(EQcorrscanRestructureAndLoad())



if __name__ == '__main__':
    import doctest
    doctest.testmod(exclude_empty=True)
