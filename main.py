from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

base_url = "https://robota.ua/candidates/all/ukraine"

with open('resumes.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(['Position', 'Name', 'Location', 'Age', 'Salary', 'Experience', 'Link'])

    for page in range(1, 25):
        url = f"{base_url}?page={page}"
        driver.get(url)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        resumes = soup.find_all('a', class_='santa-no-underline')

        desired_location = "Київ"

        for resume in resumes:
                try:
                    main_block_tag = resume.find('div', class_='santa-relative santa-p-20 santa-box-border'
                                                               ' santa-flex santa'
                                                               '-justify-between santa-items-start'
                                                               ' santa-text-black-700')

                    if main_block_tag:
                        position_tag = main_block_tag.find('p', class_='santa-m-0 santa-typo-h3 santa-pb-10')
                        position = position_tag.text if position_tag else 'N/A'

                        name_tag = main_block_tag.find('p', class_='santa-pr-20 santa-typo-regular santa-truncate')
                        name = name_tag.text if name_tag else 'N/A'

                        location_tag = main_block_tag.find('div', class_='santa-flex santa-items-center '
                                                                         'santa-overflow-hidden santa-pr-20')
                        location = location_tag.find('p', class_='santa-typo-secondary santa-truncate').text \
                            if location_tag else 'N/A'

                        age_tag = main_block_tag.find('div', class_='santa-flex santa-items-center santa-space-x-10 '
                                                                    'santa-pr-20 santa-whitespace-nowrap')
                        age = age_tag.text.strip() if age_tag else 'N/A'

                        salary_tag = age_tag.find_next_sibling('div', class_='santa-flex santa-items-center'
                                                                             ' santa-space-'
                                                                             'x-10 santa-pr-20 santa-whitespace-nowrap')
                        salary = salary_tag.text.strip().replace('\xa0', '') if salary_tag else 'N/A'

                        experience_blocks = main_block_tag.find_all('p', class_='santa-mt-0 santa-mb-10'
                                                                                ' santa-typo-regular '
                                                                                'santa-text-black-700')

                        if experience_blocks:
                            all_positions = []

                            for block in experience_blocks:
                                position_and_company = block.text.strip().replace('\xa0', '')

                                experience_tag = block.find('p', class_='santa-mt-0 santa-mb-10 santa-typo-regular'
                                                                        ' santa-text-black-700')
                                experience = experience_tag.text.strip() if experience_tag else 'N/A'
                                all_positions.append([position_and_company])
                        else:
                            all_positions = ['No experience']
                        link = "https://rabota.ua" + resume['href']

                        writer.writerow([position, name, location, age, salary, all_positions, link])

                except Exception as e:
                    print(f"Error parsing resume: {e}")
                    continue
driver.quit()
