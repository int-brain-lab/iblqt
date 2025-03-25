from qtpy.QtCore import Qt

from iblqt import widgets


class TestStatefulButton:
    def test_initial_state(self, qtbot):
        """Test the initial state of the StatefulButton."""
        button = widgets.StatefulButton('Active', 'Inactive', active=False)
        qtbot.addWidget(button)

        assert button.active is False
        assert button.text() == 'Inactive'

    def test_click_inactive_state(self, qtbot):
        """Test clicking the button while inactive."""
        button = widgets.StatefulButton('Active', 'Inactive', active=False)
        qtbot.addWidget(button)

        with qtbot.waitSignal(button.clickedWhileInactive):
            qtbot.mouseClick(button, Qt.LeftButton)

        assert button.active is False

    def test_click_active_state(self, qtbot):
        """Test clicking the button while active."""
        button = widgets.StatefulButton('Active', 'Inactive', active=True)
        qtbot.addWidget(button)

        with qtbot.waitSignal(button.clickedWhileActive):
            qtbot.mouseClick(button, Qt.LeftButton)

        assert button.active is True

    def test_state_change(self, qtbot):
        """Test state change and text update."""
        button = widgets.StatefulButton('Active', 'Inactive', active=False)
        qtbot.addWidget(button)

        with qtbot.waitSignal(button.stateChanged):
            button.setActive(True)
        assert button.active is True
        assert button.text() == 'Active'

        with qtbot.waitSignal(button.stateChanged):
            button.setActive(False)
        assert button.active is False
        assert button.text() == 'Inactive'
