# family_tree/insertion2.py
import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import text
from flask import current_app
from family_tree.domain.models.person import Person
import logging
from family_tree.app.extensions import db

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('family_tree_debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def initialize_data2():
    logger.info("Initialisation des données démarrée")

    # VRAI test de contexte
    from flask import has_app_context
    if not has_app_context():
        logger.error("Erreur: Doit être exécuté dans un contexte Flask")
        raise RuntimeError("Doit être exécuté dans un contexte Flask")

    try:

        # 1. Insertion des données de base sans full_name
        logger.info("➕ Insertion de nouveaux membres de la famille...")

        db.session.execute(text("""
            INSERT INTO persons (
                id, first_name, last_name, friends_name, image, father_id, mother_id, 
                birth_date, death_date, birth_place, residence, external_link, image_url, 
                has_offspring, alive, death_reason, died_in_battle, known_enemies, 
                fitan, notes, photo_url, gender, short_bio, full_bio, profession, 
                full_name, father_full_name  
            ) VALUES               
                (40, 'أَبُو', 'طَالِب', NULL, NULL, 1, NULL, '0539-01-01', '0619-01-01', 'مكة', 'الحجاز', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'عم النبي', NULL, 'male', 'كفيل النبي ﷺ', NULL, 'زعيم', 'أَبُو طَالِب بن عَبْدِ المُطَّلِب', 'عَبْدُ المُطَّلِب');
                (44, 'عَلِي', 'بْنُ أَبِي طَالِب', NULL, NULL, 40, 43, '0599-01-01', '0661-01-01', 'مكة', 'الحجاز', NULL, NULL, true, false, 'اغتيال', false, NULL, NULL, 'الخليفة الرابع', NULL, 'male', 'ابن عم النبي ﷺ', NULL, 'خليفة', 'عَلِيٌّ بن أَبِي طَالِب', 'أَبُو طَالِب'),
                (45, 'الحَسَن السِّبْط', 'بْنُ عَلِي',, NULL, NULL, 44, NULL, NULL, '0670-01-01', 'المدينة', 'الحجاز', NULL, NULL, true, false, NULL, NULL, NULL, NULL, 'حفيد النبي', NULL, 'male', 'سبط النبي ﷺ', NULL, 'إمام', 'الحَسَنُ السِّبْط بن عَلِيٍّ', 'عَلِيٌّ بن أَبِي طَالِب'),
                (46, 'حُسَيْن', 'بْنُ عَلِي', NULL, NULL, 44, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'حُسَيْن بْنُ عَلِي'),
                (47, 'عَبْدُاللَّه', 'بْنُ الحَسَن السِّبْط', NULL, NULL, 45, NULL, 680, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَبْدُاللَّه بْنُ الحَسَن السِّبْط'),
                (48, 'فَاطِمَة', 'بِنْتُ الحَسَن السِّبْط', NULL, NULL, 45, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'female', NULL, NULL, NULL, NULL, 'فَاطِمَة بِنْتُ الحَسَن السِّبْط'),
                (49, 'عَلِي', 'بْنُ عَبْدُاللَّه', NULL, NULL, 47, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَلِي بْنُ عَبْدُاللَّه'),
                (50, 'زَيْنَب', 'بِنْتُ عَبْدُاللَّه', NULL, NULL, 47, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'female', NULL, NULL, NULL, NULL, 'زَيْنَب بِنْتُ عَبْدُاللَّه'),
                (51, 'الحسن المُثَنَّى', 'بْنُ الحَسَن السِّبْط', NULL, NULL, 45, NULL, NULL, NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'من أحفاد الحسن', NULL, 'male', 'حفيد الإمام الحسن', NULL, 'عالم', 'الحَسَنُ المُثَنَّى بْنُ الحَسَن السِّبْط', 'الحَسَنُ السِّبْط'),
                (52, 'عَبْدُاللَّه الكَامل', 'بْنُ الحَسَن المُثَنَّى', NULL, NULL, 51, NULL, NULL, NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'من الأشراف', NULL, 'male', 'جد العلويين', NULL, 'عالم', 'عَبْدُ اللهِ الكَامِل بْنُ الحَسَن المُثَنَّى', 'الحَسَنُ المُثَنَّى'),
                (53, 'مولاَي إِدْرَيس الأَوَّل', 'بْنُ عَبْدُاللَّه الكَامل', NULL, NULL, 52, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مولاَي إِدْرَيس الأَوَّل بْنُ عَبْدُاللَّه الكَامل'),
   

                (68, 'أَبُو يَحْيَى البصِير', 'بْنُ عَلِي', NULL, NULL, 67, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'أَبُو يَحْيَى البصِير بْنُ عَلِي')
        """))
    
        db.session.commit()
        logger.info("✅ Données insérées sans calcul")
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Erreur : {str(e)}")
        raise
    
from flask import has_app_context

def full_initialize2():
    if has_app_context():
        initialize_data2()
    else:
        from family_tree.app.factory import create_app
        app = create_app()
        with app.app_context():
            initialize_data2()

print("✅ full_initialize2() a inséré X personnes")


if __name__ == '__main__':
    print("⚠ Utilisez 'flask init-db' ou appelez full_initialize2()")
