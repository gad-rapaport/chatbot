import flet as ft
from api_client import get_bot_response
import time

def main(page: ft.Page):
    # הגדרות עיצוב כלליות של העמוד
    page.title = "My 3D AI Chatbot"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50
    page.bgcolor = "#1a1a1a"  # רגע כהה עמוק

    # רשימת ההודעות (ההיסטוריה של הצ'אט)
    chat_list = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # פונקציה להוספת הודעה למסך עם אפקט "ציפה"
    def add_message(text, align, color):
        bubble = ft.Container(
            content=ft.Text(text, size=16, color=ft.colors.WHITE),
            padding=15,
            border_radius=15,
            bgcolor=color,
            margin=ft.margin.only(bottom=10),
            # אפקט צל ותלת מימד
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.with_opacity(0.5, ft.colors.BLACK),
                offset=ft.Offset(2, 4),
            ),
        )
        
        # עטיפה בשורה כדי ליישר לימין או לשמאל
        row = ft.Row(
            [bubble],
            alignment=align,
        )
        
        chat_list.controls.append(row)
        page.update()

    # פונקציה לטיפול בשליחת הודעה
    def send_click(e):
        user_text = user_input.value
        if not user_text:
            return

        # 1. הצגת הודעת המשתמש
        add_message(user_text, ft.MainAxisAlignment.END, "#304ffe") # כחול עמוק
        user_input.value = ""
        user_input.focus()
        page.update()

        # 2. קבלת תשובה מהבוט (מהקובץ שעשינו קודם)
        # נוסיף אינדיקציה שהבוט מקליד...
        loading = ft.Row([ft.Text("Bot is thinking...", italic=True, color="grey")], alignment=ft.MainAxisAlignment.START)
        chat_list.controls.append(loading)
        page.update()
        
        # קריאה ל-API
        bot_reply = get_bot_response(user_text)
        
        # הסרת ה"מקליד..." והוספת התשובה האמיתית
        chat_list.controls.remove(loading)
        add_message(bot_reply, ft.MainAxisAlignment.START, "#424242") # אפור כהה
        
        page.update()

    # שדה הקלט וכפתור השליחה
    user_input = ft.TextField(
        hint_text="Type your message...",
        expand=True,
        border_color="#304ffe",
        focused_border_color="#536dfe",
        border_radius=10,
        filled=True,
        bgcolor="#262626"
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED,
        icon_color="#304ffe",
        tooltip="Send Message",
        on_click=send_click
    )

    # בניית המבנה הראשי - "המסך בתוך מסך"
    # ניצור קונטיינר ראשי שנראה כמו מסך מחשב בתוך החלון
    main_screen = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Text("Gemini Chat", size=20, weight="bold"),
                padding=10,
                border=ft.border.only(bottom=ft.border.BorderSide(1, "#424242")),
            ),
            chat_list,
            ft.Row([user_input, send_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ]),
        width=500,
        height=700,
        bgcolor="#1e1e1e",
        border_radius=20,
        padding=20,
        # אפקט עומק חזק למסך הראשי
        shadow=ft.BoxShadow(
            spread_radius=5,
            blur_radius=30,
            color=ft.colors.with_opacity(0.6, "#000000"),
            offset=ft.Offset(10, 10),
        ),
        # גבול דק זוהר
        border=ft.border.all(2, "#333333"),
    )

    # הוספת האלמנטים לעמוד ומרכוז
    page.add(ft.Row([main_screen], alignment=ft.MainAxisAlignment.CENTER))

# הרצת האפליקציה
ft.app(target=main)
