from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import data


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
# ----------------------------------------------------------------------------------------------------------------------

class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    order_taxi_button = (By.CSS_SELECTOR, ".button.round")
    comfort_rate_icon = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    phone_number_field_one = (By.XPATH, "//div[@class='np-text' and text() ='Número de teléfono']")
    phone_number_field_two = (By.XPATH, "//label[@class='label' and text()= 'Número de teléfono']")
    next_button = (By.XPATH, "//button[@class='button full' and text()= 'Siguiente']")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_order_taxi_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.order_taxi_button)
        )

    def click_on_order_taxi_button(self):
        self.get_order_taxi_button().click()

    def get_comfort_rate_icon(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.comfort_rate_icon)
        )

    def click_on_comfort_rate_icon(self):
        self.get_comfort_rate_icon().click()

    def get_phone_number_field_one(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.phone_number_field_one)
        )
    def click_on_phone_number_field_one(self):
        self.get_phone_number_field_one().click()


    def get_phone_number_field_two(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.phone_number_field_two)
        )

    def enter_phone_number_field_two(self):
        self.get_phone_number_field_two().click()
         #enter_phone_number = self.driver.find_element(*self.phone_number_field_two)
        self.get_phone_number_field_two().send_keys(data.phone_number)


    def click_next_button(self):
        return WebDriverWait(self.driver, 5).until(
            expected_conditions.element_to_be_clickable(self.next_button)
        ).click()


#-----------------------------------------------------------------------------------------------------------------------

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):

        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=options)

# Prueba 1
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to
# Prueba 2
    def test_select_comfort_rate_icon(self):
        self.test_set_route()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.click_on_order_taxi_button()
        routes_pages.click_on_comfort_rate_icon()

        comfort_rate = routes_pages.get_comfort_rate_icon().text
        comfort_text = "Comfort"

        assert comfort_rate in comfort_text

# Prueba 3
    def test_set_phone_number(self):
        self.test_select_comfort_rate_icon()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.click_on_phone_number_field_one()
        routes_pages.get_phone_number_field_two()
        routes_pages.enter_phone_number_field_two()
        routes_pages.click_next_button()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
