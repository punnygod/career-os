from database import SessionLocal
from models.stack import Stack
from models.role import Role

STACK_DATA = [
    # ==================== LANGUAGES ====================
    {'name': 'JavaScript', 'category': 'Language', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 1, 2, 3]},
    {'name': 'TypeScript', 'category': 'Language', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 1, 2, 3]},
    {'name': 'Python', 'category': 'Language', 'demand_score': 1.3, 'scarcity_score': 1.0, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'Java', 'category': 'Language', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'C#', 'category': 'Language', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'PHP', 'category': 'Language', 'demand_score': 1.1, 'scarcity_score': 1.0, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 2, 3]},
    {'name': 'Go (Golang)', 'category': 'Language', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'Ruby', 'category': 'Language', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 2, 3]},
    {'name': 'Kotlin', 'category': 'Language', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 3]},
    {'name': 'Swift', 'category': 'Language', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 1, 3]},
    {'name': 'Rust', 'category': 'Language', 'demand_score': 1.1, 'scarcity_score': 1.4, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'Scala', 'category': 'Language', 'demand_score': 1.1, 'scarcity_score': 1.4, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 2, 3]},

    # ==================== FRONTEND FRAMEWORKS ====================
    {'name': 'React', 'category': 'Frontend Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 1, 3]},
    {'name': 'Angular', 'category': 'Frontend Framework', 'demand_score': 1.3, 'scarcity_score': 1.4, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 1, 3]},
    {'name': 'Vue.js', 'category': 'Frontend Framework', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 1, 3]},
    {'name': 'Next.js', 'category': 'Frontend Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 1, 3]},
    {'name': 'Nuxt.js', 'category': 'Frontend Framework', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 1, 3]},
    {'name': 'Svelte', 'category': 'Frontend Framework', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.0, 'multiplier': 1.0, 'roles': [0, 1, 3]},
    {'name': 'jQuery', 'category': 'Frontend Framework', 'demand_score': 1.1, 'scarcity_score': 1.0, 'enterprise_score': 1.3, 'multiplier': 0.9, 'roles': [0, 1, 3]},

    # ==================== BACKEND FRAMEWORKS ====================
    {'name': 'Express.js', 'category': 'Backend Framework', 'demand_score': 1.3, 'scarcity_score': 1.0, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'NestJS', 'category': 'Backend Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'Django', 'category': 'Backend Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'Flask', 'category': 'Backend Framework', 'demand_score': 1.3, 'scarcity_score': 1.0, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'Spring Boot', 'category': 'Backend Framework', 'demand_score': 1.3, 'scarcity_score': 1.4, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'ASP.NET Core', 'category': 'Backend Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'Ruby on Rails', 'category': 'Backend Framework', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 2, 3]},
    {'name': 'Laravel', 'category': 'Backend Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 2, 3]},
    {'name': 'Symfony', 'category': 'Backend Framework', 'demand_score': 1.1, 'scarcity_score': 1.4, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 2, 3]},
    {'name': 'FastAPI', 'category': 'Backend Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'Gin (Go)', 'category': 'Backend Framework', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': '.NET (Core/ASP.NET)', 'category': 'Backend Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3]},

    # ==================== MOBILE FRAMEWORKS ====================
    {'name': 'Android (Jetpack/Compose)', 'category': 'Mobile Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 1, 3]},
    {'name': 'iOS UIKit/SwiftUI', 'category': 'Mobile Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 1, 3]},
    {'name': 'React Native', 'category': 'Mobile Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 1, 3]},
    {'name': 'Flutter', 'category': 'Mobile Framework', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 1, 3]},
    {'name': 'Xamarin/.NET MAUI', 'category': 'Mobile Framework', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 3]},
    {'name': 'Ionic', 'category': 'Mobile Framework', 'demand_score': 1.1, 'scarcity_score': 1.0, 'enterprise_score': 1.1, 'multiplier': 0.9, 'roles': [0, 1, 3]},

    # ==================== DATABASES ====================
    {'name': 'PostgreSQL', 'category': 'Database', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'MySQL', 'category': 'Database', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.0, 'roles': [0, 2, 3]},
    {'name': 'MariaDB', 'category': 'Database', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 2, 3]},
    {'name': 'Microsoft SQL Server', 'category': 'Database', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'Oracle Database', 'category': 'Database', 'demand_score': 1.1, 'scarcity_score': 1.4, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'MongoDB', 'category': 'Database', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'Redis', 'category': 'Database', 'demand_score': 1.3, 'scarcity_score': 1.0, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'Elasticsearch (Elastic Stack)', 'category': 'Database', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'Cassandra', 'category': 'Database', 'demand_score': 1.1, 'scarcity_score': 1.4, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 2, 3]},
    {'name': 'DynamoDB', 'category': 'Database', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'Snowflake', 'category': 'Database', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'BigQuery', 'category': 'Database', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},

    # ==================== CLOUD PLATFORMS ====================
    {'name': 'Amazon Web Services (AWS)', 'category': 'Cloud Platform', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'Microsoft Azure', 'category': 'Cloud Platform', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'Google Cloud Platform (GCP)', 'category': 'Cloud Platform', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'DigitalOcean', 'category': 'Cloud Platform', 'demand_score': 1.1, 'scarcity_score': 1.0, 'enterprise_score': 1.0, 'multiplier': 1.0, 'roles': [0, 3, 4]},

    # ==================== DEVOPS TOOLS ====================
    {'name': 'Kubernetes', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.4, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'Docker', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'Terraform', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'Ansible', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'Chef', 'category': 'DevOps Tool', 'demand_score': 1.1, 'scarcity_score': 1.4, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 4]},
    {'name': 'Puppet', 'category': 'DevOps Tool', 'demand_score': 1.1, 'scarcity_score': 1.4, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 4]},
    {'name': 'Jenkins', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.0, 'roles': [0, 3, 4]},
    {'name': 'GitHub Actions', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'GitLab CI/CD', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 2, 3, 4]},
    {'name': 'CircleCI', 'category': 'DevOps Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 3, 4]},
    {'name': 'Azure DevOps', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'AWS CodePipeline', 'category': 'DevOps Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 3, 4]},
    {'name': 'Helm', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'Argo CD', 'category': 'DevOps Tool', 'demand_score': 1.1, 'scarcity_score': 1.4, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 4]},
    {'name': 'Prometheus', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'Grafana', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'ELK Stack (Elasticsearch/Logstash/Kibana)', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.4, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'Datadog', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'New Relic', 'category': 'DevOps Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'Splunk', 'category': 'DevOps Tool', 'demand_score': 1.1, 'scarcity_score': 1.4, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 3, 4]},
    {'name': 'Jira', 'category': 'DevOps Tool', 'demand_score': 1.3, 'scarcity_score': 1.0, 'enterprise_score': 1.3, 'multiplier': 1.0, 'roles': [0, 2, 3, 4]},

    # ==================== TESTING TOOLS ====================
    {'name': 'Selenium', 'category': 'Testing Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.0, 'roles': [0, 1, 2, 3]},
    {'name': 'Cypress', 'category': 'Testing Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 1, 3]},
    {'name': 'Playwright', 'category': 'Testing Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 1, 3]},
    {'name': 'JUnit', 'category': 'Testing Tool', 'demand_score': 1.3, 'scarcity_score': 1.0, 'enterprise_score': 1.3, 'multiplier': 1.0, 'roles': [0, 2, 3]},
    {'name': 'NUnit/xUnit', 'category': 'Testing Tool', 'demand_score': 1.3, 'scarcity_score': 1.0, 'enterprise_score': 1.3, 'multiplier': 1.0, 'roles': [0, 2, 3]},
    {'name': 'Jest', 'category': 'Testing Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.2, 'roles': [0, 1, 2, 3]},
    {'name': 'Mocha/Chai', 'category': 'Testing Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 1, 2, 3]},
    {'name': 'PyTest', 'category': 'Testing Tool', 'demand_score': 1.3, 'scarcity_score': 1.2, 'enterprise_score': 1.3, 'multiplier': 1.0, 'roles': [0, 2, 3]},
    {'name': 'Postman', 'category': 'Testing Tool', 'demand_score': 1.3, 'scarcity_score': 1.0, 'enterprise_score': 1.3, 'multiplier': 1.0, 'roles': [0, 1, 2, 3]},
    {'name': 'Newman/CLI Postman', 'category': 'Testing Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 2, 3, 4]},
    {'name': 'Cucumber/BDD (Java stack)', 'category': 'Testing Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 2, 3]},
    {'name': 'Appium', 'category': 'Testing Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 1, 3]},
    {'name': 'JMeter', 'category': 'Testing Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 3, 4]},
    {'name': 'Locust', 'category': 'Testing Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.0, 'roles': [0, 2, 3, 4]},
    {'name': 'Playwright Test Runner', 'category': 'Testing Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 1, 3]},
    {'name': 'Cypress Component Testing', 'category': 'Testing Tool', 'demand_score': 1.1, 'scarcity_score': 1.2, 'enterprise_score': 1.1, 'multiplier': 1.2, 'roles': [0, 1, 3]},
]


def seed_stacks():
    db = SessionLocal()
    try:
        # Clear existing stacks to refresh from the new source
        # Note: This might cascade delete stack_roles due to CASCADE on foreign keys
        db.query(Stack).delete()
        
        # Pre-fetch all roles to avoid N+1 queries during loop
        # Map ID to Role object
        all_roles = {role.id: role for role in db.query(Role).all()}
        
        for data in STACK_DATA:
            # Extract roles IDs and remove from data dict for Stack instantiation
            role_ids = data.pop('roles', [])
            
            stack = Stack(**data)
            
            # Associate roles
            for role_id in role_ids:
                if role_id in all_roles:
                    stack.roles.append(all_roles[role_id])
                else:
                    print(f"Warning: Role ID {role_id} not found for stack {stack.name}")
                    
            db.add(stack)
            
        db.commit()
        print(f"✓ {len(STACK_DATA)} Stacks seeded from industry analyst report")
    except Exception as e:
        db.rollback()
        print(f"Error seeding stacks: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_stacks()
