from unittest.mock import MagicMock, patch

import pytest
from qtpy.QtCore import Qt
from qtpy.QtGui import QPainter, QStandardItemModel
from qtpy.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QStyle,
    QStyleOptionViewItem,
    QTableView,
)

from iblqt import widgets
from iblqt.core import QAlyx


class TestCheckBoxDelegate:
    @pytest.fixture
    def setup_method(self, qtbot):
        self.model = QStandardItemModel(5, 1)  # 5 rows, 1 column
        for row in range(5):
            self.model.setData(self.model.index(row, 0), False)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        qtbot.addWidget(self.table_view)

        self.delegate = widgets.CheckBoxDelegate()
        self.table_view.setItemDelegate(self.delegate)

    def test_checkbox_initial_state(self, qtbot, setup_method):
        # Check the initial state of the checkboxes
        for row in range(5):
            index = self.model.index(row, 0)
            assert self.model.data(index) is False  # Initially, all should be False

    def test_checkbox_toggle(self, qtbot, setup_method):
        # Simulate a mouse click to toggle the checkbox
        index = self.model.index(0, 0)  # Get the first checkbox
        rect = self.table_view.visualRect(index)

        # Simulate a mouse click in the center of the checkbox
        qtbot.mouseClick(self.table_view.viewport(), Qt.LeftButton, pos=rect.center())
        assert self.model.data(index) is True

        # Simulate another click to toggle it back
        qtbot.mouseClick(self.table_view.viewport(), Qt.LeftButton, pos=rect.center())
        assert self.model.data(index) is False

    def test_painting_checkbox(self, qtbot, setup_method):
        # Create a QPainter to test the painting of the checkbox
        painter = QPainter(self.table_view.viewport())
        option = QStyleOptionViewItem()
        index = self.model.index(0, 0)

        option.rect = self.table_view.visualRect(index)
        option.state = QStyle.State_On if self.model.data(index) else QStyle.State_Off
        self.delegate.paint(painter, option, index)


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
        assert button.text() == 'Inactive'

        with qtbot.waitSignal(button.clickedWhileInactive):
            qtbot.mouseClick(button, Qt.LeftButton)

        assert button.active is False
        assert button.text() == 'Inactive'

    def test_click_active_state(self, qtbot):
        """Test clicking the button while active."""
        button = widgets.StatefulButton('Active', 'Inactive', active=True)
        qtbot.addWidget(button)
        assert button.text() == 'Active'

        with qtbot.waitSignal(button.clickedWhileActive):
            qtbot.mouseClick(button, Qt.LeftButton)

        assert button.active is True
        assert button.text() == 'Active'

    def test_state_change(self, qtbot):
        """Test state change and text update."""
        button = widgets.StatefulButton('Active', 'Inactive', active=False)
        qtbot.addWidget(button)

        assert button.getTextActive() == 'Active'
        assert button.getTextInactive() == 'Inactive'

        with qtbot.waitSignal(button.stateChanged):
            button.setActive(True)
        with qtbot.assertNotEmitted(button.stateChanged):
            button.setActive(True)
        assert button.active is True
        assert button.text() == 'Active'
        button.setTextActive('Active New')
        assert button.getTextActive() == 'Active New'
        assert button.text() == 'Active New'

        with qtbot.waitSignal(button.stateChanged):
            button.setActive(False)
        with qtbot.assertNotEmitted(button.stateChanged):
            button.setActive(False)
        assert button.active is False
        assert button.text() == 'Inactive'
        button.setTextInactive('Inactive New')
        assert button.getTextInactive() == 'Inactive New'
        assert button.text() == 'Inactive New'


class TestAlyxUserEdit:
    @pytest.fixture
    def setup_method(self, qtbot):
        """Fixture to set up the AlyxUserEdit widget for testing."""
        self.alyx_mock = MagicMock()
        self.user_edit = widgets.AlyxUserEdit(alyx=self.alyx_mock, parent=None)
        qtbot.addWidget(self.user_edit)

    def test_without_username(self, qtbot, setup_method):
        """Test login attempt without username."""
        self.user_edit.setText('')
        qtbot.keyPress(self.user_edit, Qt.Key_Return)
        self.alyx_mock.login.assert_not_called()

    def test_login_success(self, qtbot, setup_method):
        """Test successful login."""
        self.user_edit.setText('test_user')
        qtbot.keyPress(self.user_edit, Qt.Key_Return)
        self.alyx_mock.login.assert_called_once_with(username='test_user')

    def test_on_logged_in(self, qtbot, setup_method):
        """Test UI updates on successful login."""
        assert self.user_edit.isReadOnly() is False
        self.user_edit._onLoggedIn('test_user')
        assert self.user_edit.text() == 'test_user'
        assert self.user_edit.isReadOnly() is True

    def test_on_logged_out(self, qtbot, setup_method):
        """Test UI resets on logout."""
        self.user_edit._onLoggedIn('test_user')
        assert self.user_edit.isReadOnly() is True
        self.user_edit._onLoggedOut()
        assert self.user_edit.text() == ''
        assert self.user_edit.isReadOnly() is False
        assert self.user_edit.styleSheet() == ''

    def test_on_token_missing(self, qtbot, setup_method):
        """Test prompting for password when token is missing."""
        with patch('iblqt.widgets.AlyxLoginDialog', autospec=True) as mock:
            self.user_edit._onTokenMissing('test_user')
            mock.assert_called_once()
            assert 'test_user' in mock.call_args[0]


class TestAlyxLoginWidget:
    @pytest.fixture
    def setup_method(self, qtbot):
        """Fixture to set up the AlyxLoginWidget for testing."""
        self.alyx_mock = MagicMock(spec=QAlyx)
        self.login_widget = widgets.AlyxLoginWidget(alyx=self.alyx_mock, parent=None)
        qtbot.addWidget(self.login_widget)

    def test_instantiation(self, qtbot):
        """Test instantiation."""
        alyx_mock = MagicMock(spec=QAlyx)
        login_widget = widgets.AlyxLoginWidget(alyx=alyx_mock, parent=None)
        qtbot.addWidget(login_widget)
        assert login_widget.alyx is alyx_mock

        with patch('iblqt.core.AlyxClient') as client_mock:
            login_widget = widgets.AlyxLoginWidget(
                alyx='https://example.com', parent=None
            )
            qtbot.addWidget(login_widget)
            client_mock.assert_called_once()
            assert 'https://example.com' in client_mock.call_args[1].values()

    def test_enable_login_button(self, qtbot, setup_method):
        """Test that the login button is enabled when a username is entered."""
        assert not self.login_widget.button.isEnabled()
        self.login_widget.userEdit.setText('test_user')
        assert self.login_widget.button.isEnabled()
        self.login_widget.userEdit.setText('')
        assert not self.login_widget.button.isEnabled()

    def test_login_action(self, qtbot, setup_method):
        """Test that the login action is triggered when the button is clicked."""
        assert self.login_widget.button.text() == 'Login'
        self.login_widget.userEdit.setText('test_user')
        with qtbot.waitSignal(self.login_widget.button.clickedWhileInactive):
            qtbot.mouseClick(self.login_widget.button, Qt.LeftButton)
        self.alyx_mock.login.assert_called_once_with(username='test_user')
        self.login_widget.button.setActive(True)
        assert self.login_widget.button.text() == 'Logout'

    def test_logout_action(self, qtbot, setup_method):
        """Test that the logout action is triggered when the button is clicked."""
        self.login_widget.userEdit.setText('test_user')
        with qtbot.waitSignal(self.login_widget.button.clickedWhileInactive):
            qtbot.mouseClick(self.login_widget.button, Qt.LeftButton)
        self.alyx_mock.login.assert_called_once_with(username='test_user')
        self.login_widget.button.setActive(True)

        assert self.login_widget.button.text() == 'Logout'
        with qtbot.waitSignal(self.login_widget.button.clickedWhileActive):
            qtbot.mouseClick(self.login_widget.button, Qt.LeftButton)
        self.alyx_mock.logout.assert_called_once()
        self.login_widget.button.setActive(False)
        assert self.login_widget.button.text() == 'Login'


class TestAlyxLoginDialog:
    @pytest.fixture
    def mock_q_alyx(self):
        """Mock the QAlyx instance."""
        mock = MagicMock(spec=QAlyx)
        mock.client.base_url = 'https://example.com'
        return mock

    @pytest.fixture
    def dialog(self, mock_q_alyx):
        """Create an instance of AlyxLoginDialog for testing."""
        return widgets.AlyxLoginDialog(mock_q_alyx)

    def test_initial_state(self, qtbot, dialog):
        """Test the initial state of the dialog."""
        qtbot.addWidget(dialog)
        assert dialog.userEdit.text() == ''
        assert dialog.passEdit.text() == ''
        assert not dialog.buttonBox.button(QDialogButtonBox.Ok).isEnabled()

    def test_enable_ok_button_when_text_entered(self, qtbot, dialog):
        """Test that the OK button is enabled when both fields are filled."""
        qtbot.addWidget(dialog)
        dialog.userEdit.setText('test_user')
        dialog.passEdit.setText('test_password')
        assert dialog.buttonBox.button(QDialogButtonBox.Ok).isEnabled()

    def test_authentication_success(self, dialog, qtbot):
        """Test the dialog behavior on successful authentication."""
        qtbot.addWidget(dialog)
        dialog.userEdit.setText('test_user')
        dialog.passEdit.setText('test_password')
        with qtbot.waitSignal(dialog.accepted):
            qtbot.mouseClick(
                dialog.buttonBox.button(QDialogButtonBox.Ok), Qt.LeftButton
            )
            dialog._alyx.login.assert_called_once_with(
                'test_user', 'test_password', False
            )
            dialog._onAuthentificationSucceeded('test_user')
        assert dialog.result() == QDialog.Accepted

    def test_authentication_failure(self, dialog, qtbot):
        """Test the dialog behavior on failed authentication."""
        qtbot.addWidget(dialog)
        dialog.userEdit.setText('test_user')
        dialog.passEdit.setText('test_password')
        with patch('iblqt.widgets.QMessageBox.critical') as mock:
            qtbot.mouseClick(
                dialog.buttonBox.button(QDialogButtonBox.Ok), Qt.LeftButton
            )
            dialog._alyx.login.assert_called_once_with(
                'test_user', 'test_password', False
            )
            dialog._onAuthentificationFailed('test_user')
            mock.assert_called_once()
        assert dialog.passEdit.text() == ''
        assert dialog.result() == QDialog.Rejected

    def test_cache_checkbox(self, qtbot, dialog, mock_q_alyx):
        """Test the behavior of the cache checkbox."""
        qtbot.addWidget(dialog)
        check_cache = dialog.findChild(QCheckBox)
        assert check_cache is not None
        assert not check_cache.isChecked()

        check_cache.setChecked(True)
        dialog._setCache(check_cache.checkState())
        assert dialog._cache is True

        check_cache.setChecked(False)
        dialog._setCache(check_cache.checkState())
        assert dialog._cache is False

        dialog2 = widgets.AlyxLoginDialog(
            mock_q_alyx, cache=widgets.UseTokenCache.ALWAYS
        )
        qtbot.addWidget(dialog2)
        assert dialog2._cache
        assert dialog2.findChild(QCheckBox) is None

        dialog3 = widgets.AlyxLoginDialog(
            mock_q_alyx, cache=widgets.UseTokenCache.NEVER
        )
        qtbot.addWidget(dialog3)
        assert not dialog3._cache
        assert dialog3.findChild(QCheckBox) is None
