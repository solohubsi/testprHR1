from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openpyxl
from openpyxl import Workbook
import os
from tqdm import tqdm

# Шлях до Excel
excel_path = "djinni_structured_tqdm.xlsx"

# Рівні досвіду та їх відображення
experiences = [0, 1, 2, 3, 5]
exp_mapping = {
    0: ("<1 року", "junior"),
    1: ("1-2 роки", "middle"),
    2: ("2-3 роки", "middle"),
    3: ("3-5 років", "senior"),
    5: ("5+ років", "senior")
}

# Категорії для парсингу
categories = [
    "javascript", "fullstack", "java", "dotnet", "python", "php", "node_js", "ios", "android", "react_native",
    "cplusplus", "flutter", "golang", "ruby", "scala", "salesforce", "rust", "elixir", "kotlin", "erp_systems",
    "nocode", "qa_manual", "qa_automation", "qa", "design", "2d_animation", "2d_artist", "3d_animation", "3d_artist",
    "gamedev", "game_design", "game_developer", "illustrator", "graphic_design", "motion_design", "ux_research",
    "ui_ux", "product_design", "content_design", "winforms", "wpf", "xamarin", "dotnet_web", "dotnet_mobile",
    "dotnet_cloud", "dotnet_desktop", "asp_net", "blazor", "maui", "unreal", "unity", "cpp", "c", "embedded",
    "security", "security_analyst", "information_security", "penetration_tester", "sysadmin", "sql_dba", "drupal",
    "wordpress", "yii", "laravel", "magento", "symfony", "odoo", "sap", "ms_dynamics", "vue", "svelte", "react",
    "angular", "marketing", "marketing_analyst", "digital_marketing", "digital_marketing_manager", "media_buying",
    "affiliate_manager", "seo", "ppc", "social_media", "pr_manager", "sales", "lead_generation", "support",
    "hr", "recruiter", "content_manager", "content_writing", "content_marketing", "product_manager",
    "product_owner", "project_manager", "scrum_master", "engineering_manager", "delivery_manager",
    "business_analyst", "data_analyst", "data_engineer", "data_science", "ml_ai", "cto", "cpo", "cmo", "ceo", "coo",
    "cio", "cfo", "cco", "cbdo", "head_chief", "lead"
]

def create_excel(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Salaries"
    ws.append([
        "category",
        "salary_min",
        "salary_max",
        "experience_label",
        "level",
        "candidates",
        "vacancies"
    ])
    wb.save(path)

# Якщо файл не існує — створюємо з заголовками
if not os.path.exists(excel_path):
    create_excel(excel_path)

# Завантажуємо Excel
wb = openpyxl.load_workbook(excel_path)
ws = wb["Salaries"]

# Налаштування headless Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

# Прогресбар
total = len(categories) * len(experiences)
pbar = tqdm(total=total, desc="Парсинг Djinni", ncols=100)

for category in categories:
    for exp in experiences:
        url = f"https://djinni.co/salaries/?category={category}&exp={exp}"
        driver.get(url)

        min_salary = max_salary = candidates = vacancies = None

        # Парсимо мін/макс зарплату
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="candidates_salaries"]/div/div[2]')
                )
            )
            try:
                el = driver.find_element(
                    By.XPATH,
                    '//*[@id="candidates_salaries"]/div/div[2]/span[1]'
                )
                min_salary = int(el.text.strip().replace(" ", "").replace(",", ""))
            except:
                pass
            try:
                el = driver.find_element(
                    By.XPATH,
                    '//*[@id="candidates_salaries"]/div/div[2]/span[2]'
                )
                max_salary = int(el.text.strip().replace(" ", "").replace(",", ""))
            except:
                pass
        except:
            pass

        # Парсимо кількість кандидатів
        try:
            el = driver.find_element(
                By.XPATH,
                '//*[@id="candidates_card"]/div[2]/span[1]'
            )
            txt = el.text.strip().replace(" ", "").replace(",", "")
            candidates = int(txt) if txt.isdigit() else None
        except:
            pass

        # Парсимо кількість вакансій
        try:
            el = driver.find_element(
                By.XPATH,
                '//*[@id="jobs_card"]/div[2]/span[1]'
            )
            txt = el.text.strip().replace(" ", "").replace(",", "")
            vacancies = int(txt) if txt.isdigit() else None
        except:
            pass

        experience_label, level = exp_mapping.get(exp, (f"{exp} років", "unknown"))

        # Виводимо в консоль
        print(f"{category} | {experience_label} ({level}) → "
              f"salary_min={min_salary}, salary_max={max_salary}, "
              f"candidates={candidates}, vacancies={vacancies}")

        # Якщо немає даних по зарплаті — пропускаємо запис
        if min_salary is None and max_salary is None:
            pbar.update(1)
            continue

        # Додаємо рядок до Excel
        ws.append([
            category,
            min_salary,
            max_salary,
            experience_label,
            level,
            candidates,
            vacancies
        ])

        # Зберігаємо одразу після кожного додавання
        wb.save(excel_path)

        pbar.update(1)

pbar.close()

# Закриваємо браузер
driver.quit()
print("✅ Структурований файл із прогресбаром створено.")