# Copyright 2020 Артём Воронов
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class Help:
    def __init__(self):
        self.commands = {
            "tavern": {
                "stats": {
                    "aliases": ["profile"],
                    "syntax": "",
                    "description": "Показыват ваш профиль",
                    "syntax_description": "",
                    "is_alias": False
                },
                "profile": {
                    "aliases": ["stats"],
                    "syntax": "",
                    "description": "Показыват ваш профиль",
                    "syntax_description": "",
                    "is_alias": True
                },
                "top": {
                    "aliases": [],
                    "syntax": "",
                    "description": "Показать рейтинг игроков на сервере",
                    "syntax_description": "",
                    "is_alias": False
                }
            },
            "shop": {
                "shop": {
                    "aliases": [],
                    "syntax": "[type]",
                    "description": "Показать доступные к покупке предметы",
                    "syntax_description": "[type] - тип предметов (Weapon / Armor)\n\n",
                    "is_alias": False
                },
                "buy": {
                    "aliases": [],
                    "syntax": "[type] [item]",
                    "description": "Купить предмет и применить его",
                    "syntax_description": "[type] - тип предметов (Weapon / Armor)\n"
                                          "[item] - имя предмета\n\n",
                    "is_alias": False
                }
            },
            "adventure": {
                "moblist": {
                    "aliases": ["mobs"],
                    "syntax": "",
                    "description": "Показать имена всех существ",
                    "syntax_description": "",
                    "is_alias": False
                },
                "mobs": {
                    "aliases": ["moblist"],
                    "syntax": "",
                    "description": "Показать имена всех существ",
                    "syntax_description": "",
                    "is_alias": True
                },
                "mob": {
                    "aliases": [],
                    "syntax": "[name]",
                    "description": "Показать информацию о существе",
                    "syntax_description": "[name] - имя существа\n\n",
                    "is_alias": False
                },
                "fight": {
                    "aliases": [],
                    "syntax": "[name]",
                    "description": "Начать битву с существом",
                    "syntax_description": "[name] - имя существа\n\n",
                    "is_alias": False
                }
            },
        }

        self.admin_commands = {
            "guild_deploy": {
                    "aliases": ["glddep"],
                    "syntax": "",
                    "description": "Создать роли и каналы для бота. Работает в любом канали и только если бот еще небыл развернут.",
                    "syntax_description": "",
                    "is_alias": False
                },
                "glddep": {
                    "aliases": ["guild_deploy"],
                    "syntax": "",
                    "description": "Создать роли и каналы для бота. Работает в любом канали и только если бот еще небыл развернут.",
                    "syntax_description": "",
                    "is_alias": True
                },
                "upload_image": {
                    "aliases": [],
                    "syntax": "",
                    "description": "Загружает изображение на сервер. Требуется прикрепить изображение к сообщению",
                    "syntax_description": "",
                    "is_alias": False
                },
                "guild_remove": {
                    "aliases": ["gldrem"],
                    "syntax": "",
                    "description": "Удалять все каналы и роли бота, после чего бот выходит с сервера.",
                    "syntax_description": "",
                    "is_alias": False
                },
                "gldrem": {
                    "aliases": ["guild_remove"],
                    "syntax": "",
                    "description": "Удалять все каналы и роли бота, после чего бот выходит с сервера.",
                    "syntax_description": "",
                    "is_alias": True
                },
                "guild_remove_soft": {
                    "aliases": ["gldrems"],
                    "syntax": "",
                    "description": "Удалять все каналы и роли бота, но оставляет бота на сервере. После этого доступа guild_deploy для перезагрузки всех каналов и ролей",
                    "syntax_description": "",
                    "is_alias": False
                },
                "gldrems": {
                    "aliases": ["guild_remove_soft"],
                    "syntax": "",
                    "description": "Удалять все каналы и роли бота, но оставляет бота на сервере. После этого доступа guild_deploy для перезагрузки всех каналов и ролей",
                    "syntax_description": "",
                    "is_alias": True
                },
                "set_slowmode": {
                    "aliases": ["setslow"],
                    "syntax": "[seconds]",
                    "description": "Установить медленный режим на всех каналах бота",
                    "syntax_description": "[seconds] - количество секунд",
                    "is_alias": False
                },
                "setslow": {
                    "aliases": ["set_slowmode"],
                    "syntax": "[seconds]",
                    "description": "Установить медленный режим на всех каналах бота",
                    "syntax_description": "[seconds] - количество секунд",
                    "is_alias": True
                },
                "edit_mob": {
                    "aliases": [],
                    "syntax": "[name] [column] [new]",
                    "description": "Изменить параметр у существующего моба",
                    "syntax_description": "[name] - имя моба\n"
                                          "[column] - параметр, который меняем\n"
                                          "[new] - новое значение",
                    "is_alias": False
                },
                "remove_mob": {
                    "aliases": ["delmob"],
                    "syntax": "[name]",
                    "description": "Удалить моба",
                    "syntax_description": "[name] - имя моба",
                    "is_alias": False
                },
                "delmob": {
                    "aliases": ["remove_mob"],
                    "syntax": "[name]",
                    "description": "Удалить моба",
                    "syntax_description": "[name] - имя моба",
                    "is_alias": True
                },
                "create_mob": {
                    "aliases": ["makemob"],
                    "syntax": "[name] [bowed_name] [exp] [power] [hp] [money] <icon> <color>",
                    "description": "Добавить моба",
                    "syntax_description": "[name] - имя моба\n"
                                          "[bowed_name] - имя моба в творительном падеже для битвы (прим. Орк - Орком)\n"
                                          "[exp] - кол-во опыта за моба\n"
                                          "[power] - урон моба\n"
                                          "[hp] - здоровье моба\n"
                                          "[money] - кол-во монет за моба\n"
                                          "<icon> - (необязательный) имя загруженной картинки для моба\n"
                                          "<color>- (необязательный) цвет моба в int формате. Конвертер из RGB: https://vk.cc/bWgju3",
                    "is_alias": False
                },
                "makemob": {
                    "aliases": ["create_mob"],
                    "syntax": "[name] [bowed_name] [exp] [power] [hp] [money] <icon> <color>",
                    "description": "Добавить моба",
                    "syntax_description": "[name] - имя моба\n"
                                          "[bowed_name] - имя моба в творительном падеже для битвы (прим. Орк - Орком)\n"
                                          "[exp] - кол-во опыта за моба\n"
                                          "[power] - урон моба\n"
                                          "[hp] - здоровье моба\n"
                                          "[money] - кол-во монет за моба\n"
                                          "<icon> - (необязательный) имя загруженной картинки для моба\n"
                                          "<color>- (необязательный) цвет моба в int формате. Конвертер из RGB: shorturl.at/vBKLN",
                    "is_alias": True
                },
                "get_mob_info": {
                    "aliases": ["mobinfo"],
                    "syntax": "[name]",
                    "description": "Вывести полную информацию о мобе",
                    "syntax_description": "[name] - имя моба",
                    "is_alias": False
                },
                "mobinfo": {
                    "aliases": ["get_mob_info"],
                    "syntax": "[name]",
                    "description": "Вывести полную информацию о мобе",
                    "syntax_description": "[name] - имя моба",
                    "is_alias": True
                },
                "add_shop_item": {
                    "aliases": ["additem"],
                    "syntax": "[type] [name] [stat] [price]",
                    "description": "Добавить предмет",
                    "syntax_description": "[type] - тип предметов (Weapon / Armor)\n"
                                          "[name] - имя предмета\n"
                                          "[stat] - характеристика предмета (hp для брони / power для оружия)\n"
                                          "[price] - цена предмета",
                    "is_alias": False
                },
                "additem": {
                    "aliases": ["add_shop_item"],
                    "syntax": "[type] [name] [stat] [price]",
                    "description": "Добавить предмет",
                    "syntax_description": "[type] - тип предметов (Weapon / Armor)\n"
                                          "[name] - имя предмета\n"
                                          "[stat] - характеристика предмета (hp для брони / power для оружия)\n"
                                          "[price] - цена предмета",
                    "is_alias": True
                },
                "edit_shop_item": {
                    "aliases": ["edititem"],
                    "syntax": "[type] [name] [stat] [new]",
                    "description": "Изменить параметр у существующего предмета",
                    "syntax_description": "[type] - тип предметов (Weapon / Armor)\n"
                                          "[name] - имя предмета\n"
                                          "[column] - параметр, который меняем\n"
                                          "[new] - новое значение",
                    "is_alias": False
                },
                "edititem": {
                    "aliases": ["edit_shop_item"],
                    "syntax": "[type] [name] [stat] [new]",
                    "description": "Изменить параметр у существующего предмета",
                    "syntax_description": "[type] - тип предметов (Weapon / Armor)\n"
                                          "[name] - имя предмета\n"
                                          "[column] - параметр, который меняем\n"
                                          "[new] - новое значение",
                    "is_alias": True
                },
                "remove_shop_item": {
                    "aliases": ["removeitem", "delitem"],
                    "syntax": "[type] [name]",
                    "description": "Удалить предмет",
                    "syntax_description": "[type] - тип предметов (Weapon / Armor)\n"
                                          "[name] - имя предмета",
                    "is_alias": False
                },
                "removeitem": {
                    "aliases": ["remove_shop_item", "delitem"],
                    "syntax": "[type] [name]",
                    "description": "Удалить предмет",
                    "syntax_description": "[type] - тип предметов (Weapon / Armor)\n"
                                          "[name] - имя предмета",
                    "is_alias": True
                },
                "delitem": {
                    "aliases": ["removeitem", "remove_shop_item"],
                    "syntax": "[type] [name]",
                    "description": "Удалить предмет",
                    "syntax_description": "[type] - тип предметов (Weapon / Armor)\n"
                                          "[name] - имя предмета",
                    "is_alias": True
                },
                "admin_help": {
                    "aliases": ["adminhelp", "adhelp"],
                    "syntax": "",
                    "description": "Вывести это сообщение",
                    "syntax_description": "",
                    "is_alias": False
                },
                "adminhelp": {
                    "aliases": ["admin_help", "adhelp"],
                    "syntax": "",
                    "description": "Вывести это сообщение",
                    "syntax_description": "",
                    "is_alias": True
                },
                "adhelp": {
                    "aliases": ["adminhelp", "admin_help"],
                    "syntax": "",
                    "description": "Вывести это сообщение",
                    "syntax_description": "",
                    "is_alias": True
                },
                "admin_help [command]": {
                    "aliases": ["adminhelp", "adhelp"],
                    "syntax": "",
                    "description": "Вывести подбробную информация о команде",
                    "syntax_description": "[command] - админская команда",
                    "is_alias": False
                },
                "adminhelp [command]": {
                    "aliases": ["admin_help", "adhelp"],
                    "syntax": "",
                    "description": "Вывести подбробную информация о команде",
                    "syntax_description": "[command] - админская команда",
                    "is_alias": True
                },
                "adhelp [command]": {
                    "aliases": ["adminhelp", "admin_help"],
                    "syntax": "",
                    "description": "Вывести подбробную информация о команде",
                    "syntax_description": "[command] - админская команда",
                    "is_alias": True
                },
            }

    def get_command(self, command):
        types = ["tavern", "shop", "adventure"]
        found = False
        for type in types:
            try:
                command = self.commands[type][command]
                found = True
                break
            except KeyError:
                continue
        if found:
            command["type"] = type
            return command
        return None

    def get_admin_command(self, command):
        try:
            command = self.admin_commands[command]
            return command
        except KeyError:
            return None
