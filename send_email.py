import pyodbc
from logging_config import setup_logging

logger = setup_logging(__name__)

def send_mail(subject, body, recipient):
    conn_string = "DRIVER={SQL Server};SERVER=ETZ-SQL;DATABASE=SANDBOX;Trusted_Connection=yes"
    t_sql_command = f"""
    EXEC msdb.dbo.sp_send_dbmail @profile_name = "MIE Notifications",
                        @recipients = "{recipient}",
                        @subject = "{subject}",
                        @body = "{body}";
    """
    with pyodbc.connect(conn_string) as conn:
        cursor = conn.cursor()
        cursor.execute(t_sql_command)

    logger.info(f"Email command executed. Recipient -> {recipient}. SENT STATUS PENDING")
    
    query = "SELECT IDENT_CURRENT('msdb.dbo.sysmail_allitems')"
    cursor.execute(query)
    pk = cursor.fetchone()[0]
    sent_status_query = "SELECT sent_status FROM msdb.dbo.sysmail_allitems WHERE mailitem_id = ?"
    cursor.execute(sent_status_query, pk)
    
    status = cursor.fetchone()[0] 
    if status == "sent":
        logger.info(f"Eamil Sent. SENT STATUS CONFIRMED")
    elif status == "failed":
        logger.error(f"Email failed. recipient: {recipient}")
    else:
        logger.critical("Unknown error. Message not delivered")

# login 