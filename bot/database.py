from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
from bot.config import config
from bot.utils.locale_manager import LocaleKeys

Base = declarative_base()
engine = create_engine(config.DATABASE_URL)
Session = sessionmaker(bind=engine)


class FilteredWord(Base):
    __tablename__ = 'filtered_words'

    id = Column(Integer, primary_key=True)
    word = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<FilteredWord(word='{self.word}')>"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    warnings = relationship(
        "Warning", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(user_id={self.user_id}, username='{self.username}')>"

    def get_warning_count(self):
        return len(self.warnings)


class Warning(Base):
    __tablename__ = 'warnings'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    word = Column(String, nullable=False)
    chat_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    # warning, mute_3h, mute_permanent
    action_taken = Column(String, nullable=False)

    user = relationship("User", back_populates="warnings")

    def __repr__(self):
        return f"<Warning(user_id={self.user_id}, word='{self.word}', action='{self.action_taken}')>"


def init_db():
    Base.metadata.create_all(engine)


def get_session():
    return Session()


def word_list_convertor(words):
    return [word.strip().lower() for word in words.split('\n')]


def add_filtered_word(locale, words):

    result = ""
    session = get_session()
    try:

        word_list = word_list_convertor(words)
        for word in word_list:
            existing_word = session.query(
                FilteredWord).filter_by(word=word).first()
            if existing_word:
                result += f"{locale.get(LocaleKeys.word)} \"{word}\" {locale.get(LocaleKeys.word_exists)} \n"
                continue
            new_word = FilteredWord(word=word)
            session.add(new_word)

            result += f"{locale.get(LocaleKeys.word)} \"{word}\" {locale.get(LocaleKeys.word_added)} \n"

        session.commit()

        return result
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()


def remove_filtered_word(locale, words):

    result = ""
    session = get_session()
    try:
        word_list = word_list_convertor(words)
        for word in word_list:

            existing_word = session.query(
                FilteredWord).filter_by(word=word).first()
            if not existing_word:
                result += f"{locale.get(LocaleKeys.word)} \"{word}\" {locale.get(LocaleKeys.word_not_found)} \n"

            session.delete(existing_word)
            result += f"{locale.get(LocaleKeys.word)}  \"{word}\" {locale.get(LocaleKeys.word_removed)} \n"

        session.commit()
        return result
    except Exception as e:
        session.rollback()
        return False, str(e)
    finally:
        session.close()


def get_all_filtered_words():
    session = get_session()
    try:
        words = session.query(FilteredWord).all()
        return [word.word for word in words]
    finally:
        session.close()


def get_or_create_user(user_id, username=None, first_name=None):
    session = get_session()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            user = User(user_id=user_id, username=username,
                        first_name=first_name)
            session.add(user)
            session.commit()
        return user
    finally:
        session.close()


def add_warning(user_id, word, chat_id, username=None, first_name=None):
    session = get_session()
    try:
        user = get_or_create_user(user_id, username, first_name)

        warning_count = session.query(
            Warning).filter_by(user_id=user_id, chat_id=chat_id).count()

        warning_count += 1
        if warning_count in config.PENALTIES:
            action = config.PENALTIES[warning_count]
        else:
            action = "mute_permanent"

        warning = Warning(
            user_id=user_id,
            word=word,
            chat_id=chat_id,
            action_taken=action
        )

        session.add(warning)
        session.commit()

        return warning_count, action
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def remove_user_warning(user_id,chat_id):
    session = get_session()
    try:
        latest_warning = session.query(Warning).filter_by(
            user_id=user_id,chat_id=chat_id).order_by(Warning.timestamp.desc()).first()
        if latest_warning:
            session.delete(latest_warning)
            session.commit()

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_user_warnings_count(user_id,chat_id):
    session = get_session()
    try:
        warnings = session.query(Warning).filter_by(user_id=user_id,chat_id=chat_id).all()
        return len(warnings)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def remove_all_user_warnings(user_id, chat_id):
    session = get_session()
    try:
        warnings = session.query(Warning).filter_by(
            user_id=user_id, chat_id=chat_id).all()
        for warning in warnings:
            session.delete(warning)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
