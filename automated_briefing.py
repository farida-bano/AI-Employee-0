#!/usr/bin/env python3

"""
Automated Weekly CEO Briefing Generator
Generates a comprehensive report every Sunday with:
- Revenue summary
- Completed tasks
- Pending approvals
- Issues summary
"""

import os
import sys
import datetime
import re
from pathlib import Path


def read_done_folder():
    """Read all files in the Done folder and extract relevant information"""
    done_path = Path("AI_Employee_Vault/Done")
    if not done_path.exists():
        return []

    completed_tasks = []
    for file_path in done_path.iterdir():
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    completed_tasks.append({
                        'filename': file_path.name,
                        'content': content[:500],  # First 500 chars for summary
                        'size': file_path.stat().st_size,
                        'modified': datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                    })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    return completed_tasks


def read_accounting_data():
    """Read accounting data to extract revenue information"""
    # Look for accounting files in various locations
    accounting_paths = [
        Path("AI_Employee_Vault/Accounting"),
        Path("AI_Employee_Vault/Finance"),
        Path("AI_Employee_Vault/Revenue"),
        Path("AI_Employee_Vault/logs/business.log")
    ]

    revenue_data = {
        'total_revenue': 0,
        'revenue_sources': [],
        'expenses': [],
        'net_profit': 0,
        'transaction_count': 0
    }

    # Check business log for financial transactions
    business_log = Path("AI_Employee_Vault/logs/business.log")
    if business_log.exists():
        try:
            with open(business_log, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for revenue-related patterns (these are examples - adjust based on actual data format)
                revenue_matches = re.findall(r'\$(\d+\.?\d*)', content)  # Find dollar amounts
                for match in revenue_matches:
                    revenue_data['total_revenue'] += float(match)

                # Look for specific transaction types
                revenue_sources = re.findall(r'(Payment|Revenue|Sale|Invoice) .* \$(\d+\.?\d*)', content)
                revenue_data['revenue_sources'] = revenue_sources
                revenue_data['transaction_count'] = len(revenue_matches)
        except Exception as e:
            print(f"Error reading business log: {e}")

    # Look for other accounting files
    for path in accounting_paths:
        if path.exists():
            for file_path in path.iterdir():
                if file_path.is_file() and file_path.suffix in ['.csv', '.txt', '.json', '.md']:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Extract financial data based on common patterns
                            numbers = re.findall(r'\$(\d+\.?\d*)', content)
                            for num in numbers:
                                revenue_data['total_revenue'] += float(num)
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")

    return revenue_data


def read_pending_approvals():
    """Read pending approvals from the Need_Approval folder"""
    approval_path = Path("AI_Employee_Vault/Need_Approval")
    if not approval_path.exists():
        return []

    pending_approvals = []
    for file_path in approval_path.iterdir():
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    pending_approvals.append({
                        'filename': file_path.name,
                        'content': content[:300],  # First 300 chars for summary
                        'size': file_path.stat().st_size,
                        'modified': datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
                    })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    return pending_approvals


def read_issues():
    """Read issues from error logs and other sources"""
    issues = []

    # Check error logs
    error_log = Path("logs/errors.log")
    if error_log.exists():
        try:
            with open(error_log, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract recent errors (last 10)
                lines = content.split('\n')
                recent_errors = lines[-10:] if len(lines) > 10 else lines
                for line in recent_errors:
                    if line.strip() and 'ERROR' in line.upper():
                        issues.append(f"Error: {line.strip()}")
        except Exception as e:
            print(f"Error reading error log: {e}")

    # Check system health logs
    health_log = Path("AI_Employee_Vault/logs/system_health.md")
    if health_log.exists():
        try:
            with open(health_log, 'r', encoding='utf-8') as f:
                content = f.read()
                # Look for issues in recent entries
                if "❌" in content or "error" in content.lower() or "failed" in content.lower():
                    # Just count recent issues
                    issues.append("System health issues detected in recent monitoring")
        except Exception as e:
            print(f"Error reading health log: {e}")

    return issues


def generate_ceo_briefing():
    """Generate the automated weekly CEO briefing"""
    # Get current date for filename
    current_date = datetime.date.today()
    filename = f"{current_date.strftime('%Y-%m-%d')}_CEO_Briefing.md"
    output_path = Path("AI_Employee_Vault/Briefings") / filename

    # Gather data
    print("Gathering data for CEO briefing...")
    completed_tasks = read_done_folder()
    revenue_data = read_accounting_data()
    pending_approvals = read_pending_approvals()
    issues = read_issues()

    # Generate report content
    report_lines = []
    report_lines.append(f"# Weekly CEO Briefing - {current_date.strftime('%B %d, %Y')}")
    report_lines.append("")
    report_lines.append(f"*Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
    report_lines.append("=" * 60)
    report_lines.append("")

    # Revenue section
    report_lines.append("## Revenue Summary")
    report_lines.append("-" * 20)
    report_lines.append(f"**Total Revenue**: ${revenue_data['total_revenue']:,.2f}")
    report_lines.append(f"**Transaction Count**: {revenue_data['transaction_count']}")

    if revenue_data['revenue_sources']:
        report_lines.append("**Revenue Sources**:")
        for source, amount in revenue_data['revenue_sources'][:5]:  # Show top 5
            report_lines.append(f"  - {source}: ${amount}")
    else:
        report_lines.append("*No detailed revenue sources available*")

    report_lines.append("")

    # Completed Tasks section
    report_lines.append("## Completed Tasks")
    report_lines.append("-" * 20)
    if completed_tasks:
        report_lines.append(f"**Total Completed**: {len(completed_tasks)}")
        report_lines.append("")
        for i, task in enumerate(completed_tasks[:10]):  # Show top 10
            report_lines.append(f"### {task['filename']}")
            # Show a snippet of the content if available
            if task['content'].strip():
                # Extract key information from content
                lines = task['content'][:200].split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        report_lines.append(f"  - {line.strip()}")
            report_lines.append("")
    else:
        report_lines.append("*No completed tasks this week*")
        report_lines.append("")

    # Pending Approvals section
    report_lines.append("## Pending Approvals")
    report_lines.append("-" * 20)
    if pending_approvals:
        report_lines.append(f"**Total Pending**: {len(pending_approvals)}")
        report_lines.append("")
        for i, approval in enumerate(pending_approvals):
            report_lines.append(f"### {approval['filename']}")
            # Show a snippet of the content
            if approval['content'].strip():
                lines = approval['content'][:200].split('\n')
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        report_lines.append(f"  - {line.strip()}")
            report_lines.append("")
    else:
        report_lines.append("*No pending approvals*")
        report_lines.append("")

    # Issues section
    report_lines.append("## Issues Summary")
    report_lines.append("-" * 20)
    if issues:
        report_lines.append(f"**Total Issues Detected**: {len(issues)}")
        report_lines.append("")
        for issue in issues:
            report_lines.append(f"- {issue}")
    else:
        report_lines.append("*No issues detected this week*")
        report_lines.append("")

    # Summary statistics
    report_lines.append("## Weekly Summary")
    report_lines.append("-" * 20)
    report_lines.append(f"- **Tasks Completed**: {len(completed_tasks)}")
    report_lines.append(f"- **Pending Approvals**: {len(pending_approvals)}")
    report_lines.append(f"- **Revenue**: ${revenue_data['total_revenue']:,.2f}")
    report_lines.append(f"- **Issues Found**: {len(issues)}")
    report_lines.append(f"- **Report Generated**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # Write the report
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))

    print(f"Weekly CEO Briefing generated: {output_path}")
    return str(output_path)


def main():
    """Main function to run the briefing generator"""
    try:
        output_file = generate_ceo_briefing()
        print(f"Successfully generated CEO briefing: {output_file}")
    except Exception as e:
        print(f"Error generating CEO briefing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()