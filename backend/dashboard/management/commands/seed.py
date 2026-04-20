"""
management command: python manage.py seed
creates sample data so the full UI can be verified right after setup.
"""
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone


class Command(BaseCommand):
    help = "seed the database with sample data"

    @transaction.atomic
    def handle(self, *args, **options):
        from accounts.models import User
        from members.models import Member
        from staff.models import Trainer
        from horses.models import Horse, HealthRecord
        from lessons.models import Lesson
        from billing.models import MembershipPlan, Membership, Invoice

        self.stdout.write("seeding database...")

        # ── admin ────────────────────────────────────────────────────────────
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "first_name": "Club",
                "last_name": "Admin",
                "email": "admin@herradura.local",
                "role": User.Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin.set_password("admin1234")
        admin.save()
        self.stdout.write("  admin user: admin / admin1234")

        # ── trainers ─────────────────────────────────────────────────────────
        trainer_data = [
            ("sophia_trainer", "Sophia", "Martinez", "sophia@herradura.local", "Dressage"),
            ("james_trainer", "James", "Walker", "james@herradura.local", "Show Jumping"),
            ("elena_trainer", "Elena", "Rossi", "elena@herradura.local", "Western Riding"),
        ]
        trainers = []
        for username, first, last, email, spec in trainer_data:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "email": email,
                    "role": User.Role.TRAINER,
                },
            )
            user.set_password("trainer1234")
            user.save()
            trainer, _ = Trainer.objects.get_or_create(user=user, defaults={"specialisation": spec})
            trainers.append(trainer)
        self.stdout.write(f"  {len(trainers)} trainers created")

        # ── members ──────────────────────────────────────────────────────────
        member_data = [
            ("alice_m", "Alice", "Johnson", Member.SkillLevel.BEGINNER),
            ("bob_m", "Bob", "Smith", Member.SkillLevel.INTERMEDIATE),
            ("carol_m", "Carol", "Davis", Member.SkillLevel.ADVANCED),
            ("david_m", "David", "Wilson", Member.SkillLevel.BEGINNER),
            ("emma_m", "Emma", "Brown", Member.SkillLevel.INTERMEDIATE),
            ("frank_m", "Frank", "Taylor", Member.SkillLevel.BEGINNER),
            ("grace_m", "Grace", "Anderson", Member.SkillLevel.ADVANCED),
            ("henry_m", "Henry", "Thomas", Member.SkillLevel.INTERMEDIATE),
            ("isla_m", "Isla", "Moore", Member.SkillLevel.BEGINNER),
            ("jack_m", "Jack", "White", Member.SkillLevel.INTERMEDIATE),
        ]
        members = []
        for username, first, last, skill in member_data:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "email": f"{username}@herradura.local",
                    "role": User.Role.MEMBER,
                },
            )
            user.set_password("member1234")
            user.save()
            member, _ = Member.objects.get_or_create(
                user=user,
                defaults={
                    "skill_level": skill,
                    "date_of_birth": date(1990, 1, 1),
                    "emergency_contact_name": "Emergency Contact",
                    "emergency_contact_phone": "+1 555 000 0000",
                },
            )
            members.append(member)
        self.stdout.write(f"  {len(members)} members created")

        # ── horses ───────────────────────────────────────────────────────────
        horse_data = [
            ("Thunder", "Thoroughbred", "bay", date(2015, 3, 10), Horse.Status.AVAILABLE),
            ("Luna", "Arabian", "grey", date(2017, 7, 22), Horse.Status.AVAILABLE),
            ("Blaze", "Quarter Horse", "chestnut", date(2014, 5, 5), Horse.Status.AVAILABLE),
            ("Shadow", "Friesian", "black", date(2016, 11, 30), Horse.Status.RESTING),
            ("Duchess", "Warmblood", "dun", date(2018, 2, 14), Horse.Status.AVAILABLE),
            ("Apollo", "Hanoverian", "bay", date(2013, 9, 18), Horse.Status.AVAILABLE),
        ]
        horses = []
        for name, breed, color, dob, status in horse_data:
            horse, _ = Horse.objects.get_or_create(
                name=name,
                defaults={"breed": breed, "color": color, "date_of_birth": dob, "status": status},
            )
            horses.append(horse)

        # sample health records
        if horses:
            HealthRecord.objects.get_or_create(
                horse=horses[0],
                record_type=HealthRecord.RecordType.VET,
                date=date.today() - timedelta(days=30),
                defaults={
                    "description": "Annual health check — all clear.",
                    "performed_by": "Dr. Rivera",
                    "next_due_date": date.today() + timedelta(days=335),
                },
            )
            HealthRecord.objects.get_or_create(
                horse=horses[0],
                record_type=HealthRecord.RecordType.VACCINATION,
                date=date.today() - timedelta(days=60),
                defaults={
                    "description": "Flu & tetanus booster",
                    "performed_by": "Dr. Rivera",
                    "next_due_date": date.today() + timedelta(days=305),
                },
            )
        self.stdout.write(f"  {len(horses)} horses created")

        # ── membership plans ─────────────────────────────────────────────────
        plans_data = [
            ("Starter", MembershipPlan.BillingCycle.MONTHLY, 49.00, 4),
            ("Regular", MembershipPlan.BillingCycle.MONTHLY, 89.00, 8),
            ("Premium", MembershipPlan.BillingCycle.MONTHLY, 149.00, None),
            ("Quarterly Basic", MembershipPlan.BillingCycle.QUARTERLY, 120.00, 10),
            ("Annual Unlimited", MembershipPlan.BillingCycle.ANNUAL, 999.00, None),
        ]
        plans = []
        for name, cycle, price, lessons_per in plans_data:
            plan, _ = MembershipPlan.objects.get_or_create(
                name=name,
                defaults={
                    "billing_cycle": cycle,
                    "price": price,
                    "lessons_per_cycle": lessons_per,
                },
            )
            plans.append(plan)
        self.stdout.write(f"  {len(plans)} membership plans created")

        # ── memberships + invoices ───────────────────────────────────────────
        today = date.today()
        for i, member in enumerate(members[:6]):
            plan = plans[i % len(plans)]
            membership, created = Membership.objects.get_or_create(
                member=member,
                plan=plan,
                defaults={
                    "start_date": today - timedelta(days=15),
                    "end_date": today + timedelta(days=15),
                    "status": Membership.Status.ACTIVE,
                },
            )
            if created:
                Invoice.objects.create(
                    membership=membership,
                    amount=plan.price,
                    due_date=today,
                    status=Invoice.Status.PENDING,
                )
        self.stdout.write("  memberships and invoices created")

        # ── lessons ──────────────────────────────────────────────────────────
        lesson_titles = [
            "Beginner Walk & Trot",
            "Intermediate Canter",
            "Advanced Dressage",
            "Jump Training",
            "Western Horsemanship",
            "Trail Riding Prep",
            "Balance & Posture",
            "Group Hack",
        ]
        available_horses = [h for h in horses if h.status == Horse.Status.AVAILABLE]
        for i in range(20):
            start = timezone.now() + timedelta(days=i % 14, hours=8 + (i % 4) * 2)
            end = start + timedelta(hours=1)
            trainer = trainers[i % len(trainers)]
            horse = available_horses[i % len(available_horses)] if available_horses else None
            title = lesson_titles[i % len(lesson_titles)]

            lesson, created = Lesson.objects.get_or_create(
                title=title,
                start_time=start,
                defaults={
                    "end_time": end,
                    "trainer": trainer,
                    "horse": horse,
                    "status": Lesson.Status.SCHEDULED,
                },
            )
            if created and members:
                lesson.members.set(members[: 2 + (i % 3)])

        self.stdout.write("  20 lessons created")
        self.stdout.write(self.style.SUCCESS("database seeded successfully."))
