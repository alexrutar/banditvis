import pickle
import os


CORE_DEFAULTS = {
    'out': "hi",
    'Animate': False,
    'FPS': 20,
    'HelpLines': True,
    'InputData': False,
    'LevelCurves': True,
    'Multiprocess': 1,
    'NoAxesTick': False,
    'Normalized': False,
    'PlotSave': "temp.pdf",
    'PlotTitle': False,
    'DeleteData': False
}

def load_user():
    with open(os.path.dirname(__file__) + '/user_defaults.pkl', 'rb') as handle:
        _user = pickle.load(handle)
    return _user