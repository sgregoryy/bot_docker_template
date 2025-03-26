import os
import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class DatabaseConfig:
    """Database connection settings"""

    host: str
    port: str
    user: str
    password: str
    database: str

    @property
    def url(self) -> str:
        """Get database connection URL"""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class TelegramConfig:
    """Telegram bot settings"""

    token: str
    admin_ids: List[int]


@dataclass
class PaymentConfig:
    """Payment system settings"""

    manual_payment_enabled: bool = True
    manual_card_number: str = ""
    manual_recipient_name: str = ""
    manual_channel_id: str = ""


    youkassa_enabled: bool = False
    youkassa_shop_id: Optional[str] = None
    youkassa_secret_key: Optional[str] = None


@dataclass
class Config:
    """Main application configuration"""

    db: DatabaseConfig
    telegram: TelegramConfig
    payment: PaymentConfig


def load_config(env_path: Optional[str] = None) -> Config:
    """Load configuration from environment variables"""
    if env_path:
        load_dotenv(env_path)
    else:
        load_dotenv()


    admin_ids_str = os.getenv("ADMIN_IDS", "")
    admin_ids = []
    if admin_ids_str:
        try:
            admin_ids = [int(id.strip()) for id in admin_ids_str.split(",")]
        except ValueError:
            logger.error("Invalid admin IDs format, should be comma-separated integers")
    payment_methods = []

    manual_payment_enabled = os.getenv("MANUAL_PAYMENT_ENABLED", "true").lower() in ("true", "1", "yes")
    if manual_payment_enabled:
        payment_methods.append("manual")

    stars_enabaled = os.getenv("STARS_ENABLED", "false").lower() in ("true", "1", "yes")
    if stars_enabaled:
        payment_methods.append("stars")

    youkassa_enabled = os.getenv("YOUKASSA_ENABLED", "").lower() in ("true", "1", "yes")
    if youkassa_enabled and os.getenv("YOUKASSA_SHOP_ID") and os.getenv("YOUKASSA_SECRET_KEY"):
        payment_methods.append("youkassa")



    return Config(
        db=DatabaseConfig(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", ""),
            database=os.getenv("DB_NAME", "subscription_bot"),
        ),
        telegram=TelegramConfig(
            token=os.getenv("BOT_TOKEN", ""),
            admin_ids=admin_ids,
        ),
        payment=PaymentConfig(
            manual_payment_enabled=manual_payment_enabled,
            manual_card_number=os.getenv("MANUAL_CARD_NUMBER", ""),
            manual_recipient_name=os.getenv("MANUAL_RECIPIENT_NAME", ""),
            manual_channel_id=os.getenv("MANUAL_CHANNEL_ID", ""),
            youkassa_enabled=youkassa_enabled,
            youkassa_shop_id=os.getenv("YOUKASSA_SHOP_ID"),
            youkassa_secret_key=os.getenv("YOUKASSA_SECRET_KEY"),
        ),
    )


config = load_config()
