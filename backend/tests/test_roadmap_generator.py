from services.roadmap_generator import RoadmapGenerator

def test_get_interview_questions():
    weak = ["Core Technical Skills", "Architecture & Design"]
    questions = RoadmapGenerator.get_interview_questions(weak)
    
    assert len(questions) == 5 # Should be capped at 5
    assert any("process and a thread" in q for q in questions)
    assert any("high availability" in q for q in questions)

def test_get_learning_resources():
    weak = ["Core Technical Skills"]
    resources = RoadmapGenerator.get_learning_resources(weak)
    
    assert len(resources) >= 2
    assert any(r["title"] == "Clean Code" for r in resources)

def test_get_quick_wins():
    weak = ["Core Technical Skills", "Architecture & Design"]
    wins = RoadmapGenerator.get_quick_wins(weak)
    
    assert len(wins) == 2
    assert "Core Technical Skills:" in wins[0]
    assert "Architecture & Design:" in wins[1]

def test_personalize_task():
    task = "Document the architecture of your current system"
    tech_stack = ["Python", "AWS"]
    
    personalized = RoadmapGenerator._personalize_task(task, tech_stack)
    assert "Python" in personalized
    
    # Case with empty stack
    assert RoadmapGenerator._personalize_task(task, []) == task

def test_generate_roadmap():
    weak = ["Core Technical Skills"]
    roadmap = RoadmapGenerator.generate_roadmap(weak, ["React"])
    
    assert "Core Technical Skills" in roadmap
    assert len(roadmap["Core Technical Skills"]) == 4 # 4 weeks
    assert roadmap["Core Technical Skills"][0]["week"] == 1
    assert len(roadmap["Core Technical Skills"][0]["tasks"]) > 0
