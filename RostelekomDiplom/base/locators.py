from selenium.webdriver.common.by import By

class AuthLocators:
    #AUTH_REGISTRATION = None
    AUTH_EMAIL_PHONE_NUMBER = (By.CSS_SELECTOR, '#username')
    AUTH_PASS = (By.CSS_SELECTOR, '#password')
    AUTH_BTN = (By.CSS_SELECTOR, '#kc-login')
    AUTH_PASS_MASK = (By.CSS_SELECTOR, '.rt-eye-icon')
    AUTH_FORGOT_PASS_LINK = (By.CSS_SELECTOR, '#forgot_password')
    AUTH_USER_AGREEMENT_LINK = (By.CSS_SELECTOR, '#rt-auth-agreement-link')
    AUTH_ERROR_LGN = (By.CSS_SELECTOR, '#form-error-message')

    AUTH_HELP_LINK = (By.CSS_SELECTOR, '#faq-open')
    AUTH_REGISTRATION = (By.CSS_SELECTOR, '#kc-register')

    AUTH_CITY = (By.CSS_SELECTOR,'//span[contains(@class, "rt-input__mask-start") and contains(text(), "Москва г")]')
    AUTH_FIRST_NAME = (By.CSS_SELECTOR, '#name="firstName"')
    AUTH_LAST_NAME = (By.CSS_SELECTOR, '#name=lastname')
    AUTH_EMAIL_OR_PHONE = (By.CSS_SELECTOR, '#id="address"')
    AUTH_REGISTRATION_BTN = (By.CSS_SELECTOR, '#name="register"')
    AUTH_REGISTRATION_PASS = (By.CSS_SELECTOR, '#id="password"')
    AUTH_PASS_CONFIRM = (By.CSS_SELECTOR, '#id="password-confirm"')
