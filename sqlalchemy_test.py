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

    address = Column(String)


Base.metadata.create_all(engine)

# %%
from faker import Faker

fake = Faker()


def create_user():
    user = User(name=fake.name())
    session.add(user)
    user.profile = UserProfile(address=fake.address())
    session.commit()


# %%
create_user()

# %%
users = session.query(User)[2:5]
print(users)

