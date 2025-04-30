from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import data
from methodshomepage import UrbanRoutesPage, retrieve_phone_code


#-----------------------------------------------------------------------------------------------------------------------
# Pruebas

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        options = Options()
        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=options)
        cls.methods = UrbanRoutesPage(cls.driver)

# Prueba 1 Configurar la dirección
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

# Prueba 2 Seleccionar la tarifa Comfort.
    def test_select_comfort_rate_icon(self):
        self.test_set_route()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.click_on_order_taxi_button()
        routes_pages.click_on_comfort_rate_icon()
        comfort_rate = routes_pages.get_comfort_rate_icon().text
        comfort_text = "Comfort"

        assert comfort_rate in comfort_text

# Prueba 3 Rellenar el número de teléfono.
    def test_set_phone_number(self):
        self.test_select_comfort_rate_icon()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.click_on_phone_number_field_one()
        routes_pages.set_phone_number_field_two()
        routes_pages.click_next_button()
        routes_pages.set_code_number()
        routes_pages.click_confirm_button()

        assert routes_pages.get_phone_number_value() == '+1 123 123 12 12'

# Prueba 4 Agregar una tarjeta de crédito.
    def test_set_card_number(self):
        self.test_set_phone_number()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.get_card_number_field()
        routes_pages.get_add_new_card_number_button()
        routes_pages.set_new_card_number()
        routes_pages.get_cvv_field()
        routes_pages.set_cvv_number()
        routes_pages.get_confirm_add_card_button()

        assert routes_pages.new_card_value() == '1234 5678 9100'
        assert routes_pages.get_cvv_value() == '111'


# Prueba 5 Escribir un mensaje para el controlador.
    def test_send_message_for_driver(self):
        self.test_select_comfort_rate_icon()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.get_comment_field()
        routes_pages.set_message_for_driver()

        assert routes_pages.message_for_driver() == 'Traiga un aperitivo'

# Prueba 6 Pedir una manta y pañuelos.
    def test_order_blanket(self):
        self.test_send_message_for_driver()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.click_blanket_button()
# Corrección: Se agrega el assert.
        assert routes_pages.switch_button_active().is_selected() == True

# Prueba 7 Pedir 2 helados.
    def test_order_two_ice_cream(self):
        self.test_order_blanket()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.get_ice_cream_button_plus()
        routes_pages.click_ice_cream_button_plus()
        routes_pages.click_ice_cream_button_plus()
        routes_pages.ice_cream_counter_value()

        assert routes_pages.ice_cream_counter_value() == '2'

# Prueba 8 Aparece el modal para buscar un taxi.
    def test_find_a_car(self):
        self.test_order_two_ice_cream()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.click_find_a_car()
# Corrección: Se agrega el assert.
        assert routes_pages.serch_a_car_screen() == 'Buscar automóvil'


# Prueba 9 Esperar a que aparezca la información del conductor en el modal (opcional).
    def test_driver_information(self):
        self.test_find_a_car()
        routes_pages = UrbanRoutesPage(self.driver)
        routes_pages.get_timeout_modal()
# Corrección: Se agrega el assert.
        assert routes_pages.order_shown().is_displayed() == True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
