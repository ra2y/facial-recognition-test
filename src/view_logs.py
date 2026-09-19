from database import get_all_logs

def main():
    logs = get_all_logs()
    if not logs:
        print("No attendance records yet.")
        return

    print(f"{'Name':<20} {'Timestamp'}")
    print("-" * 45)
    for name, timestamp in logs:
        print(f"{name:<20} {timestamp}")

if __name__ == "__main__":
    main()