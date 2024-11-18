# app/utils/stats.py
from datetime import datetime, timedelta
from sqlalchemy import func, extract, distinct
from sqlalchemy.orm import Session
from ..models import Monkey, MonkeyCase, Vaccination, Vaccine
from collections import defaultdict

def get_dashboard_stats(db: Session):
    """Get statistics for the dashboard."""
    try:
        # Basic counts
        total_monkeys = db.query(func.count(distinct(Monkey.id))).scalar() or 0
        male_count = db.query(func.count(distinct(Monkey.id))).filter(Monkey.gender == 'M').scalar() or 0
        female_count = db.query(func.count(distinct(Monkey.id))).filter(Monkey.gender == 'F').scalar() or 0
        total_cases = db.query(func.count(distinct(MonkeyCase.id))).scalar() or 0
        total_vaccinations = db.query(func.count(distinct(Vaccination.id))).scalar() or 0

        # Calculate monthly registration data
        # Get data for the last 12 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        # Query for monthly counts
        monthly_counts = db.query(
            extract('year', Monkey.date_created).label('year'),
            extract('month', Monkey.date_created).label('month'),
            func.count('*').label('count')
        ).filter(
            Monkey.date_created.between(start_date, end_date)
        ).group_by(
            extract('year', Monkey.date_created),
            extract('month', Monkey.date_created)
        ).all()

        # Create a dictionary to store the counts
        count_dict = defaultdict(lambda: defaultdict(int))
        for year, month, count in monthly_counts:
            count_dict[int(year)][int(month)] = count

        # Generate labels and data for the last 12 months
        monthly_labels = []
        monthly_data = []
        
        current_date = end_date
        for _ in range(12):
            year = current_date.year
            month = current_date.month
            # Format the label
            month_label = current_date.strftime('%b %Y')
            monthly_labels.insert(0, month_label)
            # Get the count for this month (default to 0 if no data)
            count = count_dict[year][month]
            monthly_data.insert(0, count)
            # Move to previous month
            current_date = current_date.replace(day=1)
            if current_date.month == 1:
                current_date = current_date.replace(year=current_date.year - 1, month=12)
            else:
                current_date = current_date.replace(month=current_date.month - 1)

        # Get recent activities
        recent_activities = []
        
        # Get latest monkeys (last 5)
        latest_monkeys = db.query(Monkey)\
            .order_by(Monkey.date_created.desc())\
            .limit(5)\
            .all()
            
        for monkey in latest_monkeys:
            recent_activities.append({
                "date": monkey.date_created.strftime('%Y-%m-%d %H:%M'),
                "type": "New Registration",
                "details": f"Added new monkey {monkey.code}"
            })

        # Get latest vaccinations (last 5)
        latest_vaccinations = db.query(Vaccination)\
            .join(Monkey)\
            .join(Vaccine)\
            .order_by(Vaccination.date_created.desc())\
            .limit(5)\
            .all()
            
        for vacc in latest_vaccinations:
            recent_activities.append({
                "date": vacc.date_created.strftime('%Y-%m-%d %H:%M'),
                "type": "Vaccination",
                "details": f"Monkey {vacc.monkey.code} received {vacc.vaccine.name}"
            })

        # Sort and limit recent activities
        recent_activities.sort(key=lambda x: datetime.strptime(x["date"], '%Y-%m-%d %H:%M'), reverse=True)
        recent_activities = recent_activities[:5]

        return {
            "stats": {
                "total_monkeys": total_monkeys,
                "male_count": male_count,
                "female_count": female_count,
                "total_cases": total_cases,
                "total_vaccinations": total_vaccinations,
            },
            "monthly_labels": monthly_labels,
            "monthly_data": monthly_data,
            "recent_activities": recent_activities
        }

    except Exception as e:
        print(f"Error getting dashboard stats: {e}")
        return {
            "stats": {
                "total_monkeys": 0,
                "male_count": 0,
                "female_count": 0,
                "total_cases": 0,
                "total_vaccinations": 0,
            },
            "monthly_labels": [],
            "monthly_data": [],
            "recent_activities": []
        }