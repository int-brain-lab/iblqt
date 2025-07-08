"""Miscellaneous tools that don't fit the other categories."""

import sys
from functools import wraps
from typing import Callable, TypeVar, cast

from qtpy.QtWidgets import QApplication, QMainWindow

F = TypeVar('F', bound=Callable)


def get_app() -> QApplication:
    """
    Get the current QApplication instance.

    This function retrieves the existing QApplication instance. If no such instance
    exists or the instance is not of type QApplication (e.g., it's a QCoreApplication),
    a RuntimeError is raised.

    Returns
    -------
    QApplication
        The currently running QApplication instance.

    Raises
    ------
    RuntimeError
        If there is no running QApplication instance or if it is not a QApplication.
    """
    app = QApplication.instance()
    if not isinstance(app, QApplication):
        raise RuntimeError('No QApplication instance is currently running.')
    return app


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
    try:
        return get_app()
    except RuntimeError:
        return QApplication(argv or sys.argv)


def require_qt(func: F) -> F:
    """
    Specify that a function requires a running Qt application.

    Use this decorator to wrap functions that depend on a QApplication
    being active. If no QApplication is running at the time the function
    is called, a RuntimeError is raised.

    Parameters
    ----------
    func : Callable
        The function that requires a Qt application.

    Returns
    -------
    Callable
        The wrapped function with Qt application requirement enforcement.

    Raises
    ------
    RuntimeError
        If no QApplication instance is running when the function is called.
    """

    @wraps(func)
    def wrapped(*args, **kwargs):
        try:
            get_app()
        except RuntimeError as e:
            raise RuntimeError(
                f"'{func.__name__}' requires a running QApplication."
            ) from e
        return func(*args, **kwargs)

    return cast(F, wrapped)


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
    app = get_app()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    raise RuntimeError('No QMainWindow instance found among top-level widgets.')
