"""A collection of reusable Qt widgets designed for general use in PyQt or PySide applications."""

from qtpy.QtWidgets import QPushButton
from qtpy.QtCore import Signal, Slot, Property


class StatefulButton(QPushButton):
    """A QPushButton that maintains an active/inactive state.

    Parameters
    ----------
    *args : tuple
        Positional arguments passed to QPushButton constructor.
    active : bool, optional
        Initial state of the button (default is False).
    **kwargs : dict
        Keyword arguments passed to QPushButton constructor.

    Attributes
    ----------
    clickedWhileActive : Signal
        Emitted when the button is clicked while it is in the active state.
    clickedWhileInactive : Signal
        Emitted when the button is clicked while it is in the inactive state.
    stateChanged : Signal
        Emitted when the button's state has changed. The signal carries the new state.
    """

    clickedWhileActive = Signal(name='clickedWhileActive')
    clickedWhileInactive = Signal(name='clickedWhileInactive')
    stateChanged = Signal(bool, name='stateChanged')

    def __init__(self, *args, active: bool = False, **kwargs):
        """Initialize the StateButton with the specified active state.

        Parameters
        ----------
        *args : tuple
            Positional arguments passed to QPushButton constructor.
        active : bool, optional
            Initial state of the button (default is False).
        **kwargs : dict
            Keyword arguments passed to QPushButton constructor.
        """
        super().__init__(*args, **kwargs)
        self._isActive = active
        self.clicked.connect(self._onClick)

    @Property(bool)
    def isActive(self) -> bool:
        """Get the active state of the button.

        Returns
        -------
        bool
            True if the button is active, False otherwise.
        """
        return self._isActive

    @Slot(bool)
    def setActive(self, active: bool):
        """Set the active state of the button.

        Emits `stateChanged` if the state has changed.

        Parameters
        ----------
        active : bool
            The new active state of the button.
        """
        if self._isActive != active:
            self._isActive = active
            self.stateChanged.emit(self._isActive)

    @Slot()
    def _onClick(self):
        """Handle the button click event.

        Emits `clickedWhileActive` if the button is active,
        otherwise emits `clickedWhileInactive`.
        """
        if self._isActive:
            self.clickedWhileActive.emit()
        else:
            self.clickedWhileInactive.emit()
