# Core Defaults, do not touch these

CORE_DEFAULTS = {
    out: "hi",
    Animate: False,
    FPS: 20,
    HelpLines: True,
    InputData: False,
    LevelCurves: True,
    Multiprocess: 1,
    NoAxesTick: False,
    Normalized: False,
    PlotSave: "temp.pdf",
    PlotTitle: False,
    DeleteData: False
}
# User added defaults, these will overwrite the Core Defaults
USER_DEFAULTS = {
    out: Output,
    data: Data
}