import os
import datetime

def generate_ceo_briefing():
    """
    Generates a weekly CEO briefing report.
    """
    report_path = os.path.join("AI_Employee_Vault", "Reports", "CEO_Weekly.md")
    
    # --- Gather Data ---
    
    # 1. Tasks Completed
    tasks_completed = []
    done_tasks_dir = os.path.join("Bronze", "Done")
    if os.path.exists(done_tasks_dir):
        tasks_completed = [f for f in os.listdir(done_tasks_dir) if f.endswith(".md")]

    # 2. Emails Sent and LinkedIn Posts (from business.log)
    emails_sent = []
    linkedin_posts = []
    business_log_path = os.path.join("AI_Employee_Vault", "logs", "business.log")
    if os.path.exists(business_log_path):
        with open(business_log_path, "r") as f:
            for line in f:
                if "--- EMAIL SENT ---" in line:
                    emails_sent.append(line.strip()) # Capture the full log entry for email
                elif "--- LINKEDIN POST ---" in line:
                    linkedin_posts.append(line.strip()) # Capture the full log entry for linkedin

    # 3. Pending Approvals
    pending_approvals = []
    need_approval_dir = os.path.join("AI_Employee_Vault", "Need_Approval")
    if os.path.exists(need_approval_dir):
        pending_approvals = os.listdir(need_approval_dir)

    # --- Generate Report Content ---
    
    report_content = []
    report_content.append(f"# CEO Weekly Briefing - {datetime.date.today().strftime('%Y-%m-%d')}\n")
    
    report_content.append("## 1. Tasks Completed\n")
    if tasks_completed:
        for task in tasks_completed:
            report_content.append(f"- {task}\n")
    else:
        report_content.append("- No tasks completed this week.\n")
    report_content.append("\n")

    report_content.append("## 2. Communications\n")
    report_content.append("### Emails Sent\n")
    if emails_sent:
        for email in emails_sent:
            report_content.append(f"- {email}\n")
    else:
        report_content.append("- No emails sent this week.\n")
    report_content.append("\n")

    report_content.append("### LinkedIn Posts\n")
    if linkedin_posts:
        for post in linkedin_posts:
            report_content.append(f"- {post}\n")
    else:
        report_content.append("- No LinkedIn posts made this week.\n")
    report_content.append("\n")

    report_content.append("## 3. Pending Approvals\n")
    if pending_approvals:
        for approval in pending_approvals:
            report_content.append(f"- {approval}\n")
    else:
        report_content.append("- No pending approvals.\n")
    report_content.append("\n")

    report_content.append("## 4. Income/Expense Summary\n")
    report_content.append("- *Placeholder: Financial data integration needed.*\n\n")

    report_content.append("## 5. System Health\n")
    report_content.append("- *Placeholder: System health monitoring integration needed.*\n\n")

    # --- Write Report ---
    with open(report_path, "w") as f:
        f.writelines(report_content)
    
    print(f"CEO Weekly Briefing generated at: {report_path}")

if __name__ == "__main__":
    generate_ceo_briefing()
