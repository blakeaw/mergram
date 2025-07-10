# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.3.0] - 2025-07-10

### Added
- `flowchart.Style` class to add node/subgraph styling options to a flowchart. This includes logic to add `Style` objects to `Flowchart`.

### Fixed
- Removed unrecognized/unused style items (`fill: ...,`) from node definition strings in `Node` -- instead the new `Style` class object is used to encode them to the flowchart.

## [0.2.0] - 2025-07-08

### Added
- `Flowchart.to_markdown` function to get a mermaid code block for markdown insertion.
- `Flowchart.to_html` function to get an HTML-embedded version of the flowchart. 

## [0.1.0] - 2025-07-07

### Added
- Initial development version of the package.

------

## Entry format

## [version] - yyyy-mm-dd

### Added
- Things that have been added.

### Changed
- Things that were changed.

### Fixed
- Things that were fixed.