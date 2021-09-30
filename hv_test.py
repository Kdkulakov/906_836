from locust import HttpUser, TaskSet, task


def login(l):
    l.client.post("auth/login/", {"username": "admin", "password": "123"})


def logout(l):
    l.client.post("auth/logout/", {"username": "admin", "password": "123"})


def index(l):
    l.client.get("")

# def profile(l):
#     l.client.get("auth/edit/")


def products(l):
    l.client.get("products/")


def products_1(l):
    l.client.get("products/1/")


def products_2(l):
    l.client.get("products/2/")


def products_3(l):
    l.client.get("products/3/")


def products_4(l):
    l.client.get("products/4/")


@task
class UserBehavior(TaskSet):
    tasks = {index: 2, products: 5, products_1: 3, products_2: 3, products_3: 3, products_4: 3, }

    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)
@task
class WebsiteUser(HttpUser):
    task_set = UserBehavior
    min_wait = 500
    max_wait = 900