#!/usr/bin/env python3
"""
Script to create GitHub issues from template files.

This script reads the issue templates from .github/steps/1-step-issues/
and creates corresponding GitHub issues in the repository.
"""

import os
import re
import subprocess
import sys
from pathlib import Path


def parse_issue_template(filepath):
    """
    Parse an issue template markdown file.
    
    Returns a dictionary with:
    - title: The first heading as the issue title
    - body: The full content as the issue body
    - labels: List of labels based on the directory structure
    """
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract the first heading as title
    lines = content.split('\n')
    title = None
    for line in lines:
        if line.startswith('#'):
            # Remove the # symbols and strip whitespace
            title = line.lstrip('#').strip()
            break
    
    if not title:
        # Fallback: use filename
        title = Path(filepath).stem.replace('-', ' ').title()
    
    # Determine labels based on directory structure
    labels = []
    if 'enhancement' in str(filepath):
        labels.append('enhancement')
    elif 'bug' in str(filepath):
        labels.append('bug')
    
    return {
        'title': title,
        'body': content,
        'labels': labels
    }


def create_github_issue(title, body, labels, dry_run=False):
    """
    Create a GitHub issue using the gh CLI.
    
    Args:
        title: Issue title
        body: Issue body (markdown)
        labels: List of label strings
        dry_run: If True, only print what would be created
    """
    if dry_run:
        print(f"\n{'='*60}")
        print(f"TITLE: {title}")
        print(f"LABELS: {', '.join(labels)}")
        print(f"{'='*60}")
        print(body)
        print(f"{'='*60}\n")
        return True
    
    try:
        # Build the gh issue create command
        cmd = ['gh', 'issue', 'create', '--title', title, '--body', body]
        
        # Add labels if any
        for label in labels:
            cmd.extend(['--label', label])
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✓ Created issue: {title}")
        print(f"  URL: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create issue '{title}': {e.stderr}", file=sys.stderr)
        return False


def main():
    """Main function to create issues from templates."""
    # Check for dry-run flag
    dry_run = '--dry-run' in sys.argv
    
    if dry_run:
        print("Running in DRY-RUN mode - no issues will be created\n")
    
    # Find all issue template files
    base_path = Path(__file__).parent / '.github' / 'steps' / '1-step-issues'
    
    if not base_path.exists():
        print(f"Error: Issue templates directory not found at {base_path}", file=sys.stderr)
        return 1
    
    # Find all markdown files in subdirectories
    template_files = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.md'):
                template_files.append(Path(root) / file)
    
    if not template_files:
        print(f"Error: No issue templates found in {base_path}", file=sys.stderr)
        return 1
    
    print(f"Found {len(template_files)} issue template(s)\n")
    
    # Process each template
    success_count = 0
    for template_file in sorted(template_files):
        issue_data = parse_issue_template(template_file)
        if create_github_issue(
            issue_data['title'],
            issue_data['body'],
            issue_data['labels'],
            dry_run=dry_run
        ):
            success_count += 1
    
    print(f"\n{'='*60}")
    if dry_run:
        print(f"DRY-RUN complete: {success_count}/{len(template_files)} issues would be created")
        print("Run without --dry-run to create issues")
    else:
        print(f"Successfully created {success_count}/{len(template_files)} issues")
    print(f"{'='*60}")
    
    return 0 if success_count == len(template_files) else 1


if __name__ == '__main__':
    sys.exit(main())
