from sqlmodel import create_engine
from config.settings import get_settings

setting = get_settings()


engine = create_engine(setting.DB_URL , echo=True)