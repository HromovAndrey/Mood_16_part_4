# Створіть додаток «Музей літератури». Додаток має зберігати
# інформацію про експонати та людей, які мають відношення
# до експонатів. Можливості додатку:
# ■ вхід за логіном і паролем;
# ■ додати експонат;
# Практичнє завдання
# 1
# ■ видалити експонат;
# ■ редагування інформації про експонат;
# ■ перегляд повної інформації про експонат;
# ■ виведення інформації про всі експонати;
# ■ перегляд інформації про людей, які мають відношення
# до певного експонату;
# ■ перегляд інформації про експонати, що мають відношення
# до певної людини;
# ■ перегляд набору експонатів на основі певного критерію.
# Наприклад, показати всі книжкові експонати.
# Зберігайте дані у базі даних NoSQL. Можете використовувати Redis в якості платформи

import redis
class LiteratureMuseum:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def login(self, username, password):
        stored_password = self.r.hget(f"user:{username}", "password")
        if stored_password and stored_password.decode() == password:
            return True
        return False

    def add_exhibit(self, exhibit_id, name, description, category):
        if self.r.exists(f"exhibit:{exhibit_id}"):
            return "Exhibit already exists"
        self.r.hset(f"exhibit:{exhibit_id}", mapping={"name": name, "description": description, "category": category})
        return "Exhibit added successfully"

    def delete_exhibit(self, exhibit_id):
        self.r.delete(f"exhibit:{exhibit_id}")
        self.r.delete(f"exhibit:{exhibit_id}:people")
        return "Exhibit deleted"

    def edit_exhibit(self, exhibit_id, field, value):
        if self.r.exists(f"exhibit:{exhibit_id}"):
            self.r.hset(f"exhibit:{exhibit_id}", field, value)
            return "Exhibit information updated"
        return "Exhibit not found"

    def view_exhibit(self, exhibit_id):
        if self.r.exists(f"exhibit:{exhibit_id}"):
            return self.r.hgetall(f"exhibit:{exhibit_id}")
        return "Exhibit not found"

    def list_exhibits(self):
        keys = self.r.keys("exhibit:*")
        exhibits = []
        for key in keys:
            if b"people" not in key:
                exhibits.append(self.r.hgetall(key))
        return exhibits

    def add_person_to_exhibit(self, exhibit_id, person_name):
        self.r.rpush(f"exhibit:{exhibit_id}:people", person_name)
        return "Person added to exhibit"

    def view_people_for_exhibit(self, exhibit_id):
        return self.r.lrange(f"exhibit:{exhibit_id}:people", 0, -1)

    def view_exhibits_for_person(self, person_name):
        keys = self.r.keys("exhibit:*:people")
        exhibits = []
        for key in keys:
            if person_name.encode() in self.r.lrange(key, 0, -1):
                exhibits.append(key.decode().split(":")[1])
        return exhibits

    def search_exhibits_by_category(self, category):
        keys = self.r.keys("exhibit:*")
        exhibits = []
        for key in keys:
            if b"people" not in key and self.r.hget(key, "category").decode() == category:
                exhibits.append(self.r.hgetall(key))
        return exhibits

if __name__ == "__main__":
    lm = LiteratureMuseum()

    lm.r.hset("user:admin", mapping={"password": "admin123"})
    if lm.login("admin", "admin123"):
        print("Login successful")
    else:
        print("Login failed")
    lm.add_exhibit("ex1", "War and Peace", "A book by Leo Tolstoy", "book")
    lm.add_person_to_exhibit("ex1", "Leo Tolstoy")
    print(lm.view_exhibit("ex1"))
    print(lm.view_people_for_exhibit("ex1"))
    print(lm.view_exhibits_for_person("Leo Tolstoy"))
    print(lm.search_exhibits_by_category("book"))
