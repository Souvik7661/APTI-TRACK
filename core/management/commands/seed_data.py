"""Seed the database with sample questions."""
from django.core.management.base import BaseCommand
from core.models import Category, CompanyTag, Question
import random

class Command(BaseCommand):
    help = 'Seeds the database with 200 sample aptitude questions'

    def handle(self, *args, **options):
        self.stdout.write('Seeding categories...')
        cats = []
        for name, slug, icon, color, order in [
            ('Quantitative Aptitude', 'quantitative', '🔢', '#3b82f6', 1),
            ('Logical Reasoning', 'logical', '🧩', '#8b5cf6', 2),
            ('Verbal Ability', 'verbal', '📝', '#10b981', 3),
            ('Data Interpretation', 'data-interpretation', '📊', '#f59e0b', 4),
        ]:
            cat, _ = Category.objects.get_or_create(slug=slug, defaults={
                'name': name, 'icon': icon, 'color': color, 'order': order,
                'description': f'Practice {name} questions'
            })
            cats.append(cat)

        self.stdout.write('Seeding companies...')
        companies = []
        for name, slug in [
            ('TCS', 'tcs'), ('Infosys', 'infosys'), ('Wipro', 'wipro'),
            ('Amazon', 'amazon'), ('Cognizant', 'cognizant'), ('Accenture', 'accenture'),
            ('HCL', 'hcl'), ('Tech Mahindra', 'tech-mahindra'),
        ]:
            comp, _ = CompanyTag.objects.get_or_create(slug=slug, defaults={'name': name})
            companies.append(comp)

        self.stdout.write('Seeding 200 questions...')
        current_count = Question.objects.count()
        needed = 200 - current_count

        if needed <= 0:
            self.stdout.write(self.style.SUCCESS(f'Database already has {current_count} questions.'))
            return

        difficulties = ['easy', 'medium', 'hard']
        correct_options = ['a', 'b', 'c', 'd']

        questions_to_create = []
        for i in range(needed):
            cat = random.choice(cats)
            diff = random.choice(difficulties)
            ans = random.choice(correct_options)
            
            q = Question(
                category=cat,
                difficulty=diff,
                text=f"Sample {diff} question #{current_count + i + 1} for {cat.name}. What is the correct answer?",
                option_a="Option A",
                option_b="Option B",
                option_c="Option C",
                option_d="Option D",
                correct_answer=ans,
                explanation=f"The correct answer is {ans.upper()} because this is a generated question."
            )
            questions_to_create.append(q)

        Question.objects.bulk_create(questions_to_create)

        # Assign companies to new questions
        new_questions = list(Question.objects.order_by('-id')[:needed])
        for q in new_questions:
            # Assign 1 to 3 random companies
            num_comps = random.randint(1, 3)
            q_comps = random.sample(companies, num_comps)
            q.companies.set(q_comps)

        self.stdout.write(self.style.SUCCESS(f'Done! Created {needed} questions.'))
