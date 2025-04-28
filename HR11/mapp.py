import pandas as pd

# Список вихідних категорій
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

# Мапінг категорій на ролі, групу та тип
role_map = {
    "javascript":           ("JS FE",          "Development",              "developer"),
    "react":                ("JS FE",          "Development",              "developer"),
    "angular":              ("JS FE",          "Development",              "developer"),
    "vue":                  ("JS FE",          "Development",              "developer"),
    "svelte":               ("JS FE",          "Development",              "developer"),
    "fullstack":            ("Fullstack",      "Development",              "developer"),
    "java":                 ("Java",           "Development",              "developer"),
    "dotnet":               (".NET",           "Development",              "developer"),
    "asp_net":              (".NET",           "Development",              "developer"),
    "blazor":               (".NET",           "Development",              "developer"),
    "maui":                 (".NET",           "Development",              "developer"),
    "winforms":             (".NET",           "Development",              "developer"),
    "wpf":                  (".NET",           "Development",              "developer"),
    "node_js":              ("Node",           "Development",              "developer"),
    "python":               ("Python",         "Development",              "developer"),
    "php":                  ("PHP",            "Development",              "developer"),
    "laravel":              ("PHP",            "Development",              "developer"),
    "magento":              ("PHP",            "Development",              "developer"),
    "symfony":              ("PHP",            "Development",              "developer"),
    "yii":                  ("PHP",            "Development",              "developer"),
    "golang":               ("Go",             "Development",              "developer"),
    "scala":                ("Scala",          "Development",              "developer"),
    "cpp":                  ("C++",            "Development",              "developer"),
    "c":                    ("C",              "Development",              "developer"),
    "embedded":             ("Embedded",       "Development",              "developer"),
    "flutter":              ("Mobile Hybrid",  "Development",              "developer"),
    "react_native":         ("Mobile Native",  "Development",              "developer"),
    "ios":                  ("Mobile Native",  "Development",              "developer"),
    "android":              ("Mobile Native",  "Development",              "developer"),
    "devops":               ("DevOps",         "DevOps & Infrastructure",  "developer"),
    "data_science":         ("Data Scientist", "Data & Analytics",         "developer"),
    "data_analyst":         ("Data Scientist", "Data & Analytics",         "developer"),
    "data_engineer":        ("Data Engineer",  "Data & Analytics",         "developer"),
    "ml_ai":                ("Data Scientist", "Data & Analytics",         "developer"),
    "qa_manual":            ("QA Manual",      "Quality Assurance",        "developer"),
    "qa_automation":        ("AQA",            "Quality Assurance",        "developer"),
    "qa":                   ("QA",             "Quality Assurance",        "developer"),
    "ux_research":          ("UI/UX Designer", "Design",                   "developer"),
    "ui_ux":                ("UI/UX Designer", "Design",                   "developer"),
    "graphic_design":       ("Graphic Designer","Design",                  "developer"),
    "illustrator":          ("Graphic Designer","Design",                  "developer"),
    "motion_design":        ("Motion Designer","Design",                   "developer"),
    "sales":                ("Sales",           "Sales & Marketing",       "back_office"),
    "account_manager":      ("Account manager", "Sales & Marketing",       "back_office"),
    "marketing":            ("Marketing",       "Sales & Marketing",       "back_office"),
    "marketing_analyst":    ("Marketing specialist","Sales & Marketing",  "back_office"),
    "media_buying":         ("Marketing specialist","Sales & Marketing",  "back_office"),
    "affiliate_manager":    ("Marketing specialist","Sales & Marketing",  "back_office"),
    "smm":                  ("SMM",             "Sales & Marketing",       "back_office"),
    "pr_manager":           ("Marketing specialist","Sales & Marketing",  "back_office"),
    "copywriter":           ("Copywriter",      "Sales & Marketing",       "back_office"),
    "content_manager":      ("Copywriter",      "Sales & Marketing",       "back_office"),
    "content_writing":      ("Copywriter",      "Sales & Marketing",       "back_office"),
    "content_marketing":    ("Marketing specialist","Sales & Marketing",  "back_office"),
    "support":              ("Support",         "Sales & Marketing",       "back_office"),
    "hr":                   ("HR",              "Human Resources",         "back_office"),
    "recruiter":            ("Recruiter",       "Human Resources",         "back_office"),
    "finance":              ("Finance",         "Finance & Accounting",    "back_office"),
    "accountant":           ("Accountant",      "Finance & Accounting",    "back_office"),
    "financial_manager":    ("Financial manager","Finance & Accounting",   "back_office"),
    "administrative":       ("Office-manager",  "Administration",          "back_office"),
    "office-manager":       ("Office-manager",  "Administration",          "back_office"),
    "event_manager":        ("Event Manager",   "Operations",              "back_office"),
    "security":             ("Security",        "Operations",              "back_office"),
    "legal":                ("Legal",           "Legal & Compliance",      "back_office"),
    "lawyer":               ("Lawyer",          "Legal & Compliance",      "back_office"),
    "foreign_languages":    ("Foreign Languages","Human Resources",        "back_office"),
    "english_teacher":      ("English Teacher", "Human Resources",         "back_office"),
    "system_administrators":("System Administrators","IT Support",        "back_office"),
    "sysadmin":             ("Sysadmin",        "IT Support",              "back_office"),
    "product_manager":      ("PM",              "Management",              "back_office"),
    "product_owner":        ("PM",              "Management",              "back_office"),
    "project_manager":      ("PM",              "Management",              "back_office"),
    "scrum_master":         ("PM",              "Management",              "back_office"),
    "business_analyst":     ("BA",              "Management",              "back_office"),
    "delivery_manager":     ("PM",              "Management",              "back_office"),
    "engineering_manager":  ("PM",              "Management",              "back_office"),
    "cto":                  ("CTO",             "Executive",               "back_office"),
    "cmo":                  ("CMO",             "Executive",               "back_office"),
    "cfo":                  ("CFO",             "Executive",               "back_office"),
    "coo":                  ("COO",             "Executive",               "back_office"),
    "ceo":                  ("CEO",             "Executive",               "back_office"),
    "cco":                  ("CCO",             "Executive",               "back_office"),
    "cio":                  ("CIO",             "Executive",               "back_office"),
    "cpo":                  ("CPO",             "Executive",               "back_office"),
    "cbdo":                 ("CBDO",            "Executive",               "back_office"),
    "head_chief":           ("Head Chief",      "Executive",               "back_office"),
    "lead":                 ("Lead",            "Management",              "back_office")
}

# Формуємо DataFrame
mapping = []
for cat in categories:
    role, group, typ = role_map.get(cat, ("Unknown", "Other", "back_office"))
    mapping.append({
        "category": cat,
        "role": role,
        "group": group,
        "type": typ
    })

df = pd.DataFrame(mapping)

# Зберігаємо у Excel
output_file = "category_role_mapping.xlsx"
df.to_excel(output_file, index=False)

print(f"Мапінг категорій збережено в {output_file}")