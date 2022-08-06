from dao.model.user import User

"""
Создаем DAO  для сущности user
"""


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):  # получаем юзера по id
        return self.session.query(User).get(uid)

    def get_all(self):  # получаем всех пользователей
        return self.session.query(User).all()

    def get_by_username(self, username):  # получаем пользователя по имени
        return self.session.query(User).filter(User.username == username).one()

    def create(self, user_data):  # создаем пользователя
        ent = User(**user_data)
        self.session.add(ent)
        self.session.commit()
        return ent

    def delete(self, uid):  # удаляем пользователя
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

    def update(self, user_data):  # обновляем данные пользователя
        user = self.get_one(user_data.get("id"))
        if user_data.get("username"):
            user.username = user_data.get("username")
        if user_data.get("role"):
            user.role = user_data.get("role")
        if user_data.get("password"):
            user.password = user_data.get("password")

        self.session.add(user)
        self.session.commit()
