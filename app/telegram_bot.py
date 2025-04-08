from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import os
from dotenv import load_dotenv
from . import crud
from .database import SessionLocal
from datetime import datetime
import logging

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:3000")

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    try:
        db = SessionLocal()
        user = crud.get_user_by_telegram_id(db, update.effective_user.id)
        if not user:
            user = crud.create_user(db, {
                "telegram_id": update.effective_user.id,
                "username": update.effective_user.username,
                "first_name": update.effective_user.first_name,
                "last_name": update.effective_user.last_name
            })
        
        keyboard = [
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton("🥤 Добавить напиток", callback_data="add_drink")],
            [InlineKeyboardButton("🎯 Цели", callback_data="goals")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Привет! Я бот для контроля употребления алкоголя. "
            "Выберите действие:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Error in start command: {str(e)}")
        await update.message.reply_text(
            "Произошла ошибка. Пожалуйста, попробуйте позже."
        )
    finally:
        db.close()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    try:
        help_text = """
        Доступные команды:
        /start - Начать работу с ботом
        /help - Показать это сообщение
        /stats - Показать статистику
        /sober - Начать период трезвости
        /app - Открыть веб-приложение
        """
        await update.message.reply_text(help_text)
    except Exception as e:
        logger.error(f"Error in help command: {str(e)}")
        await update.message.reply_text(
            "Произошла ошибка. Пожалуйста, попробуйте позже."
        )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /stats"""
    try:
        db = SessionLocal()
        user = crud.get_user_by_telegram_id(db, update.effective_user.id)
        
        if not user:
            await update.message.reply_text(
                "Пожалуйста, сначала зарегистрируйтесь в веб-приложении."
            )
            return
        
        # Получаем статистику
        drinks = crud.get_user_drinks(db, user.id)
        total_alcohol = sum(drink.volume * drink.alcohol_content / 100 for drink in drinks)
        days_with_drinks = len(set(drink.created_at.date() for drink in drinks))
        
        stats_text = f"""
        📊 Ваша статистика:
        Всего алкоголя: {total_alcohol:.1f} мл
        Дней с употреблением: {days_with_drinks}
        """
        
        await update.message.reply_text(stats_text)
    except Exception as e:
        logger.error(f"Error in stats command: {str(e)}")
        await update.message.reply_text(
            "Произошла ошибка при получении статистики. "
            "Пожалуйста, попробуйте позже."
        )
    finally:
        db.close()

async def sober(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /sober"""
    try:
        db = SessionLocal()
        user = crud.get_user_by_telegram_id(db, update.effective_user.id)
        
        if not user:
            await update.message.reply_text(
                "Пожалуйста, сначала зарегистрируйтесь в веб-приложении."
            )
            return
        
        # Создаем новый период трезвости
        period = crud.create_sober_period(db, {
            "user_id": user.id,
            "start_time": datetime.now(),
            "is_active": True
        })
        await update.message.reply_text(
            "🎉 Поздравляем! Вы начали новый период трезвости. "
            "Держитесь!"
        )
    except Exception as e:
        logger.error(f"Error in sober command: {str(e)}")
        await update.message.reply_text(
            "Произошла ошибка. Пожалуйста, попробуйте позже."
        )
    finally:
        db.close()

async def app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /app"""
    try:
        await update.message.reply_text(
            "🌐 Откройте веб-приложение: https://your-app-url.com"
        )
    except Exception as e:
        logger.error(f"Error in app command: {str(e)}")
        await update.message.reply_text(
            "Произошла ошибка. Пожалуйста, попробуйте позже."
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик callback-запросов от инлайн-клавиатур"""
    try:
        query = update.callback_query
        await query.answer()
        
        if query.data == "stats":
            await stats(update, context)
        elif query.data == "add_drink":
            keyboard = [
                [InlineKeyboardButton("🍺 Пиво", callback_data="drink_beer")],
                [InlineKeyboardButton("🍷 Вино", callback_data="drink_wine")],
                [InlineKeyboardButton("🥃 Крепкий алкоголь", callback_data="drink_spirits")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "Выберите тип напитка:",
                reply_markup=reply_markup
            )
        elif query.data == "goals":
            keyboard = [
                [InlineKeyboardButton("🎯 Новая цель", callback_data="new_goal")],
                [InlineKeyboardButton("📋 Мои цели", callback_data="list_goals")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.message.reply_text(
                "Выберите действие:",
                reply_markup=reply_markup
            )
        elif query.data.startswith("drink_"):
            drink_type = query.data.split("_")[1]
            context.user_data["drink_type"] = drink_type
            await query.message.reply_text(
                f"Введите объем напитка в мл:"
            )
        elif query.data == "new_goal":
            await query.message.reply_text(
                "Введите вашу цель (например, '30 дней трезвости'):"
            )
        elif query.data == "list_goals":
            db = SessionLocal()
            user = crud.get_user_by_telegram_id(db, update.effective_user.id)
            
            if not user:
                await query.message.reply_text(
                    "Пожалуйста, сначала зарегистрируйтесь в веб-приложении."
                )
                return
            
            goals = crud.get_user_goals(db, user.id)
            if not goals:
                await query.message.reply_text(
                    "У вас пока нет целей. Создайте новую цель!"
                )
                return
            
            goals_text = "📋 Ваши цели:\n\n"
            for goal in goals:
                goals_text += f"- {goal.description}\n"
            
            await query.message.reply_text(goals_text)
    except Exception as e:
        logger.error(f"Error in button callback: {str(e)}")
        await update.callback_query.message.reply_text(
            "Произошла ошибка. Пожалуйста, попробуйте позже."
        )

def setup_bot():
    """Настройка и запуск бота"""
    try:
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Регистрация обработчиков команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("stats", stats))
        application.add_handler(CommandHandler("sober", sober))
        application.add_handler(CommandHandler("app", app))
        
        # Регистрация обработчика callback-запросов
        application.add_handler(CallbackQueryHandler(button_callback))
        
        return application
    except Exception as e:
        logger.error(f"Error setting up bot: {str(e)}")
        raise

# Запуск бота
if __name__ == "__main__":
    bot = setup_bot()
    bot.run_polling() 