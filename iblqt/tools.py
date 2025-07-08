"""Miscellaneous tools that don't fit the other categories."""

import logging
import sys
from functools import wraps

from qtpy.QtWidgets import QApplication, QMainWindow

logger = logging.getLogger(__name__)


def get_or_create_app(argv: list[str] | None = None) -> QApplication:
    """
    Return the existing QApplication instance or create a new one.

    This helper checks for an existing QApplication instance; if none exists,
    it creates a new instance using the provided command-line arguments.
    This is useful when writing tools or scripts that may be used both within
    an existing Qt context or as standalone applications.

    Parameters
    ----------
    argv : list of str, optional
        Command-line arguments to pass to QApplication. If `None`, `sys.argv` is used.

    Returns
    -------
    QApplication
        The existing or newly created QApplication instance.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication(argv or sys.argv)
    return app


def require_qt(func):
    """
    Specify that a function requires a running Qt application.

    Use this decorator to wrap functions that depend on a QApplication
    being active. If no QApplication is running at the time the function
    is called, a RuntimeError is raised.

    Parameters
    ----------
    func : callable
        The function that requires a Qt application.

    Returns
    -------
    callable
        A wrapped function that checks for an active QApplication before execution.

    Raises
    ------
    RuntimeError
        If no QApplication instance is running when the function is called.
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        if QApplication.instance() is None:
            raise RuntimeError('This function requires a running Qt application.')
        return func(*args, **kwargs)

    return wrapped


def run_app(argv: list[str] | None = None) -> int:
    """
    Run the Qt application event loop.

    This function ensures a QApplication exists, starts its event loop,
    and blocks until the application exits. This is typically called
    at the end of a script or application entry point.

    Parameters
    ----------
    argv : list of str, optional
        Command-line arguments to pass to QApplication. If `None`, `sys.argv` is used.

    Returns
    -------
    int
        The exit code returned by the Qt application's event loop.
    """
    app = get_or_create_app(argv)
    return app.exec_()


@require_qt
def get_main_window() -> QMainWindow:
    """
    Get the main QMainWindow instance of the running Qt application.

    This function searches all top-level widgets in the current QApplication
    instance and returns the first one that is an instance of QMainWindow.

    Returns
    -------
    QMainWindow
        The first top-level widget that is a QMainWindow.

    Raises
    ------
    RuntimeError
        If no QApplication is running or no QMainWindow is found.
    """
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    raise RuntimeError('No QMainWindow instance found among top-level widgets.')
