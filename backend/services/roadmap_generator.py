from typing import List, Optional, Dict, Any


class RoadmapGenerator:
    """
    Generates weekly task-based roadmaps for weak dimensions
    with practical, actionable growth tasks.
    """
    
    # Roadmap templates for each dimension
    ROADMAP_TEMPLATES = {
        "Core Technical Skills": [
            {
                "week": 1,
                "tasks": [
                    "Review and master one advanced language feature you rarely use",
                    "Solve 3 medium-level algorithm problems on LeetCode/HackerRank",
                    "Read documentation for a core library/framework you use daily"
                ]
            },
            {
                "week": 2,
                "tasks": [
                    "Build a small CLI tool using advanced language features",
                    "Deep dive into performance optimization techniques",
                    "Study and implement a common design pattern you haven't used"
                ]
            },
            {
                "week": 3,
                "tasks": [
                    "Contribute to an open-source project in your tech stack",
                    "Refactor a complex piece of code using better patterns",
                    "Learn and apply a new testing technique (property-based, mutation testing)"
                ]
            },
            {
                "week": 4,
                "tasks": [
                    "Write a technical blog post about a complex problem you solved",
                    "Mentor a junior developer on a technical concept",
                    "Review and optimize a critical path in your codebase"
                ]
            }
        ],
        "Architecture & Design": [
            {
                "week": 1,
                "tasks": [
                    "Study a well-architected open-source project in your domain",
                    "Document the architecture of your current system with diagrams",
                    "Read 'Designing Data-Intensive Applications' (first 3 chapters)"
                ]
            },
            {
                "week": 2,
                "tasks": [
                    "Design a scalable solution for a common problem (URL shortener, rate limiter)",
                    "Review and critique an architectural decision in your codebase",
                    "Learn about CAP theorem and consistency patterns"
                ]
            },
            {
                "week": 3,
                "tasks": [
                    "Propose an architectural improvement for your current project",
                    "Study microservices patterns (circuit breaker, saga, CQRS)",
                    "Create an ADR (Architecture Decision Record) for a recent decision"
                ]
            },
            {
                "week": 4,
                "tasks": [
                    "Design a system from scratch (e.g., notification service, search engine)",
                    "Present your design to peers and incorporate feedback",
                    "Study trade-offs between different architectural patterns"
                ]
            }
        ],
        "Ownership & Impact": [
            {
                "week": 1,
                "tasks": [
                    "Identify and document 3 pain points in your current workflow",
                    "Propose solutions with estimated impact and effort",
                    "Take ownership of one small improvement and ship it"
                ]
            },
            {
                "week": 2,
                "tasks": [
                    "Track and measure the impact of your recent work (metrics, user feedback)",
                    "Identify a cross-team dependency and work to resolve it",
                    "Volunteer to lead a small project or initiative"
                ]
            },
            {
                "week": 3,
                "tasks": [
                    "Create a roadmap for a feature or improvement you care about",
                    "Present your roadmap to stakeholders and get buy-in",
                    "Start execution and track progress publicly"
                ]
            },
            {
                "week": 4,
                "tasks": [
                    "Write a post-mortem or retrospective for a completed project",
                    "Share learnings with the team and document best practices",
                    "Identify your next high-impact project"
                ]
            }
        ],
        "Code Quality & Practices": [
            {
                "week": 1,
                "tasks": [
                    "Set up or improve linting and formatting in your project",
                    "Review and improve test coverage for a critical module",
                    "Refactor one complex function using SOLID principles"
                ]
            },
            {
                "week": 2,
                "tasks": [
                    "Implement pre-commit hooks for code quality checks",
                    "Write comprehensive tests for a previously untested feature",
                    "Review 5 PRs with focus on code quality and best practices"
                ]
            },
            {
                "week": 3,
                "tasks": [
                    "Set up or improve CI/CD pipeline for your project",
                    "Implement automated code quality gates (coverage, complexity)",
                    "Refactor a large file/module into smaller, testable units"
                ]
            },
            {
                "week": 4,
                "tasks": [
                    "Create a code quality checklist for your team",
                    "Give a presentation on code quality best practices",
                    "Establish code review guidelines and standards"
                ]
            }
        ],
        "Communication & Influence": [
            {
                "week": 1,
                "tasks": [
                    "Write detailed documentation for a complex feature you built",
                    "Present a technical topic in a team meeting",
                    "Practice explaining a complex concept to a non-technical person"
                ]
            },
            {
                "week": 2,
                "tasks": [
                    "Start writing a technical blog or create video content",
                    "Participate actively in 3 technical discussions (meetings, Slack, etc.)",
                    "Mentor a junior developer and document the process"
                ]
            },
            {
                "week": 3,
                "tasks": [
                    "Give a tech talk or workshop to your team",
                    "Write an RFC (Request for Comments) for a technical proposal",
                    "Gather and incorporate feedback from multiple stakeholders"
                ]
            },
            {
                "week": 4,
                "tasks": [
                    "Lead a technical discussion or design review",
                    "Create visual aids (diagrams, slides) to explain your work",
                    "Build consensus on a controversial technical decision"
                ]
            }
        ]
    }
    
    INTERVIEW_QUESTIONS = {
        "Core Technical Skills": [
            "Explain the difference between a process and a thread in your primary language.",
            "How do you handle memory management and avoid leaks in your applications?",
            "Describe a complex technical bug you found and how you resolved it."
        ],
        "Architecture & Design": [
            "How do you approach designing a system for high availability and scalability?",
            "Explain the trade-offs between SQL and NoSQL databases for a real-time analytics system.",
            "Describe the CAP theorem and its implications on distributed system design."
        ],
        "Ownership & Impact": [
            "Tell me about a time you took initiative on a project without being asked.",
            "How do you prioritize your tasks when faced with multiple competing deadlines?",
            "Describe a project where you had to manage stakeholders with conflicting interests."
        ],
        "Code Quality & Practices": [
            "How do you ensure your code is maintainable and easy for others to understand?",
            "What is your approach to unit testing and how do you decide what to test?",
            "Describe your code review process and what you look for in a PR."
        ],
        "Communication & Influence": [
            "How do you explain technical concepts to non-technical stakeholders?",
            "Tell me about a time you had to persuade a team to adopt a specific technology or pattern.",
            "How do you handle disagreements within the team regarding architectural decisions?"
        ]
    }

    LEARNING_RESOURCES = {
        "Core Technical Skills": [
            {"title": "Clean Code", "type": "Book", "url": "https://www.oreilly.com/library/view/clean-code-a/9780136083238/"},
            {"title": "The Pragmatic Programmer", "type": "Book", "url": "https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/"}
        ],
        "Architecture & Design": [
            {"title": "Designing Data-Intensive Applications", "type": "Book", "url": "https://dataintensive.net/"},
            {"title": "Architecture Patterns with Python", "type": "Book", "url": "https://www.cosmicpython.com/"}
        ],
        "Ownership & Impact": [
            {"title": "Extreme Ownership", "type": "Book", "url": "https://efonline.com/book/extreme-ownership/"},
            {"title": "The Staff Engineer's Path", "type": "Book", "url": "https://www.oreilly.com/library/view/the-staff-engineers/9781098118721/"}
        ],
        "Code Quality & Practices": [
            {"title": "Refactoring", "type": "Book", "url": "https://martinfowler.com/books/refactoring.html"},
            {"title": "Unit Testing Principles, Practices, and Patterns", "type": "Book", "url": "https://www.manning.com/books/unit-testing"}
        ],
        "Communication & Influence": [
            {"title": "Crucial Conversations", "type": "Book", "url": "https://cruciallearning.com/crucial-conversations-book/"},
            {"title": "Soft Skills: The software developer's life manual", "type": "Book", "url": "https://www.manning.com/books/soft-skills"}
        ]
    }

    @staticmethod
    def get_interview_questions(weak_dimensions: List[str]) -> List[str]:
        """Get 5 interview questions based on weak dimensions."""
        questions = []
        for dim in weak_dimensions:
            if dim in RoadmapGenerator.INTERVIEW_QUESTIONS:
                questions.extend(RoadmapGenerator.INTERVIEW_QUESTIONS[dim])
        return questions[:5]

    @staticmethod
    def get_learning_resources(weak_dimensions: List[str]) -> List[Dict[str, str]]:
        """Get learning resources for weak dimensions."""
        resources = []
        for dim in weak_dimensions:
            if dim in RoadmapGenerator.LEARNING_RESOURCES:
                resources.extend(RoadmapGenerator.LEARNING_RESOURCES[dim])
        return resources[:6]
    
    @staticmethod
    def generate_roadmap(
        weak_dimensions: List[str],
        tech_stack: Optional[List[str]] = None
    ) -> Dict[str, List[Dict]]:
        """
        Generate a 4-week roadmap for each weak dimension.
        
        Args:
            weak_dimensions: List of dimension names that need improvement
            tech_stack: Optional list of technologies to personalize tasks
            
        Returns:
            Dictionary mapping dimension names to weekly task lists
        """
        roadmap = {}
        
        for dimension in weak_dimensions:
            if dimension in RoadmapGenerator.ROADMAP_TEMPLATES:
                # Create a copy of the template to avoid modifying the original
                dimension_roadmap = []
                for week_data in RoadmapGenerator.ROADMAP_TEMPLATES[dimension]:
                    new_week = {
                        "week": week_data["week"],
                        "tasks": [
                            RoadmapGenerator._personalize_task(task, tech_stack)
                            for task in week_data["tasks"]
                        ]
                    }
                    dimension_roadmap.append(new_week)
                roadmap[dimension] = dimension_roadmap
        
        return roadmap
    
    @staticmethod
    def _personalize_task(task: str, tech_stack: Optional[List[str]] = None) -> str:
        """Helper to inject tech stack context into a task description."""
        if not tech_stack or not tech_stack:
            return task
            
        # Example personalization logic
        primary_tech = tech_stack[0]
        
        if "architecture" in task.lower():
            return f"{task} (Apply concepts specifically to {primary_tech} ecosystems)"
        elif "documentation" in task.lower():
            return f"{task} using standard {primary_tech} documentation tools"
        elif "performance" in task.lower():
            return f"{task} with a focus on {primary_tech} runtime/framework specifics"
            
        return task

    @staticmethod
    def get_quick_wins(weak_dimensions: List[str], tech_stack: Optional[List[str]] = None) -> List[str]:
        """
        Get quick win tasks for immediate action.
        
        Args:
            weak_dimensions: List of weak dimension names
            tech_stack: Optional tech stack for personalization
            
        Returns:
            List of quick win tasks
        """
        quick_wins = []
        
        for dimension in weak_dimensions:
            if dimension in RoadmapGenerator.ROADMAP_TEMPLATES:
                # Get first task from week 1
                first_week = RoadmapGenerator.ROADMAP_TEMPLATES[dimension][0]
                task = first_week['tasks'][0]
                personalized_task = RoadmapGenerator._personalize_task(task, tech_stack)
                quick_wins.append(f"{dimension}: {personalized_task}")
        
        return quick_wins
