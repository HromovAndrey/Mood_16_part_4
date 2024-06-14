# Завдання 1
# Створіть додаток «Соціальна мережа», який зберігає
# інформацію про користувача, його друзів, публікації користувача. Можливості додатку:
# ■ вхід за логіном і паролем;
# ■ додати користувача;
# ■ видалити користувача;
# ■ редагувати інформацію про користувача;
# ■ пошук користувача за ПІБ;
# ■ перегляд інформації про користувача;
# ■ перегляд усіх друзів користувача;
# ■ перегляд усіх публікацій користувача.
# Зберігайте дані у базі даних NoSQL. Можете використовувати Redis в якості платформи.

import redis

class SocialNetwork:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def login(self, username, password):
        stored_password = self.r.hget(f"user:{username}", "password")
        if stored_password and stored_password.decode() == password:
            return True
        return False

    def add_user(self, username, password, name, age, country):
        if self.r.exists(f"user:{username}"):
            return "User already exists"
        self.r.hset(f"user:{username}", mapping={"password": password, "name": name, "age": age, "country": country})
        return "User added successfully"

    def delete_user(self, username):
        self.r.delete(f"user:{username}")
        self.r.delete(f"user:{username}:friends")
        self.r.delete(f"user:{username}:posts")
        return "User deleted"

    def edit_user(self, username, field, value):
        if self.r.exists(f"user:{username}"):
            self.r.hset(f"user:{username}", field, value)
            return "User information updated"
        return "User not found"

    def search_user_by_name(self, name):
        keys = self.r.keys("user:*")
        users = []
        for key in keys:
            if b"friends" not in key and b"posts" not in key:
                if self.r.hget(key, "name").decode() == name:
                    users.append(self.r.hgetall(key))
        return users

    def view_user(self, username):
        if self.r.exists(f"user:{username}"):
            return self.r.hgetall(f"user:{username}")
        return "User not found"

    def view_friends(self, username):
        if self.r.exists(f"user:{username}:friends"):
            return self.r.smembers(f"user:{username}:friends")
        return "User not found or no friends"

    def view_posts(self, username):
        if self.r.exists(f"user:{username}:posts"):
            return self.r.lrange(f"user:{username}:posts", 0, -1)
        return "User not found or no posts"

    def add_friend(self, username, friend_username):
        if self.r.exists(f"user:{username}") and self.r.exists(f"user:{friend_username}"):
            self.r.sadd(f"user:{username}:friends", friend_username)
            self.r.sadd(f"user:{friend_username}:friends", username)
            return "Friend added"
        return "User not found"

    def add_post(self, username, post):
        if self.r.exists(f"user:{username}"):
            self.r.rpush(f"user:{username}:posts", post)
            return "Post added"
        return "User not found"
if __name__ == "__main__":
    sn = SocialNetwork()
    print(sn.add_user("john_doe", "password123", "John Doe", "30", "USA"))
    if sn.login("john_doe", "password123"):
        print("Login successful")
    else:
        print("Login failed")
    sn.add_user("jane_doe", "password456", "Jane Doe", "25", "Canada")
    print(sn.add_friend("john_doe", "jane_doe"))
    print(sn.add_post("john_doe", "Hello, this is my first post!"))
    print(sn.view_user("john_doe"))
    print(sn.view_friends("john_doe"))
    print(sn.view_posts("john_doe"))
    print(sn.search_user_by_name("John Doe"))
    print(sn.edit_user("john_doe", "country", "UK"))
    print(sn.delete_user("john_doe"))
