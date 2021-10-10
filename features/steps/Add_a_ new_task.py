import time

from behave import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


def set_up(context):
    context.driver, context.action_chains = None, None
    context.chrome_options = Options()
    context.chrome_options.add_argument("--disable-extensions")
    context.chrome_options.add_argument("--incognito")
    context.chrome_options.add_argument("--disable-popup-blocking")
    context.chrome_options.add_argument("--start-maximized")
    set_driver(context)


def set_driver(context):
    context.driver = webdriver.Chrome(options=context.chrome_options)
    context.driver.get("https://todomvc.com/examples/angularjs/#/")
    context.driver.implicitly_wait(10)
    context.action_chains = ActionChains(context.driver)


@given("I am in the todos page")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    set_up(context)
    time.sleep(2)


def add_new_task(context, task_name):
    context.driver.find_element_by_class_name("new-todo").send_keys(task_name + "\n")


@when('I add new task "Clean my house"')
def step_impl(context):
    """

    :type context: behave.runner.Context
    """
    add_new_task(context, "Clean my house")


def find_a_task(self, task_name):
    todo_list = self.driver.find_elements_by_xpath("/html/body/ng-view/section/section/ul/li")
    for i in range(len(todo_list)):
        if todo_list[i].text == task_name:
            time.sleep(1)
            return i
    time.sleep(1)
    return -1


@then('the task "Clean my house" will be added to the list')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    to_return = context.find_a_task("Clean my house") <= 0
    context.driver.close()
    assert to_return
