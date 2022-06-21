
import discord
from discord.ext import commands
import os
import asyncio
import random
import time

from discord import channel



client = commands.Bot(command_prefix = '-')

id, money, timed = [], [], []

try:
    f = open('test.txt', 'r')
except:
    f = open('test.txt', 'w')
    f.close()
    f = open('test.txt', 'r')
for line in f.readlines(): 
    data = line.split(",")
    id.append(data[0])
    money.append(int(data[1]))
    timed.append(int(data[2]))
f.close()



@client.event
async def on_ready():
    print("클라이언트에 접속 중입니다....!")


@client.event
async def on_message(message):
    if message.content == ("빙빙베베 온!"):
        helloembed = discord.Embed(title="빙빙베베 켜짐!",
                                     description=" ", 
                                        color=0xFaaaaF)
        await message.channel.send(embed=helloembed)


    if message.content == ("명령어"):
        commands = discord.Embed(title="명령어",
                                     description="명령어를 알려줄게", 
                                        color=0xFaaaaF)
        commands.add_field(name='> 돈 받기', value='돈줘')
        commands.add_field(name='> 통장 확인', value='내돈')
        commands.add_field(name='> 슬롯 게임', value='슬롯 ooo, 슬롯 올인')
        commands.add_field(name='> 컬러 매칭 게임', value='컬러 ooo, 컬러 올인')                    
        await message.channel.send(embed=commands)


    if message.content == ("굴려"):
        dice = random.randint(1,6)
        await message.channel.send("🎲"+str(dice))

    if message.content == ("돈줘"):
        ID = str(message.author.id)
        TIME = int(time.time())
        give = random.randint(1, 100000)*random.randint(1, 100)
        if ID in id:
            if TIME - timed[id.index(ID)] < 10:
                await message.channel.send("좀더 기다려 주세요")
                raise ValueError
            elif TIME - timed[id.index(ID)] >= 10:
                timed[id.index(ID)] = int(time.time())
                money[id.index(ID)] += give
        elif not ID in id:
            id.append(ID)
            money.append(give)
            timed.append(TIME)
        await message.channel.send("💶"+str(give)+"원을 받으셨습니다")
        f = open("test.txt", "w")
        for i in range(0,len(id),1):
            f.write(str(id[i])+","+str(money[i])+","+str(timed[i])+"\n")
        f.close()
        

    if message.content == "내돈":
        ID = str(message.author.id)
        if ID in id:
            await message.channel.send("$ : "+str(money[id.index(ID)])+"원")
        elif not ID in id:
            await message.channel.send("등록 되지 않은 아이디 입니다. '돈줘'를 입력해보세여")
            raise ValueError

    if message.content == ("돈줭"):
        ID = str(message.author.id)
        give = 7777777
        if ID in id:
            money[id.index(ID)] += give
            await message.channel.send("보너스 캐쉬 지급!!⭐️")
        elif not ID in id:
            id.append(ID)
            money.append(give)

    if message.content == ("돈줘!!!"):
        ID = str(message.author.id)
        give = 999999999
        if ID in id:
            money[id.index(ID)] += give
            await message.channel.send("보너스 캐쉬 지급!!⭐️")
        elif not ID in id:
            id.append(ID)
            money.append(give)

    if message.content.startswith("슬롯"):
        ID = str(message.author.id)
        insert = message.content.split()
        if insert[1] == "올인":
            ID = str(message.author.id)
            insert[1] = money[id.index(ID)]  
        elif insert[1].isdecimal() == False:
            await message.channel.send("숫자만 입력해 주세요")
            raise ValueError
        elif not ID in id or money[id.index(ID)] - int(insert[1]) < 0:
            await message.channel.send("오류가 발생했습니다")
            raise ValueError
        money[id.index(ID)] -= int(insert[1])
        


        inslot = []
        icon =['🍋','🍒','🥥','🍑','🍇','💎','⭐️']
        embed=discord.Embed(title='🎰슬롯머신 | 베팅 : 💵'+str(insert[1]), description='', color=0xF5DA81)
        embed.add_field(name='❔  |  ❔  |  ❔', value='결과 : ❔', inline=False)
        slotmachine = await message.channel.send(embed=embed)

        for i in range(3):
            await asyncio.sleep(0.2)
            roll = random.sample(icon, 3)
            slot_embed=discord.Embed(title='🎰슬롯머신 | 베팅 : 💵'+str(insert[1]), description='', color=0xF5DA81)
            slot_embed.add_field(name=str(roll[0])+' | '+str(roll[1])+' | '+str(roll[2]), value='결과 : ❔', inline=False)
            await slotmachine.edit(embed=slot_embed)
            inslot.append(random.choice(icon))

        if inslot.count('<:7seven:919822960569745468>') == 3:
            result = ['JACKPOT! 베팅의 777배를 획득하셨습니다!', 777]
        elif inslot.count('💎') == 3:
            result = ['DIAMOND! 베팅의 100배를 획득하셨습니다!', 100]
        elif inslot.count('🍇') == 3 or inslot.count('🍑') == 3 or inslot.count('🥥') == 3 or inslot.count('🍒') == 3 or inslot.count('🍋') == 3:
            result = ['TRIPLE! 베팅의 10배를 획득하셨습니다!', 10]
        elif inslot.count('<:7seven:919822960569745468>') == 2 or inslot.count('💎') == 2:
            result = ['DOUBLE! 베팅의 22배를 획득하셨습니다!', 22]
        elif inslot.count('🍇') == 2 or inslot.count('🍑') == 2 or inslot.count('🥥') == 2 or inslot.count('🍒') == 2 or inslot.count('🍋') == 2:
            result = ['DOUBLE! 베팅의 4배를 획득하셨습니다!', 4]
        else:
            result = ['돈을 잃었습니다...', 0]

        result_embed=discord.Embed(title='🎰슬롯머신 | 베팅 : 💵'+str(insert[1]), description='', color=0xF5DA81)
        result_embed.add_field(name=str(inslot[0])+' | '+str(inslot[1])+' | '+str(inslot[2]), value='결과 : '+str(result[0]), inline=False)
        await slotmachine.edit(embed=result_embed)
        money[id.index(ID)] += int(result[1])*int(insert[1])

        f = open('test.txt', 'w')
        for i in range(0,len(id),1):
            f.write(str(id[i])+","+str(money[i])+","+str(timed[i])+"\n")
        f.close()
                       

    if message.content.startswith("컬러"):
        ID = str(message.author.id)
        insert = message.content.split()
        if insert[1] == "올인":
            ID = str(message.author.id)
            insert[1] = money[id.index(ID)]  
        elif insert[1].isdecimal() == False:
            await message.channel.send("숫자만 입력해 주세요")
            raise ValueError
        elif not ID in id or money[id.index(ID)] - int(insert[1]) < 0:
            await message.channel.send("보유금액 초과. ")
            raise ValueError
        money[id.index(ID)] -= int(insert[1])


        colorembed = discord.Embed(title='🔖컬러',description='📕 📙 📘 중 선택하세요.', color=0xF6CEEC)
        colorembed.set_footer(text='딜러가 고른 색상을 맞추면 777배 보상을 얻습니다')
        color = await message.channel.send(embed=colorembed)

        color_list = ['📕', '📙', '📘']
        for r in color_list:
            await color.add_reaction(r)
        pick = random.choice(color_list)

        def check(reaction, user):
            return str(reaction) in color_list and user == message.author and reaction.message.id == color.id
        reaction, user = await client.wait_for("reaction_add", check=check)

        if pick == str(reaction):
            await color.edit(embed=discord.Embed(title="🔖컬러", description=str(reaction)+"딜러가 고른 걸 맞췄습니다 💵"+str(3*int(insert[1]))+"획득하였습니다", color=0xF6CEEC))
            money[id.index(ID)] += 777*int(insert[1])
        else:
            await color.edit(embed=discord.Embed(title="🔖컬러", description=str(pick)+"딜러가 고른 걸 맞추지 못 했습니다", color=0xF6CEEC))
            money[id.index(ID)] += 0*int(insert[1])


        f = open("test.txt", "w")
        for i in range(0, len(id), 1):
            f.write(str(id[i]) + ","+str(money[i])+str(timed[i])+"\n")
        f.close()
    
   
    

client.run(os.environ['token'])
