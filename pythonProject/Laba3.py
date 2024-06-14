import redis
from datetime import datetime

class Notebook:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def login(self, username, password):
        stored_password = self.r.hget(f"user:{username}", "password")
        if stored_password and stored_password.decode() == password:
            return True
        return False

    def add_user(self, username, password):
        if self.r.exists(f"user:{username}"):
            return "User already exists"
        self.r.hset(f"user:{username}", mapping={"password": password})
        return "User added successfully"

    def add_note(self, username, note):
        if not self.r.exists(f"user:{username}"):
            return "User not found"
        note_id = self.r.incr(f"notes:{username}:id")
        note_key = f"notes:{username}:{note_id}"
        self.r.hset(note_key, mapping={"content": note, "timestamp": datetime.now().isoformat()})
        self.r.rpush(f"notes:{username}", note_key)
        self.r.zadd(f"notes_time:{username}", {note_key: datetime.now().timestamp()})
        return "Note added"

    def delete_note_by_id(self, username, note_id):
        note_key = f"notes:{username}:{note_id}"
        if not self.r.exists(note_key):
            return "Note not found"
        self.r.delete(note_key)
        self.r.lrem(f"notes:{username}", 0, note_key)
        self.r.zrem(f"notes_time:{username}", note_key)
        return "Note deleted"

    def edit_note_by_id(self, username, note_id, new_content):
        note_key = f"notes:{username}:{note_id}"
        if not self.r.exists(note_key):
            return "Note not found"
        self.r.hset(note_key, "content", new_content)
        return "Note updated"

    def view_note_by_id(self, username, note_id):
        note_key = f"notes:{username}:{note_id}"
        if self.r.exists(note_key):
            return self.r.hgetall(note_key)
        return "Note not found"

    def view_all_notes(self, username):
        note_keys = self.r.lrange(f"notes:{username}", 0, -1)
        notes = []
        for key in note_keys:
            notes.append(self.r.hgetall(key))
        return notes

    def view_notes_by_time_range(self, username, start_time, end_time):
        start_ts = datetime.fromisoformat(start_time).timestamp()
        end_ts = datetime.fromisoformat(end_time).timestamp()
        note_keys = self.r.zrangebyscore(f"notes_time:{username}", start_ts, end_ts)
        notes = []
        for key in note_keys:
            notes.append(self.r.hgetall(key))
        return notes

    def search_notes_by_keywords(self, username, keywords):
        note_keys = self.r.lrange(f"notes:{username}", 0, -1)
        notes = []
        for key in note_keys:
            note = self.r.hgetall(key)
            content = note.get(b'content', b'').decode()
            if all(keyword in content for keyword in keywords):
                notes.append(note)
        return notes

if __name__ == "__main__":
    nb = Notebook()
    print(nb.add_user("john_doe", "password123"))
    if nb.login("john_doe", "password123"):
        print("Login successful")
    else:
        print("Login failed")
    print(nb.add_note("john_doe", "This is my first note"))
    print(nb.add_note("john_doe", "Another note with more information"))
    print(nb.view_all_notes("john_doe"))
    print(nb.edit_note_by_id("john_doe", 1, "This is my edited first note"))
    print(nb.view_note_by_id("john_doe", 1))
    print(nb.delete_note_by_id("john_doe", 1))
    print(nb.view_notes_by_time_range("john_doe", "2023-01-01T00:00:00", "2024-01-01T00:00:00"))
    print(nb.search_notes_by_keywords("john_doe", ["note", "information"]))
