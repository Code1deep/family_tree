# family_tree/insertion.py
import os
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy import text
from flask import current_app
from app.extensions import db
from domain.models.person import Person
import logging

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

def clean_database():
    """Vide la table persons de manière fiable"""
    try:
        db.session.execute(text("TRUNCATE TABLE persons RESTART IDENTITY CASCADE;"))
        db.session.commit()
        logger.info("✅ Table persons vidée avec succès")
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Échec du nettoyage: {str(e)}")
        return False

def initialize_data():
    logger.info("Initialisation des données démarrée")
    
    if not current_app:
        logger.error("Erreur: Doit être exécuté dans un contexte Flask")
        raise RuntimeError("Doit être exécuté dans un contexte Flask")

    try:
        if not clean_database():
            raise Exception("Échec du nettoyage de la base")

        # 1. Insertion des données de base sans full_name
        logger.info("➕ Insertion des membres de la famille...")
        db.session.execute(text("""
            INSERT INTO persons (id, first_name, last_name, gender, father_id, mother_id)
            VALUES
                (1, 'آدَمُ', 'عليه السلام', 'male', NULL, NULL),
                (2, 'شَيْثُ', 'بْنُ آدَمَ عليهما السلام', 'male', 1, NULL),
                (3, 'أَنُوشُ', 'بْنُ شَيْثٍ', 'male', 2, NULL),
                (4, 'قَيْنَانُ', 'بْنُ أَنُوشٍ', 'male', 3, NULL),
                (5, 'مَهْلَائِيلُ', 'بْنُ قَيْنَانَ', 'male', 4, NULL),
                (6, 'يَارَدُ', 'بْنُ مَهْلَائِيلَ', 'male', 5, NULL),
                (7, 'أَخْنُوخُ', '(إِدْرِيسُ عليه السلام) بْنُ يَارَدَ', 'male', 6, NULL),
                (8, 'مَتُوشَلَخُ', 'بْنُ أَخْنُوخَ', 'male', 7, NULL),
                (9, 'لَامَكُ', 'بْنُ مَتُوشَلَخَ', 'male', 8, NULL),
                (10, 'نُوحٌ', 'عليه السلام بْنُ لَامَكَ', 'male', 9, NULL),
                (11, 'سَامُ', 'بْنُ نُوحٍ', 'male', 10, NULL),
                (12, 'أَرْفَخْشَذُ', 'بْنُ سَامٍ', 'male', 11, NULL),
                (13, 'شَالِخُ', 'بْنُ أَرْفَخْشَذَ', 'male', 12, NULL),
                (14, 'عَابِرُ', '(هُودٌ عليه السلام) بْنُ شَالِخٍ', 'male', 13, NULL),
                (15, 'فَالَغُ', 'بْنُ عَابِرٍ', 'male', 14, NULL),
                (16, 'أَرْغُو', 'بْنُ فَالِغٍ', 'male', 15, NULL),
                (17, 'سَارُوغُ', 'بْنُ أَرْغُوَ', 'male', 16, NULL),
                (18, 'نَاحُورُ', 'بْنُ سَارُوغَ', 'male', 17, NULL),
                (19, 'تَارَحُ', '(آزَرُ) بْنُ نَاحُورَ', 'male', 18, NULL),
                (20, 'إِبْرَاهِيمُ', 'الخَلِيلُ عليه السلام بْنُ تَارَحَ', 'male', 19, NULL),
                (21, 'إِسْمَاعِيلُ', 'بْنُ إِبْرَاهِيمَ الخَلِيلِ', 'male', 20, NULL),
                (22, 'عَدْنَانُ', 'بْنُ إِسْمَاعِيل', 'male', 21, NULL),
                (23, 'مَعَدُّ', 'بْنُ عَدْنَان', 'male', 22, NULL),
                (24, 'نِزَارُ', 'بْنُ مَعَدٍّ', 'male', 23, NULL),
                (25, 'مُضَرُ', 'بْنُ نِزَار', 'male', 24, NULL),
                (26, 'إِلْيَاسُ', 'بْنُ مُضَرَ', 'male', 25, NULL),
                (27, 'مُدْرِكَةُ', 'بْنُ إِلْيَاسَ', 'male', 26, NULL),
                (28, 'خُزَيْمَةُ', 'بْنُ مُدْرِكَةَ', 'male', 27, NULL),
                (29, 'كِنَانَة', 'بْنُ خُزَيْمَةَ', 'male', 28, NULL),
                (30, 'النَّضْر', 'بْنُ كِنَانَة', 'male', 29, NULL),
                (31, 'مَالِك', 'بْنُ النَّضْر', 'male', 30, NULL),
                (32, 'فِهْر', 'بْنُ مَالِك', 'male', 31, NULL),
                (33, 'غَالِب', 'بْنُ فِهْر', 'male', 32, NULL),
                (34, 'لُؤَي', 'بْنُ غَالِب', 'male', 33, NULL),
                (35, 'كَعْب', 'بْنُ لُؤَي', 'male', 34, NULL),
                (36, 'مُرَّة', 'بْنُ كَعْب', 'male', 35, NULL),
                (37, 'كِلَاب', 'بْنُ مُرَّة', 'male', 36, NULL),
                (38, 'قُصَي', 'بْنُ كِلَاب', 'male', 37, NULL),
                (39, 'عَبْدُ مَنَاف', 'بْنُ قُصَي', 'male', 38, NULL),
                (40, 'هَاشِم', 'بْنُ عَبْدِ مَنَاف', 'male', 39, NULL),
                (41, 'عَبْدُ الْمُطَّلِب', 'بْنُ هَاشِم', 'male', 40, NULL),
                (42, 'أَبُو طَالِب', 'عَمُّ الرَّسُولِ مُحَمَّدٍ بْنُ عَبْدِ الْمُطَّلِب', 'male', 41, NULL),
                (43, 'فَاطِمَة', 'بِنْتُ أَسَد', 'female', NULL, NULL),
                (44, 'عَلِي', 'بْنُ أَبِي طَالِب', 'male', 42, 43),
                (45, 'الحَسَن السِّبْط', 'بْنُ عَلِي', 'male', 44, NULL),
                (46, 'حُسَيْن', 'بْنُ عَلِي', 'male', 44, NULL),
                (47, 'عَبْدُاللَّه', 'بْنُ الحَسَن السِّبْط', 'male', 45, NULL),
                (48, 'فَاطِمَة', 'بِنْتُ الحَسَن السِّبْط', 'female', 45, NULL),
                (49, 'عَلِي', 'بْنُ عَبْدُاللَّه', 'male', 47, NULL),
                (50, 'زَيْنَب', 'بِنْتُ عَبْدُاللَّه', 'female', 47, NULL),
                (51, 'الحسن المُثَنَّى', 'بْنُ الحَسَن السِّبْط', 'male', 45, NULL),
                (52, 'عَبْدُاللَّه الكَامل', 'بْنُ الحَسَن المُثَنَّى', 'male', 51, NULL),
                (53, 'مولاَي إِدْرَيس الأَوَّل', 'بْنُ عَبْدُاللَّه الكَامل', 'male', 52, NULL),
                (54, 'مولاَي إِدْرَيس الثَّانِي', 'بْنُ مولاَي إِدْرَيس الأَوَّل', 'male', 53, NULL),
                (55, 'مُحَمَّد', 'بْنُ إِدْرَيس الثَّانِي', 'male', 54, NULL),
                (56, 'أَحْمَد', 'بْنُ مُحَمَّد', 'male', 55, NULL),
                (57, 'إِسْحَاق', 'بْنُ أَحْمَد', 'male', 56, NULL),
                (58, 'عَلِي', 'بْنُ إِسْحَاق', 'male', 57, NULL),
                (59, 'عَبْدُالرَّحْمَن', 'بْنُ عَلِيٍّ بْنِ إِسْحَاق', 'male', 58, NULL),
                (60, 'عِيسَى', 'بْنُ عَبْدُالرَّحْمَن الْوَدْغِيرِي', 'male', 59, NULL),
                (61, 'مَنْصُور', 'بْنُ عِيسَى', 'male', 60, NULL),
                (62, 'عَلِي', 'بْنُ مَنْصُور', 'male', 61, NULL),
                (63, 'عَبْدُ الْإِلَه', 'بْنُ عَلِي', 'male', 62, NULL),
                (64, 'مُحَمَّد', 'بْنُ عَبْدُالْإِلَه', 'male', 63, NULL),
                (65, 'سَعِيد', 'بْنُ مُحَمَّد', 'male', 64, NULL),
                (66, 'أَبُو بَكْر', 'بْنُ سَعِيد', 'male', 65, NULL),
                (67, 'عَلِي', 'بْنُ أَبِي بَكْر', 'male', 66, NULL),
                (68, 'أَبُو يَحْيَى البصِير', 'بْنُ عَلِي', 'male', 67, NULL)
        """))
    
        db.session.commit()
        logger.info("✅ Données insérées sans calcul")
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Erreur : {str(e)}")
        raise
    
def full_initialize():
    if current_app:
        initialize_data()
    else:
        from app.factory import create_app
        app = create_app()
        with app.app_context():
            initialize_data()

if __name__ == '__main__':
    print("⚠ Utilisez 'flask init-db' ou appelez full_initialize()")
