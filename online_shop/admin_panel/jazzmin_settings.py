JAZZMIN_SETTINGS = {
    "site_title": "1000 Мелочей",
    "site_header": "Админка Магазина",
    "site_brand": "1000 Мелочей",
    "site_logo": "img/logo.png",
    "welcome_sign": "Добро пожаловать в админку",
    "show_sidebar": True,
    "topmenu_links": [
        {"name": "Главная", "url": "admin:index",
            "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
        {"app": "store"},
        {"name": "Статистика", "url": "/admin/dashboard/",
            "permissions": ["auth.view_user"]},
    ],
    "icons": {
        "auth": "fas fa-users-cog",
        "users.customuser": "fas fa-user",
        "auth.Group": "fas fa-users",
        "store.shoppingcart": "fas fa-shopping-cart",
        "store.category": "fas fa-list",
        "store.maincategory": "fas fa-layer-group",
        "store.product": "fas fa-box",
    },
    "custom_links": {
        "store": [
            {
                "name": "Перейти на сайт",
                "url": "store:home",
                "icon": "fas fa-globe",
                "permissions": ["auth.view_user"],
            },
        ]
    },
    "show_ui_builder": True,
}