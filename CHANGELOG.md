Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.3.2] - 2024-12-03

### Changed

- core.FileWatcher: simplified and renamed to core.PathWatcher

## [0.3.1] - 2024-11-28

### Fixed

- core.DataFrameTableModel: fixed issue with sorting

## [0.3.0] - 2024-11-28

### Added

- core.FileWatcher: watch a file for changes

## [0.2.0] - 2024-10-08

### Added

- widgets.CheckBoxDelegate: render checkboxes in a QTableView or similar widget
- start adding unit tests

### Changed

- core.DataFrameTableModel: stop use of QVariant
- core.DataFrameTableModel: set dataFrame _after_ connecting signals in initialization
- core.DataFrameTableModel: default to horizontal orientation

## [0.1.2] - 2024-10-01

### Changed

- core.DataFrameTableModel: reverted data() to return Any instead of QVariant
- core.DataFrameTableModel: setData() returns bool indicating the outcome of the operation

## [0.1.1] - 2024-10-01

### Added

- core.DataFrameTableModel: setData method

### Fixed

- core.DataFrameTableModel: data() should return QVariant
- core.ColoredDataFrameTableModel: types for data roles


## [0.1.0] - 2024-10-01

_First release._

### Added

- core.DataFrameTableModel: A Qt TableModel for Pandas DataFrames.
- core.ColoredDataFrameTableModel: An extension of DataFrameTableModel providing color-mapped numerical data.
- widgets.StatefulButton: A QPushButton that maintains an active/inactive state.

[0.3.1]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.3.1
[0.3.0]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.3.0
[0.2.0]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.2.0
[0.1.2]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.1.2
[0.1.1]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.1.1
[0.1.0]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.1.0
