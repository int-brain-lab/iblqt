Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0] - 2025-07-18

### Added
- `widgets.ColoredButton`: as the name suggests ...

### Changed
- `widgets.SlideToggle`: tweaked color-scheme

## [0.7.1] - 2025-07-16

### Changed
- `widgets.DiskSpaceIndicator`: add a tool-tip

## [0.7.0] - 2025-07-16

### Added
- `widgets.SlideToggle`: a sliding toggle switch

## [0.6.1] - 2025-07-15

### Changed
- `widgets.RestrictedWebView`: additional parameters to control tool-tips and status-tips

## [0.6.0] - 2025-07-15

### Added
- `widgets.RestrictedWebView`: a browser widget that restricts navigation to a trusted URL prefix
- `core.RestrictedWebEnginePage`: a QWebEnginePage subclass that filters navigation requests based on a URL prefix

### Changed
- moved dependency management from PDM to UV
- improved workflows for CI and testing

## [0.5.0] - 2025-07-09

### Added
- `core.Worker`: a generic worker class for executing functions concurrently in a
  separate thread
- `widgets.ThresholdProgressBar`: a progress bar that changes color based on a threshold
  value
- `widgets.DiskSpaceIndicator`: a progress bar widget that indicates the disk space
  usage of a directory
- `tools`: a collection of small Qt tools, adapted from `ibllib.misc.qt`
- `.editorconfig`: for consistent coding style

## [0.4.4] - 2025-03-26

### Fixed
- compatibility issues with PySide in `widgets.AlyxUserEdit` and
  `widgets.AlyxLoginWidget`

### Changed
- increased coverage of unit-tests

## [0.4.3] - 2025-03-25

### Added
- unit tests for `core.QAlyx`

### Changed
- removed version pin for Numpy requirement

## [0.4.2] - 2025-01-20

### Fixed
- fix wheel distribution

## [0.4.1] - 2025-01-20

### Fixed
- `core.QAlyx`: fixed handling of authentication issues during rest query

## [0.4.0] - 2025-01-17

### Added

- `core.QAlyx`: wrapper for `one.webclient.AlyxClient`
- `widgets.AlyxWidget`: widget for logging in to Alyx

### Changed

- `widgets.StatefulButton`: keep track of different labels for active and
  inactive states

## [0.3.2] - 2024-12-03

### Changed

- `core.FileWatcher`: simplified and renamed to `core.PathWatcher`

## [0.3.1] - 2024-11-28

### Fixed

- `core.DataFrameTableModel`: fixed issue with sorting

## [0.3.0] - 2024-11-28

### Added

- `core.FileWatcher`: watch a file for changes

## [0.2.0] - 2024-10-08

### Added

- `widgets.CheckBoxDelegate`: render checkboxes in a `QTableView` or similar widget
- start adding unit tests

### Changed

- `core.DataFrameTableModel`: stop use of `QVariant`
- `core.DataFrameTableModel`: set `dataFrame` _after_ connecting signals in
  initialization
- `core.DataFrameTableModel`: default to horizontal orientation

## [0.1.2] - 2024-10-01

### Changed

- `core.DataFrameTableModel`: reverted `data()` to return Any instead of `QVariant`
- `core.DataFrameTableModel`: `setData()` returns bool indicating the outcome of
  the operation

## [0.1.1] - 2024-10-01

### Added

- `core.DataFrameTableModel`: `setData()` method

### Fixed

- `core.DataFrameTableModel`: `data()` should return `QVariant`
- `core.ColoredDataFrameTableModel`: types for data roles


## [0.1.0] - 2024-10-01

_First release._

### Added

- `core.DataFrameTableModel`: A Qt `TableModel` for Pandas `DataFrames`.
- `core.ColoredDataFrameTableModel`: An extension of `DataFrameTableModel`
  providing color-mapped numerical data.
- `widgets.StatefulButton`: A `QPushButton` that maintains an active/inactive state.

[0.8.0]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.8.0
[0.7.1]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.7.1
[0.7.0]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.7.0
[0.6.1]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.6.1
[0.6.0]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.6.0
[0.5.0]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.5.0
[0.4.4]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.4.4
[0.4.3]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.4.3
[0.4.2]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.4.2
[0.4.1]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.4.1
[0.4.0]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.4.0
[0.3.2]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.3.2
[0.3.1]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.3.1
[0.3.0]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.3.0
[0.2.0]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.2.0
[0.1.2]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.1.2
[0.1.1]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.1.1
[0.1.0]: https://github.com/int-brain-lab/iblqt/releases/tag/v0.1.0
