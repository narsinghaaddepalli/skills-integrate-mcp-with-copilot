# Creating GitHub Issues from Templates

This directory contains a script to automatically create GitHub issues from the template files stored in `.github/steps/1-step-issues/`.

## Prerequisites

- GitHub CLI (`gh`) must be installed and authenticated
- Python 3.x

## Usage

### Dry Run (Preview Only)

To see what issues would be created without actually creating them:

```bash
python3 create_issues.py --dry-run
```

This will display all the issues that would be created, including their titles, labels, and content.

### Create Issues

To actually create the GitHub issues in the repository:

```bash
python3 create_issues.py
```

### Command-Line Options

```
usage: create_issues.py [-h] [--dry-run] [--templates-dir TEMPLATES_DIR]

options:
  -h, --help            Show help message and exit
  --dry-run             Preview issues without creating them
  --templates-dir TEMPLATES_DIR
                        Path to directory containing issue templates 
                        (default: .github/steps/1-step-issues)
```

Example with custom template directory:

```bash
python3 create_issues.py --templates-dir /path/to/templates --dry-run
```

This will:
1. Read all markdown files from `.github/steps/1-step-issues/`
2. Parse each template to extract the title, body, and labels
3. Create GitHub issues using the `gh` CLI
4. Report the success/failure of each issue creation

## Issue Templates

The script processes issue templates from the following directories:

- `.github/steps/1-step-issues/enhancement/` - Feature requests and enhancements
- `.github/steps/1-step-issues/bug/` - Bug reports

### Template Structure

Each template should be a markdown file with:
- A first-level heading (`#`) that will be used as the issue title
- The full content will be used as the issue body
- Labels are automatically assigned based on the directory:
  - Files in `enhancement/` get the `enhancement` label
  - Files in `bug/` get the `bug` label

## Example

```bash
# Preview issues
$ python3 create_issues.py --dry-run
Running in DRY-RUN mode - no issues will be created

Found 6 issue template(s)

============================================================
TITLE: Add filters
LABELS: enhancement
============================================================
# Add filters

There seems to be no order to the activities...
============================================================

# Create issues
$ python3 create_issues.py
Found 6 issue template(s)

✓ Created issue: Missing School Pride
  URL: https://github.com/owner/repo/issues/1
✓ Created issue: Add filters
  URL: https://github.com/owner/repo/issues/2
...
Successfully created 6/6 issues
```

## Troubleshooting

### Authentication Error

If you get an authentication error, make sure you're logged in with the GitHub CLI:

```bash
gh auth login
```

### Permission Error

Ensure you have permission to create issues in the repository. You need write access to the repository.
