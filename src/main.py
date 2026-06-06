import flet as ft
import asyncio

MOCK_DATA_UBI = {
    1: {
        "nama": "Ubi Cilembu",
        "deskripsi": "Ubi khas Sumedang yang terkenal dengan rasa manis seperti madu ketika dipanggang.",
        "perawatan": "1. Penyiraman rutin 1-2 kali sehari.\n2. Pastikan tanah gembur.\n3. Panen umur 4-5 bulan.",
    },
    2: {
        "nama": "Ubi Jalar Ungu",
        "deskripsi": "Ubi yang memiliki warna ungu pekat kaya akan antioksidan.",
        "perawatan": "1. Sinar matahari penuh.\n2. Lakukan pendangiran berkala.\n3. Beri pupuk organik.",
    },
    3: {
        "nama": "Singkong (Ubi Kayu)",
        "deskripsi": "Tanaman perdu tahunan tropika yang dimanfaatkan umbi dan daunnya.",
        "perawatan": "1. Tanam stek batang berkualitas.\n2. Penyiangan gulma penting.\n3. Panen usia 7-9 bulan.",
    },
}


def main(page: ft.Page):
    page.title = "Aplikasi Identifikasi Ubi"
    page.theme_mode = ft.ThemeMode.LIGHT

    # ===== BUILD VIEWS =====

    def build_login_view():
        txt_username = ft.TextField(
            label="Username", width=300, prefix_icon=ft.Icons.PERSON
        )
        txt_password = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=300,
            prefix_icon=ft.Icons.LOCK,
        )
        lbl_error = ft.Text(value="", color=ft.Colors.RED_500)

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
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.SPA, size=80, color=ft.Colors.GREEN_700),
                            ft.Text(
                                "Identifikasi Ubi",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_800,
                            ),
                            txt_username,
                            txt_password,
                            lbl_error,
                            ft.Button(
                                "Masuk",
                                on_click=login_clicked,
                                width=300,
                                bgcolor=ft.Colors.GREEN_700,
                                color=ft.Colors.WHITE,
                            ),
                            ft.TextButton(
                                "Belum punya akun? Daftar",
                                on_click=lambda _: navigate_to("register"),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                )
            ],
            route="/",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        )

    def build_register_view():
        txt_username = ft.TextField(
            label="Buat Username", width=300, prefix_icon=ft.Icons.PERSON_ADD
        )
        txt_password = ft.TextField(
            label="Buat Password",
            password=True,
            width=300,
            prefix_icon=ft.Icons.PASSWORD,
        )
        lbl_status = ft.Text(value="", color=ft.Colors.RED_500)

        async def register_clicked(e):
            if not txt_username.value or not txt_password.value:
                lbl_status.value = "Isi dulu datanya!"
                lbl_status.color = ft.Colors.RED_500
                page.update()
            else:
                lbl_status.value = "Berhasil! Kembali ke login..."
                lbl_status.color = ft.Colors.GREEN_600
                page.update()
                await asyncio.sleep(1)
                navigate_to("login")

        return ft.View(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Registrasi",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                            ),
                            txt_username,
                            txt_password,
                            lbl_status,
                            ft.Button(
                                "Daftar Sekarang",
                                on_click=register_clicked,
                                width=300,
                                bgcolor=ft.Colors.GREEN_700,
                                color=ft.Colors.WHITE,
                            ),
                            ft.TextButton(
                                "Kembali ke Login",
                                on_click=lambda _: navigate_to("login"),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                ),
            ],
            route="/register",
            appbar=ft.AppBar(
                title=ft.Text("Daftar Akun Baru"),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                automatically_imply_leading=False,
            ),
            vertical_alignment=ft.MainAxisAlignment.CENTER,
        )

    def build_dashboard_view():
        list_pilihan = []
        for ubi_id, data in MOCK_DATA_UBI.items():
            list_pilihan.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(
                                        ft.Icons.ECO, color=ft.Colors.GREEN_600
                                    ),
                                    title=ft.Text(
                                        data["nama"], weight=ft.FontWeight.BOLD
                                    ),
                                    subtitle=ft.Text(
                                        data["deskripsi"],
                                        max_lines=2,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                ),
                                ft.Row(
                                    [
                                        ft.TextButton(
                                            "Lihat Cara Perawatan",
                                            on_click=lambda _, uid=ubi_id: go_to_detail(
                                                uid
                                            ),
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ]
                        ),
                        padding=10,
                    )
                )
            )

        return ft.View(
            controls=[
                ft.ListView(controls=list_pilihan, expand=True, padding=10),
            ],
            route="/dashboard",
            appbar=ft.AppBar(
                title=ft.Text("Pilih Jenis Ubi"),
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
                automatically_imply_leading=False,
                actions=[
                    ft.IconButton(
                        ft.Icons.LOGOUT,
                        icon_color=ft.Colors.WHITE,
                        on_click=lambda _: navigate_to("login"),
                    )
                ],
            ),
        )

    def build_detail_view(ubi_id: int):
        if not ubi_id or ubi_id not in MOCK_DATA_UBI:
            body = ft.Text("Data tidak ditemukan")
        else:
            data = MOCK_DATA_UBI[ubi_id]
            body = ft.Column(
                [
                    ft.Text(
                        data["nama"],
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_900,
                    ),
                    ft.Divider(),
                    ft.Text("Deskripsi:", size=16, weight=ft.FontWeight.BOLD),
                    ft.Text(data["deskripsi"], size=14),
                    ft.Container(height=15),
                    ft.Text(
                        "Cara Perawatan:",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_700,
                    ),
                    ft.Text(data["perawatan"], size=14),
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )

        return ft.View(
            controls=[
                ft.Container(content=body, padding=20, expand=True),
            ],
            route="/detail",
            appbar=ft.AppBar(
                title=ft.Text("Detail Ubi"),
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
                leading=ft.IconButton(
                    ft.Icons.ARROW_BACK,
                    icon_color=ft.Colors.WHITE,
                    on_click=lambda _: navigate_back(),
                ),
                automatically_imply_leading=False,
            ),
        )

    # ===== NAVIGASI =====

    def navigate_to(screen: str):
        if screen == "login":
            page.views.clear()
            page.views.append(build_login_view())
        elif screen == "register":
            page.views.append(build_register_view())
        elif screen == "dashboard":
            page.views.clear()
            page.views.append(build_login_view())
            page.views.append(build_dashboard_view())
        page.update()

    def go_to_detail(ubi_id: int):
        page.views.append(build_detail_view(ubi_id))
        page.update()

    def navigate_back():
        if len(page.views) > 1:
            page.views.pop()
            page.update()

    # ===== INIT =====

    page.on_view_pop = lambda e: navigate_back()

    page.views.append(build_login_view())
    page.update()


ft.run(main)
