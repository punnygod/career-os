from database import SessionLocal
from models.certificate import Certificate

CERT_DATA = [
    {'name': 'AWS Certified Solutions Architect - Associate', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'AWS Certified Solutions Architect - Professional', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'AWS Certified Developer - Associate', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'AWS Certified SysOps Administrator - Associate', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'AWS Certified DevOps Engineer - Professional', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'AWS Certified Security - Specialty', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'AWS Certified Data Engineer - Associate', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'AWS Certified Machine Learning - Specialty', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Microsoft Certified: Azure Fundamentals (AZ-900)', 'tier': 'Entry', 'multiplier': 1.1},
    {'name': 'Microsoft Certified: Azure Administrator Associate (AZ-104)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Microsoft Certified: Azure Solutions Architect Expert', 'tier': 'Expert', 'multiplier': 1.3},
    {'name': 'Microsoft Certified: Azure Developer Associate (AZ-204)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Microsoft Certified: DevOps Engineer Expert', 'tier': 'Expert', 'multiplier': 1.3},
    {'name': 'Microsoft Certified: Power BI Data Analyst Associate', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Google Cloud Professional Cloud Architect', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Google Cloud Professional Data Engineer', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Google Professional Cloud DevOps Engineer', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Google Associate Cloud Engineer', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Google Professional Cloud Security Engineer', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'CompTIA Cloud+', 'tier': 'Intermediate', 'multiplier': 1.15},
    {'name': 'CompTIA Security+', 'tier': 'Entry', 'multiplier': 1.15},
    {'name': 'CompTIA Cybersecurity Analyst (CySA+)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'CompTIA PenTest+', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'CompTIA Advanced Security Practitioner (CASP+)', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'GIAC Security Essentials (GSEC)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'GIAC Penetration Tester (GPEN)', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Certified Information Systems Security Professional (CISSP)', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Certified Cloud Security Professional (CCSP)', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Systems Security Certified Practitioner (SSCP)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Certified Information Security Manager (CISM)', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Certified Information Systems Auditor (CISA)', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Certified in Risk and Information Systems Control (CRISC)', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Certified Ethical Hacker (CEH)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Oracle Certified Professional: Java SE Developer', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Oracle Certified Professional: MySQL Database Administrator', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Red Hat Certified System Administrator (RHCSA)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Red Hat Certified Engineer (RHCE)', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Certified Kubernetes Administrator (CKA)', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Certified Kubernetes Application Developer (CKAD)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Certified Kubernetes Security Specialist (CKS)', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Docker Certified Associate (DCA)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'HashiCorp Certified: Terraform Associate', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Cisco Certified Network Associate (CCNA)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Cisco Certified CyberOps Associate', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Cisco Certified Network Professional (CCNP Enterprise)', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'VMware Certified Professional - Data Center Virtualization (VCP-DCV)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'VMware Certified Professional - Network Virtualization (VCP-NV)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Google Professional Machine Learning Engineer', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'TensorFlow Developer Certificate', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Microsoft Certified: Azure AI Engineer Associate', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Google Data Analytics Professional Certificate', 'tier': 'Entry', 'multiplier': 1.1},
    {'name': 'ISTQB Certified Tester Foundation Level (CTFL)', 'tier': 'Entry', 'multiplier': 1.1},
    {'name': 'ISTQB Certified Tester Advanced Level Test Analyst', 'tier': 'Intermediate', 'multiplier': 1.15},
    {'name': 'Professional Scrum Master I (PSM I)', 'tier': 'Entry', 'multiplier': 1.1},
    {'name': 'Professional Scrum Product Owner I (PSPO I)', 'tier': 'Entry', 'multiplier': 1.1},
    {'name': 'SAFe Agilist (SAFe SA)', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Google Mobile Web Specialist (legacy but active where listed)', 'tier': 'Intermediate', 'multiplier': 1.15},
    {'name': 'Microsoft Certified: Power Platform Developer Associate', 'tier': 'Intermediate', 'multiplier': 1.15},
    {'name': 'Snowflake SnowPro Core Certification', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Databricks Certified Data Engineer Associate', 'tier': 'Intermediate', 'multiplier': 1.2},
    {'name': 'Databricks Certified Machine Learning Professional', 'tier': 'Expert', 'multiplier': 1.25},
    {'name': 'Cloudera Certified Data Analyst', 'tier': 'Intermediate', 'multiplier': 1.15},
    {'name': 'Cloudera Certified Data Scientist (CCDS)', 'tier': 'Expert', 'multiplier': 1.25},
]


def seed_certificates():
    db = SessionLocal()
    try:
        # Clear existing certificates to refresh from the new source
        db.query(Certificate).delete()
        
        for data in CERT_DATA:
            db.add(Certificate(**data))
        db.commit()
        print(f"✓ {len(CERT_DATA)} Certificates seeded from industry analyst report")
    finally:
        db.close()
