from sqlalchemy.orm import Session
from models.certificate import Certificate

class CertificationExtensionModule:
    @staticmethod
    def get_certificate_multiplier(db: Session, cert_names: list) -> float:
        """
        Calculate the combined salary multiplier for a list of certifications.
        Uses the highest multiplier found.
        """
        if not cert_names:
            return 1.0
        
        multipliers = db.query(Certificate.multiplier).filter(
            Certificate.name.in_(cert_names)
        ).all()
        
        if not multipliers:
            return 1.0
            
        return max([m[0] for m in multipliers])

    @staticmethod
    def get_certificate_tier_impact(db: Session, cert_names: list) -> float:
        """
        Return a score boost (0.0 to 1.0) based on certification tiers.
        Expert: 1.0, Intermediate: 0.6, Entry: 0.3
        """
        if not cert_names:
            return 0.0
            
        certs = db.query(Certificate).filter(Certificate.name.in_(cert_names)).all()
        if not certs:
            return 0.0
            
        tier_map = {
            "Specialization": 1.0,
            "Expert": 0.9,
            "Intermediate": 0.6,
            "Entry": 0.3
        }
        
        max_impact = 0.0
        for cert in certs:
            impact = tier_map.get(cert.tier, 0.0)
            if impact > max_impact:
                max_impact = impact
                
        return max_impact
