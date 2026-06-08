import flet as ft
import asyncio

MOCK_DATA_UBI = {
    1: {
        "nama": "Ubi Cilembu",
        "deskripsi": "Ubi khas Sumedang yang terkenal dengan rasa manis seperti madu ketika dipanggang.",
        "perawatan": "1. Penyiraman rutin 1-2 kali sehari.\n2. Pastikan tanah gembur.\n3. Panen umur 4-5 bulan.",
        "warna": ft.Colors.ORANGE_700,
        "icon": ft.Icons.GRASS,
    },
    2: {
        "nama": "Ubi Jalar Ungu",
        "deskripsi": "Ubi yang memiliki warna ungu pekat kaya akan antioksidan.",
        "perawatan": "1. Sinar matahari penuh.\n2. Lakukan pendangiran berkala.\n3. Beri pupuk organik.",
        "warna": ft.Colors.PURPLE_700,
        "icon": ft.Icons.ECO,
    },
    3: {
        "nama": "Singkong (Ubi Kayu)",
        "deskripsi": "Tanaman perdu tahunan tropika yang dimanfaatkan umbi dan daunnya.",
        "perawatan": "1. Tanam stek batang berkualitas.\n2. Penyiangan gulma penting.\n3. Panen usia 7-9 bulan.",
        "warna": ft.Colors.BROWN_600,
        "icon": ft.Icons.NATURE,
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
    page.fonts = {"Cochon" : "Petit_Cochon.ttf"}

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
            if txt_username.value and txt_password.value:
                lbl_error.value = ""
                navigate_to("dashboard")
            else:
                lbl_error.value = "Isi username dan password!"
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
                            ft.Text(
                                "Masuk ke akun Anda",
                                size=14,
                                color=ft.Colors.GREY_600,
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
            else:
                lbl_status.value = "Berhasil! Kembali ke login..."
                lbl_status.color = HIJAU_RUMPUT
                page.update()
                await asyncio.sleep(1)
                navigate_to("login")

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
        list_pilihan = []
        for ubi_id, data in MOCK_DATA_UBI.items():
            warna = data["warna"]
            list_pilihan.append(
                ft.Container(
                    margin=ft.Margin(0, 0, 0, 12),
                    border_radius=16,
                    bgcolor=ft.Colors.WHITE,
                    shadow=ft.BoxShadow(
                        blur_radius=10,
                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                        offset=ft.Offset(0, 3),
                    ),
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                width=70,
                                height=90,
                                border_radius=ft.BorderRadius(
                                    top_left=16,
                                    bottom_left=16,
                                    top_right=0,
                                    bottom_right=0,
                                ),
                                bgcolor=warna,
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(
                                    data["icon"], size=36, color=ft.Colors.WHITE
                                ),
                            ),
                            ft.Container(
                                expand=True,
                                padding=ft.Padding(12, 10, 8, 10),
                                content=ft.Column(
                                    spacing=4,
                                    controls=[
                                        ft.Text(
                                            data["nama"],
                                            weight=ft.FontWeight.BOLD,
                                            size=15,
                                            color=BIRU_TUA,
                                        ),
                                        ft.Text(
                                            data["deskripsi"],
                                            size=12,
                                            color=ft.Colors.GREY_600,
                                            max_lines=2,
                                            overflow=ft.TextOverflow.ELLIPSIS,
                                        ),
                                        ft.TextButton(
                                            "Lihat Perawatan →",
                                            on_click=lambda _, uid=ubi_id: go_to_detail(
                                                uid
                                            ),
                                            style=ft.ButtonStyle(
                                                color=HIJAU_RUMPUT,
                                                padding=ft.Padding(0, 0, 0, 0),
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
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
                        controls=[
                            ft.Container(
                                padding=ft.Padding(20, 20, 20, 16),
                                content=ft.Column(
                                    spacing=4,
                                    controls=[
                                        ft.Text(
                                            "Jenis Umbi",
                                            size=24,
                                            weight=ft.FontWeight.W_900,
                                            color=BIRU_TUA,
                                        ),
                                        ft.Text(
                                            "Pilih umbi untuk melihat cara perawatannya",
                                            size=13,
                                            color=ft.Colors.GREY_700,
                                        ),
                                    ],
                                ),
                            ),
                            ft.Container(
                                expand=True,
                                padding=ft.Padding(16, 0, 16, 0),
                                content=ft.ListView(
                                    controls=list_pilihan,
                                    expand=True,
                                ),
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
            body = ft.Text("Data tidak ditemukan")
        else:
            data = MOCK_DATA_UBI[ubi_id]
            warna = data["warna"]

            perawatan_items = []
            for baris in data["perawatan"].split("\n"):
                if baris.strip():
                    perawatan_items.append(
                        ft.Container(
                            margin=ft.Margin(0, 0, 0, 10),
                            padding=ft.Padding(12, 12, 12, 12),
                            border_radius=10,
                            bgcolor=ft.Colors.WHITE,
                            shadow=ft.BoxShadow(
                                blur_radius=6,
                                color=ft.Colors.with_opacity(0.08, ft.Colors.BLACK),
                            ),
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.CHECK_CIRCLE,
                                        color=HIJAU_RUMPUT,
                                        size=20,
                                    ),
                                    ft.Container(width=10),
                                    ft.Text(
                                        baris.strip(),
                                        size=14,
                                        color=BIRU_TUA,
                                        expand=True,
                                    ),
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.START,
                            ),
                        )
                    )

            body = ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                controls=[
                    ft.Container(
                        width=float("inf"),
                        padding=ft.Padding(24, 24, 24, 24),
                        border_radius=ft.BorderRadius(
                            top_left=0,
                            top_right=0,
                            bottom_left=24,
                            bottom_right=24,
                        ),
                        gradient=ft.LinearGradient(
                            begin=ft.Alignment(-1, -1),
                            end=ft.Alignment(1, 1),
                            colors=[warna, BIRU_TUA],
                        ),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(data["icon"], size=60, color=ft.Colors.WHITE),
                                ft.Container(height=8),
                                ft.Text(
                                    data["nama"],
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        padding=ft.Padding(20, 20, 20, 20),
                        content=ft.Column(
                            spacing=12,
                            controls=[
                                ft.Text(
                                    "Deskripsi",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=BIRU_TUA,
                                ),
                                ft.Container(
                                    padding=ft.Padding(16, 16, 16, 16),
                                    border_radius=12,
                                    bgcolor=ft.Colors.WHITE,
                                    shadow=ft.BoxShadow(
                                        blur_radius=8,
                                        color=ft.Colors.with_opacity(
                                            0.08, ft.Colors.BLACK
                                        ),
                                    ),
                                    content=ft.Text(
                                        data["deskripsi"],
                                        size=14,
                                        color=ft.Colors.GREY_800,
                                    ),
                                ),
                                ft.Container(height=4),
                                ft.Text(
                                    "Cara Perawatan",
                                    size=16,
                                    font_family="Cochon",
                                    weight=ft.FontWeight.BOLD,
                                    color=BIRU_TUA,
                                ),
                                *perawatan_items,
                            ],
                        ),
                    ),
                ],
            )

        return ft.View(
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor=PUTIH_CLOUD,
                    content=body,
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
