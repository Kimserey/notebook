# %%
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

#%%
Base = declarative_base()
engine = create_engine("sqlite:///:memory:", echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    profile = relationship("UserProfile", uselist=False, back_populates="user")

    def __repr__(self):
        return "<User(id={}, name={}>".format(self.id, self.name)


class UserProfile(Base):
    __tablename__ = "user_profile"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    user = relationship("User", back_populates="profile")

    job = Column(String)
    address = Column(String)

    def __repr__(self):
        return "<UserProfile(user_id={}, job={}, address={})>".format(
            self.user_id, self.job, self.address
        )


Base.metadata.create_all(engine)

# %%
from faker import Faker

fake = Faker()


def create_user():
    user = User(name=fake.name())
    session.add(user)
    user.profile = UserProfile(job=fake.job(), address=fake.address())
    session.commit()


# %%
for _ in range(20):
    create_user()

# %%
# Order by and limit skip
users = session.query(User).order_by(User.name)[1:6]
users

# %%
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#querying
session.query(User, UserProfile).filter(User.id == UserProfile.user_id).filter(
    UserProfile.address.like("%Green%")
).all()

# %%
from sqlalchemy.orm import joinedload

# use options joinedload to eager load by doing a join
users = (
    session.query(User)
    .options(joinedload(User.profile))
    .join(UserProfile)
    .filter(UserProfile.job.like("%"))
    .all()
)

for user in users:
    print(user.profile.job)


# %%
# https://docs.sqlalchemy.org/en/13/orm/tutorial.html#common-filter-operators
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

users = (
    session.query(User)
    .options(joinedload(User.profile))
    .join(UserProfile)
    .filter(or_(UserProfile.job.like("%manager%"), UserProfile.job.like("%engineer%")))
    .all()
)

for user in users:
    print(user.profile.job)


# %%
