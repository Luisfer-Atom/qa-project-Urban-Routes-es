from selenium.webdriver.common.by import By

#--------------------------------------------------------------------------------------------------------------------
# Localizadores

class LocatorsHomePage:

    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    order_taxi_button = (By.CSS_SELECTOR, ".button.round")
    comfort_rate_icon = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    phone_number_field_one = (By.XPATH, "//div[@class='np-text' and text() ='Número de teléfono']")
    phone_number_field_two = (By.XPATH, "//*[@id='phone']")
    next_button = (By.XPATH, "//button[@class='button full' and text()= 'Siguiente']")
    code_field = (By.XPATH, "//*[@id='code']")
    confirm_button = (By.XPATH, "//button[@class='button full' and text()= 'Confirmar']")
    card_number = (By.XPATH, "//div[@class='pp-button filled']")
    add_new_card_button = (By.XPATH, "//div[@class='pp-title' and text() ='Agregar tarjeta']")
    add_new_card_number = (By.XPATH, "//*[@id='number']")
    cvv_field = (By.NAME, "code")
    confirm_add_card_button = (By.XPATH, "//button[@class='button full' and text()='Agregar']")
    comment_field = (By.NAME, "comment")
    slider_blanket_button = (By.XPATH, "//span[@class= 'slider round']")
    ice_cream_button_plus = (By.CLASS_NAME, 'counter-plus')
    ice_cream_counter = (By.CLASS_NAME, 'counter-value')
    complete_order_button = (By.CSS_SELECTOR, "span.smart-button-main")
    timeout_modal = (By.CSS_SELECTOR, "div.order-number")
    switch_button = (By.CSS_SELECTOR, ".switch-input")
    modal_serch_a_car = (By.CLASS_NAME, 'order-header-title')
    order_screen_displayed = (By.CSS_SELECTOR, ".order.shown")