import data
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    request_taxi_button = (By.CSS_SELECTOR, ".button.round")
    comfort_rate_icon = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[2]/div[1]/div[5]/div[1]/img")
    phone_number_button = (By.CLASS_NAME, "np-button")
    phone_number_field = (By.XPATH, "/html/body/div/div/div[1]/div[2]/div[1]/form/div[1]/div[1]/input")
    close_button_phone = (By.XPATH, "/html/body/div/div/div[1]/div[2]/div[1]/button")
    method_payment_button = (By.CLASS_NAME, "pp-text")
    add_card_button = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]")
    card_field = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[2]/input")
    card_code_field = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/div[2]/div[2]/input")
    button_add = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[2]/form/div[3]/button[1]")
    close_method_payment = (By.XPATH, "/html/body/div/div/div[2]/div[2]/div[1]/button")
    message_field = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[3]/div/input")
    slider_blanket = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span")
    ice_cream_count = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]")
    ice_cream_counter = (By.XPATH, "/html/body/div/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]")
    order_taxi_button = (By.XPATH, "/html/body/div/div/div[3]/div[4]/button/span[1]")
    wait_window = (By.CLASS_NAME, "order-header-content")

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        #self.driver.find_element(*self.from_field).send_keys(from_address)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.from_field)
        ).send_keys(from_address)

    def set_to(self, to_address):
        #self.driver.find_element(*self.to_field).send_keys(to_address)
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.to_field)
        ).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)

    def get_request_taxi_button(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.request_taxi_button)
        )
    def click_on_request_button(self):
        self.get_request_taxi_button().click()

    def get_comfort_rate_icon(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.comfort_rate_icon)
        )

    def click_on_comfort_rate_icon(self):
        self.get_comfort_rate_icon().click()



    #ingresar numero de telefono
    def get_phone_number_button(self):
            return WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.phone_number_button)
            )

    def click_on_phone_number_button(self):
        self.get_phone_number_button().click()

    def get_phone_number_field(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.phone_number_field)
        )
    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_field).get_property('value')

    def set_phone_number(self):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.phone_number_field)
        ).send_keys(data.phone_number)

    def get_close_button_phone(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.close_button_phone)

        )
    def click_close_button_phone(self):
        self.get_close_button_phone().click()




   #agregar tarjeta
    def get_method_payment_button(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.method_payment_button)
        )

    def click_on_method_payment_button(self):
        self.get_method_payment_button().click()

    def get_add_card_button(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.add_card_button)
        )
    def click_on_add_card_button(self):
        self.get_add_card_button().click()

    def get_card_field(self):
        return WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(self.card_field)
        )

    def get_card(self):
        return self.driver.find_element(*self.card_field).get_property('value')

    def set_add_card(self):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.card_field)
        ).send_keys(data.card_number, Keys.TAB)

    def get_card_code_field(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.card_code_field)
        )

    def get_code(self):
        return self.driver.find_element(*self.card_code_field).get_property('value')

    def set_code(self):
        WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.card_code_field)
        ).send_keys(data.card_code, Keys.TAB)

    def get_button_add(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.button_add)
        )

    def click_button_add(self):
        self.get_button_add().click()

    def get_close_method_payment(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.close_method_payment)
        )

    def click_on_close_method_payment(self):
        self.get_close_method_payment().click()



    # escribir mensaje al conductor
    def get_message_field(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.message_field)
        )

    def get_message(self):
        return self.driver.find_element(*self.message_field).get_property('value')

    def set_message(self):
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(self.message_field)
        ).send_keys(data.message_for_driver, Keys.TAB)

    def get_slider_blanket(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.slider_blanket)
        )
    def click_on_slider_blanket(self):
        self.get_slider_blanket().click()

    def set_slider_blanket(self):
        WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.slider_blanket)
        )


    #pedir 2 helados
    def get_ice_cream_count(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.ice_cream_count)
        )

    def click_on_ice_cream_count(self):
        self.get_ice_cream_count().click()

    def get_ice_cream_counter(self):
        return WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.ice_cream_counter)
        )

    def set_ice_cream_count(self):
        WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.ice_cream_count)
        )

    def get_order_taxi_button(self):
        return WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.order_taxi_button)
        )

    def click_on_order_taxi_button(self):
        self.get_order_taxi_button().click()


    def set_order_taxi(self):
        WebDriverWait(self.driver,5).until(
            EC.element_to_be_clickable(self.order_taxi_button)
        )

    def get_wait_window(self):
        return WebDriverWait(self.driver,5).until(
            EC.presence_of_element_located(self.wait_window)
        )

    def click_on_button_and_wait(self):
        # Método para hacer clic en el botón que muestra la ventana de espera
        self.driver.find_element(By.CLASS_NAME, "order-header-content").click()  # Reemplaza con el ID correcto del botón
        self.get_wait_window()  # Espera la ventana de espera

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono

        options = Options()

        options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})

        cls.driver = webdriver.Chrome(service=Service(), options=options)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_comfort_rate(self):
        self.test_set_route()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_on_request_button()
        routes_page.click_on_comfort_rate_icon()

        assert routes_page.get_comfort_rate_icon().text in "Comfort"

    def test_enter_phone_number(self):
        self.test_comfort_rate()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_on_phone_number_button()
        routes_page.set_phone_number()
        routes_page.click_close_button_phone()


        assert routes_page.get_phone_number() == data.phone_number

    def test_enter_payment_method(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_on_method_payment_button()
        routes_page.click_on_add_card_button()
        routes_page.set_add_card()
        routes_page.set_code()
        routes_page.click_button_add()
        routes_page.click_on_close_method_payment()

        assert routes_page.get_card() == data.card_number
        assert routes_page.get_code() == data.card_code

    def test_enter_message_for_the_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_message()

        assert routes_page.get_message() == data.message_for_driver

    def test_slider_blanket(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_slider_blanket()
        routes_page.click_on_slider_blanket()


    def test_ice_cream_count(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_ice_cream_count()
        routes_page.click_on_ice_cream_count()
        routes_page.click_on_ice_cream_count()

        assert routes_page.get_ice_cream_counter().text in "2"


    def test_order_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_order_taxi()
        routes_page.click_on_order_taxi_button()
        routes_page.click_on_button_and_wait()

        wait_window = routes_page.get_wait_window()
        assert wait_window.is_displayed()


    @classmethod
    def teardown_class(cls):
        time.sleep(30)
        cls.driver.quit()
