# family_tree/insertion.py
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

    # VRAI test de contexte
    from flask import has_app_context
    if not has_app_context():
        logger.error("Erreur: Doit être exécuté dans un contexte Flask")
        raise RuntimeError("Doit être exécuté dans un contexte Flask")

    try:
        if not clean_database():
            raise Exception("Échec du nettoyage de la base")

        # 1. Insertion des données de base sans full_name
        logger.info("➕ Insertion des membres de la famille...")
        db.session.execute(text("""
        db.session.execute(text("""
            INSERT INTO persons (
                id, first_name, last_name, friends_name, image, father_id, mother_id, 
                birth_date, death_date, birth_place, residence, external_link, image_url, 
                has_offspring, alive, death_reason, died_in_battle, known_enemies, 
                fitan, notes, photo_url, gender, short_bio, full_bio, profession, 
                full_name, father_full_name  
            ) VALUES
                (1, 'آدَمُ', 'عليه السلام', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, 'آدَمُ عليه السلام', ''),
                (2, 'شَيْثُ', 'بْنُ آدَمَ عليهما السلام', NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'شَيْثُ بْنُ آدَمَ عليهما السلام'),
                (3, 'أَنُوشُ', 'بْنُ شَيْثٍ', NULL, NULL, 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'أَنُوشُ بْنُ شَيْثٍ'),
                (4, 'قَيْنَانُ', 'بْنُ أَنُوشٍ', NULL, NULL, 3, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'قَيْنَانُ بْنُ أَنُوشٍ'),
                (5, 'مَهْلَائِيلُ', 'بْنُ قَيْنَانَ', NULL, NULL, 4, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مَهْلَائِيلُ بْنُ قَيْنَانَ'),
                (6, 'يَارَدُ', 'بْنُ مَهْلَائِيلَ', NULL, NULL, 5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'يَارَدُ بْنُ مَهْلَائِيلَ'),
                (7, 'أَخْنُوخُ', '(إِدْرِيسُ عليه السلام) بْنُ يَارَدَ', NULL, NULL, 6, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'أَخْنُوخُ (إِدْرِيسُ عليه السلام) بْنُ يَارَدَ'),
                (8, 'مَتُوشَلَخُ', 'بْنُ أَخْنُوخَ', NULL, NULL, 7, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مَتُوشَلَخُ بْنُ أَخْنُوخَ'),
                (9, 'لَامَكُ', 'بْنُ مَتُوشَلَخَ', NULL, NULL, 8, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'لَامَكُ بْنُ مَتُوشَلَخَ'),
                (10, 'نُوحٌ', 'عليه السلام بْنُ لَامَكَ', NULL, NULL, 9, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'نُوحٌ عليه السلام بْنُ لَامَكَ'),
                (11, 'سَامُ', 'بْنُ نُوحٍ', NULL, NULL, 10, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'سَامُ بْنُ نُوحٍ'),
                (12, 'أَرْفَخْشَذُ', 'بْنُ سَامٍ', NULL, NULL, 11, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'أَرْفَخْشَذُ بْنُ سَامٍ'),
                (13, 'شَالِخُ', 'بْنُ أَرْفَخْشَذَ', NULL, NULL, 12, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'شَالِخُ بْنُ أَرْفَخْشَذَ'),
                (14, 'عَابِرُ', '(هُودٌ عليه السلام) بْنُ شَالِخٍ', NULL, NULL, 13, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَابِرُ (هُودٌ عليه السلام) بْنُ شَالِخٍ'),
                (15, 'فَالَغُ', 'بْنُ عَابِرٍ', NULL, NULL, 14, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'فَالَغُ بْنُ عَابِرٍ'),
                (16, 'أَرْغُو', 'بْنُ فَالِغٍ', NULL, NULL, 15, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'أَرْغُو بْنُ فَالِغٍ'),
                (17, 'سَارُوغُ', 'بْنُ أَرْغُوَ', NULL, NULL, 16, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'سَارُوغُ بْنُ أَرْغُوَ'),
                (18, 'نَاحُورُ', 'بْنُ سَارُوغَ', NULL, NULL, 17, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'نَاحُورُ بْنُ سَارُوغَ'),
                (19, 'تَارَحُ', '(آزَرُ) بْنُ نَاحُورَ', NULL, NULL, 18, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'تَارَحُ (آزَرُ) بْنُ نَاحُورَ'),
                (20, 'إِبْرَاهِيمُ', 'الخَلِيلُ عليه السلام بْنُ تَارَحَ', NULL, NULL, 19, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'إِبْرَاهِيمُ الخَلِيلُ عليه السلام بْنُ تَارَحَ'),
                (21, 'إِسْمَاعِيلُ', 'بْنُ إِبْرَاهِيمَ الخَلِيلِ', NULL, NULL, 20, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'إِسْمَاعِيلُ بْنُ إِبْرَاهِيمَ الخَلِيلِ'),
                (22, 'عَدْنَانُ', 'بْنُ إِسْمَاعِيل', NULL, NULL, 21, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَدْنَانُ بْنُ إِسْمَاعِيل'),
                (23, 'مَعَدُّ', 'بْنُ عَدْنَان', NULL, NULL, 22, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مَعَدُّ بْنُ عَدْنَان'),
                (24, 'نِزَارُ', 'بْنُ مَعَدٍّ', NULL, NULL, 23, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'نِزَارُ بْنُ مَعَدٍّ'),
                (25, 'مُضَرُ', 'بْنُ نِزَار', NULL, NULL, 24, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مُضَرُ بْنُ نِزَار'),
                (26, 'إِلْيَاسُ', 'بْنُ مُضَرَ', NULL, NULL, 25, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'إِلْيَاسُ بْنُ مُضَرَ'),
                (27, 'مُدْرِكَةُ', 'بْنُ إِلْيَاسَ', NULL, NULL, 26, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مُدْرِكَةُ بْنُ إِلْيَاسَ'),
                (28, 'خُزَيْمَةُ', 'بْنُ مُدْرِكَةَ', NULL, NULL, 27, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'خُزَيْمَةُ بْنُ مُدْرِكَةَ'),
                (29, 'كِنَانَة', 'بْنُ خُزَيْمَةَ', NULL, NULL, 28, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'كِنَانَة بْنُ خُزَيْمَةَ'),
                (30, 'النَّضْر', 'بْنُ كِنَانَة', NULL, NULL, 29, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'النَّضْر بْنُ كِنَانَة'),
                (31, 'مَالِك', 'بْنُ النَّضْر', NULL, NULL, 30, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مَالِك بْنُ النَّضْر'),
                (32, 'فِهْر', 'بْنُ مَالِك', NULL, NULL, 31, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'فِهْر بْنُ مَالِك'),
                (33, 'غَالِب', 'بْنُ فِهْر', NULL, NULL, 32, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'غَالِب بْنُ فِهْر'),
                (34, 'لُؤَي', 'بْنُ غَالِب', NULL, NULL, 33, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'لُؤَي بْنُ غَالِب'),
                (35, 'كَعْب', 'بْنُ لُؤَي', NULL, NULL, 34, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'كَعْب بْنُ لُؤَي'),
                (36, 'مُرَّة', 'بْنُ كَعْب', NULL, NULL, 35, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مُرَّة بْنُ كَعْب'),
                (37, 'كِلَاب', 'بْنُ مُرَّة', NULL, NULL, 36, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'كِلَاب بْنُ مُرَّة'),
                (38, 'قُصَي', 'بْنُ كِلَاب', NULL, NULL, 37, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'قُصَي بْنُ كِلَاب'),
                (39, 'عَبْدُ مَنَاف', 'بْنُ قُصَي', NULL, NULL, 38, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَبْدُ مَنَاف بْنُ قُصَي'),
                (40, 'هَاشِم', 'بْنُ عَبْدِ مَنَاف', NULL, NULL, 39, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'هَاشِم بْنُ عَبْدِ مَنَاف'),
                (41, 'عَبْدُ الْمُطَّلِب', 'بْنُ هَاشِم', NULL, NULL, 40, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَبْدُ الْمُطَّلِب بْنُ هَاشِم'),
                (42, 'أَبُو طَالِب', 'عَمُّ الرَّسُولِ مُحَمَّدٍ بْنُ عَبْدِ الْمُطَّلِب', NULL, NULL, 41, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'أَبُو طَالِب عَمُّ الرَّسُولِ مُحَمَّدٍ بْنُ عَبْدِ الْمُطَّلِب'),
                (43, 'فَاطِمَة', 'بِنْتُ أَسَد', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'female', NULL, NULL, NULL, NULL, 'فَاطِمَة بِنْتُ أَسَد'),
                (44, 'عَلِي', 'بْنُ أَبِي طَالِب', NULL, NULL, 42, 43, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَلِي بْنُ أَبِي طَالِب'),
                (45, 'الحَسَن السِّبْط', 'بْنُ عَلِي', NULL, NULL, 44, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'الحَسَن السِّبْط بْنُ عَلِي'),
                (46, 'حُسَيْن', 'بْنُ عَلِي', NULL, NULL, 44, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'حُسَيْن بْنُ عَلِي'),
                (47, 'عَبْدُاللَّه', 'بْنُ الحَسَن السِّبْط', NULL, NULL, 45, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَبْدُاللَّه بْنُ الحَسَن السِّبْط'),
                (48, 'فَاطِمَة', 'بِنْتُ الحَسَن السِّبْط', NULL, NULL, 45, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'female', NULL, NULL, NULL, NULL, 'فَاطِمَة بِنْتُ الحَسَن السِّبْط'),
                (49, 'عَلِي', 'بْنُ عَبْدُاللَّه', NULL, NULL, 47, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَلِي بْنُ عَبْدُاللَّه'),
                (50, 'زَيْنَب', 'بِنْتُ عَبْدُاللَّه', NULL, NULL, 47, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'female', NULL, NULL, NULL, NULL, 'زَيْنَب بِنْتُ عَبْدُاللَّه'),
                (51, 'الحسن المُثَنَّى', 'بْنُ الحَسَن السِّبْط', NULL, NULL, 45, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'الحسن المُثَنَّى بْنُ الحَسَن السِّبْط'),
                (52, 'عَبْدُاللَّه الكَامل', 'بْنُ الحَسَن المُثَنَّى', NULL, NULL, 51, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَبْدُاللَّه الكَامل بْنُ الحَسَن المُثَنَّى'),
                (53, 'مولاَي إِدْرَيس الأَوَّل', 'بْنُ عَبْدُاللَّه الكَامل', NULL, NULL, 52, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مولاَي إِدْرَيس الأَوَّل بْنُ عَبْدُاللَّه الكَامل'),
                (54, 'مولاَي إِدْرَيس الثَّانِي', 'بْنُ مولاَي إِدْرَيس الأَوَّل', NULL, NULL, 53, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مولاَي إِدْرَيس الثَّانِي بْنُ مولاَي إِدْرَيس الأَوَّل'),
                (55, 'مُحَمَّد', 'بْنُ إِدْرَيس الثَّانِي', NULL, NULL, 54, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مُحَمَّد بْنُ إِدْرَيس الثَّانِي'),
                (56, 'أَحْمَد', 'بْنُ مُحَمَّد', NULL, NULL, 55, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'أَحْمَد بْنُ مُحَمَّد'),
                (57, 'إِسْحَاق', 'بْنُ أَحْمَد', NULL, NULL, 56, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'إِسْحَاق بْنُ أَحْمَد'),
                (58, 'عَلِي', 'بْنُ إِسْحَاق', NULL, NULL, 57, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَلِي بْنُ إِسْحَاق'),
                (59, 'عَبْدُالرَّحْمَن', 'بْنُ عَلِيٍّ بْنِ إِسْحَاق', NULL, NULL, 58, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَبْدُالرَّحْمَن بْنُ عَلِيٍّ بْنِ إِسْحَاق'),
                (60, 'عِيسَى', 'بْنُ عَبْدُالرَّحْمَن الْوَدْغِيرِي', NULL, NULL, 59, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عِيسَى بْنُ عَبْدُالرَّحْمَن الْوَدْغِيرِي'),
                (61, 'مَنْصُور', 'بْنُ عِيسَى', NULL, NULL, 60, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مَنْصُور بْنُ عِيسَى'),
                (62, 'عَلِي', 'بْنُ مَنْصُور', NULL, NULL, 61, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَلِي بْنُ مَنْصُور'),
                (63, 'عَبْدُ الْإِلَه', 'بْنُ عَلِي', NULL, NULL, 62, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَبْدُ الْإِلَه بْنُ عَلِي'),
                (64, 'مُحَمَّد', 'بْنُ عَبْدُالْإِلَه', NULL, NULL, 63, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'مُحَمَّد بْنُ عَبْدُالْإِلَه'),
                (65, 'سَعِيد', 'بْنُ مُحَمَّد', NULL, NULL, 64, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'سَعِيد بْنُ مُحَمَّد'),
                (66, 'أَبُو بَكْر', 'بْنُ سَعِيد', NULL, NULL, 65, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'أَبُو بَكْر بْنُ سَعِيد'),
                (67, 'عَلِي', 'بْنُ أَبِي بَكْر', NULL, NULL, 66, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'عَلِي بْنُ أَبِي بَكْر'),
                (68, 'أَبُو يَحْيَى البصِير', 'بْنُ عَلِي', NULL, NULL, 67, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'male', NULL, NULL, NULL, NULL, 'أَبُو يَحْيَى البصِير بْنُ عَلِي')
        """))
    
        db.session.commit()
        logger.info("✅ Données insérées sans calcul")
    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Erreur : {str(e)}")
        raise
    
from flask import has_app_context

def full_initialize():
    if has_app_context():
        initialize_data()
    else:
        from family_tree.app.factory import create_app
        app = create_app()
        with app.app_context():
            initialize_data()

print("✅ full_initialize() a inséré X personnes")


if __name__ == '__main__':
    print("⚠ Utilisez 'flask init-db' ou appelez full_initialize()")
