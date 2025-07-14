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
                (102, 'مُحَمَّدٌ', 'السَّادِسُ', NULL, NULL, 3, NULL, '1963-08-21', NULL, 'الرباط', 'المغرب', NULL, NULL, true, true, NULL, false, NULL, NULL, 'ملك المغرب الحالي', NULL, 'male', 'ملك المغرب منذ 1999', NULL, 'رجل دولة', 'مُحَمَّدٌ السَّادِسُ بن الحَسَنِ', 'الحَسَنُ الثَّانِي'),
                (101, 'الحَسَنُ', 'الثَّانِي', NULL, NULL, 4, NULL, '1929-07-09', '1999-07-23', 'الرباط', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'قاد المسيرة الخضراء', NULL, 'male', 'ملك المغرب 1961-1999', NULL, 'رجل دولة', 'الحَسَنُ الثَّانِي بن مُحَمَّدٍ', 'مُحَمَّدٌ الخَامِسُ'),
                (100, 'مُحَمَّدٌ', 'الخَامِسُ', NULL, NULL, 5, NULL, '1909-08-10', '1961-02-26', 'فاس', 'المغرب', NULL, NULL, true, false, 'مرض', false, NULL, NULL, 'رمز الاستقلال', NULL, 'male', 'ملك المغرب 1927-1961', NULL, 'رجل دولة', 'مُحَمَّدٌ الخَامِسُ بن يُوسُفَ', 'يُوسُفُ بن الحَسَنِ'),
                (99, 'يُوسُفُ', 'بن الحَسَنِ', NULL, NULL, 6, NULL, '1882-01-01', '1927-11-17', 'مكناس', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'حكم تحت الحماية', NULL, 'male', 'سلطان المغرب 1912-1927', NULL, 'حاكم', 'يُوسُفُ بن الحَسَنِ', 'الحَسَنُ الأَوَّلُ'),
                (98, 'الحَسَنُ', 'الأَوَّلُ', NULL, NULL, 7, NULL, '1836-01-01', '1894-06-07', 'فاس', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'محدث الإدارة', NULL, 'male', 'سلطان المغرب 1873-1894', NULL, 'حاكم', 'الحَسَنُ الأَوَّلُ بن مُحَمَّدٍ', 'مُحَمَّدٌ الرَّابِعُ'),
                (97, 'مُحَمَّدٌ', 'الرَّابِعُ', NULL, NULL, 8, NULL, '1803-01-01', '1873-09-16', 'مراكش', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'مصلح عسكري', NULL, 'male', 'سلطان المغرب 1859-1873', NULL, 'حاكم', 'مُحَمَّدٌ الرَّابِعُ بن عَبْدِ الرَّحْمَنِ', 'عَبْدُ الرَّحْمَنِ بن هِشَامٍ'),
                (96, 'عَبْدُ', 'الرَّحْمَنِ', NULL, NULL, 9, NULL, '1778-01-01', '1859-08-28', 'مكناس', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'خاض حرب تطوان', NULL, 'male', 'سلطان المغرب 1822-1859', NULL, 'حاكم', 'عَبْدُ الرَّحْمَنِ بن هِشَامٍ', 'هِشَامُ بن مُحَمَّدٍ'),
                (95, 'هِشَامُ', 'بن مُحَمَّدٍ', NULL, NULL, 10, NULL, '1748-01-01', NULL, 'مكناس', 'المغرب', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'أمير علوي', NULL, 'male', 'أمير من الأسرة العلوية', NULL, 'أمير', 'هِشَامُ بن مُحَمَّدٍ', 'مُحَمَّدٌ الثَّالِثُ'),
                (94, 'مُحَمَّدٌ', 'الثَّالِثُ', NULL, NULL, 11, NULL, '1710-01-01', '1790-04-09', 'مكناس', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'المعروف بالخطيب', NULL, 'male', 'سلطان المغرب', NULL, 'حاكم', 'مُحَمَّدٌ الثَّالِثُ بن عَبْدِ اللهِ', 'عَبْدُ اللهِ بن إسْمَاعِيلَ'),
                (93, 'عَبْدُ', 'اللهِ', NULL, NULL, 12, NULL, '1678-01-01', '1757-11-10', 'مراكش', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'حكم متقطع', NULL, 'male', 'سلطان المغرب', NULL, 'حاكم', 'عَبْدُ اللهِ بن إسْمَاعِيلَ', 'إسْمَاعِيلُ بن الشَّرِيفِ'),
                (92, 'إسْمَاعِيلُ', 'بن الشَّرِيفِ', NULL, NULL, 13, NULL, '1645-01-01', '1727-03-22', 'سجلماسة', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'باني مدينة مكناس', NULL, 'male', 'سلطان المغرب 1672-1727', NULL, 'حاكم', 'إسْمَاعِيلُ بن الشَّرِيفِ', 'الشَّرِيفُ بن عَلِيٍّ'),
                (91, 'الشَّرِيفُ', 'بن عَلِيٍّ', NULL, NULL, 14, NULL, '1589-01-01', '1659-06-04', 'تافيلالت', 'المغرب', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'مؤسس الدولة العلوية', NULL, 'male', 'أول حاكم علوي', NULL, 'حاكم', 'الشَّرِيفُ بن عَلِيٍّ', 'عَلِيٌّ بن مُحَمَّدٍ'),
                (90, 'عَلِيٌّ', 'بن مُحَمَّدٍ', NULL, NULL, 15, NULL, '1560-01-01', NULL, 'سجلماسة', 'المغرب', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'شيخ قبيلة', NULL, 'male', 'من أجداد الأسرة العلوية', NULL, 'شيخ', 'عَلِيٌّ بن مُحَمَّدٍ', 'مُحَمَّدٌ بن عَلِيٍّ'),
                (89, 'مُحَمَّدٌ', 'بن عَلِيٍّ', NULL, NULL, 16, NULL, '1530-01-01', NULL, 'سجلماسة', 'المغرب', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'من سكان سجلماسة', NULL, 'male', 'من أجداد العلويين', NULL, 'تاجر', 'مُحَمَّدٌ بن عَلِيٍّ', 'عَلِيٌّ بن يُوسُفَ'),
                (88, 'عَلِيٌّ', 'بن يُوسُفَ', NULL, NULL, 17, NULL, '1500-01-01', NULL, 'تافيلالت', 'المغرب', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'من وجهاء تافيلالت', NULL, 'male', 'من أجداد العلويين', NULL, 'عالم', 'عَلِيٌّ بن يُوسُفَ', 'يُوسُفُ بن عَلِيٍّ'),
                (87, 'يُوسُفُ', 'بن عَلِيٍّ', NULL, NULL, 18, NULL, '1470-01-01', NULL, 'تافيلالت', 'المغرب', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'أول من استقر بالمغرب', NULL, 'male', 'من أجداد العلويين', NULL, 'تاجر', 'يُوسُفُ بن عَلِيٍّ', 'عَلِيٌّ بن الحَسَنِ'),
                (86, 'عَلِيٌّ', 'بن الحَسَنِ', NULL, NULL, 19, NULL, '1440-01-01', NULL, 'ينبع', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'حلقة الوصل', NULL, 'male', 'من أجداد العلويين', NULL, 'عالم', 'عَلِيٌّ بن الحَسَنِ', 'الحَسَنُ الدَّاخِلُ'),
                (85, 'الحَسَنُ', 'الدَّاخِلُ', NULL, NULL, 20, NULL, '1410-01-01', '1471-01-01', 'ينبع', 'الحجاز', NULL, NULL, true, false, 'naturelle', false, NULL, NULL, 'هاجر إلى المغرب', NULL, 'male', 'مؤسس الفرع المغربي', NULL, 'عالم', 'الحَسَنُ الدَّاخِلُ', 'القَاسِمُ بن مُحَمَّدٍ'),
                (84, 'القَاسِمُ', 'بن مُحَمَّدٍ', NULL, NULL, 21, NULL, '1385-01-01', NULL, 'ينبع', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'من أعيان ينبع', NULL, 'male', 'من أشراف الحجاز', NULL, 'عالم', 'القَاسِمُ بن مُحَمَّدٍ', 'مُحَمَّدٌ بن أَبِي القَاسِمِ'),
                (83, 'مُحَمَّدٌ', 'بن أَبِي القَاسِمِ', NULL, NULL, 22, NULL, '1360-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'عالم دين', NULL, 'male', 'من علماء المدينة', NULL, 'عالم', 'مُحَمَّدٌ بن أَبِي القَاسِمِ', 'أَبُو القَاسِمِ بن مُحَمَّدٍ'),
                (82, 'أَبُو', 'القَاسِمِ', NULL, NULL, 23, NULL, '1335-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'تاجر', NULL, 'male', 'من سكان المدينة', NULL, 'تاجر', 'أَبُو القَاسِمِ بن مُحَمَّدٍ', 'مُحَمَّدٌ بن الحَسَنِ'),
                (81, 'مُحَمَّدٌ', 'بن الحَسَنِ', NULL, NULL, 24, NULL, '1310-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'قاضٍ', NULL, 'male', 'قاضي المدينة', NULL, 'قاضٍ', 'مُحَمَّدٌ بن الحَسَنِ', 'الحَسَنُ بن عَبْدِ اللهِ'),
                (80, 'الحَسَنُ', 'بن عَبْدِ اللهِ', NULL, NULL, 25, NULL, '1285-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'محدث', NULL, 'male', 'عالم دين', NULL, 'عالم', 'الحَسَنُ بن عَبْدِ اللهِ', 'عَبْدُ اللهِ بن مُحَمَّدٍ'),
                (79, 'عَبْدُ', 'اللهِ', NULL, NULL, 26, NULL, '1260-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'شيخ قبيلة', NULL, 'male', 'من أشراف الحجاز', NULL, 'شيخ', 'عَبْدُ اللهِ بن مُحَمَّدٍ', 'مُحَمَّدٌ بن عَرَفَةَ'),
                (78, 'مُحَمَّدٌ', 'بن عَرَفَةَ', NULL, NULL, 27, NULL, '1235-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'خادم المسجد', NULL, 'male', 'من خدم المسجد النبوي', NULL, 'خادم', 'مُحَمَّدٌ بن عَرَفَةَ', 'عَرَفَةُ بن الحَسَنِ'),
                (77, 'عَرَفَةُ', 'بن الحَسَنِ', NULL, NULL, 28, NULL, '1210-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'تاجر إبل', NULL, 'male', 'تاجر بين الحجاز ونجد', NULL, 'تاجر', 'عَرَفَةُ بن الحَسَنِ', 'الحَسَنُ بن أَبِي بَكْرٍ'),
                (76, 'الحَسَنُ', 'بن أَبِي بَكْرٍ', NULL, NULL, 29, NULL, '1185-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'عالم أنساب', NULL, 'male', 'عالم بالأنساب', NULL, 'عالم', 'الحَسَنُ بن أَبِي بَكْرٍ', 'أَبُو بَكْرٍ بن عَلِيٍّ'),
                (75, 'أَبُو', 'بَكْرٍ', NULL, NULL, 30, NULL, '1160-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'مقيم بضواحي المدينة', NULL, 'male', 'من سكان المدينة', NULL, 'مزارع', 'أَبُو بَكْرٍ بن عَلِيٍّ', 'عَلِيٌّ بن الحَسَنِ'),
                (74, 'عَلِيٌّ', 'بن الحَسَنِ', NULL, NULL, 31, NULL, '1135-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'معلم قرآن', NULL, 'male', 'معلم للأطفال', NULL, 'معلم', 'عَلِيٌّ بن الحَسَنِ', 'الحَسَنُ بن أَحْمَدَ'),
                (73, 'الحَسَنُ', 'بن أَحْمَدَ', NULL, NULL, 32, NULL, '1110-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'تاجر توابل', NULL, 'male', 'تاجر بين الحجاز واليمن', NULL, 'تاجر', 'الحَسَنُ بن أَحْمَدَ', 'أَحْمَدُ بن إسْمَاعِيلَ'),
                (72, 'أَحْمَدُ', 'بن إسْمَاعِيلَ', NULL, NULL, 33, NULL, '1085-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'قائد قافلة', NULL, 'male', 'قائد قوافل الحجاج', NULL, 'قائد', 'أَحْمَدُ بن إسْمَاعِيلَ', 'إسْمَاعِيلُ بن القَاسِمِ'),
                (71, 'إسْمَاعِيلُ', 'بن القَاسِمِ', NULL, NULL, 34, NULL, '1060-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'مقاوم للعباسيين', NULL, 'male', 'من المعارضين للعباسيين', NULL, 'ثائر', 'إسْمَاعِيلُ بن القَاسِمِ', 'القَاسِمُ بن مُحَمَّدٍ'),
                (70, 'القَاسِمُ', 'بن مُحَمَّدٍ', NULL, NULL, 35, NULL, '1035-01-01', NULL, 'المدينة', 'الحجاز', NULL, NULL, true, NULL, NULL, NULL, NULL, NULL, 'راوي حديث', NULL, 'male', 'من رواة الحديث', NULL, 'عالم', 'القَاسِمُ بن مُحَمَّدٍ', 'مُحَمَّدٌ النَّفْسُ الزَّكِيَّةُ'),
                (69, 'مُحَمَّدٌ', 'النَّفْسُ الزَّكِيَّةُ', NULL, NULL, 36, NULL, '0722-01-01', '0762-01-01', 'المدينة', 'الحجاز', NULL, NULL, true, false, 'استشهاد', true, 'العباسيون', NULL, 'قائد الثورة', NULL, 'male', 'ثائر ضد العباسيين', NULL, 'ثائر', 'مُحَمَّدٌ النَّفْسُ الزَّكِيَّةُ', 'عَبْدُ اللهِ الكَامِل')

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
