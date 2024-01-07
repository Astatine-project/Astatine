import discord
from discord.ext import commands
import sqlite3
import random
from random import choice
import peewee
from peewee import *
from Astatine_base import Money, Bank, Shop, Language

class Econ(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="give_money", description="give some amount of your 💷 to mentioned user")
    async def give_money(self, ctx, user: discord.Member, *, much: int):
        if much < 0:
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        money_emb = discord.Embed(
                            title="Ошибка [Отрицательная сумма]",
                            color=0x39d0d6)
                        money_emb.add_field(name='Вы можете указывать только положительные суммы!', value=f'Вы указали: {much} 💷', inline=False)
                        await ctx.respond(embed=money_emb, ephemeral=True)
                    else:
                        money_emb = discord.Embed(
                            title="Error [Negative amount]",
                            color=0x39d0d6)
                        money_emb.add_field(name='You can only specify positive amounts!',
                                            value=f'You specified: {much} 💷', inline=False)
                        await ctx.respond(embed=money_emb, ephemeral=True)
            else:
                money_emb = discord.Embed(
                    title="Error [Negative amount]",
                    color=0x39d0d6)
                money_emb.add_field(name='You can only specify positive amounts!',
                                    value=f'You specified: {much} 💷', inline=False)
                await ctx.respond(embed=money_emb, ephemeral=True)
        else:
            if user.id == ctx.author.id:
                getlang = Language.get_or_none(guild_id=ctx.guild.id)
                if getlang is not None:
                    for language in Language.select().where(Language.guild_id == ctx.guild.id):
                        if language.lang == "ru":
                            money_emb = discord.Embed(
                                title="Ошибка [Попытка обратного перевода]",
                                color=0x39d0d6)
                            money_emb.add_field(name='Вы не можете давать свои 💷 себе же!',
                                                value=f'Вы указали: {much} 💷', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                        else:
                            money_emb = discord.Embed(
                                title="Error [Trying to give money to yourself]",
                                color=0x39d0d6)
                            money_emb.add_field(name='You cant give your 💷 to yourself!',
                                                value=f'You specified: {much} 💷', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                else:
                    money_emb = discord.Embed(
                        title="Error [Trying to give money to yourself]",
                        color=0x39d0d6)
                    money_emb.add_field(name='You cant give your 💷 to yourself!',
                                        value=f'You specified: {much} 💷', inline=False)
                    await ctx.respond(embed=money_emb, ephemeral=True)
            else:
                if user.bot:
                    getlang = Language.get_or_none(guild_id=ctx.guild.id)
                    if getlang is not None:
                        for language in Language.select().where(Language.guild_id == ctx.guild.id):
                            if language.lang == "ru":
                                money_emb = discord.Embed(
                                    title="Ошибка [Попытка перевода боту]",
                                    color=0x39d0d6)
                                money_emb.add_field(name='Вы не можете переводить 💷 боту!',
                                                    value=f'Вы указали: {much} 💷', inline=False)
                                await ctx.respond(embed=money_emb, ephemeral=True)
                            else:
                                money_emb = discord.Embed(
                                    title="Error [Trying to give money to a bot]",
                                    color=0x39d0d6)
                                money_emb.add_field(name='You cant give 💷 to a bot!',
                                                    value=f'You specified: {much} 💷', inline=False)
                                await ctx.respond(embed=money_emb, ephemeral=True)
                    else:
                        money_emb = discord.Embed(
                            title="Error [Trying to give money to a bot]",
                            color=0x39d0d6)
                        money_emb.add_field(name='You cant give 💷 to a bot!',
                                            value=f'You specified: {much} 💷', inline=False)
                        await ctx.respond(embed=money_emb, ephemeral=True)
                else:
                    for money in Money.select().where(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id):
                        if money.amount < much:
                            getlang = Language.get_or_none(guild_id=ctx.guild.id)
                            if getlang is not None:
                                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                                    if language.lang == "ru":
                                        money_emb = discord.Embed(
                                            title="Ошибка [Недостаточно средств]",
                                            color=0x39d0d6)
                                        money_emb.add_field(name='У вас недостаточно 💷!',
                                                            value=f'Вы указали: {much} 💷', inline=False)
                                        await ctx.respond(embed=money_emb, ephemeral=True)
                                    else:
                                        money_emb = discord.Embed(
                                            title="Error [Not enough money]",
                                            color=0x39d0d6)
                                        money_emb.add_field(name='You dont have enough 💷!',
                                                            value=f'You specified: {much} 💷', inline=False)
                                        await ctx.respond(embed=money_emb, ephemeral=True)
                            else:
                                money_emb = discord.Embed(
                                    title="Error [Not enough money]",
                                    color=0x39d0d6)
                                money_emb.add_field(name='You dont have enough 💷!',
                                                    value=f'You specified: {much} 💷', inline=False)
                                await ctx.respond(embed=money_emb, ephemeral=True)
                        else:
                            for money in Money.select().where(Money.user_id == ctx.author.id,
                                                              Money.guild_id == ctx.guild.id):
                                delete = Money.get(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id)
                                delete.delete_instance()
                                account = Money.create(user_id=ctx.author.id, amount=money.amount - much,
                                                       guild_id=ctx.guild.id)
                                for money in Money.select().where(Money.user_id == user.id,
                                                                  Money.guild_id == ctx.guild.id):
                                    delete = Money.get(Money.user_id == user.id, Money.guild_id == ctx.guild.id)
                                    delete.delete_instance()
                                    account = Money.create(user_id=user.id, amount=money.amount + much,
                                                           guild_id=ctx.guild.id)
                                    getlang = Language.get_or_none(guild_id=ctx.guild.id)
                                    if getlang is not None:
                                        for language in Language.select().where(Language.guild_id == ctx.guild.id):
                                            if language.lang == "ru":
                                                money_emb = discord.Embed(
                                                    title="Успешный перевод!",
                                                    color=0x39d0d6)
                                                money_emb.add_field(name=f'Вы перевели {much} 💷 пользователю: {user.name}',
                                                                    value='---------------------', inline=False)
                                                await ctx.respond(embed=money_emb, ephemeral=True)
                                            else:
                                                money_emb = discord.Embed(
                                                    title="Success!",
                                                    color=0x39d0d6)
                                                money_emb.add_field(
                                                    name=f'You gave {much} 💷 to user: {user.name}',
                                                    value='---------------------', inline=False)
                                                await ctx.respond(embed=money_emb, ephemeral=True)
                                    else:
                                        money_emb = discord.Embed(
                                            title="Success!",
                                            color=0x39d0d6)
                                        money_emb.add_field(
                                            name=f'You gave {much} 💷 to user: {user.name}',
                                            value='---------------------', inline=False)
                                        await ctx.respond(embed=money_emb, ephemeral=True)

    @commands.slash_command(name="balance", description="shows your current balance")
    async def balance(self, ctx, user: discord.Member = None):
        if user is None:
            getbank = Bank.get_or_none(guild_id=ctx.guild.id, user_id=ctx.author.id)
            if getbank is None:
                bank_amount = 0
            else:
                for bank in Bank.select().where(Bank.user_id == ctx.author.id, Bank.guild_id == ctx.guild.id):
                    bank_amount = bank.amount
            for money in Money.select().where(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id):
                getlang = Language.get_or_none(guild_id=ctx.guild.id)
                if getlang is not None:
                    for language in Language.select().where(Language.guild_id == ctx.guild.id):
                        if language.lang == "ru":
                            balance_emb = discord.Embed(title=f'Баланс пользователя {ctx.author}', colour=0x39d0d6)
                            balance_emb.add_field(name='На счету:', value=f'{money.amount} 💷', inline=False)
                            balance_emb.add_field(name='В банке:', value=f'{bank_amount} 💷', inline=False)
                            await ctx.respond(embed=balance_emb)
                        else:
                            balance_emb = discord.Embed(title=f'User balance {ctx.author}', colour=0x39d0d6)
                            balance_emb.add_field(name='Wallet:', value=f'{money.amount} 💷', inline=False)
                            balance_emb.add_field(name='Bank:', value=f'{bank_amount} 💷', inline=False)
                            await ctx.respond(embed=balance_emb)
                else:
                    balance_emb = discord.Embed(title=f'User balance {ctx.author}', colour=0x39d0d6)
                    balance_emb.add_field(name='Wallet:', value=f'{money.amount} 💷', inline=False)
                    balance_emb.add_field(name='Bank:', value=f'{bank_amount} 💷', inline=False)
                    await ctx.respond(embed=balance_emb)
        elif user is not None:
            if user.bot:
                getlang = Language.get_or_none(guild_id=ctx.guild.id)
                if getlang is not None:
                    for language in Language.select().where(Language.guild_id == ctx.guild.id):
                        if language.lang == "ru":
                            money_emb = discord.Embed(
                                title="Ошибка [Бот, это не пользователь!]",
                                color=0x39d0d6)
                            money_emb.add_field(name='Баланс можно смотреть только у пользователей!',
                                                value=f'Вы указали бота: {user.name} 💷', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                        else:
                            money_emb = discord.Embed(
                                title="Error [Bot is not a user!]",
                                color=0x39d0d6)
                            money_emb.add_field(name='The balance can only be viewed from users!',
                                                value=f'You specified bot: {user.name} 💷', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                else:
                    money_emb = discord.Embed(
                        title="Error [Bot is not a user!]",
                        color=0x39d0d6)
                    money_emb.add_field(name='The balance can only be viewed from users!',
                                        value=f'You specified bot: {user.name} 💷', inline=False)
                    await ctx.respond(embed=money_emb, ephemeral=True)
            else:
                getbank = Bank.get_or_none(guild_id=ctx.guild.id, user_id=user.id)
                if getbank is None:
                    bank_amount = 0
                else:
                    for bank in Bank.select().where(Bank.user_id == user.id, Bank.guild_id == ctx.guild.id):
                        bank_amount = bank.amount
                for money in Money.select().where(Money.user_id == user.id, Money.guild_id == ctx.guild.id):
                    getlang = Language.get_or_none(guild_id=ctx.guild.id)
                    if getlang is not None:
                        for language in Language.select().where(Language.guild_id == ctx.guild.id):
                            if language.lang == "ru":
                                balance_emb = discord.Embed(title=f'Баланс пользователя {user}', colour=0x39d0d6)
                                balance_emb.add_field(name='На счету:', value=f'{money.amount} 💷', inline=False)
                                balance_emb.add_field(name='В банке:', value=f'{bank_amount} 💷', inline=False)
                                await ctx.respond(embed=balance_emb)
                            else:
                                balance_emb = discord.Embed(title=f'User balance {user}', colour=0x39d0d6)
                                balance_emb.add_field(name='Wallet:', value=f'{money.amount} 💷', inline=False)
                                balance_emb.add_field(name='Bank:', value=f'{bank_amount} 💷', inline=False)
                                await ctx.respond(embed=balance_emb)
                    else:
                        balance_emb = discord.Embed(title=f'User balance {user}', colour=0x39d0d6)
                        balance_emb.add_field(name='Wallet:', value=f'{money.amount} 💷', inline=False)
                        balance_emb.add_field(name='Bank:', value=f'{bank_amount} 💷', inline=False)
                        await ctx.respond(embed=balance_emb)

    @commands.slash_command(name="set_money", description="sets mentioned amount of 💷 to mentioned user")
    @commands.has_permissions(administrator=True)
    async def set_money(self, ctx, user: discord.Member, *, much: int):
        if much < 0:
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        money_emb = discord.Embed(
                            title="Ошибка [Отрицательная сумма]",
                            color=0x39d0d6)
                        money_emb.add_field(name='Вы можете указывать только положительные суммы!',
                                            value=f'Вы указали: {much} 💷', inline=False)
                        await ctx.respond(embed=money_emb, ephemeral=True)
                    else:
                        money_emb = discord.Embed(
                            title="Error [Negative amount]",
                            color=0x39d0d6)
                        money_emb.add_field(name='You can only specify positive amounts!',
                                            value=f'You specified: {much} 💷', inline=False)
                        await ctx.respond(embed=money_emb, ephemeral=True)
            else:
                money_emb = discord.Embed(
                    title="Error [Negative amount]",
                    color=0x39d0d6)
                money_emb.add_field(name='You can only specify positive amounts!',
                                    value=f'You specified: {much} 💷', inline=False)
                await ctx.respond(embed=money_emb, ephemeral=True)
        else:
            if user.bot:
                getlang = Language.get_or_none(guild_id=ctx.guild.id)
                if getlang is not None:
                    for language in Language.select().where(Language.guild_id == ctx.guild.id):
                        if language.lang == "ru":
                            money_emb = discord.Embed(
                                title="Ошибка [Попытка перевода боту]",
                                color=0x39d0d6)
                            money_emb.add_field(name='Вы не можете переводить 💷 боту!',
                                                value=f'Вы указали: {much} 💷', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                        else:
                            money_emb = discord.Embed(
                                title="Error [Trying to give money to a bot]",
                                color=0x39d0d6)
                            money_emb.add_field(name='You cant give 💷 to a bot!',
                                                value=f'You specified: {much} 💷', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                else:
                    money_emb = discord.Embed(
                        title="Error [Trying to give money to a bot]",
                        color=0x39d0d6)
                    money_emb.add_field(name='You cant give 💷 to a bot!',
                                        value=f'You specified: {much} 💷', inline=False)
                    await ctx.respond(embed=money_emb, ephemeral=True)
            else:
                delete = Money.get(Money.user_id == user.id, Money.guild_id == ctx.guild.id)
                delete.delete_instance()
                account = Money.create(user_id=user.id, amount=much, guild_id=ctx.guild.id)
                getlang = Language.get_or_none(guild_id=ctx.guild.id)
                if getlang is not None:
                    for language in Language.select().where(Language.guild_id == ctx.guild.id):
                        if language.lang == "ru":
                            money_emb = discord.Embed(
                                title="Успешная установка!",
                                color=0x39d0d6)
                            money_emb.add_field(name=f'Вы установили {much} 💷 пользователю: {user.name}',
                                                value='---------------------', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                        else:
                            money_emb = discord.Embed(
                                title="Success!",
                                color=0x39d0d6)
                            money_emb.add_field(
                                name=f'You set {much} 💷 for user: {user.name}',
                                value='---------------------', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                else:
                    money_emb = discord.Embed(
                        title="Success!",
                        color=0x39d0d6)
                    money_emb.add_field(
                        name=f'You gave {much} 💷 for user: {user.name}',
                        value='---------------------', inline=False)
                    await ctx.respond(embed=money_emb, ephemeral=True)

    @commands.slash_command(name="work", description="you can earn some 💷, but your salary is not stable")
    @commands.cooldown(1, 10000.0, commands.BucketType.member)
    async def work(self, ctx, type: discord.Option(str, choices=[
        discord.OptionChoice(name="crime", value="crime", name_localizations=None),
        discord.OptionChoice(name="business", value="business", name_localizations=None),
        discord.OptionChoice(name="casual", value="casual", name_localizations=None)]), user: discord.Member = None):
        if type == 'crime':
            luck = random.randint(1, 5)
            if luck < 3:
                crime = random.randint(1, 200)
                for money in Money.select().where(Money.user_id == user.id, Money.guild_id == ctx.guild.id):
                    if money.amount == 0:
                        getlang = Language.get_or_none(guild_id=ctx.guild.id)
                        if getlang is not None:
                            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                                if language.lang == "ru":
                                    money_emb = discord.Embed(
                                        title="Ошибка [Недостаточно средств]",
                                        color=0x39d0d6)
                                    money_emb.add_field(name=f'У пользователя {user.name} недостаточно денег, вы не можете его ограбить',
                                                        value='---------------------', inline=False)
                                    await ctx.respond(embed=money_emb, ephemeral=True)
                                else:
                                    money_emb = discord.Embed(
                                        title="Error [Not enough money]",
                                        color=0x39d0d6)
                                    money_emb.add_field(
                                        name=f'User {user.name} does not have enough money, for you to rob him',
                                        value='---------------------', inline=False)
                                    await ctx.respond(embed=money_emb, ephemeral=True)
                        else:
                            money_emb = discord.Embed(
                                title="Error [Not enough money]",
                                color=0x39d0d6)
                            money_emb.add_field(
                                name=f'User {user.name} does not have enough money, for you to rob him',
                                value='---------------------', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                    else:
                        crime = random.randint(1, money.amount)
                        for money in Money.select().where(Money.user_id == user.id, Money.guild_id == ctx.guild.id):
                            delete = Money.get(Money.user_id == user.id, Money.guild_id == ctx.guild.id)
                            delete.delete_instance()
                            account = Money.create(user_id=user.id, amount=money.amount - crime, guild_id=ctx.guild.id)
                            for money in Money.select().where(Money.user_id == ctx.author.id,
                                                              Money.guild_id == ctx.guild.id):
                                delete = Money.get(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id)
                                delete.delete_instance()
                                account = Money.create(user_id=ctx.author.id, amount=money.amount + crime,
                                                       guild_id=ctx.guild.id)
                                getlang = Language.get_or_none(guild_id=ctx.guild.id)
                                if getlang is not None:
                                    for language in Language.select().where(Language.guild_id == ctx.guild.id):
                                        if language.lang == "ru":
                                            money_emb = discord.Embed(
                                                title="Success!",
                                                color=0x39d0d6)
                                            money_emb.add_field(
                                                name=f'Вы успешно ограбили пользователя {user.name}',
                                                value=f'Ваш доход: {money.amount + crime}', inline=False)
                                            await ctx.respond(embed=money_emb, ephemeral=True)
                                        else:
                                            money_emb = discord.Embed(
                                                title="Success!",
                                                color=0x39d0d6)
                                            money_emb.add_field(
                                                name=f'You successfully robbed user {user.name}',
                                                value=f'You got: {money.amount + crime}', inline=False)
                                            await ctx.respond(embed=money_emb, ephemeral=True)
                                else:
                                    money_emb = discord.Embed(
                                        title="Success!",
                                        color=0x39d0d6)
                                    money_emb.add_field(
                                        name=f'You successfully robbed user {user.name}',
                                        value=f'You got: {money.amount + crime}', inline=False)
                                    await ctx.respond(embed=money_emb, ephemeral=True)
            else:
                getlang = Language.get_or_none(guild_id=ctx.guild.id)
                if getlang is not None:
                    for language in Language.select().where(Language.guild_id == ctx.guild.id):
                        if language.lang == "ru":
                            money_emb = discord.Embed(
                                title="Неудача",
                                color=0x39d0d6)
                            money_emb.add_field(
                                name=f'Вам не удалось ограбить {user.name}',
                                value='---------------------', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                        else:
                            money_emb = discord.Embed(
                                title="No success",
                                color=0x39d0d6)
                            money_emb.add_field(
                                name=f'You failed robbering {user.name}',
                                value='---------------------', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                else:
                    money_emb = discord.Embed(
                        title="No success",
                        color=0x39d0d6)
                    money_emb.add_field(
                        name=f'You failed robbering {user.name}',
                        value='---------------------', inline=False)
                    await ctx.respond(embed=money_emb, ephemeral=True)
        elif type == "casual":
            salary = random.randint(1, 150)
            for money in Money.select().where(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id):
                delete = Money.get(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id)
                delete.delete_instance()
                account = Money.create(user_id=ctx.author.id, amount=money.amount + salary, guild_id=ctx.guild.id)
                getlang = Language.get_or_none(guild_id=ctx.guild.id)
                if getlang is not None:
                    for language in Language.select().where(Language.guild_id == ctx.guild.id):
                        if language.lang == "ru":
                            money_emb = discord.Embed(
                                title="Удача!",
                                color=0x39d0d6)
                            money_emb.add_field(
                                name=f'Вы заработали {salary} 💷',
                                value='---------------------', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                        else:
                            money_emb = discord.Embed(
                                title="Success!",
                                color=0x39d0d6)
                            money_emb.add_field(
                                name=f'You earned {salary} 💷',
                                value='---------------------', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                else:
                    money_emb = discord.Embed(
                        title="Success!",
                        color=0x39d0d6)
                    money_emb.add_field(
                        name=f'You earned {salary} 💷',
                        value='---------------------', inline=False)
                    await ctx.respond(embed=money_emb, ephemeral=True)

        elif type == 'business':
            luck = random.randint(1, 20)
            if luck < 9:
                business = random.randint(500, 1000)
                for money in Money.select().where(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id):
                    delete = Money.get(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id)
                    delete.delete_instance()
                    account = Money.create(user_id=ctx.author.id, amount=money.amount + business, guild_id=ctx.guild.id)
                    getlang = Language.get_or_none(guild_id=ctx.guild.id)
                    if getlang is not None:
                        for language in Language.select().where(Language.guild_id == ctx.guild.id):
                            if language.lang == "ru":
                                money_emb = discord.Embed(
                                    title="Удача!",
                                    color=0x39d0d6)
                                money_emb.add_field(
                                    name=f'Ваш бизнес оказался крайне успешным и вы заработали {business} 💷!',
                                    value='---------------------', inline=False)
                                await ctx.respond(embed=money_emb, ephemeral=True)
                            else:
                                money_emb = discord.Embed(
                                    title="Success!",
                                    color=0x39d0d6)
                                money_emb.add_field(
                                    name=f'Your business turned out to be extremely successful and you earned {business} 💷 !',
                                    value='---------------------', inline=False)
                                await ctx.respond(embed=money_emb, ephemeral=True)
                    else:
                        money_emb = discord.Embed(
                            title="Success!",
                            color=0x39d0d6)
                        money_emb.add_field(
                            name=f'Your business turned out to be extremely successful and you earned {business} 💷 !',
                            value='---------------------', inline=False)
                        await ctx.respond(embed=money_emb, ephemeral=True)
            else:
                getlang = Language.get_or_none(guild_id=ctx.guild.id)
                if getlang is not None:
                    for language in Language.select().where(Language.guild_id == ctx.guild.id):
                        if language.lang == "ru":
                            money_emb = discord.Embed(
                                title="Неудача",
                                color=0x39d0d6)
                            money_emb.add_field(
                                name='К сожалению ваш бизнес не удался и прогорел',
                                value='---------------------', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                        else:
                            money_emb = discord.Embed(
                                title="No success",
                                color=0x39d0d6)
                            money_emb.add_field(
                                name='Unfortunately your business failed',
                                value='---------------------', inline=False)
                            await ctx.respond(embed=money_emb, ephemeral=True)
                else:
                    money_emb = discord.Embed(
                        title="No success",
                        color=0x39d0d6)
                    money_emb.add_field(
                        name='Unfortunately your business failed',
                        value='---------------------', inline=False)
                    await ctx.respond(embed=money_emb, ephemeral=True)

    @commands.slash_command(name="deposit", description="Deposit some money to your bank account")
    async def deposit(self, ctx, *, amount: int):
        if amount < 0:
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        money_emb = discord.Embed(
                            title="⚠Вы можете указывать только положительные суммы!⚠",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
                    else:
                        money_emb = discord.Embed(
                            title="⚠You can only specify positive amounts!⚠",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
            else:
                money_emb = discord.Embed(
                    title="⚠You can only specify positive amounts!⚠",
                    color=0x39d0d6)
                await ctx.respond(embed=money_emb)
        else:
            for money in Money.select().where(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id):
                if money.amount < amount:
                    getlang = Language.get_or_none(guild_id=ctx.guild.id)
                    if getlang is not None:
                        for language in Language.select().where(Language.guild_id == ctx.guild.id):
                            if language.lang == "ru":
                                money_emb = discord.Embed(
                                    title="⚠У вас недостаточно 💷⚠",
                                    color=0x39d0d6)
                                await ctx.respond(embed=money_emb)
                            else:
                                money_emb = discord.Embed(
                                    title="⚠You dont have enough 💷⚠",
                                    color=0x39d0d6)
                                await ctx.respond(embed=money_emb)
                    else:
                        money_emb = discord.Embed(
                            title="⚠You dont have enough 💷⚠",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
                else:
                    getbank = Bank.get_or_none(guild_id=ctx.guild.id, user_id=ctx.author.id)
                    if getbank is None:
                        for money in Money.select().where(Money.user_id == ctx.author.id,
                                                          Money.guild_id == ctx.guild.id):
                            delete = Money.get(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id)
                            delete.delete_instance()
                            account = Money.create(user_id=ctx.author.id, amount=money.amount - amount,
                                                   guild_id=ctx.guild.id)
                            newbank = Bank.create(user_id=ctx.author.id, amount=amount, guild_id=ctx.guild.id)
                    else:
                        for money in Money.select().where(Money.user_id == ctx.author.id,
                                                          Money.guild_id == ctx.guild.id):
                            delete = Money.get(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id)
                            delete.delete_instance()
                            account = Money.create(user_id=ctx.author.id, amount=money.amount - amount,
                                                   guild_id=ctx.guild.id)
                        for bank in Bank.select().where(Bank.user_id == ctx.author.id, Bank.guild_id == ctx.guild.id):
                            delete = Bank.get(Bank.user_id == ctx.author.id, Bank.guild_id == ctx.guild.id)
                            delete.delete_instance()
                            newbank = Bank.create(user_id=ctx.author.id, amount=bank.amount + amount,
                                                  guild_id=ctx.guild.id)
                    getlang = Language.get_or_none(guild_id=ctx.guild.id)
                    if getlang is not None:
                        for language in Language.select().where(Language.guild_id == ctx.guild.id):
                            if language.lang == "ru":
                                money_emb = discord.Embed(
                                    title=f"Вы успешно зачислили {amount} 💷 на ваш банковский счет",
                                    color=0x39d0d6)
                                await ctx.respond(embed=money_emb)
                            else:
                                money_emb = discord.Embed(
                                    title=f"You have successfully deposit {amount} 💷 to your bank account",
                                    color=0x39d0d6)
                                await ctx.respond(embed=money_emb)
                    else:
                        money_emb = discord.Embed(
                            title=f"You have successfully deposit {amount} 💷 to your bank account",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)

    @commands.slash_command(name="deduct", description="Deduct some money from your bank account")
    async def deduct(self, ctx, *, amount: int):
        if amount < 0:
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        money_emb = discord.Embed(
                            title="⚠Вы можете указывать только положительные суммы!⚠",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
                    else:
                        money_emb = discord.Embed(
                            title="⚠You can only specify positive amounts!⚠",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
            else:
                money_emb = discord.Embed(
                    title="⚠You can only specify positive amounts!⚠",
                    color=0x39d0d6)
                await ctx.respond(embed=money_emb)
        else:
            getbank = Bank.get_or_none(guild_id=ctx.guild.id, user_id=ctx.author.id)
            if getbank is None:
                newbank = Bank.create(user_id=ctx.author.id, amount='0', guild_id=ctx.guild.id)
                getlang = Language.get_or_none(guild_id=ctx.guild.id)
                if getlang is not None:
                    for language in Language.select().where(Language.guild_id == ctx.guild.id):
                        if language.lang == "ru":
                            money_emb = discord.Embed(
                                title="⚠У вас нету 💷 на вашем счету⚠",
                                color=0x39d0d6)
                            await ctx.respond(embed=money_emb)
                        else:
                            money_emb = discord.Embed(
                                title="⚠You dont have any 💷 in your bank⚠",
                                color=0x39d0d6)
                            await ctx.respond(embed=money_emb)
                else:
                    money_emb = discord.Embed(
                        title="⚠You dont have any 💷 in your bank⚠",
                        color=0x39d0d6)
                    await ctx.respond(embed=money_emb)
            else:
                for bank in Bank.select().where(Bank.user_id == ctx.author.id, Bank.guild_id == ctx.guild.id):
                    if bank.amount < amount:
                        getlang = Language.get_or_none(guild_id=ctx.guild.id)
                        if getlang is not None:
                            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                                if language.lang == "ru":
                                    money_emb = discord.Embed(
                                        title="⚠У вас недостаточно 💷 на вашем счету⚠",
                                        color=0x39d0d6)
                                    await ctx.respond(embed=money_emb)
                                else:
                                    money_emb = discord.Embed(
                                        title="⚠You dont have enough 💷 in your bank⚠",
                                        color=0x39d0d6)
                                    await ctx.respond(embed=money_emb)
                        else:
                            money_emb = discord.Embed(
                                title="⚠You dont have enough 💷 in your bank⚠",
                                color=0x39d0d6)
                            await ctx.respond(embed=money_emb)
                    else:
                        for money in Money.select().where(Money.user_id == ctx.author.id,
                                                          Money.guild_id == ctx.guild.id):
                            delete = Money.get(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id)
                            delete.delete_instance()
                            account = Money.create(user_id=ctx.author.id, amount=money.amount + amount,
                                                   guild_id=ctx.guild.id)
                        for bank in Bank.select().where(Bank.user_id == ctx.author.id, Bank.guild_id == ctx.guild.id):
                            delete = Bank.get(Bank.user_id == ctx.author.id, Bank.guild_id == ctx.guild.id)
                            delete.delete_instance()
                            newbank = Bank.create(user_id=ctx.author.id, amount=bank.amount - amount,
                                                  guild_id=ctx.guild.id)
                        getlang = Language.get_or_none(guild_id=ctx.guild.id)
                        if getlang is not None:
                            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                                if language.lang == "ru":
                                    money_emb = discord.Embed(
                                        title=f"Вы успешно сняли {amount} 💷 с вашего банковского счета",
                                        color=0x39d0d6)
                                    await ctx.respond(embed=money_emb)
                                else:
                                    money_emb = discord.Embed(
                                        title=f"You have successfully deducted {amount} 💷 from your bank account",
                                        color=0x39d0d6)
                                    await ctx.respond(embed=money_emb)
                        else:
                            money_emb = discord.Embed(
                                title=f"You have successfully deducted {amount} 💷 from your bank account",
                                color=0x39d0d6)
                            await ctx.respond(embed=money_emb)

    @commands.slash_command(name="buy", description="buy some items")
    async def buy(self, ctx, *, name: str):
        getshop = Shop.get_or_none(guild_id=ctx.guild.id, item=name)
        if getshop is None:
            await ctx.respond("No such item found!")
        else:
            for shop in Shop.select().where(Shop.guild_id == ctx.guild.id, Shop.item == name):
                for money in Money.select().where(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id):
                    if money.amount < shop.cost:
                        getlang = Language.get_or_none(guild_id=ctx.guild.id)
                        if getlang is not None:
                            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                                if language.lang == "ru":
                                    money_emb = discord.Embed(
                                        title="⚠У вас недостаточно 💷!⚠",
                                        color=0x39d0d6)
                                    await ctx.respond(embed=money_emb)
                                else:
                                    money_emb = discord.Embed(
                                        title="⚠You dont have enough 💷!⚠",
                                        color=0x39d0d6)
                                    await ctx.respond(embed=money_emb)
                        else:
                            money_emb = discord.Embed(
                                title="⚠You dont have enough 💷!⚠",
                                color=0x39d0d6)
                            await ctx.respond(embed=money_emb)
                    else:
                        for money in Money.select().where(Money.user_id == ctx.author.id,
                                                          Money.guild_id == ctx.guild.id):
                            delete = Money.get(Money.user_id == ctx.author.id, Money.guild_id == ctx.guild.id)
                            delete.delete_instance()
                            account = Money.create(user_id=ctx.author.id, amount=money.amount - shop.cost,
                                                   guild_id=ctx.guild.id)
                            await ctx.author.add_roles(ctx.guild.get_role(shop.extra_roles))
                        getlang = Language.get_or_none(guild_id=ctx.guild.id)
                        if getlang is not None:
                            for language in Language.select().where(Language.guild_id == ctx.guild.id):
                                if language.lang == "ru":
                                    money_emb = discord.Embed(
                                        title=f"Вы купили {name}, за {shop.cost} 💷",
                                        color=0x39d0d6)
                                    await ctx.respond(embed=money_emb)
                                else:
                                    money_emb = discord.Embed(
                                        title=f"You have bought {name}, for {shop.cost} 💷",
                                        color=0x39d0d6)
                                    await ctx.respond(embed=money_emb)
                        else:
                            money_emb = discord.Embed(
                                title=f"You have bought {name}, for {shop.cost} 💷",
                                color=0x39d0d6)
                            await ctx.respond(embed=money_emb)

    @commands.slash_command(name="shop", description="list of all items available for this server")
    async def shop(self, ctx):
        getshop = Shop.get_or_none(guild_id=ctx.guild.id)
        if getshop is None:
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        shop_emb = discord.Embed(title='Магазин', colour=0x39d0d6)
                        shop_emb.add_field(name="[-]", value=f'Магазин пуст!',
                                           inline=False)
                        shop_emb.add_field(name="Всего: ", value=f'0 предметов', inline=False)
                        await ctx.respond(embed=shop_emb)
                    else:
                        shop_emb = discord.Embed(title='Shop', colour=0x39d0d6)
                        shop_emb.add_field(name="[-]", value=f'The shop is empty!',
                                           inline=False)
                        shop_emb.add_field(name="Total number: ", value=f'0 items', inline=False)
                        await ctx.respond(embed=shop_emb)
            else:
                shop_emb = discord.Embed(title='Shop', colour=0x39d0d6)
                shop_emb.add_field(name="[-]", value=f'The shop is empty!',
                                   inline=False)
                shop_emb.add_field(name="Total number: ", value=f'0 items', inline=False)
                await ctx.respond(embed=shop_emb)
        else:
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        shop_emb = discord.Embed(title='Магазин', colour=0x39d0d6)
                        for shop in Shop.select().where(Shop.guild_id == ctx.guild.id):
                            shop_emb.add_field(name=shop.item,
                                               value=f'стоимость: {shop.cost}, доп. роли: {ctx.guild.get_role(shop.extra_roles)}',
                                               inline=False)
                        shop_emb.add_field(name="Всего: ",
                                           value=f'{Shop.select().where(Shop.guild_id == ctx.guild.id).count()} предметов',
                                           inline=False)
                        await ctx.respond(embed=shop_emb)
                    else:
                        shop_emb = discord.Embed(title='Shop', colour=0x39d0d6)
                        for shop in Shop.select().where(Shop.guild_id == ctx.guild.id):
                            shop_emb.add_field(name=shop.item,
                                               value=f'cost: {shop.cost}, extra roles: {ctx.guild.get_role(shop.extra_roles)}',
                                               inline=False)
                        shop_emb.add_field(name="Total number: ",
                                           value=f'{Shop.select().where(Shop.guild_id == ctx.guild.id).count()} items',
                                           inline=False)
                        await ctx.respond(embed=shop_emb)
            else:
                shop_emb = discord.Embed(title='Shop', colour=0x39d0d6)
                for shop in Shop.select().where(Shop.guild_id == ctx.guild.id):
                    shop_emb.add_field(name=shop.item,
                                       value=f'cost: {shop.cost}, extra roles: {ctx.guild.get_role(shop.extra_roles)}',
                                       inline=False)
                shop_emb.add_field(name="Total number: ",
                                   value=f'{Shop.select().where(Shop.guild_id == ctx.guild.id).count()} items',
                                   inline=False)
                await ctx.respond(embed=shop_emb)

    @commands.slash_command(name="add_item", description="add new item to the shop")
    @commands.has_permissions(administrator=True)
    async def add_item(self, ctx, *, name: str, cost: int, role: discord.Role = None):
        if cost < 0:
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        money_emb = discord.Embed(
                            title=f"⚠Вы можете указывать только положительные значения!⚠",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
                    else:
                        money_emb = discord.Embed(
                            title=f"⚠You can only specify positive amounts!⚠",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
            else:
                money_emb = discord.Embed(
                    title=f"⚠You can only specify positive amounts!⚠",
                    color=0x39d0d6)
                await ctx.respond(embed=money_emb)
        else:
            newshop = Shop.create(guild_id=ctx.guild.id, item=name, cost=cost, extra_roles=role.id)
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        money_emb = discord.Embed(
                            title=f"Вы добавили новый предмет в магазин",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
                    else:
                        money_emb = discord.Embed(
                            title=f"You have added new item to the shop",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
            else:
                money_emb = discord.Embed(
                    title=f"You have added new item to the shop",
                    color=0x39d0d6)
                await ctx.respond(embed=money_emb)

    @commands.slash_command(name="remove_item", description="remove item from the shop")
    @commands.has_permissions(administrator=True)
    async def remove_item(self, ctx, *, name: str):
        getshop = Shop.get_or_none(guild_id=ctx.guild.id, item=name)
        if getshop is None:
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        money_emb = discord.Embed(
                            title=f"⚠Предмет не был найден!⚠",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
                    else:
                        money_emb = discord.Embed(
                            title=f"⚠No such item found!⚠",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
            else:
                money_emb = discord.Embed(
                    title=f"⚠No such item found!⚠",
                    color=0x39d0d6)
                await ctx.respond(embed=money_emb)
        else:
            delete = Shop.get(Shop.guild_id == ctx.guild.id, Shop.item == name)
            delete.delete_instance()
            getlang = Language.get_or_none(guild_id=ctx.guild.id)
            if getlang is not None:
                for language in Language.select().where(Language.guild_id == ctx.guild.id):
                    if language.lang == "ru":
                        money_emb = discord.Embed(
                            title=f"Предмет/предметы с именем {name} были успешно удалены",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
                    else:
                        money_emb = discord.Embed(
                            title=f"Successfully deleted item/items, named {name}",
                            color=0x39d0d6)
                        await ctx.respond(embed=money_emb)
            else:
                money_emb = discord.Embed(
                    title=f"Successfully deleted item/items, named {name}",
                    color=0x39d0d6)
                await ctx.respond(embed=money_emb)

def setup(bot):
    bot.add_cog(Econ(bot))
