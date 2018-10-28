import discord
import datetime
import random
import asyncio
import requests
import time
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps
from discord import opus

OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll',
             'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

opts = {
            'default_search': 'auto',
            'quiet': True,
        }
def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
            try:
                opus.load_opus(opus_lib)
                return
            except OSError:
                pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %
                       (', '.join(opus_libs)))
load_opus_lib()



client = discord.Client()
players = {}
COR = 0xF7FE2E
msg_id = None
msg_user = None
tempo = []

dcs = ["discord.gg/", "discord.gg//", "https://discord.gg/"]


@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name="Use o n!happy"))
    print('Estou ligado')
    print(client.user.name)
    print(client.user.id)
    print('-----Natsu-----')


@client.event
async def on_message(message):
    if message.content.startswith("n!daily"):
        x = message.author
        if not x in tempo:
            if os.path.isfile('users/' + str(message.author) + '.txt') == False:
                with open('users/' + str(message.author) + '.txt', 'w') as file:
                    file.write('0')
            money = open('users/' + str(message.author) + '.txt', 'r')
            money1 = int(money.read())
            money.close()
            moneysoma = random.randint(10, 50)
            moneyf = money1 + moneysoma

            open('users/' + str(message.author) + '.txt', 'w').close()

            with open('users/' + str(message.author) + '.txt', 'w') as file:
                file.write(str(moneyf))
            e = discord.Embed(title='💸 {}, você acabou de fazer sua coleta diaria de {} money, agora só amanha para recoletar.'.format(format(message.author.name), moneysoma ), color=COR)
            await client.send_message(message.channel, embed=e)
            tempo.append(x)
            await asyncio.sleep(86400)
            tempo.remove(x)
        else:
            await client.send_message(message.channel, "Você precisa esperar 24 horas para reutilizar o Daily")


    if message.content.startswith('n!saldo'):
        if os.path.isfile('users/' + str(message.author) + '.txt') == False:
            with open('users/' + str(message.author) + '.txt', 'w') as file:
                file.write('0')
        saldo = open('users/' + str(message.author) + '.txt', 'r')
        money1 = str(saldo.read())
        saldo2 = money1

        open('users/' + str(message.author) + '.txt', 'w').close()

        with open('users/' + str(message.author) + '.txt', 'w') as file:
            file.write(str(saldo2))
            e2 = discord.Embed(title='💰 {}, você possui {} moedas diárias.'.format(message.author.name, saldo2), color=COR)
            await client.send_message(message.channel, embed=e2)


    if message.content.startswith('n!entrar'):
        try:
            channel = message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except discord.errors.InvalidArgument:
            await client.send_message(message.channel, "O bot ja esta em um canal de voz")
        except Exception as error:
            await client.send_message(message.channel, "Ein Error: ```{error}```".format(error=error))

    if message.content.startswith('n!sair'):
        try:
            mscleave = discord.Embed(
                title="\n",
                color=COR,
                description="Sai do canal de voz e a musica parou!"
            )
            voice_client = client.voice_client_in(message.server)
            await client.send_message(message.channel, embed=mscleave)
            await voice_client.disconnect()
        except AttributeError:
            await client.send_message(message.channel, "O bot não esta em nenhum canal de voz.")
        except Exception as Hugo:
            await client.send_message(message.channel, "Ein Error: ```{haus}```".format(haus=Hugo))

    if message.content.startswith('n!play'):
        try:
            yt_url = message.content[6:]
            if client.is_voice_connected(message.server):
                try:
                    voice = client.voice_client_in(message.server)
                    players[message.server.id].stop()
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[message.server.id] = player
                    player.start()
                    mscemb = discord.Embed(
                        title="Música para tocar:",
                        color=COR
                    )
                    mscemb.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb.add_field(name="Enviado em:", value="`{}`".format(player.uploaded_date))
                    mscemb.add_field(name="Enviado por:", value="`{}`".format(player.uploadeder))
                    mscemb.add_field(name="Duraçao:", value="`{}`".format(player.uploadeder))
                    mscemb.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb.add_field(name="Deslikes:", value="`{}`".format(player.dislikes))
                    await client.send_message(message.channel, embed=mscemb)
                except Exception as e:
                    await client.send_message(message.server, "Error: [{error}]".format(error=e))

            if not client.is_voice_connected(message.server):
                try:
                    channel = message.author.voice.voice_channel
                    voice = await client.join_voice_channel(channel)
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[message.server.id] = player
                    player.start()
                    mscemb2 = discord.Embed(
                        title="Música para tocar:",
                        color=COR
                    )
                    mscemb2.add_field(name="Nome:", value="`{}`".format(player.title))
                    mscemb2.add_field(name="Visualizações:", value="`{}`".format(player.views))
                    mscemb2.add_field(name="Enviado em:", value="`{}`".format(player.upload_date))
                    mscemb2.add_field(name="Enviado por:", value="`{}`".format(player.uploader))
                    mscemb2.add_field(name="Duraçao:", value="`{}`".format(player.duration))
                    mscemb2.add_field(name="Likes:", value="`{}`".format(player.likes))
                    mscemb2.add_field(name="Deslikes:", value="`{}`".format(player.dislikes))
                    await client.send_message(message.channel, embed=mscemb2)
                except Exception as error:
                    await client.send_message(message.channel, "Error: [{error}]".format(error=error))
        except Exception as e:
            await client.send_message(message.channel, "Error: [{error}]".format(error=e))



    if message.content.startswith('n!pause'):
        try:
            mscpause = discord.Embed(
                title="\n",
                color=COR,
                description="Musica pausada com sucesso!"
            )
            await client.send_message(message.channel, embed=mscpause)
            players[message.server.id].pause()
        except Exception as error:
            await client.send_message(message.channel, "Error: [{error}]".format(error=error))
    if message.content.startswith('n!resume'):
        try:
            mscresume = discord.Embed(
                title="\n",
                color=COR,
                description="Musica pausada com sucesso!"
            )
            await client.send_message(message.channel, embed=mscresume)
            players[message.server.id].resume()
        except Exception as error:
            await client.send_message(message.channel, "Error: [{error}]".format(error=error))

    for listadc in dcs:
        if listadc in message.content.lower():
            if not message.author.server_permissions.administrator:
                return await client.delete_message(message)
                await client.send_message(message.channel, message.author.mention + " ❌ Você precisa da permissao de admin para divulgar!**")

    if message.content.startswith('n!falar'):
        def check(msg):
            return msg.content.startswith('n!falar')
        message = await client.wait_for_message(author=message.author, check=check)
        falar = message.content[len('n!falar'):].strip()
        await client.send_message(message.channel, falar)

    if message.content.lower().startswith('n!apagar'):
        if not message.author.server_permissions.manage_messages:
            return await client.send_message(message.channel, "**Você não tem permissão para executar esse comando SATANÁS!!! !**")
        try:
            limite = int(message.content[8:]) + 1
            await client.purge_from(message.channel, limit=limite)
            await client.send_message(message.channel, '{} mensagens foram deletadas por {}'.format(limite - 1,message.author.mention))
        except:
            await client.send_message(message.channel, 'Eu não tenho permissão para apagar mensagens nesse servidor.')

    if message.content.lower().startswith('n!kick'):
        if not message.author.server_permissions.kick_members:
            return await client.send_message(message.channel, "**Você não tem permissão para executar esse comando bobinho(a)!**")
        try:
            user = message.mentions[0]
            embed = discord.Embed(title="CHUTÃO", colour=discord.Colour(0x191f30),description="Um úsuario não teve sorte, e infelizmente foi kickado de nosso servidor! Pelo menos não foi um ban certo?")
            embed.set_thumbnail(url="https://pictogram-free.com/material/353-pictogram-free.jpg")
            embed.set_footer()
            embed.add_field(name="Informações", value="**O usuario(a) <@{}> foi kickado com sucesso do servidor.**".format(user.id))
            await client.send_message(message.channel, embed=embed)
            await client.kick(user)
        except:
            await client.send_message(message.channel, "**Você deve especificar um usuario para kickar!**")

    if message.content.lower().startswith('n!ban'):
        if not message.author.server_permissions.ban_members:
            return await client.send_message(message.channel, "**Você não tem permissão para executar essa merda!**")
        try:
            user = message.mentions[0]
            embed = discord.Embed(title="BANIDO", colour=discord.Colour(0x191f30),description="O Shinobi pertubou tanto o ADM, que foi banido!")
            embed.set_thumbnail(url="https://pictogram-free.com/highresolution/307-free-pictogram.png")
            embed.set_footer()
            embed.add_field(name="Informações", value="**O <@{}> foi banido com sucesso do servidor.**".format(user.id))
            await client.send_message(message.channel, embed=embed)
            await client.ban(user)
        except:
            await client.send_message(message.channel, "**Você deve especificar um usuario para banir!**")

    if message.content.lower().startswith('n!botinfo'):
        horario = datetime.datetime.now().strftime("%H:%M:%S")
        await client.delete_message(message)
        embedbot = discord.Embed(
            title='**🤖 Informações do Bot**',
            color=0x00a3cc,
            description='\n'
        )
        embedbot.set_thumbnail(url="https://cdn.discordapp.com/attachments/476866172684337152/497246773182464001/screenNaruto_Hero_Online167.jpg")  # Aqui você coloca a url da foto do seu bot!
        embedbot.add_field(name='`💮 | Nome`', value=client.user.name, inline=True)
        embedbot.add_field(name='`◼ | ID`', value=client.user.id, inline=True)
        embedbot.add_field(name='💠 | Criado em', value=client.user.created_at.strftime("%d %b %Y %H:%M"))
        embedbot.add_field(name='📛 | Tag', value=client.user)
        embedbot.add_field(name='💻 | Servidores', value=len(client.servers))
        embedbot.add_field(name='👥 | Usuarios', value=len(list(client.get_all_members())))
        embedbot.add_field(name='⚙ | Programador', value="`Saga`")  # Aqui você coloca seu nome/discord
        embedbot.add_field(name='🐍 Python  | Version',
                           value="`3.6.6`")  # Aqui você coloca a versão do python que você está utilizando!
        embedbot.set_footer(
            text="Comando usado por {} as {} Hrs".format(message.author, horario),
            icon_url=message.author.avatar_url)

        await client.send_message(message.channel, embed=embedbot)

    if message.content.lower().startswith("n!sorteio"):  # esse comandos sorteia um memebro
        if message.author.server_permissions.administrator:
            n = random.choice(list(message.server.members))
            n1 = '{}'.format(n.name)
            m1 = discord.utils.get(message.server.members, name="{}".format(n1))
            embed = discord.Embed(
                title="Sorteiar membro",
                colour=0xab00fd,
                description="Membro sorteado foi {}!".format(m1.mention)
                )
            hh = await client.send_message(message.channel, "{}".format(m1.mention))
            await client.delete_message(hh)
            await client.send_message(message.channel, embed=embed)
        else:
            await client.send_message("{} você não tem permissão de executar esse comando!".format(message.author.mention))

    if message.content.lower().startswith('n!natsu'):
        try:
            respostas = ['Sim', 'Não', 'Talvez', 'Nunca', 'Claro', 'Sei de Nada', 'BOT morreu não pôde responder', 'Pergunte no posto ipiranga']
            resposta = random.choice(respostas)
            mensagem = message.content[6:]
            embed = discord.Embed(color=0xFF0000)
            embed.add_field(name="Pergunta:", value='{}'.format(mensagem), inline=False)
            embed.add_field(name="Resposta:", value=resposta, inline=False)
            await client.send_message(message.channel, embed=embed)
            await client.delete_message(message)
        except:
            await client.send_message(message.channel, 'Você precisa perguntar alguma coisa!')

    if message.content.lower().startswith('n!ping'):
        horario = datetime.datetime.now().strftime("%H:%M:%S")
        channel = message.channel
        t1 = time.perf_counter()
        await client.send_typing(channel)
        t2 = time.perf_counter()
        ping_embed = discord.Embed(title="🏓 Pong!", color=0xFF0000, description='Meu tempo de resposta é `{}ms`!'.format(round((t2 - t1) * 1000)))
        ping_embed.set_footer(
            text="Comando usado por {} as {} Hrs".format(message.author, horario))
        await client.send_message(message.channel, embed=ping_embed)

    if message.content.lower().startswith("n!serverinfo"):
        horario = datetime.datetime.now().strftime("%H:%M:%S")
        embed = discord.Embed(title="\n", description="Abaixo está as informaçoes principais do servidor!")
        embed.set_thumbnail(url=message.server.icon_url)
        embed.set_footer(text="{} • {}".format(message.author, horario))
        embed.add_field(name="Nome:", value=message.server.name, inline=True)
        embed.add_field(name="Dono:", value=message.server.owner.mention)
        embed.add_field(name="ID:", value=message.server.id, inline=True)
        embed.add_field(name="Cargos:", value=str(len(message.server.roles)), inline=True)
        embed.add_field(name="Canais de texto:", value=str(len([c.mention for c in message.server.channels if c.type == discord.ChannelType.text])),
                                   inline=True)
        embed.add_field(name="Canais de voz:", value=str(len([c.mention for c in message.server.channels if c.type == discord.ChannelType.voice])),
                                   inline=True)
        embed.add_field(name="Membros:", value=str(len(message.server.members)), inline=True)
        embed.add_field(name="Bots:",
                                   value=str(len([a for a in message.server.members if a.bot])),
                                   inline=True)
        embed.add_field(name="Criado em:", value=message.server.created_at.strftime("%d %b %Y %H:%M"),
                                   inline=True)
        embed.add_field(name="Região:", value=str(message.server.region).title(), inline=True)
        await client.send_message(message.channel, embed=embed)

    if message.content.lower().startswith('n!userinfo'):
        try:
            user = message.mentions[0]
            server = message.server
            embedinfo = discord.Embed(title='Informações do usuário', color=0x03c3f5, )
            embedinfo.set_thumbnail(url=user.avatar_url)
            embedinfo.add_field(name='Usuário:', value=user.name)
            embedinfo.add_field(name='Apelido', value=user.nick)
            embedinfo.add_field(name='🆔 ID:', value=user.id)
            embedinfo.add_field(name='📅 Entrou em:', value=user.joined_at.strftime("%d %b %Y às %H:%M"))
            embedinfo.add_field(name='📅 Server criado em:', value=server.created_at.strftime("%d %b %Y %H:%M"))
            embedinfo.add_field(name='Jogando:', value=user.game)
            embedinfo.add_field(name="Status:", value=user.status)
            embedinfo.add_field(name='Cargos:', value=([role.name for role in user.roles if role.name != "@everyone"]))
            await client.send_message(message.channel, embed=embedinfo)
        except ImportError:
            await client.send_message(message.channel, 'Buguei!')
        except:
            await client.send_message(message.channel, '? | Mencione um usuário válido!')
        finally:
            pass

    if message.content.lower().startswith('n!vote'):
        vote = message.content[5:].strip()
        votee = await client.send_message(message.channel,
                                          message.author.mention + " **Iniciou uma votação?**\n\n``" + vote + "``")
        await client.delete_message(message)
        await client.add_reaction(votee, '👍')
        await client.add_reaction(votee, '👎')
        await client.add_reaction(votee, '👏')

    if message.content.lower().startswith('n!corrida'):
        await client.send_message(message.channel, "Mencione o player que deseja desafiar.")
        msg = await client.wait_for_message(author=message.author)
        user = msg.mentions[0]
        await client.send_message(message.channel, "🏎️ = {} ".format(message.author.name))
        await client.send_message(message.channel, "🚗 = {}".format(user.name))
        await asyncio.sleep(2)
        contagem = 3
        while contagem > 0:
            await client.send_message(message.channel, "***" + str(contagem) + "***")
            await asyncio.sleep(1)
            contagem = contagem - 1
        velocidade1 = random.randint(10, 15)
        velocidade2 = random.randint(10, 15)
        vm1 = velocidade1 / 1
        vm2 = velocidade2 / 1
        metros1 = 0
        metros2 = 0
        while metros1 < 100 and metros2 < 100:
            v1 = random.randint(10, 15)
            v2 = random.randint(10, 15)
            metros1 = metros1 + v1
            metros2 = metros2 + v2
            ms1 = await client.send_message(message.channel, "🏎️ = {} ".format(message.author.mention))
            ms2 = await client.send_message(message.channel, "🚗  = {}".format(user.name))
            m1 = await client.edit_message(ms1, "🏎️ = {} ".format(str(metros1)))
            m2 = await client.edit_message(ms2, "🚗  = {}".format(str(metros2)))
            await asyncio.sleep(2)
            await client.delete_message(m1)
            await client.delete_message(m2)
            if metros1 > 100:
                if metros1 > metros2:
                    await client.send_message(message.channel,
                                              "O Vencedor foi {} obtendo uma velocidade de {} m/s".format(
                                                  message.author.name, str(vm1)))
                    fim = 0
                    return fim
                if metros2 > metros1:
                    await client.send_message(message.channel,
                                              "O Vencedor foi {} obtendo uma velocidade de {} m/s".format(user.name,
                                                                                                          str(vm2)))
                    fim = 0
                    return fim
            if metros2 > 100:
                if metros1 > metros2:
                    await client.send_message(message.channel,
                                              "O Vencedor foi {} obtendo uma velocidade de {} m/s".format(
                                                  message.author.name, str(vm1)))
                    fim = 0
                    return fim
                if metros2 > metros1:
                    await client.send_message(message.channel,
                                              "O Vencedor foi {} obtendo uma velocidade de {} m/s".format(user.name,
                                                                                                          str(vm2)))
                    fim = 0
                    return fim

    if message.content.startswith("n!servidores"):
            servidores = '\n'.join([s.name for s in client.servers])
            embe = discord.Embed(title="Olá, sou o Saga, atualmente estou online em " + str(len(client.servers)) + " servidores com " + str(
                len(set(client.get_all_members()))) + " membros!",
                                color=0xFF0000,
                                description=servidores)
            await client.send_message(message.channel, embed=embe)


    if message.content.startswith("n!avatar"):
        xtx = message.content.split(' ')
        if len(xtx) == 1:
            useravatar = message.author
            avatar = discord.Embed(
                title="Avatar de: {}".format(useravatar.name),
                color=0x00FF00,
                description="[Clique aqui](" + useravatar.avatar_url + ") para baixar a imagem"
            )

            avatar.set_image(url=useravatar.avatar_url)
            avatar.set_footer(text="Pedido por {}#{}".format(useravatar.name, useravatar.discriminator))
            await client.send_message(message.channel, embed=avatar)
        else:
            try:
                useravatar = message.mentions[0]
                avatar = discord.Embed(
                      title="Avatar de: {}".format(useravatar.name),
                      color=0x00FF00,
                      description="[Clique aqui]("+useravatar.avatar_url+") para baixar a imagem"
                )

                avatar.set_image(url=useravatar.avatar_url)
                avatar.set_footer(text="Pedido por {}".format(message.author))
                await client.send_message(message.channel, embed=avatar)

            except IndexError:
                a = len() + 7
                uid = message.content[a:]
                useravatar = message.server.get_member(uid)
                avatar = discord.Embed(
                    title="Avatar de: {}".format(useravatar.name),
                    color=0x00FF00,
                    description="[Clique aqui](" + useravatar.avatar_url + ") para baixar a imagem"
                )

                avatar.set_image(url=useravatar.avatar_url)
                avatar.set_footer(text="Pedido por {}".format(message.author))
                await client.send_message(message.channel, embed=avatar)

    if message.content.lower().startswith('n!fechar'):
        membro = discord.utils.find(lambda r: r.name == "@everyone", message.server.roles)
        fechado = discord.PermissionOverwrite()
        fechado.read_messages = False
        fechado.send_messages = False
        await client.edit_channel_permissions(message.channel, membro, fechado)
        await client.send_message(message.channel, "Canal fechado para membros!")

    if message.content.lower().startswith('n!liberar'):
        membro = discord.utils.find(lambda r: r.name == "@everyone", message.server.roles)
        aberto = discord.PermissionOverwrite()
        aberto.read_messages = True
        aberto.send_messages = True
        await client.edit_channel_permissions(message.channel, membro, aberto)
        await client.send_message(message.channel, "Canal Aberto novamente")

    if message.content.lower().startswith('n!lock'):
        if not message.author.server_permissions.administrator:
            membro = discord.utils.find(lambda r: r.name == "@everyone", message.server.roles)
            lock = discord.PermissionOverwrite()
            lock.send_messages = False
            await client.edit_channel_permissions(message.channel, membro, lock)
            await client.send_message(message.channel, "Não se pode mandar mensagem nesse canal ate segunda ordem!")

    if message.content.lower().startswith('n!unlock'):
        if not message.author.server_permissions.administrator:
            membro = discord.utils.find(lambda r: r.name == "@everyone", message.server.roles)
            unlock = discord.PermissionOverwrite()
            unlock.send_messages = True
            await client.edit_channel_permissions(message.channel, membro, unlock)
            await client.send_message(message.channel, "Já pode mandar mensagem novamente !")

    if message.content.lower().startswith('n!abraçar'):
        try:
            user = message.mentions[0]
            embed = discord.Embed(title='{} deu um forte abraço em {}'.format(message.author.name, user.name), colour=discord.Colour(0x0f0f0f), description='\n')
            embed.set_image(url='https://66.media.tumblr.com/36a8846fadf080496c4ff8000f7126aa/tumblr_o4gzpr5Da11vnh6hco1_500.gif')
            await client.send_message(message.channel, embed=embed)
        except:
            await client.send_message(message.channel, "Você precisa marcar alguém!")

    if message.content.startswith('n!ship'):
        try:
            ship = random.randint(0, 100)
            user = message.mentions[0]
            user1 = message.mentions[1]
            em1 = discord.Embed(title='{} e {} Tem {}% de ficarem juntos! '.format(user1.name, user.name, ship), colour=discord.Colour(0x0ff00))
            await client.send_message(message.channel, embed=em1)
            url = requests.get(user1.avatar_url)
            avatar = Image.open(BytesIO(url.content))
            avatar = avatar.resize((80, 80))
            bigavatar = (avatar.size[0] * 3, avatar.size[1] * 3)
            mascara = Image.new('L', bigavatar, 0)
            recortar = ImageDraw.Draw(mascara)
            recortar.ellipse((0, 0) + bigavatar, fill=255)
            mascara = mascara.resize(avatar.size, Image.ANTIALIAS)
            avatar.putalpha(mascara)

            url1 = requests.get(user.avatar_url)
            avatar1 = Image.open(BytesIO(url1.content))
            avatar1 = avatar1.resize((80, 80))
            bigavatar1 = (avatar1.size[0] * 3, avatar1.size[1] * 3)
            mascara1 = Image.new('L', bigavatar1, 0)
            recortar1 = ImageDraw.Draw(mascara1)
            recortar1.ellipse((0, 0) + bigavatar, fill=255)
            mascara1 = mascara1.resize(avatar1.size, Image.ANTIALIAS)
            avatar1.putalpha(mascara1)
            saida1 = ImageOps.fit(avatar1, mascara1.size, centering=(0.5, 0.5))
            saida1.putalpha(mascara1)
            saida1.save('avatar1.png')

            saida = ImageOps.fit(avatar, mascara.size, centering=(0.5, 0.5))
            saida.putalpha(mascara)
            saida.save('avatar.png')
            img = Image.open("img.png")
            fonte = ImageFont.truetype('font.ttf', 35)
            gg = str(ship)+"%"
            texto = ImageDraw.Draw(img)
            texto.text(xy=(117, 60), text=gg, fill=(255, 255, 255), font=fonte)
            img.paste(avatar, (10, 40), avatar)
            img.paste(avatar1, (190, 40), avatar1)
            img.save('nova.png')
            await client.send_file(message.channel, 'nova.png')
        except:
            await client.send_message(message.channel, '? | Mencione dois usuários válido!')

    if message.content.startswith('n!beijar'):
        try:
            user = message.mentions[0]
            emb = discord.Embed(title='O {} deseja beijar o usuário {}, aceita ?'.format(message.author.name, user.name), color=discord.Colour(0xfb0e0))
            emb.add_field(name='-', value="{}, digite aceitar, para aceitar a proposta de beijo!".format(user.name))
            await client.send_message(message.channel, embed=emb)
            await client.wait_for_message(author=user)
            emb2 = discord.Embed(title='O {} aceitou o beijo do {}!'.format(user.name, message.author.name), color=discord.Colour(0xfb0e0))
            emb2.set_image(url='https://data.whicdn.com/images/166662929/original.gif')
            await client.send_message(message.channel, embed=emb2)
        except:
            await client.send_message(message.channel, '? | Mencione um usuário válido!')

    if message.content.startswith('n!adver'):
        if not message.author.server_permissions.kick_members:
            return await client.send_message(message.channel, "**Você não tem permissão para executar esse comando bobinho(a)!**")
        await client.send_message(message.channel, "**User ?**")
        user = await client.wait_for_message(author=message.author)
        for member in user.mentions:
            await client.send_message(message.channel, "**Motivo ?**")
            motivo = await client.wait_for_message(author=message.author)
            embed1 = discord.Embed(
                title='**Advertencia**',
                color=0x00a3cc,
                description='\n'
            )
            embed1.add_field(name=':warning: Você foi advertido por {}'.format(str(message.author.name)),
                             value='Motivo : {}'.format(motivo.content), inline=False)
            await client.send_message(member, embed=embed1)

    if message.content.startswith('n!roleta'):
        choice = random.randint(1, 2)
        if choice == 1:
            msg = await client.send_message(message.channel, "{}, você deu azar, arma disparou. ".format(message.author.name))
            await client.add_reaction(msg, "💀")
        if choice == 2:
            msg1 = await client.send_message(message.channel, "{}, você deu sorte, a arma não disparou, pronto para outra tentativa?".format(message.author.name))
            await client.add_reaction(msg1, "😰")

    if message.content.startswith('n!batalhar'):
        await client.send_message(message.channel, "Mencione alguém que deseja desafiar!")
        msg = await client.wait_for_message(author=message.author)
        user = msg.mentions[0]
        hp1 = 250
        hp2 = 250
        msg1 = await client.send_message(message.channel, "{} = {} ❤".format(message.author.name, str(hp1)))
        msg2 = await client.send_message(message.channel, "{} = {} ❤".format(user.name, str(hp2)))
        atq1 = 0
        atq2 = 0
        while hp1 > 0 and hp2 > 0:

            msg3 = await client.send_message(message.channel,
                                      "É a vez de {} atacar, digite atacar ou Rugido!".format(message.author.name))
            ação1 = await client.wait_for_message(author=message.author)

            if  ação1.content == "Rugido":
                atq1 = random.randint(60,80)
                embed = discord.Embed(title='{}, utilizou o Rugido do Dragão Fogo e Raio tirando {}, do {}'.format(message.author.name, atq1, user.name))
                embed.set_image(url='https://i.imgur.com/W2ghZbK.gif')
                msg4 = await client.send_message(message.channel, embed=embed)

            if  ação1.content == "atacar":
                atq1 = random.randint(20, 50)
                msg4 = await client.send_message(message.channel, "{}, utiizou atacar, tirando {} do {}".format(message.author.name, atq1, user.name))
            if ação1.content != "Rugido" and ação1.content != "atacar":
                await client.send_message(message.channel, "Ação invalida")
            msg6 = await client.send_message(message.channel, "Agora é a vez de {} atacar, digite atacar ou Gelo!".format(user.name))
            ação2 = await client.wait_for_message(author=user)

            if ação2.content == "Gelo":
                atq2 = random.randint(60, 80)
                embe = discord.Embed(title='{}, utilizou o Arco Destruidor de Demonios, tirando {}, do {}'.format(user.name, atq1, message.author.name))
                embe.set_image(url='https://vignette.wikia.nocookie.net/fairytailfanon/images/c/c3/Destruction_Bow.gif')
                msg7 = await client.send_message(message.channel, embed=embe)
            if  ação2.content == "atacar":
                atq2 = random.randint(20,50)
                msg7 = await client.send_message(message.channel, "{}, utiizou atacar, tirando {} do {}".format(user.name, atq2, message.author.name))
            if ação2.content != "Gelo" and ação2.content != "atacar":
                await client.send_message(message.channel, "Ação invalida")
            await asyncio.sleep(2)
            await client.delete_message(msg3)
            await client.delete_message(msg6)
            await client.delete_message(msg4)
            await client.delete_message(msg7)
            hp1 = hp1 - atq2
            hp2 = hp2 - atq1
            await client.edit_message(msg1, "{} = {} ❤".format(message.author.name, str(hp1)))
            await client.edit_message(msg2, "{} = {} ❤".format(user.name, str(hp2)))
        if hp1 <= 0 or hp2 <= 0:
            if hp1 > hp2:
                await client.send_message(message.channel, " O {}, utilizou o RUGIDO DO DRAGÃO e acabou com o {}.".format(message.author.name, user.name))
            if hp2 > hp1:
                await client.send_message(message.channel, "O {}, usou o RUGIDO DO DRAGÃO e acabou com o {}.".format(user.name, message.author.name))
        embed = discord.Embed(title='\n', color=discord.Colour(0x00000))
        embed.set_image(url='https://orig00.deviantart.net/5fbd/f/2016/136/a/c/enter_the_dragon_force_2_by_strunton-da2nyzt.gif')
        await client.send_message(message.channel, embed=embed)

    if message.content.startswith('n!happy'):
        await client.delete_message(message)
        loop = 1
        emb1 = discord.Embed(title='\n')
        nulo = await client.send_message(message.channel, embed=emb1)
        while loop == 1:
            embed = discord.Embed(title='Eu sou o Happy, o melhor amigo do BOT Natsu.', color=discord.Colour(0x0f0ff0))
            embed.set_thumbnail(url='https://i.pinimg.com/originals/ed/04/54/ed0454a53fae45fc38059ea67a3589b2.gif')
            embed.add_field(name='Eu serei o seu guia para conhecer mais sobre o BOT Natsu.', value='Para conhecer seus comandos, clique na reação abaixo.')
            msg1 = await client.edit_message(nulo, embed=embed)
            await client.add_reaction(msg1, '▶')
            await client.wait_for_reaction('▶',user=message.author)
            em = discord.Embed(title='**🤖 Comandos do Natsu.**',color=discord.Colour(0x0f00ff))
            em.add_field(name='**⚙Moderação**', value='`!ban`'
                                                      ' `n!kick`'
                                                      ' `n!vote + assunto da votação`'
                                                      ' `n!apagar + quantidade`'
                                                      ' `n!lock`'
                                                      ' `n!unlock`'
                                                      ' `n!fechar`'
                                                      ' `n!liberar`'
                                                      ' `n!invite`'
                                                      ' `n!adver`')
            em.add_field(name='**🕹️Diversão**', value=' `n!natsu + pergunta`'
                                                       ' `n!batalhar`'
                                                       ' `n!ship`'
                                                       ' `n!beijar`'
                                                       ' `n!roleta`'
                                                       ' `n!corrida`')
            em.add_field(name='**💻Utilidades**', value=' `n!ping`'
                                                        ' `n!serverinfo`'
                                                        ' `n!userinfo`'
                                                        ' `n!botinfo`'
                                                        ' `n!invite`'
                                                        ' `n!avatar')
            em.add_field(name='**🎵PlayList**', value=' `n!entrar`'
                                                      ' `n!sair`'
                                                      ' `n!play`'
                                                      ' `n!resume`')
            em.add_field(name='**💰 Economia**', value=' `n!daily`'
                                                       ' `n!saldo`')
            em.set_footer(text='Caso queira voltar a aba, clique na reação ◀.')
            msg2 = await client.edit_message(msg1, embed=em)
            await client.add_reaction(msg2, '◀')
            await client.wait_for_reaction('◀', user=message.author)
            await client.edit_message(msg2, embed=embed)





client.run('NTA1ODQwNzQzODUyNTM5OTA1.DrZdCw.Aq6LW_EWys6OD6_DTVBCBXwOtlo')