import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aptitrack.settings')
django.setup()

from core.models import Category, CompanyTag, Question
import random

def create_seed_data():
    categories = list(Category.objects.all())
    if not categories:
        Category.objects.create(name='Quantitative', slug='quantitative')
        Category.objects.create(name='Logical Reasoning', slug='logical')
        Category.objects.create(name='Verbal', slug='verbal')
        categories = list(Category.objects.all())

    companies = list(CompanyTag.objects.all())
    if not companies:
        CompanyTag.objects.create(name='Google', slug='google')
        CompanyTag.objects.create(name='Microsoft', slug='microsoft')
        CompanyTag.objects.create(name='Amazon', slug='amazon')
        CompanyTag.objects.create(name='TCS', slug='tcs')
        companies = list(CompanyTag.objects.all())

    difficulties = ['easy', 'medium', 'hard']
    correct_options = ['a', 'b', 'c', 'd']

    print(f"Creating 200 questions...")
    
    questions_to_create = []
    
    for i in range(200):
        category = random.choice(categories)
        difficulty = random.choice(difficulties)
        correct_answer = random.choice(correct_options)
        
        q = Question(
            category=category,
            difficulty=difficulty,
            text=f"This is a generated {difficulty} question #{i} for {category.name}. What is the correct answer?",
            option_a="Option A text",
            option_b="Option B text",
            option_c="Option C text",
            option_d="Option D text",
            correct_answer=correct_answer,
            explanation=f"The correct answer is {correct_answer.upper()} because this is a generated question."
        )
        questions_to_create.append(q)

    Question.objects.bulk_create(questions_to_create)
    
    # Add companies to questions
    all_questions = Question.objects.order_by('-id')[:200]
    for q in all_questions:
        # Assign 1-3 random companies
        q_companies = random.sample(companies, random.randint(1, min(3, len(companies))))
        q.companies.set(q_companies)

    print(f"Successfully added 200 questions. Total Questions now: {Question.objects.count()}")

if __name__ == '__main__':
    create_seed_data()
