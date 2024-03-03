import time
from base.auth_page import AuthPage, AuthRegistration
from base.locators import AuthLocators
import allure

@allure.feature("Авторизация")
def base_test_auth_page(web_driver, username, password="Kozdrin23805"):
    page = AuthPage(web_driver)
    page.open_auth_page()
    time.sleep(5)
    if not username.startswith("+"):
        page = web_driver.find_element('#t-btn-tab-login').click()
    page.enter_email_phone_number(username)
    page.enter_pass(password)
    page.btn_click()
    time.sleep(5)

@allure.story("Авторизация по номеру телефона")
def test_auth_phone(web_driver):
    phone = "+79962049394"
    base_test_auth_page(web_driver, username=phone)

@allure.story("Авторизация по электронной почте")
def test_auth_email(web_driver):
    email = "kozdrin2013@yandex.ru"
    base_test_auth_page(web_driver, username=email)

@allure.story("Авторизация по номеру без кода страны")
def test_auth_number(web_driver):
    number = "79962049394"
    base_test_auth_page(web_driver, username=number)

@allure.feature("Проверка ссылок на странице авторизации")
def base_test_auth_links(web_driver, *locator):
    page = AuthPage(web_driver)
    page.open_auth_page()
    time.sleep(5)

    # "Забыл пароль" и возврат на страницу авторизации
    # base_redirect_link -> forgot_password_link или user_agreement_link или help_link или registration_link
    link = web_driver.find_element(*locator)
    link.click()
    time.sleep(1)

@allure.story("Проверка ссылки 'Пользовательское соглашение'")
def test_user_agreement_link(web_driver):
    base_test_auth_links(*AuthLocators.AUTH_USER_AGREEMENT_LINK)

@allure.story("Проверка ссылки 'Помощь'")
def test_help_links(web_driver):
    base_test_auth_links(*AuthLocators.AUTH_HELP_LINK)

@allure.story("Проверка ссылки 'Регистрация'")
def test_registration_link(web_driver):
    base_test_auth_links(*AuthLocators.AUTH_REGISTRATION)

@allure.story("Проверка ссылки 'Забыл пароль'")
def test_forgot_password_links(web_driver):
    base_test_auth_links(*AuthLocators.AUTH_FORGOT_PASS_LINK)

    # Вернемся назад
    web_driver.back()
    time.sleep(3)

    # Проверим, что вернулись на страницу авторизации
    assert '/auth' in web_driver.current_url, "Did not return to the login page"

@allure.feature("Проверка маскировки пароля")
def test_password_masking(web_driver):
    page = AuthPage(web_driver)
    page.open_auth_page()
    time.sleep(5)

    # локатор маскировки пароля
    password_mask = web_driver.find_element(*AuthLocators.AUTH_PASS_MASK)
    assert password_mask.is_displayed(), "Password masking not visible"

    # После ввода пароля и двойного нажатия на глазик он дважды меняет состояние на отображение пароля
    page.enter_pass("123")
    time.sleep(2)
    password_mask.click()
    time.sleep(2)
    assert password_mask.is_displayed(), "Password is not open"

# Негативные тесты:

@allure.feature("Негативные тесты")
@allure.story("Регистрация с использованием существующих данных")
def test_registration_with_existing_data(web_driver):
    page = AuthRegistration(web_driver)
    # Откроем страницу регистрации
    page = page.open_registration_page()
    time.sleep(5)

    # Заполним поля регистрации с данными уже существующего пользователя
    first_name = "Роман"
    last_name = "Коздринь"
    city = "Энгельс"
    phone_or_email = "kozdrin2013@yandex.ru"
    password = "Kozdrin23805"

    page.enter_first_name(first_name)
    page.enter_last_name(last_name)
    page.enter_city(city)
    page.enter_email_or_phone(phone_or_email)
    page.enter_pass(password)
    page.enter_pass_confirm(password)
    page.click_register_button()
    time.sleep(3)
    # Проверим, что мы видим сообщение об ошибке
    assert page.is_error_message_displayed(), "Error message not displayed for duplicate registration"

@allure.story("Проверка авторизации с некорректными данными")
def base_test_wrong_auth_data(web_driver, locator, username, password):
    page = AuthPage(web_driver)
    page.open_auth_page()
    time.sleep(5)

    # Оставляем поле пароля пустым и пытаемся войти
    empty_password = web_driver.find_element(locator)
    empty_password.click()

    page.enter_phone(username)
    page.enter_pass(password)
    page.btn_click()
    time.sleep(2)

@allure.story("Авторизация с пустым полем пароля")
def test_empty_password(web_driver):
    phone = "+79117805671"
    password = ""
    base_test_wrong_auth_data(web_driver, *AuthLocators.AUTH_PASS, phone, password)

    # Проверяем, что отобразилось сообщение об ошибке
    assert web_driver.find_element(*AuthLocators.AUTH_PASS).is_displayed(), ("Error message not displayed for empty "
                                                                             "password")

@allure.story("Авторизация с неверным паролем")
def test_wrong_password(web_driver):
    phone = "+79117805671"
    password = "212445"
    base_test_wrong_auth_data(web_driver, *AuthLocators.AUTH_PASS, phone, password)

    # Проверяем, что отобразилась ошибка в поле ввода
    assert web_driver.find_element(*AuthLocators.AUTH_ERROR_LGN).is_displayed(), ("Error message displayed for wrong "
                                                                                  "password")

@allure.story("Авторизация с неверным номером телефона")
def test_wrong_phone(web_driver):
    phone = "+791232311"
    password = "Yakish98"
    base_test_wrong_auth_data(web_driver, *AuthLocators.AUTH_EMAIL_OR_PHONE, phone, password)

    # Проверяем, что отобразилась ошибка в поле ввода
    assert web_driver.find_element(*AuthLocators.AUTH_ERROR_LGN).is_displayed(), ("Error message displayed for wrong "
                                                                                  "phone number")

@allure.story("Авторизация с неверным номером без кода страны")
def test_wrong_number(web_driver):
    phone = "278015185543"
    password = "Yakish98"
    base_test_wrong_auth_data(web_driver, *AuthLocators.AUTH_EMAIL_OR_PHONE, phone, password)

    # Проверяем, что отобразилась ошибка в поле ввода
    assert web_driver.find_element(*AuthLocators.AUTH_ERROR_LGN).is_displayed(), ("Error message displayed for wrong "
                                                                                  "phone number")

@allure.story("Авторизация с неверным email")
def test_wrong_email(web_driver):
    number = "asdadasd@sdd.asd"
    password = "Yakish98"
    base_test_wrong_auth_data(web_driver, *AuthLocators.AUTH_EMAIL_OR_PHONE, number, password)

    # Проверяем, что отобразилось сообщение об ошибке
    assert web_driver.find_element(*AuthLocators.AUTH_ERROR_LGN).is_displayed(), ("Error message not displayed for "
                                                                                  "wrong number")


# def test_copy_hidden_password(web_driver):
#     page = AuthPage(web_driver)
#     page.open_auth_page()
#     time.sleep(5)
#
#     password_field = web_driver.find_element(*AuthLocators.AUTH_PASS)
#     page.enter_pass("Yakish98")
#
#     password_mask = web_driver.find_element(*AuthLocators.AUTH_PASS_MASK)
#     assert password_mask.is_displayed(), "Password masking not working"
#
#     # Копируем скрытый пароль
#     password_field.send_keys(Keys.CONTROL, 'a')
#     password_field.send_keys(Keys.CONTROL, 'c')
#
#     # Вставляем скопированный пароль в другое поле
#     another_field = web_driver.find_element(By.CSS_SELECTOR, 'your_another_field_locator')
#     another_field.send_keys(Keys.CONTROL, 'v')
#
#     # Проверяем, что скрытый пароль не скопировался
#     assert another_field.get_attribute("value") == "", "Hidden password copied"
