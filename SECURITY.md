# Security Policy

## Local-Only Operation
- DocSyn runs entirely locally with no networked services
- No web servers, remote APIs, or external dependencies
- All processing happens on your local machine

## Data Handling
- Do not commit sensitive source documents to version control
- Staging and output directories may contain processed content
- Use .gitignore to exclude sensitive files if needed

## Supported Environment
- Python 3.11+ (required for deterministic behavior)
- GNU Make 4.x+ (build system dependency)
- UTF-8 terminal encoding (recommended)

## Reporting Issues
- Report security concerns via GitHub Issues with "Security" label
- Include system information and steps to reproduce
- No sensitive data should be included in issue reports

## Risk Assessment
- **Low Risk**: Local file processing only
- **No Network Exposure**: No listening ports or external connections
- **File System Access**: Limited to project directory and staging areas
