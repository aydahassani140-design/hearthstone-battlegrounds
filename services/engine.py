# engine.py
# Hearthstone Clone Project

# services/engine.py
import random
from common.models import Player, Shop, MinionInstance
from data.minions_data import CARD_DB, create_minion

class GameEngine:
    def __init__(self):
        """
        راه‌اندازی اولیه بازی
        """
        # 1. ساخت ۴ بازیکن طبق داکیومنت
        self.players = {
            "p1": Player("p1", "Sylvanas Windrunner"),
            "p2": Player("p2", "The Lich King"),
            "p3": Player("p3", "Millhouse Manastorm"),
            "p4": Player("p4", "Yogg-Saron")
        }
        
        # فعلاً فرض می‌کنیم ما بازیکن ۱ هستیم
        self.current_player_id = "p1"
        self.shop = Shop()
        
        # 2. متغیرهای مربوط به نوبت و فاز (بخش جدید)
        self.turn = 1
        self.phase = "RECRUIT"  # فازهای بازی: 'RECRUIT' یا 'COMBAT'
        self.combat_data = []   # برای ذخیره نتیجه جنگ
        
        # 3. شروع بازی
        self.start_turn()
     

    def start_turn(self):
        """
        شروع نوبت جدید: تنظیم طلا و رفرش کردن شاپ
        """
        player = self.players[self.current_player_id]
        
        # فرمول طلا: نوبت ۱ = ۳ طلا، نوبت ۲ = ۴ طلا ... تا سقف ۱۰
        player.max_gold = min(10, 2 + self.turn)
        player.gold = player.max_gold
        
        # اگر شاپ فریز نشده بود، کارت‌های جدید بیاور
        if not self.shop.frozen:
            self.refresh_shop(player, is_free_start=True)
        else:
            # اگر فریز بود، برای نوبت بعد آنفریز کن (مگر اینکه بازیکن دوباره فریز کند)
            self.shop.frozen = False 
    def switch_phase(self):
        """
        تغییر فاز بین خرید و جنگ طبق دیاگرام State Machine
        """
        if self.phase == "RECRUIT":
            print(f"--- Turn {self.turn} Recruit Phase Ended ---")
            print(">>> Starting COMBAT Phase...")
            self.phase = "COMBAT"
            
            # نکته برای بعد: اینجا باید تابع start_combat از کد نفر سوم صدا زده شود.
            # فعلاً فقط فاز را عوض می‌کنیم.

        elif self.phase == "COMBAT":
            print(">>> Combat finished! Back to RECRUIT Phase...")
            self.phase = "RECRUIT"
            
            # رفتن به نوبت بعد
            self.turn += 1
            self.start_turn() # پول دادن و رفرش شاپ
    def refresh_shop(self, player: Player, is_free_start=False):
        """
        عوض کردن کارت‌های داخل شاپ
        """
        # هزینه رفرش ۱ طلا است (مگر اینکه شروع نوبت باشد)
        cost = 0 if is_free_start else 1
        
        # استثنا: میلهوس هزینه رفرشش ۲ است
        if player.hero_name == "Millhouse Manastorm" and not is_free_start:
            cost = 2

        if player.gold < cost:
            print("Not enough gold to refresh!")
            return False

        player.gold -= cost
        
        # تعیین تعداد کارت‌ها بر اساس سطح (Tier)
        # Tier 1 -> 3 cards
        # Tier 2,3 -> 4 cards
        # Tier 4+ -> 5 cards
        count = 3
        if player.tavern_tier >= 4:
            count = 5
        elif player.tavern_tier >= 2:
            count = 4
            
        # انتخاب کارت‌های تصادفی
        # نکته: فعلاً از کل دیتابیس انتخاب می‌کنیم. بعداً باید بر اساس Tier فیلتر کنیم.
        all_card_ids = list(CARD_DB.keys())
        new_slots = []
        
        for _ in range(count):
            random_id = random.choice(all_card_ids)
            new_minion = create_minion(random_id)
            new_slots.append(new_minion)
            
        self.shop.slots = new_slots
        return True

    def buy_minion(self, player_id: str, shop_index: int):
        """
        خرید مینیون از شاپ و انتقال به دست
        """
        player = self.players[player_id]
        
        # چک کردن ایندکس
        if shop_index >= len(self.shop.slots) or self.shop.slots[shop_index] is None:
            return False
            
        minion = self.shop.slots[shop_index]
        cost = 3 # قیمت ثابت خرید
        
        # چک کردن طلا و جای خالی در دست
        if player.gold < cost:
            print("Not enough gold!")
            return False
            
        if len(player.hand) >= 10:
            print("Hand is full!")
            return False
            
        # انجام تراکنش
        player.gold -= cost
        player.hand.append(minion)
        self.shop.slots[shop_index] = None # خالی کردن جای کارت در شاپ
        
        print(f"Bought {minion.card_id}")
        return True

    def play_minion(self, player_id: str, hand_index: int, board_index: int):
        """
        بازی کردن کارت: انتقال از دست به زمین
        """
        player = self.players[player_id]
        
        if hand_index >= len(player.hand):
            return False
            
        if len(player.board) >= 7:
            print("Board is full!")
            return False
            
        # انتقال
        minion = player.hand.pop(hand_index)
        
        # اگر اندیس -1 بود یعنی ته لیست اضافه کن
        if board_index == -1 or board_index > len(player.board):
            player.board.append(minion)
        else:
            player.board.insert(board_index, minion)
            
        print(f"Played {minion.card_id} on board")
        return True

    def sell_minion(self, player_id: str, board_index: int):
        """
        فروش مینیون: حذف از زمین و دریافت ۱ طلا
        """
        player = self.players[player_id]
        
        if board_index >= len(player.board):
            return False
            
        # حذف و دریافت طلا
        removed_minion = player.board.pop(board_index)
        player.gold += 1
        
        print(f"Sold {removed_minion.card_id}")
        return True

    def freeze_shop(self):
        """
        فریز کردن شاپ برای نوبت بعد
        """
        self.shop.frozen = not self.shop.frozen # Toggle (خاموش/روشن)
        print(f"Shop frozen status: {self.shop.frozen}")