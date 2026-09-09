# Doremon File Sharing Bot 🤖

A Telegram bot that allows users to unlock and download files through an interactive interface. Members click a link, see available files, unlock them, and receive downloads directly.

## Features ✨

- **File Management**: Upload and manage multiple files
- **Lock/Unlock System**: Files can be locked requiring action to unlock
- **User Tracking**: Track which users have unlocked which files
- **Download History**: Monitor file download statistics
- **Database Persistence**: SQLite database for storing all data
- **Interactive UI**: Inline keyboard buttons for smooth user experience

## Workflow 📋

```
User clicks link/starts bot
         ↓
User sees "View Files" menu
         ↓
Bot displays available files with lock status
         ↓
User clicks "Unlock File"
         ↓
File unlocked (free or requires action)
         ↓
User clicks "Download"
         ↓
Bot sends file to user
```

## Installation 🚀

### Prerequisites
- Python 3.8+
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/sajidking0101-bit/Doremon-File-Sharing.git
cd Doremon-File-Sharing
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your BOT_TOKEN and ADMIN_ID
```

5. **Create files directory**
```bash
mkdir files
# Add your files to this directory
```

6. **Run the bot**
```bash
python bot.py
```

## Configuration ⚙️

Edit `.env` file:
```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_ID=your_telegram_user_id
DATABASE_URL=sqlite:///bot.db
```

## File Management 📁

### Adding Files

Edit `bot.py` and update the `FILES_DB` dictionary:

```python
FILES_DB = {
    'file_1': {
        'name': 'document.pdf',
        'path': './files/document.pdf',
        'locked': True,
        'unlock_cost': 0,  # 0 = free
    },
    'file_2': {
        'name': 'image.jpg',
        'path': './files/image.jpg',
        'locked': True,
        'unlock_cost': 1,  # requires action
    }
}
```

Or use the Database module:

```python
from database import db

db.add_file('file_1', 'document.pdf', './files/document.pdf', locked=True, unlock_cost=0)
db.add_file('file_2', 'image.jpg', './files/image.jpg', locked=True, unlock_cost=1)
```

## Usage 📖

### For Users
1. Start the bot: `/start`
2. Click "📁 View Files"
3. See all files with their lock status
4. Click "🔓 Unlock" to unlock a file
5. Click "⬇️ Download" to receive the file

### For Developers

#### Check User Unlocks
```python
unlocked_files = db.get_user_unlocks(user_id=123456)
```

#### Log Download
```python
db.log_download(user_id=123456, file_id='file_1')
```

#### Get Statistics
```python
downloads = db.get_download_stats('file_1')
print(f"File downloaded {downloads} times")
```

## API Structure 🔧

### Bot Commands
- `/start` - Start the bot and show main menu
- `/help` - Show help information

### Callback Handlers
- `view_files` - Display all files
- `unlock_{file_id}` - Unlock a specific file
- `download_{file_id}` - Send file to user
- `help` - Show help
- `back` - Return to main menu

### Database Methods
- `add_file()` - Add new file
- `add_user()` - Register user
- `unlock_file()` - Unlock file for user
- `is_file_unlocked()` - Check unlock status
- `get_user_unlocks()` - Get all unlocked files
- `log_download()` - Log download action
- `get_download_stats()` - Get download count

## Customization 🎨

### Modify Unlock Mechanism

Edit the `unlock_file()` function in `bot.py`:

```python
async def unlock_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Add your custom unlock logic here
    # Examples:
    # - Require referral (invite friends)
    # - Require channel subscription
    # - Require payment
    # - Require completing a task
```

### Add Custom Messages

```python
WELCOME_MESSAGE = "Your custom welcome message"
FILE_UNLOCKED_MESSAGE = "Your custom unlock message"
```

## Advanced Features 🚀

### Database Backups
```bash
sqlite3 bot.db ".backup backup.db"
```

### Monitor Download Stats
```python
from database import db

all_files = db.get_all_files()
for file_info in all_files:
    stats = db.get_download_stats(file_info['file_id'])
    print(f"{file_info['name']}: {stats} downloads")
```

### Track User Activity
```python
from database import db

unlocked = db.get_user_unlocks(user_id=123456)
print(f"User has unlocked {len(unlocked)} files")
```

## Troubleshooting 🔧

### Bot not responding
- Check BOT_TOKEN in `.env`
- Ensure bot is running: `python bot.py`
- Check internet connection

### File not sending
- Verify file exists in `./files/` directory
- Check file permissions
- Ensure file size is within Telegram limits (50MB for free users)

### Database errors
- Delete `bot.db` to reset database
- Re-run bot to initialize fresh database

## Security 🔒

- Never commit `.env` file to repository
- Use strong admin IDs
- Validate all user inputs
- Monitor download statistics for abuse

## Future Enhancements 📈

- [ ] Admin dashboard
- [ ] Payment integration
- [ ] File encryption
- [ ] User roles (admin, moderator)
- [ ] Scheduled file releases
- [ ] Custom unlock conditions
- [ ] Analytics and reporting
- [ ] Multi-language support

## Support 💬

For issues or questions, create an issue on GitHub or contact the admin.

## License 📄

This project is open source and available under the MIT License.

---

**Built with ❤️ using python-telegram-bot**
