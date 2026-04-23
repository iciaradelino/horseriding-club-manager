"""
management command: python manage.py seed
creates sample data so the full UI can be verified right after setup.
includes 6 months of historical data so all dashboard charts are populated.
"""
import random
from datetime import date, timedelta, datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone


def _months_ago(n, day=1):
    """return a date n months before today, clamped to a valid day."""
    today = date.today()
    month = today.month - n
    year = today.year
    while month <= 0:
        month += 12
        year -= 1
    import calendar
    day = min(day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


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
        # current active memberships (one per member)
        today = date.today()
        memberships = []
        for i, member in enumerate(members):
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
            memberships.append((member, membership, plan))
            if created:
                # pending invoice for the current cycle
                Invoice.objects.create(
                    membership=membership,
                    amount=plan.price,
                    due_date=today + timedelta(days=7),
                    status=Invoice.Status.PENDING,
                )

        # historical memberships + paid invoices spread over last 6 months
        # → populates the admin revenue bar chart and new-memberships bar chart
        invoice_count = 0
        membership_count = 0
        for months_back in range(1, 7):
            start_d = _months_ago(months_back, day=1)
            end_d = _months_ago(months_back - 1, day=28)
            paid_d = start_d + timedelta(days=3)
            # 2–4 new memberships each historical month
            slots = members[(months_back * 2) % len(members):][:4]
            for member in slots:
                plan = plans[random.randint(0, len(plans) - 1)]
                ms = Membership.objects.create(
                    member=member,
                    plan=plan,
                    start_date=start_d,
                    end_date=end_d,
                    status=Membership.Status.EXPIRED,
                )
                membership_count += 1
                Invoice.objects.create(
                    membership=ms,
                    amount=plan.price,
                    due_date=start_d,
                    status=Invoice.Status.PAID,
                    paid_date=paid_d,
                )
                invoice_count += 1

        self.stdout.write(
            f"  memberships and invoices created "
            f"(+{membership_count} historical, +{invoice_count} paid invoices)"
        )

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

        # upcoming scheduled lessons (next 2 weeks) — unchanged from before
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

        # historical completed lessons spread across the last 6 months
        # → populates member activity bar chart, horse workload doughnut,
        #   horse usage doughnut, and trainer heatmap
        completed_count = 0
        # weekday + hour combos that make the heatmap look realistic
        time_slots = [
            (0, 9), (0, 11), (0, 14),   # mon
            (1, 10), (1, 16),            # tue
            (2, 9), (2, 11), (2, 15),   # wed
            (3, 14), (3, 17),            # thu
            (4, 9), (4, 11),             # fri
            (5, 10), (5, 14), (5, 16),  # sat
        ]
        for months_back in range(1, 7):
            # pick a monday in that month to anchor the week
            anchor = _months_ago(months_back, day=7)
            # walk back to monday of that week
            anchor -= timedelta(days=anchor.weekday())
            for week_offset in range(3):  # 3 weeks of lessons per month
                week_anchor = anchor + timedelta(weeks=week_offset)
                for slot_i, (weekday, hour) in enumerate(time_slots):
                    lesson_date = week_anchor + timedelta(days=weekday)
                    if lesson_date >= today:
                        continue
                    start_dt = datetime(
                        lesson_date.year, lesson_date.month, lesson_date.day,
                        hour, 0, tzinfo=timezone.get_current_timezone()
                    )
                    end_dt = start_dt + timedelta(hours=1)
                    trainer = trainers[slot_i % len(trainers)]
                    horse = available_horses[slot_i % len(available_horses)] if available_horses else None
                    title = lesson_titles[slot_i % len(lesson_titles)]

                    lesson = Lesson.objects.create(
                        title=title,
                        start_time=start_dt,
                        end_time=end_dt,
                        trainer=trainer,
                        horse=horse,
                        status=Lesson.Status.COMPLETED,
                    )
                    # assign 2–4 members, rotating so each member gets history
                    offset = (months_back + week_offset + slot_i) % len(members)
                    lesson.members.set(members[offset: offset + 3] or members[:3])
                    completed_count += 1

        self.stdout.write(f"  20 upcoming + {completed_count} historical completed lessons created")
        self.stdout.write(self.style.SUCCESS("database seeded successfully."))
