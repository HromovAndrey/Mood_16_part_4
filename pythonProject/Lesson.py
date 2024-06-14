import redis

class Museum:
    def __init__(self, host='location', port=6379, db=0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)

    def _get_admins_key(self):
        return'museum:admins'

    def _get_exibit_key(self, exibit_id):
        return f"musuem:exhibits:{exibit_id}"

    def _check_login(self):
        if self.current_admin is None:
            print('Ви не ввійшли як адміністратор')
            return False
        return True

    def add_admin(self, admin_id, password):
        admin_key = self._get_admins_key()
        if self.redis.hexists('museum:admins', admin_id):
            print('Адміністратор вже існує')
            return
        self.redis.hset(admin_key, admin_id, password)
        print('Адміністратора додано')

    def login(self, admin_id, password):
         admin_key = self._get_admins_key()
         admin_password = self.redis.hget(admin_key, admin_id,)
         if admin_password is not None and password == admin_password:
            print('Вхід дозволено')

         else:
             print('Невірний логін або пароль')

    def add_exibit(self):
    '''
    exibit info:
         admin-value
         name-value
         descriptio-value
         related_people-set
      person ionfo:
         related_exhibit - set
     :return:
     '''
     if not self._check_login():
         return
     exibit_key = self._get_exhibit_key(exhibit_id)

    data = {
         "admin":self.current_admi
         name-value
         descriptio-value
         related_people-set
    }
musuem = Museum()

while True:
    print('Оберіть функцію')
    print('1. Ренєстрація адміністратору  музею')
    print('2. Вхід')
    command = int(input('Ввкдіть номер команди:'))

    if command == 1:
        admin_id = int(input('Введыть id фдміністратора :'))
        password = input('Введить пароль:')
        musuem.add_admin(admin_id, password)
        print('+++++++++++++++++')
        print('=================')

    elif command == 2:
         admin_id = int(input('Введіть id адмыныстратора:'))
         password = input('Введыть пароль:')

         musuem.login(admin_id, password)
         print('===========================')
         print('===========================')
