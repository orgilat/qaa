import pytest
import allure
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
import time
import shutil  # נוסיף לבדיקה האם chromedriver קיים

# ⏱️ לא חובה אבל נחמד לדיבוג
start_time = time.time()


# 🧪 Pytest Fixture שפותחת וסוגרת דפדפן אוטומטית
@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless")  # אם רוצים מצב בלי GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver_path = shutil.which("chromedriver")
    if not driver_path:
        raise RuntimeError("chromedriver לא נמצא במערכת או ב־PATH")

    service = Service(driver_path)
    _driver = webdriver.Chrome(service=service, options=options)
    yield _driver
    _driver.quit()


@allure.feature("ניהול סקרים")
@allure.story("בדיקת לחצנים באתר תמורות")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("Selenium", "UI", "Regression", "Automation")
@allure.description_html("""
    <h2>תיאור הבדיקה</h2>
    <p>בדיקה מקיפה של לחצנים באתר ניהול סקרים, הכוללת מעבר בין מסכים ובדיקות פנימיות
    על רכיבי ממשק שונים. הבדיקה כוללת:</p>
    <ul>
      <li>כניסה למסך ניהול סקרים והתחברות עם שם משתמש וסיסמה.</li>
      <li>מעבר בין מסכים כמו 'עונות', 'שאלות חובה' ו'חוקים על שאלות'.</li>
      <li>בדיקות פנימיות הכוללות לחיצות, חזרה למסך הקודם והקלדה בתיבות חיפוש.</li>
      <li>תיעוד מפורט של כל שלב בדוח Allure.</li>
    </ul>
""")
def test_survey_buttons(driver):
    global passed, failed
    passed, failed = 0, 0  # איפוס משתני הצלחה/כישלון

    # המשך הקוד התקני כאן...

    try:
        buttons = [
            {"name": "ניהול הסקר", "xpath": "//a[contains(text(), 'ניהול הסקר')]"},
            {"name": "ניהול סוציומטרי", "xpath": "//a[contains(text(), 'ניהול סוציומטרי')]"},
            {"name": "עונות", "xpath": "//input[contains(@value, 'עונות')]"},
            {"name": "שאלות חובה", "xpath": "//input[contains(@value, 'שאלות חובה')]"},
            {"name": "חוקים לבדיקת שאלונים חריגים", "xpath": "//input[contains(@value, 'חוקים לבדיקת שאלונים חריגים')]"},
            {"name": "חוקים על שאלות", "xpath": "//input[contains(@value, 'חוקים על שאלות')]"},
            {"name": "כללי השתתפות לפי סוג יחידה", "xpath": "//input[contains(@value, 'כללי השתתפות לפי סוג יחידה')]"},
            {"name": "הגדרת השדות שיופיעו בטבלאות", "xpath": "//input[contains(@value, 'הגדרת השדות שיופיעו בטבלאות')]"},
            {"name": "אופציות לסוציומטרי", "xpath": "//input[contains(@value, 'אופציות לסוציומטרי')]"},
            {"name": "הגדרה וניהול סטטוסים לאירועים", "xpath": "//input[contains(@value, 'הגדרה וניהול סטטוסים לאירועים')]"},
            {"name": "סיבות להוספת או הסרת משתתפים באירוע", "xpath": "//input[contains(@value, 'סיבות להוספת או הסרת משתתפים באירוע')]"},
            {"name": "הגדרת כללי חריגות בגין מידת היכרות", "xpath": "//input[contains(@value, 'הגדרת שאלונים בהם מותר למחוק נתונים')]"},
            {"name": "רשימת אשכולות לאיגוד קבוצות של היגדים", "xpath": "//input[contains(@value, 'רשימת אשכולות לאיגוד קבוצות של היגדים')]"},
            {"name": "העברת משיבים ממאגר", "xpath": "//input[contains(@value, 'העברת משיבים ממאגר')]"},
            {"name": "ניהול הרשאות משתמשים", "xpath": "//input[contains(@value, 'ניהול הרשאות משתמשים')]"},
            {"name": "של פוטנציאל המשתתפים בסוציומטרי", "xpath": "//input[contains(@value, 'של פוטנציאל המשתתפים בסוציומטרי')]"},
            {"name": "הגדרת חוקי העתקה של נתונים מחושבים לשאלון העזר", "xpath": "//input[contains(@value, 'הגדרת חוקי העתקה של נתונים מחושבים לשאלון העזר')]"},
            {"name": "הגדרת כללים לחוקות חישוב", "xpath": "//input[contains(@value, 'הגדרת כללים לחוקות חישוב')]"},
            {"name": "עריכה שדות במאגר המשיבים", "xpath": "//input[contains(@value, 'עריכה שדות במאגר המשיבים')]"},
            {"name": "הגדרת שאלונים בהם מותר למחוק נתונים", "xpath": "//input[contains(@value, 'הגדרת שאלונים בהם מותר למחוק נתונים')]"},
            {"name": "ייצוא דוחות אישיים", "xpath": "//input[contains(@value, 'ייצוא דוחות אישיים')]"},
            {"name": "שיוך יחידות לאשכול", "xpath": "//input[contains(@value, 'שיוך יחידות לאשכול')]"},
            {"name": "פלט אישי בתיקיית עובד", "xpath": "//input[contains(@value, 'פלט אישי בתיקיית עובד')]"},
            {"name": "ניהול אירועים", "xpath": "//input[contains(@value, 'ניהול אירועים')]"},
        ]

        def close_alert_if_present():
            try:
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                alert = Alert(driver)
                alert.accept()
                allure.attach("Alert נסגר בהצלחה", name="Alert", attachment_type=allure.attachment_type.TEXT)
            except Exception as e:
                allure.attach(f"Alert לא נמצא או שגיאה: {e}", name="Alert Info", attachment_type=allure.attachment_type.TEXT)

        # מבצע את הלחיצות על כל הכפתורים
        for button in buttons:
            try:
                close_alert_if_present()
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button["xpath"])))
                element.click()
                allure.attach(f"לחצן '{button['name']}' נלחץ בהצלחה", name="Button Clicked", attachment_type=allure.attachment_type.TEXT)
                passed += 1  # סומן כהצלחה
            except Exception as e:
                allure.attach(f"לא ניתן ללחוץ על הכפתור '{button['name']}': {str(e)}", name="Error", attachment_type=allure.attachment_type.TEXT)
                failed += 1  # סומן ככישלון

    except Exception as e:
        failed += 1  # אם הייתה בעיה בבדיקה כולה
        allure.attach(f"שגיאה במהלך הבדיקה: {e}", name="Error Info", attachment_type=allure.attachment_type.TEXT)

    # בסוף תעשה תיעוד של התוצאות
    allure.attach(f"Total Passed: {passed}, Total Failed: {failed}", name="Test Results", attachment_type=allure.attachment_type.TEXT)

    try:
        with allure.step("פתיחת האתר והתחברות"):
            driver.get("https://www.survey.co.il/pms/MMDANEW/default.asp")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "login")))

            username = driver.find_element(By.NAME, "login")
            password = driver.find_element(By.NAME, "password")
            username.send_keys("MARINAS")
            password.send_keys("Ms123456")
            password.send_keys(Keys.RETURN)

            WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Logout')]")))
            allure.attach(driver.current_url, name="כתובת האתר לאחר התחברות", attachment_type=allure.attachment_type.TEXT)

        with allure.step("מעבר למסך ניהול סוציומטרי"):
            close_alert_if_present()

            # חכה להופעת כפתור 'ניהול סקרים'
            manage_survey_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, buttons[0]["xpath"]))
            )

            actions = ActionChains(driver)
            actions.move_to_element(manage_survey_button).perform()

            # חכה עד שהכפתור יהיה קליקבילי
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, buttons[1]["xpath"])))

            close_alert_if_present()
            soc_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, buttons[1]["xpath"]))
            )
            soc_button.click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@value, 'סוציומטרי')]")))

            allure.attach(driver.current_url, name="כתובת האתר לאחר המעבר", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
     allure.attach(f"שגיאה במהלך הבדיקה: {e}", name="Error Info", attachment_type=allure.attachment_type.TEXT)
     for button in buttons[23:]:
       if button["name"] == "ניהול אירועים":
        with allure.step("בדיקות פנימיות עבור 'ניהול אירועים'"):
            events_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, button["xpath"]))
            )
            events_button.click()
            WebDriverWait(driver, 0.5).until(EC.staleness_of(events_button))  # Wait for the page to update
            passed += 1

        with allure.step("לחיצה על 'להקמת אירוע חדש'"):
            add_event_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.//span[contains(@class, 'block')])='להקמת אירוע חדש']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", add_event_button)
            add_event_button.click()
            WebDriverWait(driver, 25).until(EC.staleness_of(add_event_button))  # Wait for the page to update
            passed += 1

        with allure.step("מילוי שם האירוע ב-'מאי הגיי'"):
            event_name_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='field floating-label' and @label='שם האירוע']//input"))
            )
            event_name_input.send_keys("אירוע לדוגמה ")
            WebDriverWait(driver, 5.5).until(EC.text_to_be_present_in_element_value((By.XPATH, "//div[@class='field floating-label' and @label='שם האירוע']//input"), "אירוע לדוגמה"))
            passed += 1

        with allure.step("בחירת עונת הערכה"):
            dropdown_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown dropdown-select' and @label='בחר עונת הערכה']//div[contains(@class, 'dropdown-btn')]"))
            )
            dropdown_button.click()

            season_option = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown-list']//li//div[@class='list-item']/span[text()='עונת 1']"))
            )
            season_option.click()
            passed += 1

        with allure.step("בחירת תאריך 18"):
            calendar_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'dx-dropdowneditor-button') and @aria-label='Select']"))
            )
            calendar_button.click()

            date_18 = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//td[contains(@class, 'dx-calendar-cell') and not(contains(@class, 'dx-calendar-other-view'))]//span[text()='18']"))
            )
            date_18.click()
            passed += 1

        with allure.step("בחירת תאריך 26 בתאריך סיום"):
            calendar_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'dx-datebox') and .//span[contains(., 'תאריך סיום')]]//div[contains(@class, 'dx-dropdowneditor-button') and @aria-label='Select']"))
            )
            calendar_button.click()

            date_input = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'dx-datebox') and .//span[contains(., 'תאריך סיום')]]//input[@type='text']"))
            )
            date_input.send_keys("18-03-2025" + Keys.ENTER)
            passed += 1

        with allure.step("בחירת סוג היחידה לאירוע - בחירת 'מטה'"):
            unit_dropdown_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown dropdown-select' and @label='הגדרת סוג היחידה לאירוע ']/div[contains(@class, 'dropdown-btn')]"))
            )
            unit_dropdown_button.click()

            unit_option_mathe = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown-list']//li//div[contains(@class, 'list-item')]//span[normalize-space(text())='מטה']"))
            )
            unit_option_mathe.click()
            passed += 2

        with allure.step("לחיצה פנימית על הריבוע ליד 'פיקוד 2'"):
            checkbox_pikud2 = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//li[@data-item-id='249']//div[contains(@class, 'dx-checkbox-container')]"))
            )
            checkbox_pikud2.click()
            passed += 1

        with allure.step("בחירת 'אוגדה 1' להצגת דוח מילוי"):
            section_header = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, "//div[normalize-space()='בחירת יחידות מאגדות להצגת דוח מילוי']"))
            )

            checkbox = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//div[normalize-space()='בחירת יחידות מאגדות להצגת דוח מילוי']/following::li[@aria-label='אוגדה 1' and @aria-level='2'][1]//div[contains(@class, 'dx-checkbox')]"))
            )
            checkbox.click()
            passed += 1

        with allure.step("גלילה לתחתית העמוד"):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        with allure.step("סימון מקוריות ויכולת תכנון"):
            label_originality = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='מקוריות וחדשנות']"))
            )
            label_originality.click()
            passed += 1

            label_planning = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='יכולת תכנון']"))
            )
            label_planning.click()
            passed += 1

       with allure.step("גלילה לראש העמוד"):
        driver.execute_script("window.scrollTo(0, 0);")

with allure.step("לחיצה על ניהול פוטנציאל"):
    try:
        manage_potential_tab = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "//a[.//div[contains(@class, 'q-tab__label') and normalize-space(text())='ניהול פוטנציאל']]"))
        )
        manage_potential_tab.click()
        passed += 1
    except TimeoutException:
        print("❌ לא נמצא כפתור ניהול פוטנציאל")
        failed += 1

with allure.step("חשב פוטנציאל מחדש"):
    try:
        button_recalculate = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'חשב פוטנציאל מחדש')]"))
        )
        button_recalculate.click()
        WebDriverWait(driver, 100).until_not(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".q-loading"))
        )
        passed += 1
    except TimeoutException:
        print("❌ לא נמצא כפתור 'חשב פוטנציאל מחדש'")
        failed += 1

with allure.step("הצגת פוטנציאל"):
    try:
        button_show = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'הצג פוטנציאל')]"))
        )
        button_show.click()
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'dx-datagrid-rowsview')]//table"))
        )
        passed += 1
    except TimeoutException:
        print("❌ לא נמצא כפתור הצגת פוטנציאל")
        failed += 1

with allure.step("בחירת 'לא' מהתפריט השמאלי ביותר"):
    try:
        dropdown_buttons = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='dx-widget dx-button-mode-contained dx-button-normal dx-rtl dx-dropdowneditor-button']"))
        )
        leftmost_button = sorted(dropdown_buttons, key=lambda el: el.location['x'])[0]
        leftmost_button.click()
        option_no = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and .//div[text()='לא']]"))
        )
        option_no.click()
        passed += 1
    except TimeoutException:
        print("❌ לא נמצא אפשרות 'לא' בתפריט")
        failed += 1

with allure.step("לולאת סימון צ'קבוקסים והגדרת אפשרות"):
    try:
        for _ in range(100):
            try:
                checkboxes = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//td[@role='gridcell']//div[@role='checkbox' and @aria-checked='false']"))
                )
                if not checkboxes:
                    break  # אין יותר צ'קבוקסים
            except TimeoutException:
                break

            for checkbox in checkboxes:
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                    checkbox.click()

                    # המתנה להסרת מצב הטעינה
                    WebDriverWait(driver, 10).until_not(
                        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'dx-overlay-wrapper') and contains(@class, 'dx-loadpanel-wrapper')]"))
                    )

                    # בחירת אפשרות מתוך תפריט
                    dropdown_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown-btn text-box valid populated']"))
                    )
                    dropdown_button.click()

                    option_to_select = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@class='list-item']/span[text()='המוערך נוסף על פי בקשתו']"))
                    )
                    option_to_select.click()
                    passed += 1
                    driver.execute_script("window.scrollBy(0, 100);")
                except TimeoutException as e_inner:
                    print(f"⚠️ Timeout during checkbox interaction: {e_inner}")
                    continue  # ממשיכים לצ'קבוקס הבא
                except Exception as e_inner:
                    print(f"⚠️ Error processing checkbox: {e_inner}")
                    continue  # ממשיכים לצ'קבוקס הבא

        with allure.step("סגירת חלון אם קיים"):
            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'material-icons') and normalize-space()='close']"))
                )
                close_button.click()
                passed += 1
            except TimeoutException:
                print("⚠️ לא נמצא כפתור סגירה, ממשיכים")

        with allure.step("מעבר לטאב 'מודל הערכה'"):
            try:
                tab_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[.//div[contains(@class, 'q-tab__label') and normalize-space(text())='מודל הערכה']]"))
                )
                tab_button.click()
                passed += 1
            except TimeoutException:
                print("❌ לא נמצא כפתור 'מודל הערכה'")
                failed += 1

        with allure.step("לחיצה על 'בחר מודל הערכה חדש'"):
            try:
                model_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space(text())='בחר מודל הערכה חדש']]"))
                )
                model_button.click()
                passed += 1
            except TimeoutException:
                print("❌ לא נמצא כפתור 'בחר מודל הערכה חדש'")
                failed += 1
    except Exception as e:
        failed += 1
        print(f"❌ Error in loop: {e}")

# Summary של הטסט
with allure.step(f"Test Summary - Passed: {passed}, Failed: {failed}"):
    assert failed == 0, f"Some tests failed. Passed: {passed}, Failed: {failed}"

# הצגת הודעת סיום
elapsed_time = round(time.time() - start_time, 2)
driver.execute_script(f"""
    var message = document.createElement('div');
    message.innerHTML = '✅<strong> השלמנו אירוע!</strong><br><br>⏳ הזמן שלקח לאוטומציה הוא: <strong>{elapsed_time} שניות</strong>';
    message.style.position = 'fixed';
    message.style.top = '100%';
    message.style.left = '100%';
    message.style.transform = 'translate(-100%, -100%)';
    message.style.backgroundColor = '#4CAF50';
    message.style.color = '#fff';
    message.style.padding = '20px';
    message.style.borderRadius = '100px';
    message.style.boxShadow = '0 2px 6px rgba(0,0,0,0.2)';
    message.style.zIndex = '9999';
    message.style.fontSize = '20px';
    message.style.textAlign = 'center';
    document.body.appendChild(message);
    setTimeout(() => message.remove(), 10000);
""")

# מאפשר להציג את ההודעה על סיום גם בסביבת CI
time.sleep(10)