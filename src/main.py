import flet as ft
import asyncio
import sqlite3
import hashlib
import os

DB_PATH = "users.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username: str, password: str) -> tuple[bool, str]:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username.strip(), hash_password(password)),
        )
        conn.commit()
        conn.close()
        return True, "Berhasil didaftarkan!"
    except sqlite3.IntegrityError:
        return False, "Username sudah digunakan!"
    except Exception as e:
        return False, f"Error: {str(e)}"
    finally:
        conn.close()


def login_user(username: str, password: str) -> tuple[bool, str]:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username FROM users WHERE username = ? AND password = ?",
            (username.strip(), hash_password(password)),
        )
        user = cursor.fetchone()
        conn.close()
        if user:
            return True, user[1]
        else:
            return False, "Username atau password salah!"
    except Exception as e:
        return False, f"Error: {str(e)}"


init_db()

MOCK_DATA_UBI = {
    1: {
        "nama": "Ubi Jalar",
        "deskripsi": "Ubi yang memiliki warna ungu pekat kaya akan antioksidan.",
        "perawatan": "1. Lakukan penggemburan tanah.\n2. Angkat dan balikkan batang-batang yang menjalar setiap beberapa minggu.\n3. Berikan pupuk yang mengandung Nitrogen.\n4. Memotong sebagian pucuk atau daun yang tumbuh terlalu rimbun.",
        "warna": ft.Colors.PURPLE_700,
        "icon": ft.Icons.ECO,
    },
    2: {
        "nama": "Singkong",
        "deskripsi": "Tanaman perdu tahunan tropika yang dimanfaatkan umbi dan daunnya.",
        "perawatan": "1. Lakukan penyiangan pada 2-4 minggu.\n2. Menggemburkan tanah.\n3. Gunakan kombinasi urea.\n4. Pastikan tanah tetap lembap.\n5. Pastikan air cukup pada 5 bulan pertama, namun hindari tanah becek.\n6. Bersihkan rumput liar (gulma) di sekitar tanaman secara berkala",
        "warna": ft.Colors.BROWN_600,
        "icon": ft.Icons.NATURE,
    },
    3: {
        "nama": "Kentang",
        "deskripsi": "Umbi batang yang kaya karbohidrat, cocok ditanam di dataran tinggi.",
        "perawatan": "1. Hindari umbi terkena sinar matahari langsung karena dapat menyebabkan umbi menjadi hijau dan beracun.\n2. Pertahankan kelembapan tanah yang stabil selama fase pembentukan umbi.\n3. Kurangi penyiraman menjelang panen untuk mencegah umbi membusuk.\n4. Gunakan bibit kentang bersertifikat dan bebas penyakit.\n5. Buang tunas atau tanaman yang terserang penyakit agar tidak menular ke tanaman lain.\n6. Kendalikan penyakit busuk daun (late blight) yang merupakan penyakit utama pada kentang.\n7. Lakukan rotasi tanaman dan hindari menanam kentang pada lahan yang sama secara terus-menerus.\n8. Berikan pupuk kalium lebih tinggi saat pembentukan umbi.",
        "warna": ft.Colors.AMBER_700,
        "icon": ft.Icons.CIRCLE,
    },
    4: {
        "nama": "Talas",
        "deskripsi": "Umbi tropis yang kaya serat dan cocok untuk berbagai olahan makanan.",
        "perawatan": "1. Hindari genangan air berkepanjangan yang dapat menyebabkan busuk umbi.\n2. Lakukan penyiangan gulma secara rutin agar tidak bersaing memperebutkan unsur hara.\n3. Tambahkan pupuk organik atau kompos untuk mendukung pertumbuhan umbi.\n4. Lakukan pembumbunan ringan di sekitar pangkal tanaman jika umbi mulai muncul ke permukaan.\n5. Pangkas daun tua atau rusak untuk mengurangi risiko penyakit.\n6. Pantau hama seperti ulat dan kutu daun.",
        "warna": ft.Colors.GREEN_800,
        "icon": ft.Icons.PARK,
    },
    5: {
        "nama": "Bit",
        "deskripsi": "Umbi akar berwarna merah gelap yang kaya antioksidan, sering diolah menjadi jus atau salad.",
        "perawatan": "1. Pastikan tanaman mendapat pasokan air yang konsisten dan merata.\n2. Gunakan pupuk yang kaya akan Kalium (K) dan Fosfor (P) untuk pertumbuhan umbi.\n3. Jaga sirkulasi udara dengan memberikan jarak tanam yang cukup.\n4. Lakukan penyiraman langsung ke area tanah, bukan pada daun.",
        "warna": ft.Colors.RED_800,
        "icon": ft.Icons.SPA,
    },
    6: {
        "nama": "Lobak",
        "deskripsi": "Sayuran umbi bertekstur renyah dan segar yang sangat baik untuk pencernaan.",
        "perawatan": "1. Lakukan penyiraman secara teratur agar tanah tetap lembap, tetapi tidak becek.\n2. Jaga jarak tanam yang cukup untuk mendukung perkembangan umbi.\n3. Lakukan penjarangan bibit setelah tanaman tumbuh agar umbi dapat berkembang optimal.\n4. Berikan pupuk organik (kompos atau pupuk kandang matang) sebelum tanam.\n5. Hindari pemberian pupuk nitrogen berlebihan karena dapat menyebabkan daun tumbuh lebih banyak daripada umbi.",
        "warna": ft.Colors.TEAL_700,
        "icon": ft.Icons.ECO,
    },
}


BIRU_LANGIT = "#87CEEB"
BIRU_TUA = "#1a2a5e"
HIJAU_RUMPUT = "#4CAF50"
HIJAU_MUDA = "#81C784"
PUTIH_CLOUD = "#f0f8ff"


def main(page: ft.Page):
    page.title = "Aplikasi Jenis Umbi"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = BIRU_LANGIT
    page.fonts = {"Cochon": "Petit_Cochon.ttf"}

    def build_splash_view():
        return ft.View(
            controls=[
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(
                        src="ubi_background.png", fit=ft.BoxFit.COVER
                    ),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                        controls=[
                            ft.Container(
                                padding=ft.Padding(20, 60, 20, 0),
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=0,
                                    controls=[
                                        ft.Text(
                                            "APLIKASI",
                                            size=44,
                                            font_family="Cochon",
                                            weight=ft.FontWeight.W_900,
                                            color=BIRU_TUA,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        ft.Text(
                                            "JENIS UMBI",
                                            size=64,
                                            font_family="Cochon",
                                            weight=ft.FontWeight.W_900,
                                            color=BIRU_TUA,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        ft.Text(
                                            "DAN",
                                            size=44,
                                            font_family="Cochon",
                                            weight=ft.FontWeight.W_900,
                                            color=BIRU_TUA,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                        ft.Text(
                                            "CARA PERAWATANNYA",
                                            size=28,
                                            font_family="Cochon",
                                            weight=ft.FontWeight.W_900,
                                            color=BIRU_TUA,
                                            text_align=ft.TextAlign.CENTER,
                                        ),
                                    ],
                                ),
                            ),
                            ft.Container(expand=True),
                            ft.Container(
                                padding=ft.Padding(0, 0, 0, 80),
                                content=ft.GestureDetector(
                                    on_tap=lambda _: navigate_to("login"),
                                    content=ft.Container(
                                        width=220,
                                        height=60,
                                        border_radius=30,
                                        bgcolor=ft.Colors.WHITE,
                                        shadow=ft.BoxShadow(
                                            blur_radius=15,
                                            color=ft.Colors.with_opacity(
                                                0.3, ft.Colors.BLACK
                                            ),
                                            offset=ft.Offset(0, 4),
                                        ),
                                        alignment=ft.Alignment(0, 0),
                                        content=ft.Text(
                                            "ENTER",
                                            size=24,
                                            weight=ft.FontWeight.W_900,
                                            color=BIRU_TUA,
                                            style=ft.TextStyle(letter_spacing=3),
                                        ),
                                    ),
                                ),
                            ),
                        ],
                    ),
                )
            ],
            route="/",
            padding=0,
        )

    def build_login_view():
        txt_username = ft.TextField(
            label="Username",
            width=300,
            prefix_icon=ft.Icons.PERSON,
            border_color=BIRU_TUA,
            focused_border_color=HIJAU_RUMPUT,
            label_style=ft.TextStyle(color=BIRU_TUA),
            border_radius=12,
        )
        txt_password = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=300,
            prefix_icon=ft.Icons.LOCK,
            border_color=BIRU_TUA,
            focused_border_color=HIJAU_RUMPUT,
            label_style=ft.TextStyle(color=BIRU_TUA),
            border_radius=12,
        )
        lbl_error = ft.Text(value="", color=ft.Colors.RED_400)

        def login_clicked(e):
            if not txt_username.value or not txt_password.value:
                lbl_error.value = "Isi username dan password!"
                page.update()
                return

            sukses, pesan = login_user(txt_username.value, txt_password.value)
            if sukses:
                lbl_error.value = ""
                navigate_to("dashboard")
            else:
                lbl_error.value = pesan
                page.update()

        return ft.View(
            controls=[
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(
                        src="ubi_background.png", fit=ft.BoxFit.COVER
                    ),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                        controls=[
                            ft.Container(
                                width=100,
                                height=100,
                                border_radius=50,
                                bgcolor=ft.Colors.WHITE,
                                shadow=ft.BoxShadow(
                                    blur_radius=20,
                                    color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
                                ),
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(
                                    ft.Icons.ECO, size=60, color=HIJAU_RUMPUT
                                ),
                            ),
                            ft.Container(height=10),
                            ft.Text(
                                "JENIS UMBI",
                                size=28,
                                font_family="Cochon",
                                weight=ft.FontWeight.W_900,
                                color=BIRU_TUA,
                            ),
                            ft.Container(height=20),
                            ft.Container(
                                width=340,
                                padding=ft.Padding(30, 30, 30, 30),
                                border_radius=20,
                                bgcolor=ft.Colors.WHITE,
                                shadow=ft.BoxShadow(
                                    blur_radius=20,
                                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                                    offset=ft.Offset(0, 5),
                                ),
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=16,
                                    controls=[
                                        txt_username,
                                        txt_password,
                                        lbl_error,
                                        ft.GestureDetector(
                                            on_tap=login_clicked,
                                            content=ft.Container(
                                                width=300,
                                                height=50,
                                                border_radius=12,
                                                bgcolor=BIRU_TUA,
                                                alignment=ft.Alignment(0, 0),
                                                content=ft.Text(
                                                    "MASUK",
                                                    color=ft.Colors.WHITE,
                                                    size=16,
                                                    weight=ft.FontWeight.BOLD,
                                                    style=ft.TextStyle(
                                                        letter_spacing=2
                                                    ),
                                                ),
                                            ),
                                        ),
                                        ft.TextButton(
                                            "Belum punya akun? Daftar",
                                            on_click=lambda _: navigate_to("register"),
                                            style=ft.ButtonStyle(
                                                color=HIJAU_RUMPUT,
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                )
            ],
            route="/login",
            padding=0,
        )

    def build_register_view():
        txt_username = ft.TextField(
            label="Buat Username",
            width=300,
            prefix_icon=ft.Icons.PERSON_ADD,
            border_color=BIRU_TUA,
            focused_border_color=HIJAU_RUMPUT,
            border_radius=12,
        )
        txt_password = ft.TextField(
            label="Buat Password",
            password=True,
            width=300,
            prefix_icon=ft.Icons.PASSWORD,
            border_color=BIRU_TUA,
            focused_border_color=HIJAU_RUMPUT,
            border_radius=12,
        )
        lbl_status = ft.Text(value="", color=ft.Colors.RED_400)

        async def register_clicked(e):
            if not txt_username.value or not txt_password.value:
                lbl_status.value = "Isi dulu datanya!"
                lbl_status.color = ft.Colors.RED_400
                page.update()
                return

            sukses, pesan = register_user(txt_username.value, txt_password.value)
            if sukses:
                lbl_status.value = "Berhasil! Kembali ke login..."
                lbl_status.color = HIJAU_RUMPUT
                page.update()
                await asyncio.sleep(1)
                navigate_to("login")
            else:
                lbl_status.value = pesan
                lbl_status.color = ft.Colors.RED_400
                page.update()

        return ft.View(
            controls=[
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(
                        src="ubi_background.png", fit=ft.BoxFit.COVER
                    ),
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True,
                        controls=[
                            ft.Text(
                                "DAFTAR AKUN",
                                size=28,
                                weight=ft.FontWeight.W_900,
                                color=BIRU_TUA,
                            ),
                            ft.Container(height=20),
                            ft.Container(
                                width=340,
                                padding=ft.Padding(30, 30, 30, 30),
                                border_radius=20,
                                bgcolor=ft.Colors.WHITE,
                                shadow=ft.BoxShadow(
                                    blur_radius=20,
                                    color=ft.Colors.with_opacity(0.15, ft.Colors.BLACK),
                                    offset=ft.Offset(0, 5),
                                ),
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=16,
                                    controls=[
                                        txt_username,
                                        txt_password,
                                        lbl_status,
                                        ft.GestureDetector(
                                            on_tap=register_clicked,
                                            content=ft.Container(
                                                width=300,
                                                height=50,
                                                border_radius=12,
                                                bgcolor=HIJAU_RUMPUT,
                                                alignment=ft.Alignment(0, 0),
                                                content=ft.Text(
                                                    "DAFTAR SEKARANG",
                                                    color=ft.Colors.WHITE,
                                                    size=15,
                                                    weight=ft.FontWeight.BOLD,
                                                    style=ft.TextStyle(
                                                        letter_spacing=1
                                                    ),
                                                ),
                                            ),
                                        ),
                                        ft.TextButton(
                                            "Kembali ke Login",
                                            on_click=lambda _: navigate_to("login"),
                                            style=ft.ButtonStyle(color=BIRU_TUA),
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                )
            ],
            route="/register",
            appbar=ft.AppBar(
                title=ft.Text(
                    "Daftar Akun Baru",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
                bgcolor=BIRU_TUA,
                automatically_imply_leading=False,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda _: navigate_back(),
                ),
            ),
            padding=0,
        )

    def build_dashboard_view():
        def buat_kartu(nama, img_src, tanaman_key):
            return ft.GestureDetector(
                on_tap=lambda _, k=tanaman_key: go_to_detail(k),
                content=ft.Container(
                    width=160,
                    height=180,
                    border_radius=24,
                    bgcolor="#F5A623",
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    shadow=ft.BoxShadow(
                        blur_radius=12,
                        color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                        offset=ft.Offset(0, 4),
                    ),
                    content=ft.Stack(
                        controls=[
                            ft.Container(
                                width=160,
                                height=180,
                                image=ft.DecorationImage(
                                    src=img_src,
                                    fit=ft.BoxFit.CONTAIN,
                                    opacity=0.35,
                                ),
                            ),
                            ft.Container(
                                width=160,
                                height=180,
                                alignment=ft.Alignment(0, 0.6),
                                content=ft.Text(
                                    nama.upper(),
                                    size=16,
                                    weight=ft.FontWeight.W_900,
                                    color=BIRU_TUA,
                                    text_align=ft.TextAlign.CENTER,
                                    font_family="Cochon",
                                ),
                            ),
                        ],
                    ),
                ),
            )

        return ft.View(
            controls=[
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(
                        src="ubi_background.png", fit=ft.BoxFit.COVER
                    ),
                    content=ft.Column(
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(height=20),
                            ft.Container(
                                padding=ft.Padding(20, 0, 20, 0),
                                content=ft.Text(
                                    "JENIS UMBI UMBIAN",
                                    size=36,
                                    weight=ft.FontWeight.W_900,
                                    font_family="Cochon",
                                    color=BIRU_TUA,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ),
                            ft.Container(height=30),
                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=20,
                                        controls=[
                                            buat_kartu("Singkong", "singkong.png", 2),
                                            buat_kartu("Kentang", "kentang.png", 3),
                                        ],
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=20,
                                        controls=[
                                            buat_kartu("Ubi Jalar", "ubi_jalar.png", 1),
                                            buat_kartu("Talas", "talas.png", 4),
                                        ],
                                    ),
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=20,
                                        controls=[
                                            buat_kartu("Bit", "bit.png", 5),
                                            buat_kartu("Lobak", "lobak.png", 6),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                )
            ],
            route="/dashboard",
            appbar=ft.AppBar(
                title=ft.Text(
                    "JENIS UMBI",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.W_900,
                    font_family="Cochon",
                    style=ft.TextStyle(letter_spacing=2),
                ),
                bgcolor=BIRU_TUA,
                automatically_imply_leading=False,
                center_title=True,
                actions=[
                    ft.IconButton(
                        ft.Icons.LOGOUT,
                        icon_color=ft.Colors.WHITE,
                        tooltip="Keluar",
                        on_click=lambda _: navigate_to("splash"),
                    )
                ],
            ),
            padding=0,
        )

    def build_detail_view(ubi_id: int):
        if not ubi_id or ubi_id not in MOCK_DATA_UBI:
            data = None
        else:
            data = MOCK_DATA_UBI[ubi_id]

        if not data:
            return ft.View(
                controls=[ft.Text("Data tidak ditemukan")],
                route="/detail",
            )

        perawatan_items = []
        for baris in data["perawatan"].split("\n"):
            baris = baris.strip()
            if baris:
                teks = baris.lstrip("0123456789. ")
                perawatan_items.append(
                    ft.Text(
                        f"-{teks.upper()}",
                        size=12,
                        weight=ft.FontWeight.W_900,
                        color=BIRU_TUA,
                        text_align=ft.TextAlign.CENTER,
                    )
                )

        return ft.View(
            controls=[
                ft.Container(
                    expand=True,
                    image=ft.DecorationImage(
                        src="ubi_background.png", fit=ft.BoxFit.COVER
                    ),
                    content=ft.Column(
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                        controls=[
                            ft.Container(height=16),
                            ft.Container(
                                padding=ft.Padding(20, 0, 20, 0),
                                content=ft.Text(
                                    "CARA PERAWATANNYA",
                                    size=34,
                                    weight=ft.FontWeight.W_900,
                                    font_family="Cochon",
                                    color=BIRU_TUA,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ),
                            ft.Container(height=16),
                            ft.Container(
                                width=140,
                                height=160,
                                border_radius=20,
                                bgcolor="#F5A623",
                                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                shadow=ft.BoxShadow(
                                    blur_radius=12,
                                    color=ft.Colors.with_opacity(0.25, ft.Colors.BLACK),
                                    offset=ft.Offset(0, 4),
                                ),
                                content=ft.Stack(
                                    controls=[
                                        ft.Container(
                                            width=140,
                                            height=160,
                                            image=ft.DecorationImage(
                                                src=f"{data['nama'].lower().replace(' ', '_').replace('(', '').replace(')', '')}.png",
                                                fit=ft.BoxFit.CONTAIN,
                                                opacity=0.4,
                                            ),
                                        ),
                                        ft.Container(
                                            width=140,
                                            height=160,
                                            alignment=ft.Alignment(0, 0.6),
                                            content=ft.Text(
                                                data["nama"].upper(),
                                                size=13,
                                                weight=ft.FontWeight.W_900,
                                                font_family="Cochon",
                                                color=BIRU_TUA,
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                            ft.Container(height=20),
                            ft.Container(
                                expand=True,
                                margin=ft.Margin(24, 0, 24, 80),
                                border_radius=20,
                                border=ft.Border(
                                    left=ft.BorderSide(4, "#7090d0"),
                                    right=ft.BorderSide(4, "#7090d0"),
                                    top=ft.BorderSide(4, "#7090d0"),
                                    bottom=ft.BorderSide(4, "#7090d0"),
                                ),
                                bgcolor=ft.Colors.with_opacity(0.55, "#b8c8f0"),
                                padding=ft.Padding(20, 24, 20, 24),
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    spacing=16,
                                    scroll=ft.ScrollMode.AUTO,
                                    controls=perawatan_items,
                                ),
                            ),
                        ],
                    ),
                )
            ],
            route="/detail",
            appbar=ft.AppBar(
                title=ft.Text(
                    "Detail Umbi",
                    color=ft.Colors.WHITE,
                    weight=ft.FontWeight.BOLD,
                ),
                bgcolor=BIRU_TUA,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda _: navigate_back(),
                ),
                automatically_imply_leading=False,
            ),
            floating_action_button=ft.FloatingActionButton(
                content=ft.Text(
                    "BACK",
                    size=14,
                    weight=ft.FontWeight.W_900,
                    font_family="Cochon",
                    color=BIRU_TUA,
                ),
                bgcolor=ft.Colors.WHITE,
                on_click=lambda _: navigate_back(),
                mini=False,
            ),
            floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
            padding=0,
        )

    def navigate_to(screen: str):
        if screen == "splash":
            page.views.clear()
            page.views.append(build_splash_view())
        elif screen == "login":
            page.views.clear()
            page.views.append(build_splash_view())
            page.views.append(build_login_view())
        elif screen == "register":
            page.views.append(build_register_view())
        elif screen == "dashboard":
            page.views.clear()
            page.views.append(build_splash_view())
            page.views.append(build_dashboard_view())
        page.update()

    def go_to_detail(ubi_id: int):
        page.views.append(build_detail_view(ubi_id))
        page.update()

    def navigate_back():
        if len(page.views) > 1:
            page.views.pop()
            page.update()

    page.on_view_pop = lambda e: navigate_back()

    page.views.append(build_splash_view())
    page.update()


ft.run(main, assets_dir="assets")
