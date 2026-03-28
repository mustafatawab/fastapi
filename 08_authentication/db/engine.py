from config.setting import get_settings
from sqlmodel import create_engine


settings = get_settings()


engine = create_engine(settings.DATABASE_URL, echo=True)