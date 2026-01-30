"""
Seed script for questions data.
Run this to populate the questions table with 25 questions per role across 5 dimensions.
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, init_db
from models.question import Question
from models.role import Role


# Question templates for each role
FRONTEND_QUESTIONS = [
    # Core Technical Skills (5 questions)
    {
        "dimension": "Core Technical Skills",
        "question_text": "How proficient are you with modern JavaScript/TypeScript features (async/await, destructuring, modules, generics)?",
        "answer_options": "1: Basic understanding|2: Can use common features|3: Proficient with advanced features|4: Expert, can teach others",
        "order": 1
    },
    {
        "dimension": "Core Technical Skills",
        "question_text": "How well do you understand and implement React/Vue/Angular patterns (hooks, composition API, lifecycle, state management)?",
        "answer_options": "1: Basic component creation|2: Can build features independently|3: Deep understanding of patterns|4: Can architect complex applications",
        "order": 2
    },
    {
        "dimension": "Core Technical Skills",
        "question_text": "How experienced are you with CSS/styling solutions (CSS-in-JS, Tailwind, CSS modules, responsive design)?",
        "answer_options": "1: Basic styling|2: Can implement designs|3: Advanced layouts and animations|4: Expert in performance and accessibility",
        "order": 3
    },
    {
        "dimension": "Core Technical Skills",
        "question_text": "How proficient are you with browser APIs and web platform features (Storage, Workers, WebSockets, Performance APIs)?",
        "answer_options": "1: Limited knowledge|2: Can use common APIs|3: Deep understanding of browser internals|4: Expert in optimization and debugging",
        "order": 4
    },
    {
        "dimension": "Core Technical Skills",
        "question_text": "How experienced are you with frontend build tools and bundlers (Webpack, Vite, esbuild, module federation)?",
        "answer_options": "1: Basic usage|2: Can configure for projects|3: Deep understanding of optimization|4: Can build custom tooling",
        "order": 5
    },
    
    # Architecture & Design (5 questions)
    {
        "dimension": "Architecture & Design",
        "question_text": "How well do you design component architectures (composition, reusability, separation of concerns)?",
        "answer_options": "1: Basic components|2: Reusable components|3: Well-architected systems|4: Can design design systems",
        "order": 6
    },
    {
        "dimension": "Architecture & Design",
        "question_text": "How experienced are you with state management patterns (Redux, MobX, Zustand, Context, server state)?",
        "answer_options": "1: Basic state handling|2: Can implement patterns|3: Choose appropriate solutions|4: Design custom state solutions",
        "order": 7
    },
    {
        "dimension": "Architecture & Design",
        "question_text": "How well do you handle performance optimization (code splitting, lazy loading, memoization, virtual scrolling)?",
        "answer_options": "1: Basic awareness|2: Can implement common optimizations|3: Proactive performance engineering|4: Expert in profiling and optimization",
        "order": 8
    },
    {
        "dimension": "Architecture & Design",
        "question_text": "How experienced are you with frontend architecture patterns (micro-frontends, monorepos, module federation)?",
        "answer_options": "1: Limited knowledge|2: Basic understanding|3: Have implemented patterns|4: Can architect large-scale systems",
        "order": 9
    },
    {
        "dimension": "Architecture & Design",
        "question_text": "How well do you design for accessibility and internationalization?",
        "answer_options": "1: Basic awareness|2: Follow guidelines|3: Proactive implementation|4: Expert, can audit and teach",
        "order": 10
    },
    
    # Ownership & Impact (5 questions)
    {
        "dimension": "Ownership & Impact",
        "question_text": "How often do you identify and solve problems beyond your assigned tasks?",
        "answer_options": "1: Rarely|2: Sometimes|3: Regularly|4: Consistently drive improvements",
        "order": 11
    },
    {
        "dimension": "Ownership & Impact",
        "question_text": "How do you measure and communicate the impact of your work?",
        "answer_options": "1: Don't track impact|2: Basic metrics|3: Comprehensive tracking|4: Data-driven decision making",
        "order": 12
    },
    {
        "dimension": "Ownership & Impact",
        "question_text": "How often do you take ownership of critical features or initiatives?",
        "answer_options": "1: Rarely|2: When assigned|3: Proactively volunteer|4: Lead multiple initiatives",
        "order": 13
    },
    {
        "dimension": "Ownership & Impact",
        "question_text": "How well do you handle ambiguous or undefined problems?",
        "answer_options": "1: Need clear requirements|2: Can work with guidance|3: Thrive in ambiguity|4: Define problems and solutions",
        "order": 14
    },
    {
        "dimension": "Ownership & Impact",
        "question_text": "How do you contribute to product decisions and user experience improvements?",
        "answer_options": "1: Implement as specified|2: Provide feedback|3: Actively influence decisions|4: Drive product strategy",
        "order": 15
    },
    
    # Code Quality & Practices (5 questions)
    {
        "dimension": "Code Quality & Practices",
        "question_text": "How comprehensive is your testing approach (unit, integration, E2E, visual regression)?",
        "answer_options": "1: Minimal testing|2: Basic unit tests|3: Comprehensive test coverage|4: Test-driven development advocate",
        "order": 16
    },
    {
        "dimension": "Code Quality & Practices",
        "question_text": "How well do you write clean, maintainable code (naming, structure, documentation)?",
        "answer_options": "1: Functional but messy|2: Generally clean|3: Consistently high quality|4: Set standards for team",
        "order": 17
    },
    {
        "dimension": "Code Quality & Practices",
        "question_text": "How experienced are you with code review practices (giving and receiving feedback)?",
        "answer_options": "1: Basic reviews|2: Constructive feedback|3: Thorough, educational reviews|4: Mentor others on reviews",
        "order": 18
    },
    {
        "dimension": "Code Quality & Practices",
        "question_text": "How well do you implement error handling and monitoring (error boundaries, logging, analytics)?",
        "answer_options": "1: Basic error handling|2: Comprehensive error handling|3: Proactive monitoring|4: Build error tracking systems",
        "order": 19
    },
    {
        "dimension": "Code Quality & Practices",
        "question_text": "How do you ensure code quality through automation (linting, formatting, CI/CD)?",
        "answer_options": "1: Manual checks|2: Basic automation|3: Comprehensive automation|4: Build quality infrastructure",
        "order": 20
    },
    
    # Communication & Influence (5 questions)
    {
        "dimension": "Communication & Influence",
        "question_text": "How effectively do you communicate technical decisions and trade-offs?",
        "answer_options": "1: Struggle to explain|2: Can explain when asked|3: Proactively communicate|4: Influence technical direction",
        "order": 21
    },
    {
        "dimension": "Communication & Influence",
        "question_text": "How well do you collaborate with designers, PMs, and backend engineers?",
        "answer_options": "1: Limited collaboration|2: Responsive to requests|3: Proactive collaboration|4: Bridge between teams",
        "order": 22
    },
    {
        "dimension": "Communication & Influence",
        "question_text": "How do you document your work (code comments, READMEs, technical docs)?",
        "answer_options": "1: Minimal documentation|2: Basic documentation|3: Comprehensive documentation|4: Create documentation standards",
        "order": 23
    },
    {
        "dimension": "Communication & Influence",
        "question_text": "How often do you share knowledge through presentations, blog posts, or mentoring?",
        "answer_options": "1: Rarely|2: Occasionally|3: Regularly|4: Recognized thought leader",
        "order": 24
    },
    {
        "dimension": "Communication & Influence",
        "question_text": "How well do you handle disagreements and build consensus?",
        "answer_options": "1: Avoid conflict|2: State opinions|3: Navigate disagreements well|4: Build consensus across teams",
        "order": 25
    }
]

BACKEND_QUESTIONS = [
    # Core Technical Skills (5 questions)
    {
        "dimension": "Core Technical Skills",
        "question_text": "How proficient are you with your primary backend language (Python, Java, Go, Node.js, etc.)?",
        "answer_options": "1: Basic syntax|2: Can build features|3: Advanced patterns and idioms|4: Language expert, can teach",
        "order": 1
    },
    {
        "dimension": "Core Technical Skills",
        "question_text": "How experienced are you with database design and optimization (SQL, NoSQL, indexing, query optimization)?",
        "answer_options": "1: Basic queries|2: Can design schemas|3: Optimize for performance|4: Database architecture expert",
        "order": 2
    },
    {
        "dimension": "Core Technical Skills",
        "question_text": "How well do you design and implement RESTful APIs or GraphQL?",
        "answer_options": "1: Basic endpoints|2: Well-designed APIs|3: Advanced patterns (versioning, pagination)|4: API architecture expert",
        "order": 3
    },
    {
        "dimension": "Core Technical Skills",
        "question_text": "How experienced are you with caching strategies (Redis, Memcached, CDN, application-level)?",
        "answer_options": "1: Limited knowledge|2: Basic implementation|3: Advanced caching patterns|4: Design caching architectures",
        "order": 4
    },
    {
        "dimension": "Core Technical Skills",
        "question_text": "How proficient are you with asynchronous programming and concurrency?",
        "answer_options": "1: Basic understanding|2: Can implement async code|3: Deep understanding of concurrency|4: Expert in distributed systems",
        "order": 5
    },
    
    # Architecture & Design (5 questions)
    {
        "dimension": "Architecture & Design",
        "question_text": "How well do you design scalable backend architectures?",
        "answer_options": "1: Monolithic apps|2: Basic microservices|3: Scalable distributed systems|4: Architect large-scale systems",
        "order": 6
    },
    {
        "dimension": "Architecture & Design",
        "question_text": "How experienced are you with system design patterns (CQRS, Event Sourcing, Saga, Circuit Breaker)?",
        "answer_options": "1: Limited knowledge|2: Basic understanding|3: Have implemented patterns|4: Design pattern expert",
        "order": 7
    },
    {
        "dimension": "Architecture & Design",
        "question_text": "How well do you handle data consistency and transactions in distributed systems?",
        "answer_options": "1: Basic transactions|2: Understand CAP theorem|3: Implement consistency patterns|4: Distributed systems expert",
        "order": 8
    },
    {
        "dimension": "Architecture & Design",
        "question_text": "How experienced are you with message queues and event-driven architectures (Kafka, RabbitMQ, SQS)?",
        "answer_options": "1: Limited knowledge|2: Basic usage|3: Design event-driven systems|4: Messaging architecture expert",
        "order": 9
    },
    {
        "dimension": "Architecture & Design",
        "question_text": "How well do you design for observability (logging, metrics, tracing)?",
        "answer_options": "1: Basic logging|2: Structured logging and metrics|3: Comprehensive observability|4: Build observability platforms",
        "order": 10
    },
    
    # Ownership & Impact (5 questions)
    {
        "dimension": "Ownership & Impact",
        "question_text": "How often do you identify and solve performance bottlenecks proactively?",
        "answer_options": "1: Rarely|2: When issues arise|3: Proactive optimization|4: Performance culture champion",
        "order": 11
    },
    {
        "dimension": "Ownership & Impact",
        "question_text": "How do you measure and improve system reliability and uptime?",
        "answer_options": "1: Don't track|2: Basic monitoring|3: SLOs and error budgets|4: Reliability engineering expert",
        "order": 12
    },
    {
        "dimension": "Ownership & Impact",
        "question_text": "How often do you take ownership of critical services or infrastructure?",
        "answer_options": "1: Rarely|2: When assigned|3: Proactively volunteer|4: Own critical systems",
        "order": 13
    },
    {
        "dimension": "Ownership & Impact",
        "question_text": "How well do you handle production incidents and on-call responsibilities?",
        "answer_options": "1: Need guidance|2: Can resolve incidents|3: Lead incident response|4: Improve incident processes",
        "order": 14
    },
    {
        "dimension": "Ownership & Impact",
        "question_text": "How do you contribute to technical roadmap and architecture decisions?",
        "answer_options": "1: Implement as specified|2: Provide input|3: Influence decisions|4: Drive technical strategy",
        "order": 15
    },
    
    # Code Quality & Practices (5 questions)
    {
        "dimension": "Code Quality & Practices",
        "question_text": "How comprehensive is your testing strategy (unit, integration, contract, load testing)?",
        "answer_options": "1: Minimal testing|2: Basic unit tests|3: Comprehensive test coverage|4: Testing infrastructure expert",
        "order": 16
    },
    {
        "dimension": "Code Quality & Practices",
        "question_text": "How well do you implement security best practices (auth, encryption, input validation)?",
        "answer_options": "1: Basic awareness|2: Follow guidelines|3: Security-first mindset|4: Security expert",
        "order": 17
    },
    {
        "dimension": "Code Quality & Practices",
        "question_text": "How experienced are you with CI/CD and deployment automation?",
        "answer_options": "1: Manual deployments|2: Basic CI/CD|3: Advanced pipelines|4: DevOps culture champion",
        "order": 18
    },
    {
        "dimension": "Code Quality & Practices",
        "question_text": "How well do you write maintainable, documented code?",
        "answer_options": "1: Functional but messy|2: Generally clean|3: Consistently high quality|4: Set code standards",
        "order": 19
    },
    {
        "dimension": "Code Quality & Practices",
        "question_text": "How do you ensure API backward compatibility and versioning?",
        "answer_options": "1: Don't consider|2: Basic versioning|3: Comprehensive compatibility|4: API governance expert",
        "order": 20
    },
    
    # Communication & Influence (5 questions)
    {
        "dimension": "Communication & Influence",
        "question_text": "How effectively do you communicate system design and technical trade-offs?",
        "answer_options": "1: Struggle to explain|2: Can explain when asked|3: Proactively communicate|4: Influence architecture",
        "order": 21
    },
    {
        "dimension": "Communication & Influence",
        "question_text": "How well do you collaborate with frontend, mobile, and data teams?",
        "answer_options": "1: Limited collaboration|2: Responsive to requests|3: Proactive collaboration|4: Cross-team leader",
        "order": 22
    },
    {
        "dimension": "Communication & Influence",
        "question_text": "How do you document APIs, services, and architecture?",
        "answer_options": "1: Minimal documentation|2: Basic docs|3: Comprehensive documentation|4: Documentation standards owner",
        "order": 23
    },
    {
        "dimension": "Communication & Influence",
        "question_text": "How often do you share knowledge through tech talks, RFCs, or mentoring?",
        "answer_options": "1: Rarely|2: Occasionally|3: Regularly|4: Recognized technical leader",
        "order": 24
    },
    {
        "dimension": "Communication & Influence",
        "question_text": "How well do you build consensus on technical decisions?",
        "answer_options": "1: Avoid conflict|2: State opinions|3: Navigate disagreements|4: Build cross-team consensus",
        "order": 25
    }
]


def seed_questions():
    """Seed questions table with initial data."""
    db = SessionLocal()
    
    try:
        # Check if questions already exist
        existing_questions = db.query(Question).count()
        if existing_questions > 0:
            print(f"Questions already seeded ({existing_questions} questions found). Skipping...")
            return
        
        # Get role IDs
        frontend_role = db.query(Role).filter(Role.name == "frontend").first()
        backend_role = db.query(Role).filter(Role.name == "backend").first()
        
        if not frontend_role or not backend_role:
            print("Error: Roles not found. Please run roles_seed.py first.")
            return
        
        questions = []
        
        # Add frontend questions
        for q in FRONTEND_QUESTIONS:
            questions.append(Question(
                role_id=frontend_role.id,
                dimension=q["dimension"],
                question_text=q["question_text"],
                question_order=q["order"],
                answer_options=q["answer_options"],
                weight=1.0
            ))
        
        # Add backend questions
        for q in BACKEND_QUESTIONS:
            questions.append(Question(
                role_id=backend_role.id,
                dimension=q["dimension"],
                question_text=q["question_text"],
                question_order=q["order"],
                answer_options=q["answer_options"],
                weight=1.0
            ))
        
        db.add_all(questions)
        db.commit()
        
        print(f"Successfully seeded {len(questions)} questions!")
        print(f"  - Frontend: {len(FRONTEND_QUESTIONS)} questions")
        print(f"  - Backend: {len(BACKEND_QUESTIONS)} questions")
        
    except Exception as e:
        print(f"Error seeding questions: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_questions()
