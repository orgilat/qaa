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
    options.add_argument("--headless=new")  # מצב ללא GUI בצורה יציבה יותר
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # בדיקה אם chromedriver קיים במערכת
    driver_path = shutil.which("chromedriver")
    if not driver_path:
        raise RuntimeError("chromedriver לא נמצא במערכת או ב־PATH")

    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()




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
    passed = 0
    failed = 0

    # רשימת הכפתורים במסך ניהול סוציומטרי
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
            WebDriverWait(driver, 20).until(EC.alert_is_present())  # מחכה שה-Alert יופיע
            alert = Alert(driver)
            alert.accept()  # קבלת ה-alert ולחיצה על "OK"
            allure.attach("חלון Alert נסגר בהצלחה", name="Alert", attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            allure.attach(f"הודעת Alert לא נמצאה או שגיאה אחרת: {e}", name="Alert Info", attachment_type=allure.attachment_type.TEXT)

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

            # במקום time.sleep(0.5), השתמש ב-WebDriverWait כאן אם הכפתור כבר מוצג
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, buttons[1]["xpath"])))

            close_alert_if_present()
            soc_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, buttons[1]["xpath"]))
            )
            soc_button.click()

            # חכה להופעת כתובת האתר החדשה אחרי הלחיצה או אלמנט אחר שזמין רק אחרי הלחיצה
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[contains(@value, 'סוציומטרי')]")))

            allure.attach(driver.current_url, name="כתובת האתר לאחר המעבר", attachment_type=allure.attachment_type.TEXT)

    except Exception as e:
        allure.attach(f"שגיאה במהלך הבדיקה: {e}", name="Error Info", attachment_type=allure.attachment_type.TEXT)



        # מעבר על שאר הכפתורים במסך ניהול סוציומטרי
        for button in buttons[2:22]:
            
            if button["name"] == "שאלות חובה":
             with allure.step("בדיקות פנימיות עבור 'שאלות חובה'"):
                close_alert_if_present()
                try:
                  questions_btn = WebDriverWait(driver, 100).until(
                    EC.element_to_be_clickable((By.XPATH, button["xpath"]))
                )
                  questions_btn.click()
                except TimeoutException as e:
                # במקרה של TimeoutException, אנחנו שומרים את הודעת השגיאה
                 allure.attach(driver.get_screenshot_as_png(), name="❌ צילום שגיאה", attachment_type=allure.attachment_type.PNG)
                 allure.attach(f"<b style='color:red;'>❌ שגיאה בלחיצה על '{button['name']}':</b><br><pre>{e}</pre>", 
                              name="שגיאה", attachment_type=allure.attachment_type.HTML)
                 failed += 1
                 continue  # נמשיך לכפתור הבאהכפתור, נעבור לשלב הבא

             with allure.step("לחיצה על 'ערוך' וחזרה"):
                edit_btn = WebDriverWait(driver, 100).until(
                  EC.element_to_be_clickable((By.XPATH, "//input[contains(@value, 'ערוך')]"))
            )
                edit_btn.click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                driver.back()

                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button["xpath"])))  # חזרה למסך שאלות חובה
                driver.back()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, buttons[2]["xpath"])))  # חזרה לניהול סוציומטרי
                passed += 1
            elif button["name"] == "חוקים על שאלות":
               with allure.step("בדיקות פנימיות עבור 'חוקים על שאלות'"):
                  try:
                    with allure.step("כניסה למסך 'חוקים על שאלות'"):
                     element = WebDriverWait(driver, 100).until(
                     EC.element_to_be_clickable((By.XPATH, button["xpath"]))
                )
                     element.click()

                    with allure.step("הקלדה בתיבת החיפוש בתוך 'חוקים על שאלות'"):
                     search_input = WebDriverWait(driver, 100).until(
                     EC.visibility_of_element_located((By.ID, "dt-search-0"))
                )
                     search_input.clear()
                     search_input.send_keys("שי אגיב שי אגיב")
                     passed += 1

                    with allure.step("לחיצה על 'שאלון סוציומטרי' בתוך 'חוקים על שאלות'"):
                     combo = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "svg.ss-arrow"))
                )
                    combo.click()
                    passed += 1

                    driver.back()
                    WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, button["xpath"]))
                )  # חזרה אחורה

                  except TimeoutException as e:
                        failed += 1
                        allure.attach(driver.get_screenshot_as_png(), name="❌ חוקים על שאלות - שגיאה", attachment_type=allure.attachment_type.PNG)
                        allure.attach(f"<b style='color:red;'>שגיאה בחוקים על שאלות:</b><br><pre>{e}</pre>",
                          name="שגיאה", attachment_type=allure.attachment_type.HTML)

                    
            elif button["name"] == "כללי השתתפות לפי סוג יחידה":
             with allure.step("בדיקות פנימיות עבור 'כללי השתתפות לפי סוג יחידה'"):
              close_alert_if_present()

              try:
            # המרה ל-presence_of_element_located במידה וצריך רק לוודא שהאלמנט קיים
                unit_participation_btn = WebDriverWait(driver, 100).until(
                  EC.presence_of_element_located((By.XPATH, button["xpath"]))
            )
            
                driver.execute_script("arguments[0].scrollIntoView();", unit_participation_btn)
                unit_participation_btn.click()
            
              except TimeoutException as e:
               allure.attach(driver.get_screenshot_as_png(), name="❌ צילום שגיאה", attachment_type=allure.attachment_type.PNG)
               allure.attach(f"<b style='color:red;'>❌ שגיאה בלחיצה על '{button['name']}':</b><br><pre>{e}</pre>",
                          name="שגיאה", attachment_type=allure.attachment_type.HTML)
               failed += 1  # במקום continue, פשוט נעדכן את המשתנה failed

        # המתנה אחרי החזרה לדף
              try:
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, button["xpath"]))
            )
                passed += 1  # נעדכן את מספר ההצלחה אחרי אם הכל עבר בהצלחה

              except TimeoutException as e:
               allure.attach(f"שגיאה בחזרה לדף אחרי לחיצה על {button['name']}", name="שגיאה ב-back", attachment_type=allure.attachment_type.HTML)
               failed += 1

            elif button["name"] == "אופציות לסוציומטרי":
                try:
                  with allure.step("בדיקות פנימיות עבור 'אופציות לסוציומטרי'"):
            # מוודא שהכפתור קיים וניתן ללחיצה
                   options_button = WebDriverWait(driver, 30).until(
                     EC.element_to_be_clickable((By.XPATH, button["xpath"]))
            )
                  driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", options_button)
                  time.sleep(1)  # המתנה קטנה כדי לוודא שה-scroll הסתיים
                  options_button.click()

            # מוודא שהדף נטען מחדש אחרי הלחיצה
                  WebDriverWait(driver, 10).until(
                   EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

                  with allure.step("לחיצה על 'שמור' וחזרה"):
                   save_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[contains(@value, 'שמור')]"))
            )
                  driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
                  time.sleep(1)
                  save_button.click()

            # ווידוא שהפעולה הושלמה
                  WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

                except TimeoutException as e:
                 allure.attach(driver.page_source, name="שגיאה באופציות סוציומטרי", attachment_type=allure.attachment_type.HTML)
                 pytest.fail("הכפתור 'אופציות לסוציומטרי' או 'שמור' לא נמצא/לא היה לחיץ בזמן")

    # הודעת ויזואלית מדליקה – לא נוגע 😎
                driver.execute_script("""
        var message = document.createElement('div');
        message.innerText = '✅ לחצתי על שמור!';
        message.style.position = 'fixed';
        message.style.top = '20px';
        message.style.right = '20px';
        message.style.backgroundColor = 'green';
        message.style.color = 'white';
        message.style.padding = '100px';
        message.style.borderRadius = '5px';
        message.style.zIndex = '9999';
        message.style.fontSize = '20px';
        document.body.appendChild(message);
        setTimeout(function(){ message.remove(); }, 3000); // ההודעה תיעלם אחרי 3 שניות
    """)

    # חזרה אחורה וממתין שנטען שוב דף קודם
                driver.back()
                WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//input[contains(@value, 'שמור')]"))  # או כל אלמנט שמבטיח שהדף הקודם נטען
    )

                passed += 1
                driver.back()
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, button["xpath"]))  # דואג שהחזרה הושלמה
)

                        
            else:
                  with allure.step(f"📌 בדיקת כפתור: '{button['name']}'"):
                    try:
                       start_time = time.time()

                       element = WebDriverWait(driver, 100).until(
                       EC.element_to_be_clickable((By.XPATH, button["xpath"]))
            )
                       driver.execute_script("arguments[0].scrollIntoView(true);", element)
                       allure.attach(driver.get_screenshot_as_png(), name="📸 לפני לחיצה", attachment_type=allure.attachment_type.PNG)

                       element.click()
                       time.sleep(0.5)

                       allure.attach(driver.get_screenshot_as_png(), name="📸 אחרי לחיצה", attachment_type=allure.attachment_type.PNG)
                       allure.attach(driver.current_url, name="🌐 כתובת נוכחית", attachment_type=allure.attachment_type.TEXT)

                       duration = round(time.time() - start_time, 2)
                       allure.attach(f"⏱️ משך הפעולה: {duration} שניות", name="משך פעולה", attachment_type=allure.attachment_type.TEXT)

                       allure.attach(f"<b style='color:green;'>✔️ לחיצה על '{button['name']}' הצליחה!</b>", name="סטטוס", attachment_type=allure.attachment_type.HTML)
                       passed += 1
                       driver.back()
                       time.sleep(0.5)

                    except Exception as e:
                     allure.attach(driver.get_screenshot_as_png(), name="❌ צילום שגיאה", attachment_type=allure.attachment_type.PNG)
                     allure.attach(f"<b style='color:red;'>❌ שגיאה בלחיצה על '{button['name']}':</b><br><pre>{e}</pre>",
                          name="שגיאה", attachment_type=allure.attachment_type.HTML)
                     failed += 1               
  
    finally:
        time.sleep(3.5)
        driver.execute_script("new Audio('https://www.soundjay.com/button/beep-07.wav').play();")
        driver.execute_script("""
                              var message = document.createElement('div');
                              message.innerText = 'סיימנו את השלב הראשון- כעת נעבור לשלב השני!';
                              message.style.position = 'fixed';
         message.style.top = '120px';
        message.style.right = '120px';
        message.style.backgroundColor = 'green';
        message.style.color = 'white';
        message.style.padding = '40px';
        message.style.borderRadius = '100px';
        message.style.zIndex = '9999';
        message.style.fontSize = '20px';
        document.body.appendChild(message);
        setTimeout(function(){ message.remove(); }, 100000); // ההודעה תיעלם אחרי 3 שניות
    """) 
        time.sleep(3.5)  
      
    for button in buttons[23:]:
      if button["name"] == "ניהול אירועים":
        with allure.step("בדיקות פנימיות עבור 'ניהול אירועים'"):
            close_alert_if_present()
            events_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, button["xpath"]))
            )
            events_button.click()
            time.sleep(0.5)
            passed += 1
        with allure.step("לחיצה על 'להקמת אירוע חדש'"):
            # שים לב: השתמשנו בשם "add_event_button" באופן עקבי
            add_event_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.//span[contains(@class, 'block')])='להקמת אירוע חדש']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", add_event_button)
            time.sleep(1)
            add_event_button.click()
            time.sleep(25)
            passed += 1
        with allure.step("מילוי שם האירוע ב-'מאי הגיי'"):
            # המתן עד שהשדה "שם האירוע" יהיה זמין (המסך החדש נטען)
            event_name_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='field floating-label' and @label='שם האירוע']//input"))
            )
            # עכשיו המלא את השדה עם הטקסט "אירוע לדוגמה"
            event_name_input.send_keys("אירוע לדוגמה ")
            time.sleep(5.5)  # הוספת זמן המתנה לוודא שהטקסט נכתב
            passed += 1

        with allure.step("בחירת עונת הערכה"):
            # המתן עד שהכפתור של Dropdown יהיה לחיץ
            dropdown_button = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown dropdown-select' and @label='בחר עונת הערכה']//div[contains(@class, 'dropdown-btn')]"))
            )
            dropdown_button.click()
            time.sleep(3)  # המתן להופעת רשימת הבחירה
           

            # בחר באפשרות "עונת 1"
            season_option = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='dropdown-list']//li//div[@class='list-item']/span[text()='עונת 1']"))
            )
            season_option.click()
            passed += 1
            time.sleep(3)
          

        with allure.step("בחירת תאריך 18"):
    # המתן עד שכפתור לוח השנה יהיה לחיץ
          calendar_button = WebDriverWait(driver, 100).until(
          EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'dx-dropdowneditor-button') and @aria-label='Select']"))
    )
          calendar_button.click()
          passed += 1
          time.sleep(1)  # המתן להופעת לוח השנה

    # לחץ על התאריך 18
          date_18 = WebDriverWait(driver, 100).until(
          EC.element_to_be_clickable((By.XPATH, "//td[contains(@class, 'dx-calendar-cell') and not(contains(@class, 'dx-calendar-other-view'))]//span[text()='18']"))
    )
          date_18.click()
          passed += 1
          time.sleep(2)
        

        with allure.step("בחירת תאריך 26 בתאריך סיום"):
    # המתן עד שכפתור פתיחת לוח השנה יהיה לחיץ – שימו לב למבנה הקלסים
         calendar_button = WebDriverWait(driver, 100).until(  # הגדלתי את זמן ההמתנה
         EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class, 'dx-datebox') and .//span[contains(., 'תאריך סיום')]]//div[contains(@class, 'dx-dropdowneditor-button') and @aria-label='Select']")
        )
    )
         calendar_button.click()
         passed += 1

    # המתן עד שהכפתור עם הערך "2" יהיה לחיץ ולחץ עליו
        date_input = WebDriverWait(driver, 100).until(
         EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'dx-datebox') and .//span[contains(., 'תאריך סיום')]]//input[@type='text']"))
    )
        date_input.send_keys("18-03-2025" + Keys.ENTER)
        passed += 1
        time.sleep(6)  # ש
   

    with allure.step("בחירת סוג היחידה לאירוע - בחירת 'מטה'"):
    # המתן עד שכפתור ה-dropdown יהיה לחיץ בתוך התיבה עם התווית "הגדרת סוג היחידה לאירוע"
     unit_dropdown_button = WebDriverWait(driver, 100).until(  # הגדלתי את זמן ההמתנה
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='dropdown dropdown-select' and @label='הגדרת סוג היחידה לאירוע ']/div[contains(@class, 'dropdown-btn')]")
        )
    )
     unit_dropdown_button.click()

    # המתן עד להופעת רשימת הבחירה ובחר באפשרות "מטה"
     unit_option_mathe = WebDriverWait(driver, 100).until(  # הגדלתי את זמן ההמתנה
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@class='dropdown-list']//li//div[contains(@class, 'list-item')]//span[normalize-space(text())='מטה']")
        )
    )
     unit_option_mathe.click()
     passed += 2
     time.sleep(3)




     
  
     with allure.step("לחיצה פנימית על הריבוע ליד 'פיקוד 2'"):
      checkbox_pikud2 = WebDriverWait(driver, 100).until(  # הגדלתי את זמן ההמתנה
        EC.element_to_be_clickable(
            (By.XPATH, "//li[@data-item-id='249']//div[contains(@class, 'dx-checkbox-container')]")
        )
    )
     checkbox_pikud2.click()
     passed += 1
    time.sleep(11)






    with allure.step("Selecting the checkbox for 'אוגדה 1' under 'Selecting units to display fill report'"):
    # Locate the section header first
      section_header = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[normalize-space()='בחירת יחידות מאגדות להצגת דוח מילוי']")
        )
    )
    # Then, locate the first <li> with aria-label 'אוגדה 1' (and level 2) following the header,
    # and within it, find its checkbox element (the square to the right).
      checkbox = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[normalize-space()='בחירת יחידות מאגדות להצגת דוח מילוי']"
            "/following::li[@aria-label='אוגדה 1' and @aria-level='2'][1]"
            "//div[contains(@class, 'dx-checkbox')]"
        ))
    )
    checkbox.click()
    passed += 1
    time.sleep(1.2)





    with allure.step("Scrolling to the bottom of the page"):
    # Scroll to the bottom of the page using JavaScript
     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
     time.sleep(1.1)  # Brief pause to allow any lazy-loaded elements to appear

    with allure.step("Selecting 'Originality and Innovation' and 'Planning Ability' checkboxes via label click"):
    # Click on the label for "Originality and Innovation" to select its checkbox
     label_originality = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='מקוריות וחדשנות']"))
    )
     label_originality.click()
     passed += 1
     time.sleep(5)

    # Click on the label for "Planning Ability" to select its checkbox
    label_planning = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='יכולת תכנון']"))
    )
    label_planning.click()
    passed += 1
    time.sleep(1.2)

    with allure.step("Scrolling to the top of the page"):
    # Scroll to the top using JavaScript
     driver.execute_script("window.scrollTo(0, 0);")
     time.sleep(2.2)  # Pause to allow any page adjustments

    with allure.step("Clicking on the 'ניהול פוטנציאל' (Manage Potential) tab"):
     manage_potential_tab = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[.//div[contains(@class, 'q-tab__label') and normalize-space(text())='ניהול פוטנציאל']]")
        )
    )
     manage_potential_tab.click()
     passed += 1

    with allure.step("Clicking on the 'הצג פוטנציאל' button using JavaScript"):
    # Locate the button using its text
      button_recalculate = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'חשב פוטנציאל מחדש')]"))
    )
    button_recalculate.click()
    
    # המתן להיעלמות הלודר או להופעת תוצאה חדשה
    WebDriverWait(driver, 100).until_not(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".q-loading"))
    )

    with allure.step("Clicking on the 'הצג פוטנציאל' button using JavaScript"):
    # Locate the button using its text
     button_show = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'הצג פוטנציאל')]"))
    )
     button_show.click()

    # המתן להופעת טבלת התוצאות או רכיב מייצג אחר
     WebDriverWait(driver, 100).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'dx-datagrid-rowsview')]//table")
        )
    )


    with allure.step("Click leftmost dropdown button"):
    # Find all dropdown buttons
     dropdown_buttons = WebDriverWait(driver, 100).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='dx-widget dx-button-mode-contained dx-button-normal dx-rtl dx-dropdowneditor-button']")
        )
    )
    
    # Sort buttons by x-location (leftmost first)
     leftmost_button = sorted(dropdown_buttons, key=lambda el: el.location['x'])[0]

    # Click the leftmost button
     leftmost_button.click()
     option_no = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//div[@role='option' and .//div[text()='לא']]")
        )
    )
     option_no.click()
     time.sleep(0.5)



    with allure.step("Loop through empty checkboxes and process them"):
     for _ in range(100):  # ננסה עד 100 מחזורים
        # מציאת כל הצ'קבוקסים הריקים
        checkboxes = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//td[@role='gridcell']//div[@role='checkbox' and @aria-checked='false']")
            )
        )
        for checkbox in checkboxes:
            try:
                # גלילה לצ'קבוקס כדי לוודא שהוא נגיש
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                time.sleep(0.3)

                with allure.step("Click empty checkbox"):
                    checkbox.click()
                    time.sleep(0.3)  # זמן קצר יותר כי המערכת מגיבה מהר בלחיצה

                with allure.step("Click the dropdown button"):
                 WebDriverWait(driver, 10).until_not(
                  EC.presence_of_element_located((
                    By.XPATH,
            "//div[contains(@class, 'dx-overlay-wrapper') and contains(@class, 'dx-loadpanel-wrapper')]"
        ))
    )

    # רק אחרי שהשכבה נעלמה - לחץ על ה-dropdown
                dropdown_button = WebDriverWait(driver, 100).until(
                  EC.element_to_be_clickable(
                    (By.XPATH, "//div[@class='dropdown-btn text-box valid populated']")
        )
    )
                dropdown_button.click()
                time.sleep(0.2)  # זמן קצר יותר לפתיחת ה-dropdown


                with allure.step("Select 'המוערך נוסף על פי בקשתו' option"):
                 option_to_select = WebDriverWait(driver, 100).until(
                  EC.element_to_be_clickable(
                   (By.XPATH, "//div[@class='list-item']/span[text()='המוערך נוסף על פי בקשתו']")
        )
    )
                option_to_select.click()
                time.sleep(0.3)
                passed += 1  # המתנה קצרה להשלמת הפעולה

                # גלילה קטנה למטה כדי לחשוף את הצ'קבוקס הבא
                driver.execute_script("window.scrollBy(0, 100);")
                time.sleep(0.5)  # זמן מינימלי כדי לאפשר סנכרון

            except Exception as e:
                print(f"⚠️ Error processing checkbox: {e}")
                continue

        # רענון הרשימה אחרי כל מחזור
        time.sleep(1)



    with allure.step("Clicking on 'close' button if available"):
     close_button = WebDriverWait(driver, 22).until(
        EC.element_to_be_clickable((By.XPATH, "//i[contains(@class, 'material-icons') and normalize-space()='close']"))
    )
     close_button.click()
     passed += 1
     time.sleep(2)  # השהיה קצרה אחרי הלחיצה



    with allure.step("Clicking on the 'מודל הערכה' (Evaluation Model) tab"):
     manage_potential_tab1 = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[.//div[contains(@class, 'q-tab__label') and normalize-space(text())='מודל הערכה']]")
        )
    )
     manage_potential_tab1.click()
     passed += 1
    time.sleep(0.3)  # השהיה קצרה אחרי הלחיצה


    with allure.step("Clicking on the 'בחר מודל הערכה חדש' (Select New Evaluation Model) button"):
     select_model_button = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[normalize-space(text())='בחר מודל הערכה חדש']]")
        )
    )
     select_model_button.click()
     passed += 1
      # השהיה קצרה אחרי הלחיצה
 # השהיה קצרה אחרי הלחיצה


    with allure.step(f"Test Summary - Passed: {passed}, Failed: {failed}"):
     assert failed == 0, f"Some tests failed. Passed: {passed}, Failed: {failed}"

    elapsed_time = round(time.time() - start_time, 2)  # חישוב זמן סופי
    driver.execute_script(f"""
    var message = document.createElement('div');
    message.innerHTML = '✅<strong> השלמנו אירוע!</strong><br><br>⏳ הזמן שלקח לאוטומציה הוא: <strong>{elapsed_time} שניות</strong>';
    message.style.position = 'fixed';
    message.style.top = '100%';
    message.style.left = '100%';
    message.style.transform = 'translate(-100%, -100%)';
    message.style.backgroundColor = '#4CAF100';
    message.style.color = '#fff';
    message.style.padding = '20px';
    message.style.borderRadius = '100px';
    message.style.boxShadow = '0 2px 6px rgba(0,0,0,0.2)';
    message.style.zIndex = '9999';
    message.style.fontSize = '20px';
    message.style.textAlign = 'center';
    document.body.appendChild(message);

    // מחיקה אחרי 100 שניות
    setTimeout(() => message.remove(), 100000);
""")

# השהיה לסיום התהליך
time.sleep(8)


# להרצה דרך CMD:
# cd C:\Users\User\Documents\sell
# pytest --alluredir=allure-results
# allure serve allured-results
