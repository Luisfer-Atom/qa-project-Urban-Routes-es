from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import data
from locatorshomepage import LocatorsHomePage

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code
# ----------------------------------------------------------------------------------------------------------------------------
# Métodos

class UrbanRoutesPage:

    def __init__(self, driver):
                self.driver = driver
                self.locators = LocatorsHomePage
# Prueba 1:
    def set_from(self, from_address):
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.locators.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.locators.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.locators.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.locators.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

# Prueba 2:
    def get_order_taxi_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.order_taxi_button)
        )

    def click_on_order_taxi_button(self):
        self.get_order_taxi_button().click()

    def get_comfort_rate_icon(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.comfort_rate_icon)
        )

    def click_on_comfort_rate_icon(self):
        self.get_comfort_rate_icon().click()

# Prueba 3:
    def get_phone_number_field_one(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.phone_number_field_one)
        )
    def click_on_phone_number_field_one(self):
        self.get_phone_number_field_one().click()

    def set_phone_number_field_two(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.phone_number_field_two)
        ).send_keys(data.phone_number)

    def click_next_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.next_button)
        ).click()

    def get_code_field(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.code_field)
        )

    def set_code_number(self):
        self.get_code_field().send_keys(retrieve_phone_code(driver=self.driver))

    def click_confirm_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.confirm_button)
        ).click()

    def get_phone_number_value(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.locators.phone_number_field_two)
        ).get_property('value')

#Prueba 4:
    def get_card_number_field(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.card_number)
        ).click()

    def get_add_new_card_number_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.add_new_card_button)
        ).click()

    def set_new_card_number(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.add_new_card_number)
        ).send_keys(data.card_number)

    def new_card_value(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.locators.add_new_card_number)
        ).get_property('value')

    def get_cvv_field(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.locators.cvv_field)
        )

    def set_cvv_number(self):
        self.get_cvv_field().send_keys(data.card_code + Keys.TAB)

    def get_cvv_value(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.locators.cvv_field)
        ).get_property('value')

    def get_confirm_add_card_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.locators.confirm_add_card_button)
        ).click()

# Prueba 5:
    def get_comment_field(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.comment_field)
        )

    def set_message_for_driver(self):
        self.get_comment_field().send_keys(data.message_for_driver)

    def message_for_driver(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.locators.comment_field)
        ).get_property('value')

# Prueba 6:
    def click_blanket_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.slider_blanket_button)
        ).click()

    def switch_button_active(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.locators.switch_button)
        )

# Prueba 7:
    def get_ice_cream_button_plus(self):
        return WebDriverWait(self.driver, 5 ).until(
            expected_conditions.element_to_be_clickable(self.locators.ice_cream_button_plus)
        )
    def click_ice_cream_button_plus(self):
        self.get_ice_cream_button_plus().click()

    def ice_cream_counter_value(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.locators.ice_cream_counter)
        ).text

# Prueba 8:
    def click_find_a_car(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.locators.complete_order_button)
        ).click()

    def serch_a_car_screen(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.locators.modal_serch_a_car)
        ).text


# Prueba 9:
    def get_timeout_modal(self):
        return WebDriverWait(self.driver,55).until(
            expected_conditions.visibility_of_element_located(self.locators.timeout_modal)
        )

    def order_shown(self):
        return WebDriverWait(self.driver, 55).until(
            expected_conditions.visibility_of_element_located(self.locators.order_screen_displayed)
        )

