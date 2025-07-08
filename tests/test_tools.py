import pytest
from qtpy.QtWidgets import QApplication, QMainWindow, QWidget

from iblqt import tools


class TestGetOrCreateApp:
    def test_returns_qapplication_instance(self):
        app = tools.get_or_create_app([])
        assert isinstance(app, QApplication)

    def test_returns_same_instance_on_multiple_calls(self):
        app1 = tools.get_or_create_app([])
        app2 = tools.get_or_create_app([])
        assert app1 is app2


class TestRequireQtDecorator:
    @tools.require_qt
    def func(self):
        return 42

    def test_runs_function_when_qt_running(self, qtbot):
        assert self.func() == 42  # qtbot ensures QApplication is running

    def test_raises_runtime_error_when_no_qt(self, monkeypatch):
        monkeypatch.setattr('qtpy.QtWidgets.QApplication.instance', lambda: None)
        with pytest.raises(RuntimeError, match='requires a running Qt application.'):
            self.func()


class TestGetMainWindow:
    def test_returns_main_window_instance(self, qtbot):
        main_win = QMainWindow()
        main_win.show()
        qtbot.addWidget(main_win)

        assert tools.get_main_window() is main_win

        main_win.close()

    def test_raises_if_no_main_window_found(self, qtbot):
        widget = QWidget()
        widget.show()
        qtbot.addWidget(widget)

        with pytest.raises(RuntimeError, match='No QMainWindow instance found'):
            tools.get_main_window()

        widget.close()


class TestRunApp:
    def test_executes_event_loop_and_returns_exit_code(self, monkeypatch):
        called = {}

        def fake_exec_(*_):
            called['executed'] = True
            return 123

        monkeypatch.setattr(tools.QApplication, "exec_", fake_exec_)

        exit_code = tools.run_app()
        assert exit_code == 123
        assert called.get('executed') is True
