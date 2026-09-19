from database import init_db, log_attendance, get_all_logs

init_db()
log_attendance("TestUser")
print(get_all_logs())