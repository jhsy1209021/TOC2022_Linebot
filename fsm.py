from transitions.extensions import GraphMachine
from linebot.models import MessageTemplateAction, CarouselColumn
from utils import send_text_message, send_button_message, send_carousel_message

meal_type="not avail"
meal_name="not avail"
exercise_type=""
breakfast=[]
lunch=[]
aft_tea=[]
dinner=[]
late_meal=[]
exercise=[]

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def on_enter_menu(self, event):
        print("Entering menu")
        title = "歡迎使用熱量計算機，幫助您追蹤一天的能量"
        text = "請選擇想要紀錄的項目"
        btn = [
            MessageTemplateAction(
                label='進食',
                text='進食'
            ),
            MessageTemplateAction(
                label='運動',
                text='運動'
            ),
            MessageTemplateAction(
                label='查看總表',
                text='查看總表'
            ),
        ]
        send_button_message(event.reply_token, title, text, btn)

    def on_enter_meal_type(self, event):
        print("Entering meal_type")
        title = "剛剛吃了什麼呢?"
        text = "請選擇一個分類"
        btn = [
            MessageTemplateAction(
                label='早餐',
                text='早餐'
            ),
            MessageTemplateAction(
                label='午餐',
                text='午餐'
            ),
            MessageTemplateAction(
                label='晚餐',
                text='晚餐'
            ),
            MessageTemplateAction(
                label='宵夜',
                text='宵夜'
            ),
        ]
        send_button_message(event.reply_token, title, text, btn)

    def on_enter_meal_name(self, event):
        send_text_message(event.reply_token, '請輸入食物的名稱')

    def on_enter_add_calories(self, event):
        send_text_message(event.reply_token, '請輸入預估攝取的熱量(kcal)')

    def on_enter_exercise_type(self, event):
        send_text_message(event.reply_token, '請輸入運動的名稱')

    def on_enter_sub_calories(self, event):
        send_text_message(event.reply_token, '請輸入預估消耗的熱量(kcal)')

    def on_enter_summary(self, event):
        """
        breakfast_text=""
        breakfast_cal=0
        lunch_text=""
        lunch_cal=0
        aft_tea_text=""
        aft_tea_cal=0
        dinner_text=""
        dinner_cal=0
        late_meal_text=""
        late_meal_cal=0
        exercise_text=""
        exercise_cal=0
        for item_name, calorie in breakfast:
            breakfast_text += item_name + ":" + str(calorie) + "\n"
            breakfast_cal += calorie
        for item_name, calorie in lunch:
            lunch_text += item_name + ":" + str(calorie) + "\n"
            lunch_cal += calorie
        for item_name, calorie in aft_tea:
            aft_tea_text += item_name + ":" + str(calorie) + "\n"
            aft_tea_cal += calorie
        for item_name, calorie in dinner:
            dinner_text += item_name + ":" + str(calorie) + "\n"
            dinner_cal += calorie
        for item_name, calorie in late_meal:
            late_meal_text += item_name + ":" + str(calorie) + "\n"
            late_meal_cal += calorie
        for item_name, calorie in exercise:
            exercise_text += item_name + ":" + str(calorie) + "\n"
            exercise_cal += calorie
        
        reply_col = [
            CarouselColumn(
                title="早餐",
                text=breakfast_text + "----------\nTotal Calorie:" + str(breakfast_cal),
                actions=MessageTemplateAction(text="restart")
            ),
            CarouselColumn(
                title="午餐",
                text=lunch_text + "----------\nTotal Calorie:" + str(lunch_cal),
                actions=MessageTemplateAction(text="restart")
            ),
            CarouselColumn(
                title="下午茶",
                text=aft_tea_text + "----------\nTotal Calorie:" + str(aft_tea_cal),
                actions=MessageTemplateAction(text="restart")
            ),
            CarouselColumn(
                title="晚餐",
                text=dinner_text + "----------\nTotal Calorie:" + str(dinner_cal),
                actions=MessageTemplateAction(text="restart")
            ),
            CarouselColumn(
                title="宵夜",
                text=late_meal_text + "----------\nTotal Calorie:" + str(late_meal_cal),
                actions=MessageTemplateAction(text="restart")
            ),
            CarouselColumn(
                title="運動消耗",
                text=exercise_text + "----------\nTotal Calorie:" + str(exercise_cal),
                actions=MessageTemplateAction(text="restart")
            ),
            CarouselColumn(
                title="總計",
                text="攝取:" + str(breakfast_cal + lunch_cal + aft_tea_cal + dinner_cal + late_meal_cal) +\
                     "\n消耗:" + str(exercise_cal) +\
                     "\n----------\n淨熱量:" + str(breakfast_cal + lunch_cal + aft_tea_cal + dinner_cal + late_meal_cal - exercise_cal),
                actions=MessageTemplateAction(text="restart")
            ),
        ]
        """
        text = "==========\n"
        text += "早餐:\n"
        breakfast_cal = 0
        for item_name, calorie in breakfast:
            text += item_name + ":" + str(calorie) + "\n"
            breakfast_cal += calorie
        text += "------>Total:" + str(breakfast_cal) + "(kcal)" + "\n=========="

        text += "\n午餐:\n"
        lunch_cal = 0
        for item_name, calorie in lunch:
            text += item_name + ":" + str(calorie) + "\n"
            lunch_cal += calorie
        text += "------>Total:" + str(lunch_cal) + "(kcal)" + "\n=========="

        text += "\n下午茶\n"
        aft_tea_cal = 0
        for item_name, calorie in aft_tea:
            text += item_name + ":" + str(calorie) + "\n"
            aft_tea_cal += calorie
        text += "------>Total:" + str(aft_tea_cal) + "(kcal)" + "\n=========="
        
        text += "\n晚餐:\n"
        dinner_cal = 0
        for item_name, calorie in dinner:
            text += item_name + ":" + str(calorie) + "\n"
            dinner_cal += calorie
        text += "------>Total:" + str(dinner_cal) + "(kcal)" + "\n=========="

        text += "\n消夜:\n"
        late_meal_cal = 0
        for item_name, calorie in late_meal:
            text += item_name + ":" + str(calorie) + "\n"
            late_meal_cal += calorie
        text += "------>Total:" + str(late_meal_cal) + "(kcal)" + "\n=========="

        text += "\n運動:\n"
        exercise_cal = 0
        for item_name, calorie in exercise:
            text += item_name + ":" + str(calorie) + "\n" + "\n=========="
            exercise_cal += calorie
        text += "------>Total:" + str(exercise_cal) + "(kcal)"
        
        text += "\n====================\n淨攝取:" + str(breakfast_cal + lunch_cal + aft_tea_cal + dinner_cal + late_meal_cal) +\
                "-" + str(exercise_cal) +\
                "=" + str(breakfast_cal + lunch_cal + aft_tea_cal + dinner_cal + late_meal_cal - exercise_cal)
        text += "\n***輸入continue繼續使用***\n***輸入reset重設***\n***輸入exit退出計算機***"
        send_text_message(event.reply_token, text)

    def is_going_to_menu(self, event):
        text = event.message.text
        return text.lower() == "calcal"

    def is_going_to_meal_type(self, event):
        text = event.message.text
        return text.lower() == "進食"

    def is_going_to_exercise_type(self, event):
        text = event.message.text
        return text.lower() == "運動"

    def is_going_to_summary(self, event):
        text = event.message.text
        return text.lower() == "查看總表"

    def is_going_to_meal_name(self, event):
        global meal_type
        text = event.message.text.lower()
        if text in ["早餐", "午餐", "下午茶", "晚餐", "宵夜"]:
            meal_type = text
            return True

        return False

    def is_going_to_add_calories(self, event):
        global meal_name
        meal_name = event.message.text.lower()
        return True

    def is_going_to_sub_calories(self, event):
        global exercise_type
        exercise_type = event.message.text.lower()
        return True

    def complete_add_calories(self, event):
        global meal_type
        global meal_name
        global breakfast
        global lunch
        global aft_tea
        global dinner
        global late_meal
        text = event.message.text.lower()
        if not str.isdigit(text):
            return False

        if meal_type == "早餐":
            breakfast.append((meal_name, int(text)))
        if meal_type == "午餐":
            lunch.append((meal_name, int(text)))
        if meal_type == "下午茶":
            aft_tea.append((meal_name, int(text)))
        if meal_type == "晚餐":
            dinner.append((meal_name, int(text)))
        if meal_type == "宵夜":
            late_meal.append((meal_name, int(text)))
        return True

    def complete_sub_calories(self, event):
        global exercise_type
        global exercise
        text = event.message.text.lower()
        if not str.isdigit(text):
            return False
        exercise.append((exercise_type, int(text)))
        return True

    def is_going_back_to_menu(self, event):
        global meal_type
        global meal_name
        global exercise_type
        global breakfast
        global lunch
        global aft_tea
        global dinner
        global late_meal
        global exercise
        text = event.message.text.lower()
        if "reset" in text:
            meal_type="not avail"
            meal_name="not avail"
            exercise_type=""
            breakfast=[]
            lunch=[]
            aft_tea=[]
            dinner=[]
            late_meal=[]
            exercise=[]
            return True
        if "continue" in text:
            return True
        return False

    def is_going_back_to_user(self, event):
        text = event.message.text.lower()
        if text == "exit":
            return True
        return False

"""def on_enter_input_gender(self, event):
        title = '請先提供您的基本資訊'
        text = '您是『男生』還是『女生』'
        btn = [
            MessageTemplateAction(
                label = '男生',
                text ='男生'
            ),
            MessageTemplateAction(
                label = '女生',
                text = '女生'
            ),
        ]
        url = 'https://i.imgur.com/T2bLdbN.jpg'
        send_button_message(event.reply_token, title, text, btn, url)
        
    def on_exit_state2(self):
        print("Leaving state2")  
"""
