"""Seeder module."""
import sys
import random
from faker import Faker
from sqlalchemy import create_engine, orm
from app.models import Profile, Friends, Base

# TODO: load this from a config file (config.yml)
SQLALCHEMY_DATABASE_URL = "sqlite:///./storage.sqlite3"

def create_profiles(session, profile_total=10):
    """Create random profiles."""
    fake = Faker()
    for _ in range(profile_total):
        profile = Profile(
            img=fake.image_url(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone=fake.phone_number(),
            address=fake.street_address(),
            city=fake.city(),
            state=fake.state_abbr(),
            zipcode=fake.zipcode(),
            available=random.choice([True, False])
        )
        session.add(profile)
    session.commit()

def add_friends(session, friend_total=5):
    """add random friends to all profiles."""
    profiles = session.query(Profile).all()
    for profile in profiles:
        friends = random.sample(profiles, friend_total)
        for friend in friends:
            if profile.id != friend.id:
                friend = Friends(profile_id=profile.id, friend_id=friend.id)
                session.add(friend)
    session.commit()

def seed(profile_total=10, friend_total=5):
    """Seed the database."""
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    session = orm.scoped_session(
        orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    # clean the database
    session.query(Profile).delete()
    session.query(Friends).delete()

    create_profiles(session, profile_total)
    add_friends(session, friend_total)

    print("Database seeded.")

if __name__ == "__main__":
    profile_total = sys.argv[1] if len(sys.argv) > 1 else 10
    friend_total = sys.argv[2] if len(sys.argv) > 1 else 5
    seed(int(profile_total), int(friend_total))
