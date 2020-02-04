import importlib

from nana import ASSISTANT_LOAD, ASSISTANT_NOLOAD, log

def __list_all_modules():
    from os.path import dirname, basename, isfile
    import glob
    # This generates a list of modules in this folder for the * in __main__ to work.
    mod_paths = glob.glob(dirname(__file__) + "/*.py")
    all_modules = [basename(f)[:-3] for f in mod_paths if isfile(f)
                   and f.endswith(".py")
                   and not f.endswith('__init__.py')]

    if ASSISTANT_LOAD or ASSISTANT_NOLOAD:
        to_Load = ASSISTANT_LOAD
        if to_Load:
            if not all(any(mod == module_name for module_name in all_modules) for mod in to_Load):
                log.error("Invalid Module name for Assistant bot!")
                quit(1)

        else:
            to_Load = all_modules

        if ASSISTANT_NOLOAD:
            log.info("Not loaded: {}".format(ASSISTANT_NOLOAD))
            return [item for item in to_Load if item not in ASSISTANT_NOLOAD]

        return to_Load

    return all_modules


ALL_SETTINGS = sorted(__list_all_modules())
log.info("Assistant bot module loaded: %s", str(ALL_SETTINGS))
__all__ = ALL_SETTINGS + ["ALL_SETTINGS"]
