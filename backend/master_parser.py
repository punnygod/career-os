import re
import os
import json

# Paths
DOWNLOADS = "/Users/siddheshchavan/Downloads"
FRONTEND_MD = os.path.join(DOWNLOADS, "You are a senior frontend engineering educator.__G.md")
BACKEND_MD = os.path.join(DOWNLOADS, "backend_assessment_qbank.md")
FULLSTACK_MD = os.path.join(DOWNLOADS, "fullstack_qa_bank.md")
DEVOPS_MD = os.path.join(DOWNLOADS, "devops_qa_bank.md")
BEHAVIORAL_JSON = os.path.join(DOWNLOADS, "engineering_maturity_qbank.json")

SEED_PATH = "/Users/siddheshchavan/Temp/backend/seeds/questions_seed.py"

def clean_val(val):
    # Remove escaping from pipes
    val = val.replace("\\|", "|")
    return val.strip()

def parse_md_table(path, role_id_override=None, is_behavioral=0):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return []
        
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    questions = []
    start_table = False
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if "| role_id |" in line or "| dimension |" in line:
            start_table = True
            continue
        if start_table and (line.startswith("|---") or line.startswith("|:---")):
            continue
        if start_table and line.startswith("|"):
            # Clean and split
            temp_line = line.strip()
            if temp_line.startswith("|"): temp_line = temp_line[1:]
            if temp_line.endswith("|"): temp_line = temp_line[:-1]
            
            cells = [clean_val(c) for c in re.split(r'(?<!\\)\|', temp_line)]
            if len(cells) < 6: continue 
            
            try:
                # Standard format: role_id | dimension | text | order | options | stack | cert | min | max | weight
                if len(cells) >= 10:
                    q = {
                        "role_id": int(cells[0].strip()) if cells[0].strip().isdigit() else (role_id_override if role_id_override else 1),
                        "dimension": cells[1].strip(),
                        "question_text": cells[2].strip(),
                        "question_order": int(cells[3].strip()) if cells[3].strip().isdigit() else 0,
                        "answer_options": cells[4].strip(),
                        "stack_name": cells[5].strip() if cells[5].strip() else None,
                        "certificate_name": cells[6].strip() if cells[6].strip() else None,
                        "experience_min": float(cells[7].strip()) if cells[7].strip() else 0.0,
                        "experience_max": float(cells[8].strip()) if cells[8].strip() else 15.0,
                        "weight": float(cells[9].strip()) if cells[9].strip() else 1.0,
                        "is_behavioral": is_behavioral
                    }
                elif len(cells) >= 6:
                    # Smaller format
                    q = {
                        "role_id": role_id_override if role_id_override else 1,
                        "dimension": cells[0].strip(),
                        "question_text": cells[1].strip(),
                        "question_order": 0,
                        "answer_options": cells[2].strip(),
                        "stack_name": cells[3].strip() if cells[3].strip() else None,
                        "certificate_name": None,
                        "experience_min": float(cells[4].strip()) if cells[4].strip().replace('.','',1).isdigit() else 0.0,
                        "experience_max": 15.0,
                        "weight": float(cells[5].strip()) if cells[5].strip().replace('.','',1).isdigit() else 1.0,
                        "is_behavioral": is_behavioral
                    }
                else:
                    continue
                questions.append(q)
            except Exception as e:
                # print(f"Error: {e}")
                continue
        elif start_table:
            # Table ended if we encounter a non-pipe line after starting
            if line and not line.startswith("|"):
                # We might have multiple tables in a file, don't break yet?
                # For our files, they are mostly 1 big table.
                pass
            
    return questions

def parse_behavioral():
    if not os.path.exists(BEHAVIORAL_JSON): return []
    with open(BEHAVIORAL_JSON, 'r') as f:
        data = json.load(f)
    results = []
    for item in data:
        results.append({
            "role_id": 0, # HIDDEN CORE ROLE
            "dimension": item["dimension"],
            "question_text": item["question_text"],
            "question_order": 0,
            "answer_options": item["answer_options"],
            "stack_name": None,
            "certificate_name": None,
            "experience_min": float(item.get("experience_min", 0)),
            "experience_max": float(item.get("experience_max", 15)),
            "weight": float(item.get("weight", 1.0)),
            "is_behavioral": 1
        })
    return results

print("Starting master parsing...")
all_questions = []
all_questions.extend(parse_md_table(FRONTEND_MD, role_id_override=1))
print(f"Loaded Frontend: {len(all_questions)}")
prev_count = len(all_questions)
all_questions.extend(parse_md_table(BACKEND_MD, role_id_override=2))
print(f"Loaded Backend: {len(all_questions) - prev_count}")
prev_count = len(all_questions)
all_questions.extend(parse_md_table(FULLSTACK_MD, role_id_override=3))
print(f"Loaded Full Stack: {len(all_questions) - prev_count}")
prev_count = len(all_questions)
all_questions.extend(parse_md_table(DEVOPS_MD, role_id_override=4))
print(f"Loaded DevOps: {len(all_questions) - prev_count}")
prev_count = len(all_questions)
all_questions.extend(parse_behavioral())
print(f"Loaded Behavioral: {len(all_questions) - prev_count}")

# Deduplicate
unique_questions = {}
for q in all_questions:
    key = (q['question_text'], q['role_id'])
    unique_questions[key] = q

final_list = list(unique_questions.values())

# Write to file
questions_repr = "QUESTION_DATA = [\n"
for q in final_list:
    questions_repr += f'    {q},\n'
questions_repr += "]\n"

content = f"""from database import SessionLocal
from models.question import Question

{questions_repr}

def seed_questions():
    db = SessionLocal()
    try:
        db.query(Question).delete()
        for data in QUESTION_DATA:
            db.add(Question(**data))
        db.commit()
        print(f"✓ {{len(QUESTION_DATA)}} Questions seeded (Roles: 0, 1, 2, 3, 4)")
    except Exception as e:
        db.rollback()
        print(f"Error seeding questions: {{e}}")
    finally:
        db.close()
"""

with open(SEED_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Master seeding complete! Total unified questions: {len(final_list)}")
