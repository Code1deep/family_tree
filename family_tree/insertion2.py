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
                (69, 'مُحَمَّدٌ', 'النَّفْسُ الزَّكِيَّةُ', NULL, NULL, 52, NULL, '0722-01-01', '0762-01-01', 'المدينة', 'الحجاز', NULL, NULL, true, false, 'استشهاد', true, 'العباسيون', NULL, 'قائد الثورة', NULL, 'male', 'ثائر ضد العباسيين', NULL, 'عالم', NULL, 'مُحَمَّد النَّفْسُ الزَّكِيَّة'),
                (70, 'القَاسِمُ', 'بْنُ مُحَمَّدٍ', NULL, NULL, 69, NULL, '1035-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'راوي حديث', NULL, 'male', 'من رواة الحديث', NULL, 'عالم', NULL, 'القَاسِمُ بن مُحَمَّدٍ'),
                (71, 'إسْمَاعِيلُ', 'بْنُ القَاسِمِ', NULL, NULL, 70, NULL, '1060-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'مقاوم للعباسيين', NULL, 'male', 'من المعارضين للعباسيين', NULL, 'عالم', NULL, 'إسْمَاعِيلُ بن القَاسِمِ'),
                (72, 'أَحْمَدُ', 'بْنُ إسْمَاعِيلَ', NULL, NULL, 71, NULL, '1085-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'قائد قافلة', NULL, 'male', 'قائد قوافل الحجاج', NULL, 'قائد',  NULL, 'أَحْمَدُ بن إسْمَاعِيلَ'),
                (73, 'الحَسَنُ', 'بْنُ أَحْمَدَ', NULL, NULL, 72, NULL, '1110-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'تاجر توابل', NULL, 'male', 'تاجر بين الحجاز واليمن', NULL, 'تاجر', NULL, 'الحَسَنُ بن أَحْمَدَ'),
                (74, 'عَلِيٌّ', 'بْنُ الحَسَنِ', NULL, NULL, 73, NULL, '1135-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'معلم قرآن', NULL, 'male', 'معلم للأطفال', NULL, 'معلم', NULL, 'عَلِيٌّ بن الحَسَنِ'),
                (75, 'أَبُو', ' بَكْرٍ بن عَلِيٍّ', NULL, NULL, 74, NULL, '1160-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'مقيم بضواحي المدينة', NULL, 'male', 'من سكان المدينة', NULL, 'مزارع', NULL, 'أَبُو بَكْرٍ بن عَلِيٍّ'),
                (76, 'الحَسَنُ ', 'بْنُ أَبِي بَكْرٍ', NULL, NULL, 75, NULL, '1185-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'عالم أنساب', NULL, 'male', 'عالم بالأنساب', NULL, 'عالم', NULL, 'الحَسَنُ بن أَبِي بَكْرٍ'),
                (77, 'عَرَفَةُ ', 'بْنُ الحَسَنِ', NULL, NULL, 76, NULL, '1210-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'تاجر إبل', NULL, 'male', 'تاجر بين الحجاز ونجد', NULL, 'تاجر', NULL, 'عَرَفَةُ بن الحَسَنِ'),
                (78, 'مُحَمَّدٌ ', 'بْنُ عَرَفَةَ', NULL, NULL, 77, NULL, '1235-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'خادم المسجد', NULL, 'male', 'من خدم المسجد النبوي', NULL, 'خادم', NULL, 'مُحَمَّدٌ بن عَرَفَةَ'),
                (79, 'عَبْدُ ', 'اللهِ بن مُحَمَّدٍ', NULL, NULL, 78, NULL, '1260-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'شيخ قبيلة', NULL, 'male', 'من أشراف الحجاز', NULL, 'شيخ', NULL, 'عَبْدُ اللهِ بن مُحَمَّدٍ'),
                (80, 'الحَسَنُ', 'بْنُ عَبْدِ اللهِ', NULL, NULL, 79, NULL, '1285-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'محدث', NULL, 'male', 'عالم دين', NULL, 'عالم', NULL, 'الحَسَنُ بن عَبْدِ اللهِ'),
                (81, 'مُحَمَّدٌ', 'بْنُ الحَسَنِ', NULL, NULL, 80, NULL, '1310-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'قاضٍ', NULL, 'male', 'قاضي المدينة', NULL, 'قاضٍ', NULL, 'مُحَمَّدٌ بن الحَسَنِ'),
                (82, 'أَبُو', ' القَاسِمِ بن مُحَمَّدٍ', NULL, NULL, 81, NULL, '1335-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'تاجر', NULL, 'male', 'من سكان المدينة', NULL, 'تاجر', NULL, 'أَبُو القَاسِمِ بن مُحَمَّدٍ'),
                (83, 'مُحَمَّدٌ', ' بْنُ أَبِي القَاسِمِ', NULL, NULL, 82, NULL, '1360-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'عالم دين', NULL, 'male', 'من علماء المدينة', NULL, 'عالم', NULL, 'أَبُو القَاسِمِ بن مُحَمَّدٍ'),
                (84, 'القَاسِمُ', ' بْنُ مُحَمَّدٍ', NULL, NULL, 83, NULL, '1385-01-01', NULL, 'ينبع', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'من أعيان ينبع', NULL, 'male', 'من أشراف الحجاز', NULL, 'عالم',NULL, 'مُحَمَّدٌ بْنُ أَبِي القَاسِمِ'),
                (85, 'الحَسَنُ', ' الدَّاخِلُ', NULL, NULL, 84, NULL, '1410-01-01', '1471-01-01', 'ينبع', 'الحجاز', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'هاجر إلى المغرب', NULL, 'male', 'مؤسس الفرع المغربي', NULL, 'عالم', NULL, 'الحَسَنُ الدَّاخِلُ'),
                (86, 'عَلِيٌّ', ' بْنُ الحَسَنِ', NULL, NULL, 85, NULL, '1440-01-01', NULL, 'ينبع', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'حلقة الوصل', NULL, 'male', 'من أجداد العلويين', NULL, 'عالم', NULL, 'عَلِيٌّ بن الحَسَنِ'),
                (87, 'يُوسُفُ', ' بْنُ عَلِيٍّ', NULL, NULL, 86, NULL, '1470-01-01', NULL, 'تافيلالت', 'المغرب', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'أول من استقر بالمغرب', NULL, 'male', 'من أجداد العلويين', NULL, 'تاجر', NULL, 'يُوسُفُ بن عَلِيٍّ'),
                (88, 'عَلِيٌّ', ' بْنُ يُوسُفَ', NULL, NULL, 87, NULL, '1500-01-01', NULL, 'تافيلالت', 'المغرب', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'من وجهاء تافيلالت', NULL, 'male', 'من أجداد العلويين', NULL, 'عالم', NULL, 'عَلِيٌّ بن يُوسُفَ'),
                (89, 'مُحَمَّدٌ', ' بْنُ عَلِيٍّ', NULL, NULL, 88, NULL, '1530-01-01', NULL, 'سجلماسة', 'المغرب', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'من سكان سجلماسة', NULL, 'male', 'من أجداد العلويين', NULL, 'تاجر', NULL, 'مُحَمَّدٌ بن عَلِيٍّ'),
                (90, 'عَلِيٌّ', ' بْنُ مُحَمَّدٍ', NULL, NULL, 89, NULL, '1560-01-01', NULL, 'سجلماسة', 'المغرب', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'شيخ قبيلة', NULL, 'male', 'من أجداد الأسرة العلوية', NULL, 'شيخ', NULL, 'عَلِيٌّ بن مُحَمَّدٍ'),
                (91, 'الشَّرِيفُ', ' بْنُ عَلِيٍّ', NULL, NULL, 90, NULL, '1589-01-01', '1659-06-04', 'تافيلالت', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'مؤسس الدولة العلوية', NULL, 'male', 'أول حاكم علوي', NULL, 'حاكم', NULL, 'الشَّرِيفُ بن عَلِيٍّ'),
                (92, 'إسْمَاعِيلُ', ' بْنُ الشَّرِيفِ', NULL, NULL, 91, NULL, '1645-01-01', '1727-03-22', 'سجلماسة', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'باني مدينة مكناس', NULL, 'male', 'سلطان المغرب 1672-1727', NULL, 'حاكم', NULL, 'إسْمَاعِيلُ بن الشَّرِيفِ'),
                (93, 'عَبْدُ ', 'اللهِ بن إسْمَاعِيل', NULL, NULL, 92, NULL, '1678-01-01', '1757-11-10', 'مراكش', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'حكم متقطع', NULL, 'male', 'سلطان المغرب', NULL, 'حاكم', NULL, 'عَبْدُ اللهِ بن إسْمَاعِيل'),
                (94, 'مُحَمَّدٌ', ' الثَّالِثُ بن عَبْدِ اللهِ', NULL, NULL, 93, NULL, '1710-01-01', '1790-04-09', 'مكناس', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'المعروف بالخطيب', NULL, 'male', 'سلطان المغرب', NULL, 'حاكم', NULL, 'مُحَمَّدٌ الثَّالِثُ بن عَبْدِ اللهِ'),
                (95, 'هِشَامُ ', 'بْنُ مُحَمَّدٍ', NULL, NULL, 94, NULL, '1748-01-01', NULL, 'مكناس', 'المغرب', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'أمير علوي', NULL, 'male', 'أمير من الأسرة العلوية', NULL, 'أمير', NULL, 'هِشَامُ بن مُحَمَّدٍ'),
                (96, 'عَبْدِ الرَّحْمَن ', 'بن هِشَام', NULL, NULL, 95, NULL, '1778-01-01', '1859-08-28', 'مكناس', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'خاض حرب تطوان', NULL, 'male', 'سلطان المغرب 1822-1859', NULL, 'حاكم',  NULL, 'عَبْدُ الرَّحْمَنِ بن هِشَامٍ'),
                (97, 'مُحَمَّد الرَّابِع ', 'بن عَبْدِ الرَّحْمَن', NULL, NULL, 96, NULL, '1803-01-01', '1873-09-16', 'مراكش', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'مصلح عسكري', NULL, 'male', 'سلطان المغرب 1859-1873', NULL, 'حاكم', NULL, 'مُحَمَّدٌ الرَّابِعُ بن عَبْدِ الرَّحْمَنِ'),
                (98, 'الحَسَنُ ', 'الأَوَّلُ', NULL, NULL, 97, NULL, '1836-01-01', '1894-06-07', 'فاس', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'محدث الإدارة', NULL, 'male', 'سلطان المغرب 1873-1894', NULL, 'حاكم', NULL, 'الحَسَنُ الأَوَّلُ بن مُحَمَّدٍ'),
                (99, 'يُوسُفُ ', 'بْنُ الحَسَنِ', NULL, NULL, 98, NULL, '1882-01-01', '1927-11-17', 'مكناس', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'حكم تحت الحماية', NULL, 'male', 'سلطان المغرب 1912-1927', NULL, 'حاكم', NULL, 'يُوسُفُ بْنُ الحَسَن'),
                (100, 'مُحَمَّدٌ ', 'الخَامِسُ', NULL, NULL, 99, NULL, '1909-08-10', '1961-02-26', 'فاس', 'المغرب', NULL, NULL, true, false, 'مرض', false, NULL, NULL, 'رمز الاستقلال', NULL, 'male', 'ملك المغرب 1927-1961', NULL, 'رجل دولة', NULL, 'مُحَمَّد الخَامِس'),
                (101, 'الحَسَنُ ', 'الثَّانِي', NULL, NULL, 100, NULL, '1929-07-09', '1999-07-23', 'الرباط', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'قاد المسيرة الخضراء', NULL, 'male', 'ملك المغرب 1961-1999', NULL, 'رجل دولة', NULL, 'الحَسَنُ الثَّانِي'),
                (102, 'مُحَمَّدٌ ', 'السَّادِسُ', NULL, NULL, NULL, 101, NULL, '1963-08-21', NULL, 'الرباط', 'المغرب', NULL, NULL, true, true, NULL, false, NULL, NULL, 'ملك المغرب الحالي', NULL, 'male', 'ملك المملكة المغربية منذ عام 1999', NULL, 'رجل دولة', NULL, 'مُحَمَّدٌ السَّادِسُ  ),
                (102, 'مُحَمَّدٌ ', 'السَّادِسُ', NULL, NULL, 101, NULL, '1963-08-21', NULL, 'الرباط', 'المغرب', NULL, NULL, true, true, NULL, false, NULL, NULL, 'ملك المغرب الحالي', NULL, 'male', 'ملك المغرب depuis 1999', NULL, 'رجل دولة', NULL, 'الحَسَنُ الثَّانِي بن مُحَمَّدٍ'),
                (103, 'مولاَي الحَسَن ', 'بنُ مُحَمَّدٌ السَّادِس ', NULL, NULL, 102, NULL, '2003-03-08', NULL, 'الرباط', 'المغرب', NULL, NULL, true, true, NULL, false, NULL, NULL, 'ولِيُّ العَهْد الحالي', NULL, 'male', 'ولِيُّ العَهْد', NULL, 'رجل دولة', NULL, 'مولاَي الحَسَن بنُ مُحَمَّدٌ السَّادِسُ'),
                
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
