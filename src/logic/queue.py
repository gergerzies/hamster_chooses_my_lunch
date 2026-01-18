def get_queue_status(stall_data):
    reports = stall_data.get('queue_reports', [])
    now = datetime.now()
    recent_reports = [t for t in reports if now - datetime.fromisoformat(t) < timedelta(minutes=10)]
    if len(recent_reports) >= 5: return "🔴 CROWDED", f"High alert! {len(recent_reports)} reports."
    elif len(recent_reports) >= 1: return "🟡 BUILDING UP", f"{len(recent_reports)} recent reports."
    else: return "🟢 CLEAR", "Looks chill. Go eat."
