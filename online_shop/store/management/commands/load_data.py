import pandas as pd
import re
from django.core.management.base import BaseCommand
from store.models import Category, Product


class Command(BaseCommand):
    help = 'Load data from Excel file into the database'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str,
                            help='Path to the Excel file')

    def handle(self, *args, **kwargs):
        excel_file_path = kwargs['excel_file']
        # Step 1: Process the Excel file and save it as a CSV
        df = self.process_excel_file(excel_file_path)
        csv_file_path = excel_file_path.replace('.xls', '.csv')
        df.to_csv(csv_file_path, index=False)

        # Step 2: Load data from the CSV file into the database
        self.load_data_to_db(csv_file_path)

        self.stdout.write(self.style.SUCCESS(
            'Data successfully processed and loaded from %s' % excel_file_path))

    def process_excel_file(self, file_path):
        # Загрузка файла Excel, пропуская начальные строки, которые не являются частью данных
        df = pd.read_excel(file_path, skiprows=4)
        df.columns = ['Номенклатура', '', 'Артикул', 'Цена', 'Закупочная цена',
                      'Остаток', 'Стоимость остатка', 'Розн. сумма остатка', 'Процент']

        # Функция для извлечения артикула из номенклатуры
        def extract_article(nomenclature):
            match = re.search(r'\(([\d-]+)\)$', nomenclature)
            if match:
                return match.group(1)
            return None

        # Предварительная обработка столбца "Номенклатура"
        df['Номенклатура'] = df['Номенклатура'].str.replace(
            r'^\d+\s*\|\s*', '', regex=True)
        df['Артикул'] = df['Номенклатура'].apply(extract_article)
        df['Номенклатура'] = df['Номенклатура'].str.replace(
            r'\s*\(\d+\)$', '', regex=True)
        df['Номенклатура'] = df['Номенклатура'].str.replace(
            r'\s*\([\d-]+\)$', '', regex=True)

        # Удаление пустых столбцов
        df = df.dropna(axis=1, how='all')

        # Инициализация столбца для категорий
        df['Категория'] = None

        # Переменная для хранения текущей категории
        current_category = None

        # Заполнение столбца "Категория" на основе строк категорий
        for index, row in df.iterrows():
            if pd.isna(row['Цена']) and pd.isna(row['Закупочная цена']):
                current_category = row['Номенклатура']
            df.at[index, 'Категория'] = current_category

        # Удаление строк с пустыми значениями в столбцах "Артикул", "Цена" и "Закупочная цена"
        df = df.dropna(subset=['Артикул', 'Цена', 'Закупочная цена'])

        # Удаление строк, у которых значение в столбце "Категория" равно "Архив" или "АРХИВ 2"
        df = df[~df['Категория'].isin(['Архив', 'АРХИВ 2'])]

        return df

    def load_data_to_db(self, csv_file_path):
        # Загрузка данных из CSV файла в DataFrame
        df = pd.read_csv(csv_file_path)

        for index, row in df.iterrows():
            # Получаем или создаем категорию
            category_name = row['Категория']
            category, created = Category.objects.get_or_create(
                name=category_name)

            # Создаем или обновляем продукт
            product, created = Product.objects.update_or_create(
                article_number=row['Артикул'],
                defaults={
                    'name': row['Номенклатура'],
                    'price': row['Цена'],
                    'purchase_price': row['Закупочная цена'],
                    'remains': row['Остаток'],
                    'remains_cost': row['Стоимость остатка'],
                    'retail_remains_cost': row['Розн. сумма остатка'],
                    'percent': row['Процент'],
                    'category': category
                }
            )
