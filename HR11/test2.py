from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Тестові категорії та досвід
test_categories = ["python", "java"]
test_experiences = [0, 5]

# Мапа досвіду (для виводу)
exp_mapping = {
    0: ("<1 року", "junior"),
    5: ("5+ років", "senior")
}

# Налаштування Selenium (headless)
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(options=options)

for category in test_categories:
    for exp in test_experiences:
        url = f"https://djinni.co/salaries/?category={category}&exp={exp}"
        driver.get(url)

        # Ініціалізуємо змінні
        min_salary = max_salary = candidates = vacancies = None

        # Парсимо зарплати через жорсткі XPATH
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="candidates_salaries"]/div/div[2]'))
            )
            try:
                el = driver.find_element(By.XPATH,
                    '//*[@id="candidates_salaries"]/div/div[2]/span[1]')
                min_salary = int(el.text.strip().replace(" ", "").replace(",", ""))
            except:
                pass
            try:
                el = driver.find_element(By.XPATH,
                    '//*[@id="candidates_salaries"]/div/div[2]/span[2]')
                max_salary = int(el.text.strip().replace(" ", "").replace(",", ""))
            except:
                pass
        except:
            pass

        # Парсимо кандидатів
        try:
            el = driver.find_element(By.XPATH,
                '//*[@id="candidates_card"]/div[2]/span[1]')
            text = el.text.strip().replace(" ", "").replace(",", "")
            candidates = int(text) if text.isdigit() else None
        except:
            pass

        # Парсимо вакансії
        try:
            el = driver.find_element(By.XPATH,
                '//*[@id="jobs_card"]/div[2]/span[1]')
            text = el.text.strip().replace(" ", "").replace(",", "")
            vacancies = int(text) if text.isdigit() else None
        except:
            pass

        label, level = exp_mapping[exp]
        print(f"{category} | {label} ({level}) → "
              f"salary_min={min_salary}, salary_max={max_salary}, "
              f"candidates={candidates}, vacancies={vacancies}")

driver.quit()