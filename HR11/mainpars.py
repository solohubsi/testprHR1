import os
import sys
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook, load_workbook
from tqdm import tqdm

# Шлях до Excel
excel_path = "djinni_structured_tqdm.xlsx"
today = date.today().isoformat()

# 1) Перевірка дублювання: якщо в останньому рядку вже today's date — вихід
if os.path.exists(excel_path):
    wb_check = load_workbook(excel_path, read_only=True)
    ws_check = wb_check.active
    last_date = ws_check.cell(row=ws_check.max_row, column=8).value
    wb_check.close()
    if last_date == today:
        print(f"✅ Дані за {today} уже збережені — завершуємо.")
        sys.exit(0)

# 2) Якщо файлу нема — створюємо з шапкою
if not os.path.exists(excel_path):
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
        "vacancies",
        "scrape_date"
    ])
    wb.save(excel_path)

# 3) Відкриваємо Excel для дозапису
wb = load_workbook(excel_path)
ws = wb.active

# 4) Налаштування Selenium (Chromium у Actions, локально теж)
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

# 5) Задаємо рівні досвіду
experiences = [0, 1, 2, 3, 5]
exp_mapping = {
    0: ("<1 року", "junior"),
    1: ("1-2 роки", "middle"),
    2: ("2-3 роки", "middle"),
    3: ("3-5 років", "senior"),
    5: ("5+ років", "senior"),
}

# 6) Повний список категорій
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

# 7) Основний цикл із прогресбаром
total = len(categories) * len(experiences)
pbar = tqdm(total=total, desc="Парсинг Djinni")

for category in categories:
    for exp in experiences:
        url = f"https://djinni.co/salaries/?category={category}&exp={exp}"
        driver.get(url)

        # парсимо мінімальну зарплату
        try:
            el_min = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="candidates_salaries"]/div/div[2]/span[1]')
                )
            )
            min_salary = int(el_min.text.strip().replace(" ", "").replace(",", ""))
        except:
            min_salary = None

        # парсимо максимальну зарплату
        try:
            el_max = driver.find_element(
                By.XPATH, '//*[@id="candidates_salaries"]/div/div[2]/span[2]'
            )
            max_salary = int(el_max.text.strip().replace(" ", "").replace(",", ""))
        except:
            max_salary = None

        # кількість кандидатів
        try:
            el_c = driver.find_element(
                By.XPATH, '//*[@id="candidates_card"]/div[2]/span[1]'
            )
            candidates = int(el_c.text.strip().replace(" ", "").replace(",", ""))
        except:
            candidates = None

        # кількість вакансій
        try:
            el_v = driver.find_element(
                By.XPATH, '//*[@id="jobs_card"]/div[2]/span[1]'
            )
            vacancies = int(el_v.text.strip().replace(" ", "").replace(",", ""))
        except:
            vacancies = None

        label, level = exp_mapping[exp]

        # тільки якщо є хоч одна цифра зарплати — дозапис
        if min_salary is not None or max_salary is not None:
            ws.append([
                category,
                min_salary,
                max_salary,
                label,
                level,
                candidates,
                vacancies,
                today
            ])
            wb.save(excel_path)

        pbar.update(1)

# 8) Завершуємо
driver.quit()
pbar.close()
print(f"✅ Файл оновлено: {excel_path}")