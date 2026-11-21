import pytest
from playwright.sync_api import Page, expect




def test_home_page(page : Page):
    page.goto("https://didakticek.sk/")

    expect(page).to_have_title("Živý Portál Chrobáčik")

def test_login_button_exists(page : Page):
    page.goto("https://didakticek.sk/")

    login_button = (
        page.get_by_role("navigation", name="Verejná navigácia")
        .get_by_role("button", name="Prihlásiť sa")
    )

    expect(login_button).to_be_visible()
    expect(login_button).to_be_enabled()

def test_login(page : Page):
    page.goto("https://didakticek.sk/")

    login_button = (
        page.get_by_role("navigation", name="Verejná navigácia")
        .get_by_role("button", name="Prihlásiť sa")
    )

    login_button.click()

@pytest.mark.parametrize(
        "email, expected", [
            ("test@example.com", True),
            ("testexample.com", False),
            ("test.com@example", True),
            (" ", False),
            ("", False),
            ("email@", False),
            ("te st@example.com", False),
            ("test@example .com", False),
            ("test@example.com.us", True),
            ("test@example.io", True),
            ("+š+ťáéľšť=ééč+ľ´´", False),
            ("121341412", False),
            ("___", False)
        ]
)

def test_input_email(page : Page, email, expected):
    page.goto("https://didakticek.sk/")

    login_button = (
        page.get_by_role("navigation", name="Verejná navigácia")
        .get_by_role("button", name="Prihlásiť sa")
    )

    login_button.click()

    email_input = (
        page.get_by_role("textbox", name="Email")
    )

    expect(email_input).to_be_visible()
    expect(email_input).to_be_enabled()

    email_input.fill(email)

    is_valid_email = email_input.evaluate("(element) => element.checkValidity()")

    assert is_valid_email == expected

@pytest.mark.parametrize(
        "email, expected", [
            ("test@example.com", True),
            ("testexample.com", False),
            ("test.com@example", True),
            (" ", False),
            ("", False),
            ("email@", False),
            ("te st@example.com", False),
            ("test@example .com", False),
            ("test@example.com.us", True),
            ("test@example.io", True),
            ("+š+ťáéľšť=ééč+ľ´´", False),
            ("121341412", False),
            ("___", False)
        ]
)

def test_forgotten_password_page(page : Page, email, expected):
    page.goto("https://didakticek.sk/")

    login_button = (
        page.get_by_role("navigation", name="Verejná navigácia")
        .get_by_role("button", name="Prihlásiť sa")
    )

    login_button.click()

    forgotten_password_button = (
        page.get_by_role("link", name="Zabudnuté heslo?")
    )

    expect(forgotten_password_button).to_be_visible()
    expect(forgotten_password_button).to_be_enabled()

    forgotten_password_button.click()

    expect(page).to_have_url("https://didakticek.sk/admin/public/index.php?page=portal%2Flogin&flow=password")

    email_input = (
        page.get_by_role("textbox", name="Prihlasovací e-mail")
    )

    expect(email_input).to_be_visible()
    expect(email_input).to_be_enabled()

    confirm_button = (
        page.get_by_role("button", name="Poslať odkaz na obnovu")
    )

    expect(confirm_button).to_be_visible()

    email_input.fill(email)

    is_valid_email = email_input.evaluate("(element) => element.checkValidity()")

    validation = email_input.evaluate("""
                                      (element) => ({
                                          value: element.value,
                                          type: element.type,
                                          required: element.required,
                                          pattern: element.pattern,
                                          valid: element.checkValidity(),
                                          message: element.validationMessage
                                      })
                                      """)

    print(f"EMAIL: {email}")
    print(f"EXPECTED: {expected}")
    print(f"ACTUAL: {validation}")

    assert validation["valid"] == expected

@pytest.mark.parametrize(
    "email", [
        " ",
        "test@example.com",
        "@",
        "testexamplecom",
        ".com",
        "example.com",
        "123",
        "-.+ľ"
    ]
)

def test_forgotten_password_invalid_email(page : Page, email):
    page.goto("https://didakticek.sk/")

    login_button = (page.get_by_role("navigation", name="Verejná navigácia").get_by_role("button", name="Prihlásiť sa"))
    login_button.click()

    forgotten_password_button = (page.get_by_role("link", name="Zabudnuté heslo?"))
    forgotten_password_button.click()

    email_input = (page.get_by_role("textbox", name="Prihlasovací e-mail"))
    email_input.fill(email)

    confirm_button = (page.get_by_role("button", name="Poslať odkaz na obnovu"))
    confirm_button.click()

    print("URL:", page.url)

    print("PAGE TEXT:")
    print(page.locator("body").inner_text())

    print("BROWSER VALIDATION:")
    print(email_input.evaluate(
        "(element) => element.validationMessage"
    ))





